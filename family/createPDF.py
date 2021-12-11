import io
import math
from copy import deepcopy
from decimal import Decimal
from functools import partial
import pandas as pd

from django.db.models import Min, Max, F
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, TableStyle, BaseDocTemplate, Frame, PageTemplate, FrameBreak, PageBreak, \
    NextPageTemplate, KeepTogether, CondPageBreak
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1

from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import TableStyle, Paragraph

from application.models import ApplDetails
from characteristics.models import Country
from estimation.models import BaseEst
from famform.models import FamEstFormData
from family import utils
from family.models import Family
from family.utils import get_totals_per_country

from reportlab.lib.units import mm


class NoSplitTable(Table):

    def split(self, availWidth, availHeight):
        tables = []
        return tables


class NumberedPageCanvas(Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    http://www.blog.pythonlibrary.org/2013/08/12/reportlab-how-to-add-page-numbers/
    """

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            # self.draw_family_name(family_no)
            super().showPage()

        super().save()

    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        if self._pageNumber > 1:
            page = "Page %s of %s" % (self._pageNumber, page_count)
            self.setFont("Helvetica", 8)
            self.drawRightString(8 * inch, 0.25 * inch, page)


def generate_pdf_report(id):
    table_style = TableStyle([
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f3f3f3')),
        ('ALIGNMENT', (0, 0), (-1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('LINEAFTER', (0, 0), (0, -1), 1, colors.black),
    ])

    chart_buffer = io.BytesIO()
    my_doc_loc = io.BytesIO()

    family = Family.objects.get(id=id)
    totals_data = get_totals_per_country(id)
    # get data
    arr = utils.createFamEstDetails(id)
    totals_arr = utils.get_totals_per_year(id)
    query_list = list(arr)
    totals_list = list(totals_arr)
    baseEsts = BaseEst.objects.filter(application__family=id)
    famestformdata = FamEstFormData.objects.get(family=family)
    init_details = ApplDetails.objects.get(id=famestformdata.init_appl_details_id)

    min_year = baseEsts.aggregate(Min('date'))['date__min'].year
    max_year = baseEsts.aggregate(Max('date'))['date__max'].year

    my_doc = BaseDocTemplate(my_doc_loc, pagesize=letter)

    title_template = generate_title_template(my_doc)
    overview_template = generate_overview_template(my_doc, family)
    body_template = generate_basic_template(my_doc, family)
    my_doc.addPageTemplates([title_template, body_template, overview_template])
    flowables = []
    countries = Country.objects.filter(baseapplication__family=family).distinct().order_by(
        'long_name')  # .values('long_name', 'color', 'id')

    flowables = generate_title_page(flowables, family)
    flowables.append(NextPageTemplate(['overview']))
    flowables.append(PageBreak())
    flowables = generate_overview_page(flowables, family, totals_data, famestformdata, init_details)
    flowables.append(NextPageTemplate(['ee']))
    flowables.append(PageBreak())
    bottom_frame_height = my_doc.height / 2
    flowables = generate_pdf_report_old_page(chart_buffer, my_doc_loc, flowables, my_doc, query_list,
                                             baseEsts, countries, min_year, max_year, family,
                                             bottom_frame_height, totals_list, deepcopy(table_style))

    for country in countries:
        flowables = generate_country_page(country, flowables, query_list, baseEsts, min_year, max_year, id,
                                          deepcopy(table_style))

    my_doc.build(flowables, canvasmaker=NumberedPageCanvas)
    plt.close()  # !important essential to prevent memory leaks

    return my_doc_loc


def TitlePageSetup(canvas, my_doc):
    canvas.saveState()
    canvas.setStrokeGray(0.90)
    canvas.setFillGray(0.90)
    canvas.rect(my_doc.leftMargin, my_doc.bottomMargin, my_doc.width, my_doc.height, stroke=1, fill=1)
    canvas.restoreState()


def NormalPageSetup(canvas, my_doc, family):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    # canvas.setFont("Times-Bold", 8)
    canvas.drawString(0.5 * inch, 0.25 * inch, 'EstPat Patent Cost Estimator')
    canvas.drawRightString(8 * inch, 10.5 * inch, 'Family No: %s' % family.family_no)
    canvas.restoreState()


def generate_title_template(my_doc):
    frame1 = Frame(my_doc.leftMargin, my_doc.bottomMargin,
                   my_doc.width, 3 * my_doc.height / 4, showBoundary=0, id='frame1')
    page_template = PageTemplate(id='title', frames=[frame1], onPage=TitlePageSetup)
    return page_template


def generate_overview_template(my_doc, family):
    frame5 = Frame(my_doc.leftMargin, my_doc.bottomMargin + my_doc.height - 60,
                   my_doc.width, 60, showBoundary=0, id='col5b')
    frame1 = Frame(my_doc.leftMargin, my_doc.bottomMargin,
                   (my_doc.width / 2) - 0.1 * inch, my_doc.height - 65, showBoundary=0, id='frame1')
    frame2 = Frame(my_doc.leftMargin + my_doc.width / 2 + 0.2 * inch, my_doc.bottomMargin,
                   (my_doc.width / 2) - 0.1 * inch, my_doc.height - 65, showBoundary=0, id='frame2')
    page_template = PageTemplate(id='overview', frames=[frame5, frame1, frame2],
                                 onPage=partial(NormalPageSetup, family=family))
    return page_template


def generate_overview_page(flowables, family, totals_data, famestformdata, init_details):
    sample_style_sheet = getSampleStyleSheet()
    header_style = ParagraphStyle(fontSize=12,
                                  leading=18,
                                  spaceBefore=12,
                                  alignment=TA_LEFT, name='header')
    item_style = ParagraphStyle(fontSize=10,
                                leading=12, leftIndent=12,
                                fontName='Helvetica',
                                alignment=TA_LEFT, name='item')
    paragraph_pre_1 = Paragraph("Overview of Patent Cost Estimate for %s" % family.family_name,
                                sample_style_sheet['Heading2'])
    flowables.append(paragraph_pre_1)
    flowables.append(FrameBreak())
    paragraph_0 = Paragraph("Details on Patent Family:", header_style)
    paragraph_1 = Paragraph("Family Name %s" % family.family_name, item_style)
    paragraph_2 = Paragraph("Family No. %s" % family.family_no, item_style)
    paragraph_5 = Paragraph("Details on First Application:", header_style)
    paragraph_4 = Paragraph("Country: %s" % famestformdata.init_appl_country.long_name, item_style)
    paragraph_6 = Paragraph("Application Type: %s" % famestformdata.init_appl_type.long_name, item_style)
    paragraph_7 = Paragraph("Num Indep Claims: %s" % famestformdata.init_appl_details.num_indep_claims, item_style)
    paragraph_8 = Paragraph("Num Claims: %s" % famestformdata.init_appl_details.num_claims, item_style)
    paragraph_9 = Paragraph(
        "Num Multiple Dependent Claims: %s" % famestformdata.init_appl_details.num_claims_multiple_dependent,
        item_style)
    paragraph_10 = Paragraph("Num Drawings: %s" % famestformdata.init_appl_details.num_drawings, item_style)
    paragraph_11 = Paragraph("Num Pages DescriptionT: %s" % famestformdata.init_appl_details.num_pages_description,
                             item_style)
    paragraph_12 = Paragraph("Num Pages Claims: %s" % famestformdata.init_appl_details.num_pages_drawings, item_style)

    flowables.append(paragraph_0)
    flowables.append(paragraph_1)
    flowables.append(paragraph_2)
    flowables.append(paragraph_5)
    flowables.append(paragraph_4)
    flowables.append(paragraph_6)
    flowables.append(paragraph_7)
    flowables.append(paragraph_8)
    flowables.append(paragraph_9)
    flowables.append(paragraph_10)
    flowables.append(paragraph_11)
    flowables.append(paragraph_12)
    if init_details.entity_size:
        paragraph_13 = Paragraph("Entity Size: %s" % init_details.entity_size.entity_size, item_style)
        flowables.append(paragraph_13)
    paragraph_14 = Paragraph("Language: %s" % init_details.language.name, item_style)
    flowables.append(paragraph_14)
    paragraph_15 = Paragraph("Details on International Filing: ", header_style)
    flowables.append(paragraph_15)
    paragraph_16 = Paragraph("Using PCT Method: %s" % famestformdata.pct_method, item_style)
    flowables.append(paragraph_16)
    if famestformdata.pct_country:
        paragraph_17 = Paragraph("PCT Receiving Office : %s" % famestformdata.pct_country.long_name, item_style)
        flowables.append(paragraph_17)
    if famestformdata.isa_country:
        paragraph_18 = Paragraph("PCT International Search Authority: %s" % famestformdata.isa_country.long_name,
                                 item_style)
        flowables.append(paragraph_18)
    paragraph_19 = Paragraph("Using EP Method: %s" % famestformdata.ep_method, item_style)
    flowables.append(paragraph_19)

    if famestformdata.paris_countries.all().count() > 0:
        paragraph_20 = Paragraph("Direct Filing Countries: ", header_style)
        flowables.append(paragraph_20)
        paris_countries = famestformdata.paris_countries.all()
        for c in paris_countries:
            paragraph_c = Paragraph(c.long_name, item_style)
            flowables.append(paragraph_c)

    if famestformdata.pct_method:
        paragraph_21 = Paragraph("PCT National Phase Countries: ", header_style)
        flowables.append(paragraph_21)
        pct_countries = famestformdata.pct_countries.all()
        for c in pct_countries:
            paragraph_c = Paragraph(c.long_name, item_style)
            flowables.append(paragraph_c)
    if famestformdata.ep_method:
        paragraph_22 = Paragraph("EP Validation Countries: ", header_style)
        flowables.append(paragraph_22)
        ep_countries = famestformdata.ep_countries.all()
        for c in ep_countries:
            paragraph_c = Paragraph(c.long_name, item_style)
            flowables.append(paragraph_c)
    # flowables.append(FrameBreak())
    paragraph_3 = Paragraph("Total Costs Summary:", header_style)
    # flowables.append(paragraph_3)
    totals_data_table = createPdfTotalsTable(totals_data)
    flowables.append(KeepTogether([paragraph_3, totals_data_table]))

    return flowables


def generate_title_page(flowables, family):
    ps = ParagraphStyle(fontSize=32,
                        leading=40,
                        alignment=TA_CENTER, name='Title')
    ps_sub = ParagraphStyle(fontSize=18,
                            leading=18,
                            alignment=TA_CENTER, name='Sub')
    paragraph_1 = Paragraph("Estimate Details for %s" % family.family_name, ps, )
    paragraph_2 = Paragraph("EstPat Patent Cost Estimator", ps_sub)

    flowables.append(paragraph_1)
    flowables.append(paragraph_2)

    return flowables


def generate_basic_template(my_doc, family):
    frame5 = Frame(my_doc.leftMargin, my_doc.bottomMargin + my_doc.height - 60,
                   my_doc.width, 60, showBoundary=0, id='col5a')
    frame2 = Frame(my_doc.leftMargin, my_doc.bottomMargin + my_doc.height / 2 + 6,
                   my_doc.width, my_doc.height / 2 - 60 - 12, id='col2a', showBoundary=0)
    frame3 = Frame(my_doc.leftMargin, my_doc.bottomMargin,
                   my_doc.width, my_doc.height / 2, id='col3a', showBoundary=0)
    page_template = PageTemplate(id='ee', frames=[frame5, frame2, frame3],
                                 onPage=partial(NormalPageSetup, family=family))
    return page_template


def generate_country_page(country, flowables, query_list, baseEsts, min_year, max_year, fam_id, table_style):
    chart_buffer = io.BytesIO()
    width, height = letter
    inner_width = width - inch
    sample_style_sheet = getSampleStyleSheet()

    if country.long_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        paragraph_1 = Paragraph("Estimate Details for the %s" % country.long_name, sample_style_sheet['Heading2'])
    else:
        paragraph_1 = Paragraph("Estimate Details for %s" % country.long_name, sample_style_sheet['Heading2'])
    # paragraph_2 = Paragraph(
    #     "EstPat Patent Cost Estimator",
    #     sample_style_sheet['BodyText']
    # )
    flowables.append(paragraph_1)
    # flowables.append(paragraph_2)
    flowables.append(Spacer(1, 0.2 * inch))

    # empty data template
    empty_data = []
    label_data = []
    year = min_year
    count = 0
    while year <= max_year:
        empty_data.append(0)
        label_data.append(str(year))
        year += 1
        count += 1

    country_col = []
    # group according to country
    # place in array

    filtered = filter(lambda aggEst: aggEst['country'] == country.id, query_list)

    # color = '#0000ff'
    color_official = '#4682AB'
    color_trans = '#AA4C46'
    row_data = deepcopy(empty_data)
    row_trans_data = deepcopy(empty_data)
    row_tot_data = deepcopy(empty_data)
    for row in filtered:
        row_data[row['year'] - min_year] = int(row['official_cost_sum'])
        row_trans_data[row['year'] - min_year] = int(row['translation_cost_sum'])
        row_tot_data[row['year'] - min_year] = int(row['total_cost_sum'])
    country_col.append([color_official, country.id, 'Official Fees', row_data])
    country_col.append([color_trans, country.id, 'Translation Fees', row_trans_data])
    data = sorted(country_col, key=lambda x: x[2], reverse=True)
    create_country_chart_using_plt(data, empty_data, label_data, flowables, chart_buffer, country)

    new_data = sorted(country_col, key=lambda x: x[2], reverse=False)
    label_data.append('Total')

    country_col.append([color_trans, country.id, 'Total Fees', row_tot_data])
    new_data.append([color_trans, country.id, 'Total Fees', row_tot_data])
    table_data = []
    first_row = ['Fee Type']
    year = min_year
    while year <= max_year:
        first_row.append(year)
        year += 1
    first_row.append('Total')
    table_data.append(first_row)
    table_cell_width = 30
    table_cell_height = 15
    year = min_year
    col_widths = []
    while year <= max_year:
        col_widths.append(table_cell_width)
        year += 1
    totals_col_width = table_cell_width + 10
    col_widths.append(totals_col_width)
    data_num_cells = len(new_data[0][3])
    num_mega_rows = math.ceil((data_num_cells * table_cell_width + 1) / inner_width)
    cells_per_row = math.ceil(data_num_cells / num_mega_rows)

    num_rows = 0
    for i, row in enumerate(new_data):
        new_row = []
        new_row.append(row[2])
        tot_col = 0
        for item in row[3]:
            tot_col += item
            new_row.append(item)
        num_rows = i
        new_row.append(tot_col)
        table_data.append(new_row)
    flowables.append(FrameBreak())
    paragraph_4 = Paragraph("""Data Table (USD)""")
    flowables.append(paragraph_4)
    mega_row_counter = 0
    while mega_row_counter < num_mega_rows:
        min_col = mega_row_counter * cells_per_row
        max_col = (1 + mega_row_counter) * cells_per_row

        short_col_widths = [4 * table_cell_width]
        print('mega_row_counter', mega_row_counter)
        short_col_widths += col_widths[min_col: max_col]
        short_table = []
        for row in table_data:
            if mega_row_counter > 0:
                short_row = [row[0]]
                short_row += row[min_col + 1: max_col + 1]
                table_style.add('BACKGROUND', (-1, 0), (-1, num_rows), colors.HexColor('#f3f3f3'))
            else:
                short_row = row[min_col: max_col + 1]
            short_table.append(short_row)
        t = Table(short_table, short_col_widths, table_cell_height, table_style,
                  spaceAfter=0.2 * inch, spaceBefore=0.2 * inch, hAlign='LEFT')

        flowables.append(t)
        mega_row_counter += 1
    # display_table_data
    flowables.append(PageBreak())

    return flowables


def generate_pdf_report_old_page(chart_buffer, my_doc_loc, flowables, my_doc, query_list,
                                 baseEsts, countries, min_year, max_year, family, bottom_frame_height,
                                 totals_list, table_style):
    chart_buffer = io.BytesIO()
    width, height = letter
    inner_width = width - inch
    sample_style_sheet = getSampleStyleSheet()

    paragraph_1 = Paragraph("Patent Cost Estimate for " + family.family_name, sample_style_sheet['Heading2'])
    # paragraph_2 = Paragraph(
    #     "EstPat Patent Cost Estimator",
    #     sample_style_sheet['BodyText']
    # )
    flowables.append(paragraph_1)
    # flowables.append(paragraph_2)
    flowables.append(Spacer(1, 0.2 * inch))

    # find min year and max year

    # empty data template
    empty_data = []
    label_data = []
    year = min_year
    count = 0
    while year <= max_year:
        empty_data.append(0)
        # label_data.append(str(year))
        label_data.append(year)
        year += 1
        count += 1
    country_col = []
    # group according to country
    for country in countries:
        filtered = filter(lambda aggEst: aggEst['country'] == country.id, query_list)
        # place in array
        row_data = deepcopy(empty_data)
        for row in filtered:
            row_data[row['year'] - min_year] = int(row['total_cost_sum'])
        country_col.append([country.long_name, country.color, country.id, row_data])
    # country_col.append()
    data = sorted(country_col, key=lambda x: x[0], reverse=True)
    # create chart using plt
    create_chart_using_plt(data, empty_data, label_data, flowables, chart_buffer)

    df = pd.DataFrame(query_list)
    pivoted = df.pivot_table(index='country_long_name', columns='year',
                             values='total_cost_sum', margins_name='Total', margins=True, aggfunc=np.sum)
    label_data.append('Total')
    pivoted = pivoted.reindex(columns=label_data).fillna(0)
    cols = pivoted.columns.tolist()
    index = pivoted.index.tolist()
    super_data = pivoted.to_numpy().astype(int).tolist()

    table_data = []
    first_row = ['Country']
    year = min_year
    while year <= max_year:
        first_row.append(year)
        year += 1
    table_data.append(first_row)
    table_cell_width = 30
    table_cell_height = 15
    year = min_year
    col_widths = []
    while year <= max_year:
        col_widths.append(table_cell_width)
        year += 1
    totals_col_width = table_cell_width + 10
    col_widths.append(totals_col_width)
    data_num_cells = len(data[0][3])
    num_mega_rows = math.ceil((data_num_cells * table_cell_width + 1) / inner_width)
    cells_per_row = math.ceil(data_num_cells / num_mega_rows)
    num_rows = 0

    flowables.append(FrameBreak())

    paragraph_4 = Paragraph("""Data Table (USD)""")
    flowables.append(paragraph_4)
    mega_row_counter = 0
    while mega_row_counter < num_mega_rows:
        min_col = mega_row_counter * cells_per_row
        max_col = (1 + mega_row_counter) * cells_per_row
        short_table = []
        short_row = ['Country']
        short_col_widths = [4 * table_cell_width]
        short_row += cols[min_col: max_col]
        short_col_widths += col_widths[min_col: max_col]

        short_table.append(short_row)
        for i, row in enumerate(super_data):
            if mega_row_counter > 0:
                short_row = [index[i]]
                short_row += row[min_col: max_col]
                table_style.add('BACKGROUND', (-1, 0), (-1, num_rows), colors.HexColor('#f3f3f3'))
            else:
                short_row = [index[i]]
                short_row += row[min_col: max_col]
            num_rows = i + 1
            short_table.append(short_row)

        t = Table(data=short_table, colWidths=short_col_widths, rowHeights=table_cell_height,
                  style=table_style,
                  spaceAfter=0.2 * inch, spaceBefore=0.2 * inch, hAlign='LEFT')
        used_height = (0.2 * inch) + num_mega_rows * table_cell_height * num_rows * 1.5

        if mega_row_counter != 0:
            if bottom_frame_height < used_height:
                ps_1 = ParagraphStyle(alignment=TA_RIGHT, rightIndent=0.5 * inch, name='ps_1')
                paragraph_5 = Paragraph("""data continued on next page...""", ps_1)
                flowables.append(paragraph_5)
                flowables.append(PageBreak())
                flowables.append(paragraph_1)
                # flowables.append(paragraph_2)

                ps_2 = ParagraphStyle(alignment=TA_LEFT, leftIndent=0.5 * inch, name='ps_2')
                paragraph_6 = Paragraph("""...continued from previous page""", ps_2)
                flowables.append(KeepTogether([paragraph_6, t]))
            else:
                flowables.append(t)
        else:
            flowables.append(t)
        mega_row_counter += 1

    flowables.append(PageBreak())
    # my_doc.build(flowables)
    # return my_doc_loc
    return flowables

    # return my_doc


def createPdfTotalsTable(data):
    first_row = ['Country', 'Total']
    table_data = [first_row]
    # header row
    # country, total cost
    par_style = ParagraphStyle(name='right', alignment=TA_RIGHT)
    total_row = 0
    for item in data:
        total_row += item['official_cost_sum']
        table_data.append(
            [Paragraph(item['country_long_name'], par_style),
             "${:,}".format(int(item['official_cost_sum']))
             ],
        )
    table_data.append([Paragraph('Total', par_style),
                       "${:,}".format(int(total_row))
                       ])

    table_cell_width = 50
    cell_widths = [2 * table_cell_width, table_cell_width]
    totals_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                               ('LINEAFTER', (0, 0), (0, -1), 1, colors.black),
                               ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                               ('LINEABOVE', (0, -1), (-1, -1), 1, colors.grey),
                               ('ALIGNMENT', (0, 0), (-1, -1), 'RIGHT'),
                               ])
    totals_table = Table(table_data, cell_widths, None, totals_style, spaceAfter=0.2 * inch,
                         spaceBefore=0.2 * inch, )
    return totals_table


def create_chart_using_plt(data, empty_data, label_data, pdf, chart_buffer):
    bar_width = 0.80  # the width of the bars: can also be len(x) sequence
    dx, dy = 2, 1
    figsize = plt.figaspect(float(dy) / float(dx))
    fig, ax = plt.subplots(figsize=figsize)
    bottom = empty_data
    chart_label_data = []
    for t in label_data:
        chart_label_data.append(str(t))
    for i, row in enumerate(data):
        ax.bar(chart_label_data, row[3], bar_width, label=row[0], bottom=bottom, color=row[1])
        bottom = np.add(row[3], bottom)
    ax.set_ylabel('Total Cost (USD)')
    ax.set_title('Total Estimated Cost per Year')
    ylim = ax.get_ylim()[1]
    ax.set_ylim(top=ylim + .1 * ylim)
    plt.xticks(rotation=45)

    ax.legend()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=reversed(handles), labels=reversed(labels), bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(chart_buffer, bbox_inches='tight')
    image_chart = Image(chart_buffer, height=225, width=450)

    image_chart.hAlign = 'CENTER'
    pdf.append(image_chart)
    return pdf


def create_country_chart_using_plt(data, empty_data, label_data, pdf, chart_buffer, country):
    bar_width = 0.80  # the width of the bars: can also be len(x) sequence
    dx, dy = 2, 1
    figsize = plt.figaspect(float(dy) / float(dx))
    fig, ax = plt.subplots(figsize=figsize)
    bottom = empty_data
    for i, row in enumerate(data):
        ax.bar(label_data, row[3], bar_width, label=row[2], bottom=bottom, color=row[0])
        bottom = np.add(row[3], bottom)
    ax.set_ylabel('Cost (USD)')
    if country.long_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        ax.set_title('Estimated Cost per Year for the %s' % country.long_name)
    else:
        ax.set_title('Estimated Cost per Year for %s' % country.long_name)
    ylim = ax.get_ylim()[1]
    ax.set_ylim(top=ylim + .1 * ylim)
    plt.xticks(rotation=45)
    ax.legend()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=reversed(handles), labels=reversed(labels),
              bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.legend(loc=(1.02, 0.0))
    plt.savefig(chart_buffer, bbox_inches='tight')
    image_chart = Image(chart_buffer, height=225, width=450)

    image_chart.hAlign = 'CENTER'
    pdf.append(image_chart)
    return pdf
