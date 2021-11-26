import io
import math
from copy import deepcopy
from decimal import Decimal

from django.db.models import Min, Max, F
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import Paragraph, TableStyle, BaseDocTemplate, Frame, PageTemplate, FrameBreak
import numpy as np
from reportlab.graphics.shapes import Drawing
import matplotlib.pyplot as plt
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import TableStyle, Paragraph

from estimation.models import BaseEst
from family import utils
from family.models import Family
from family.utils import get_totals_per_country


def generate_pdf_report(id):
    # c = canvas.Canvas("hello.pdf", pagesize=letter)
    # width, height = letter
    # c.drawString(100, 750, "Welcomt ")
    # c.save()
    # my_doc = SimpleDocTemplate('simplehello.pdf', pagesize=letter)
    # my_doc = BaseDocTemplate('simplehello.pdf', pagesize=letter, showBoundary=1)
    my_doc_loc = io.BytesIO()
    my_doc = BaseDocTemplate(my_doc_loc, pagesize=letter)

    frame5 = Frame(my_doc.leftMargin, my_doc.bottomMargin + my_doc.height - 60,
                   my_doc.width, 60)
    frame1 = Frame(my_doc.leftMargin, my_doc.bottomMargin + my_doc.height / 2 + 6,
                   my_doc.width / 3 - 6, my_doc.height / 2 - 60 - 12, id='col1')
    frame2 = Frame(my_doc.leftMargin + my_doc.width / 3, my_doc.bottomMargin + my_doc.height / 2 + 6,
                   2 * my_doc.width / 3, my_doc.height / 2 - 60 - 12, id='col2')
    frame3 = Frame(my_doc.leftMargin, my_doc.bottomMargin,
                   my_doc.width, my_doc.height / 2, id='col3')
    frame4 = Frame(my_doc.leftMargin, my_doc.bottomMargin,
                   my_doc.width / 2 - 6, my_doc.height / 2, id='col4')
    # my_doc.addPageTemplates([PageTemplate(id='bb', frames=[frame1, frame2, frame3, frame4]),])
    my_doc.addPageTemplates([PageTemplate(id='bb', frames=[frame5, frame1, frame2, frame3]), ])
    width, height = letter
    inner_width = width - inch
    inner_height = height - inch
    sample_style_sheet = getSampleStyleSheet()
    # sample_style_sheet.list()
    flowables = []
    family = Family.objects.get(id=id)
    paragraph_1 = Paragraph("Patent Cost Estimate for " + family.family_name, sample_style_sheet['Heading1'])
    paragraph_2 = Paragraph(
        "EstPat Patent Cost Estimator",
        sample_style_sheet['BodyText']
    )
    flowables.append(paragraph_1)
    flowables.append(paragraph_2)
    # paragraph_3 = Paragraph(
    #     """Totals""",
    #     sample_style_sheet['BodyText']
    # )
    # flowables.append(paragraph_3)

    flowables.append(Spacer(1, 0.2 * inch))
    flowables.append(createPdfTotalsTable(id))

    drawing = Drawing(400, 200)
    arr = utils.createFamEstDetails(id)
    query_list = list(arr)
    # find min year and max year
    baseEsts = BaseEst.objects.filter(application__family=id)
    countries = baseEsts.order_by('application__country') \
        .distinct('application__country') \
        .values(country=F('application__country__long_name'),
                color=F('application__country__color'),
                country_id=F('application__country'))
    min_year = baseEsts.aggregate(Min('date'))['date__min'].year
    max_year = baseEsts.aggregate(Max('date'))['date__max'].year
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
    for country in countries:
        filtered = filter(lambda aggEst: aggEst['country'] == country['country_id'], query_list)
        # place in array
        row_data = deepcopy(empty_data)
        for row in filtered:
            row_data[row['year'] - min_year] = int(row['official_cost_sum'].quantize(Decimal('0.')))
        country_col.append([country['country'], country['color'], country['country_id'], row_data])
    data = country_col

    bar_width = 0.80  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    chart = io.BytesIO()
    bottom = empty_data
    data = sorted(data, key=lambda x: x[2])
    for i, row in enumerate(data):
        ax.bar(label_data, row[3], bar_width, label=row[0], bottom=bottom, color=row[1])
        bottom = np.add(row[3], bottom)
    ax.set_ylabel('Total Cost (USD)')
    ax.set_title('Total Estimated Cost per Year')
    # plt.xticks(y_pos, bars, color='orange', rotation=45, fontweight='bold', fontsize='17', horizontalalignment='right')
    # ax.bar_label(label_data, label_type='center')
    plt.xticks(rotation=45)
    ax.legend()
    plt.savefig(chart, bbox_inches='tight')
    # plt.show()
    image_chart = Image(chart, height=225, width=300)
    image_chart.hAlign = 'RIGHT'
    flowables.append(image_chart)
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
        if (year == min_year):
            col_widths.append(table_cell_width * 4)
        else:
            col_widths.append(table_cell_width)
        year += 1
    data_num_cells = len(row[3])
    num_mega_rows = math.ceil((data_num_cells * table_cell_width + 1) / (inner_width))
    cells_per_row = math.ceil(data_num_cells / num_mega_rows)
    for i, row in enumerate(data):
        for item in row[3]:
            row.append(item)
        row.pop(3)
        row.pop(2)
        row.pop(1)
        table_data.append(row)

    flowables.append(FrameBreak())
    paragraph_4 = Paragraph("""
        Data Table (USD)
        """
                            )
    flowables.append(paragraph_4)
    mega_row_counter = 0
    while mega_row_counter < num_mega_rows:
        min_col = mega_row_counter * cells_per_row
        max_col = (1 + mega_row_counter) * cells_per_row
        short_table = []
        for row in table_data:
            if mega_row_counter > 0:
                short_row = [row[0]]
                short_row += row[min_col + 1: max_col + 1]
            else:
                short_row = row[min_col: max_col + 1]
            short_table.append(short_row)
        table_style = TableStyle([
            ('ALIGNMENT', (0, 0), (-1, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('LINEAFTER', (0, 0), (0, -1), 1, colors.black),
        ])
        t = Table(short_table, col_widths, table_cell_height, table_style)

        flowables.append(Spacer(1, 0.2 * inch))
        flowables.append(t)

        mega_row_counter += 1
    # display_table_data

    # t = Table(table_data, table_cell_width, table_cell_height)
    # flowables.append(t)

    my_doc.build(flowables)
    return my_doc_loc


def createPdfTotalsTable(id):
    family = Family.objects.get(id=id)
    data = get_totals_per_country(id)
    print('data', data)
    first_row = ['Country', 'Total']
    table_data = [first_row]
    # header row
    # country, total cost
    par_style = ParagraphStyle(name='right', alignment=TA_RIGHT)

    for item in data:
        table_data.append(
            [Paragraph(item['country_long_name'], par_style),
             '$' + str(int(item['official_cost_sum']))
             ],
        )

    table_cell_width = 50
    table_cell_height = 15
    cell_widths = [2 * table_cell_width, table_cell_width]
    totals_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                               ('LINEAFTER', (0, 0), (0, -1), 1, colors.black),
                               ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                               ('ALIGNMENT', (0, 0), (-1, -1), 'RIGHT'),
                               ])
    totals_table = Table(table_data, cell_widths, None, totals_style)
    return totals_table
