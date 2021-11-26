from copy import deepcopy
from decimal import Decimal

from django.db.models import Min, Max, F

from characteristics.models import Country
from estimation.models import BaseEst
from famform.models import FamEstFormData, PCTCountryCustomization, ParisCountryCustomization
from family import utils
from family.models import Family


def create_synopsis_sheet(id, workbook):
    worksheet = workbook.add_worksheet('Synopsis')
    # data is simple aggregation
    family = Family.objects.get(id=id)

    data = utils.get_totals_per_country(id)
    total_costs_data = utils.get_total_costs(id)
    string_format_even = workbook.add_format({'bg_color': 'white'})
    string_format_odd = workbook.add_format({'bg_color': '#c8c7c8'})
    currency_format_even = workbook.add_format({'num_format': '[$$-409]#,##0.00',
                                                'bg_color': 'white'})
    currency_format_odd = workbook.add_format({'num_format': '[$$-409]#,##0.00',
                                               'bg_color': '#c8c7c8'})
    total_row = workbook.add_format({'num_format': '[$$-409]#,##0.00',
                                     'top': True, 'bottom': True,
                                     'bg_color': 'white',
                                     'underline': True,
                                     })
    header_format = workbook.add_format({'bold': True, 'bg_color': '#494349',
                                         'font_color': "white"})

    worksheet.write(0, 0, 'Synopsis', header_format)
    worksheet.write(0, 1, 'Total Costs', header_format)
    worksheet.set_column(0, 0, 22)
    worksheet.set_column(1, 2, 12)
    next_row = 1
    last_max_row = next_row + 1
    for i, countryRow in enumerate(data):
        if i % 2 == 0:
            worksheet.write(i + next_row, 0, countryRow['country_long_name'], string_format_even)
            worksheet.write(i + next_row, 1, countryRow['total_cost_sum'].quantize(Decimal('.01')),
                            currency_format_even)
        else:
            worksheet.write(i + next_row, 0, countryRow['country_long_name'], string_format_odd)
            worksheet.write(i + next_row, 1, countryRow['total_cost_sum'].quantize(Decimal('.01')), currency_format_odd)
        next_max_row = next_row + i + 1

    worksheet.write(next_max_row, 0, 'Total', total_row)
    worksheet.write(next_max_row, 1, total_costs_data[0]['total_cost_sum'], total_row)


def create_parameters_sheet(id, workbook):
    main_format = workbook.add_format({
        # 'text_wrap': True,
    })
    merge_format = workbook.add_format({
        'text_wrap': True, 'align': 'center', 'valign': 'vcenter'
    })
    date_format = workbook.add_format({
        'num_format': 'd mmmm yyyy', 'align': 'left'
    })
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 18
    })
    basic_format = workbook.add_format({
        'align': 'left',
        'valign': 'vcenter'
    })

    family = Family.objects.get(id=id)
    famFormData = FamEstFormData.objects.get(family=family)
    worksheet = workbook.add_worksheet('Parameters')
    worksheet.set_column(0, 2, 20, basic_format)
    worksheet.set_row(0, 20)
    worksheet.write(0, 0, 'Parameters', title_format)
    familyNameArr = ['Family Name', family.family_name]
    worksheet.write_row(1, 0, familyNameArr, main_format)
    familyNoArr = ['Family No.', family.family_no]
    worksheet.write_row(2, 0, familyNoArr)

    # init applDetails
    initIndepClaims = ['Indep Claims', famFormData.init_appl_details.num_indep_claims]
    worksheet.write_row(3, 0, initIndepClaims)
    initClaims = ['Claims', famFormData.init_appl_details.num_claims]
    worksheet.write_row(4, 0, initClaims)
    initDrawings = ['Drawings', famFormData.init_appl_details.num_drawings]
    worksheet.write_row(5, 0, initDrawings)
    initPagesDrawings = ['Pages Drawings', famFormData.init_appl_details.num_pages_drawings]
    worksheet.write_row(6, 0, initPagesDrawings)
    initPagesClaims = ['Pages Claims', famFormData.init_appl_details.num_pages_claims]
    worksheet.write_row(7, 0, initPagesClaims)
    initPagesDesc = ['Pages Description', famFormData.init_appl_details.num_pages_description]
    worksheet.write_row(8, 0, initPagesDesc)
    if famFormData.init_appl_details.entity_size:
        entitySize = ['Entity Size', famFormData.init_appl_details.entity_size.entity_size]
        worksheet.write_row(9, 0, entitySize)

    firstApplDate = 'First Application Filing Date'
    worksheet.write(10, 0, firstApplDate)
    firstApplDate = famFormData.init_appl_filing_date
    worksheet.write(10, 1, firstApplDate, date_format)
    firstAppl = ['First Application Country', famFormData.init_appl_country.long_name]
    worksheet.write_row(11, 0, firstAppl)

    firstDfRow = 13
    pcountryCustomization = famFormData.pariscountrycustomization_set.all()
    worksheet.write(firstDfRow, 0, 'Direct Filing Countries')
    lastDfRow = create_custom_details(worksheet, pcountryCustomization, firstDfRow, merge_format)
    worksheet.merge_range(firstDfRow, 0, lastDfRow, 0,
                          'Direct Filing Countries', merge_format)

    lastDfRow = lastDfRow + 2
    pct_method = ['Use PCT', str(famFormData.pct_method)]
    if famFormData.pct_method:
        worksheet.write_row(lastDfRow, 0, pct_method)
        # pctmethod customization
        firstDetRow = lastDfRow + 1
        lastDetRow = createCustomApplDetails(worksheet, famFormData.pct_method_customization.custom_appl_details,
                                             firstDetRow)
        if lastDetRow == firstDetRow:
            # worksheet.write(lastDetRow, 1, 'Custom PCT Details', merge_format)
            # pct_country = ['PCT Receiving Office', (famFormData.pct_country.long_name)]
            worksheet.write(firstDetRow, 0, 'PCT Receiving Office', merge_format)
            worksheet.write(firstDetRow, 0, famFormData.pct_country.long_name, merge_format)
        else:
            # worksheet.merge_range(firstDetRow, 1, lastDetRow, 1, 'Custom PCT Details', merge_format)
            worksheet.merge_range(firstDetRow, 1, lastDetRow, 1, famFormData.pct_country.long_name)
            worksheet.merge_range(firstDetRow, 0, lastDetRow, 0, 'PCT Receiving Office')
        lastDfRow = lastDetRow
        isa_country = ['ISA Office', (famFormData.isa_country.long_name)]
        worksheet.write_row(lastDfRow + 1, 0, isa_country)
        firstDfRow = lastDfRow + 3
        pctCountriesCustomization = famFormData.pctcountrycustomization_set.all()
        lastDfRow = create_custom_details(worksheet, pctCountriesCustomization, firstDfRow, merge_format)
        worksheet.merge_range(firstDfRow, 0, lastDfRow, 0,
                              'PCT National Phase Countries', merge_format)
        lastDfRow = lastDfRow + 2

    ep_method = ['Use EPO', str(famFormData.ep_method)]
    if famFormData.ep_method:
        worksheet.write_row(lastDfRow, 0, ep_method)
        firstDetRow = lastDfRow + 1
        lastDetRow = createCustomApplDetails(worksheet, famFormData.ep_method_customization.custom_appl_details,
                                             firstDetRow)
        if lastDetRow == firstDetRow:
            # worksheet.write(lastDetRow, 1, 'Custom PCT Details', merge_format)
            # pct_country = ['PCT Receiving Office', (famFormData.pct_country.long_name)]
            worksheet.write(firstDetRow, 1, 'EP', merge_format)
            worksheet.write(firstDetRow, 0, 'EP Customization', merge_format)
        else:
            # worksheet.merge_range(firstDetRow, 1, lastDetRow, 1, 'Custom PCT Details', merge_format)
            worksheet.merge_range(firstDetRow, 1, lastDetRow, 1, 'EP')
            worksheet.merge_range(firstDetRow, 0, lastDetRow, 0, 'EP Customization')
        lastDfRow = lastDetRow

        epCountriesCustomization = famFormData.epcountrycustomization_set.all()
        firstDfRow = lastDfRow + 1
        lastDfRow = create_custom_details(worksheet, epCountriesCustomization, firstDfRow, merge_format)
        worksheet.merge_range(firstDfRow, 0, lastDfRow, 0,
                              'EP Validation Countries', merge_format)


def create_custom_details(worksheet, country_customizations, firstRow, merge_format):
    firstDetRow = firstRow
    for c in country_customizations:
        lastDetRow = createCustomApplDetails(worksheet, c.custom_appl_details, firstDetRow)
        if lastDetRow == firstDetRow:
            worksheet.write(lastDetRow, 1, c.country.long_name, merge_format)
        else:
            worksheet.merge_range(firstDetRow, 1, lastDetRow, 1, c.country.long_name, merge_format)
        firstDetRow = lastDetRow + 1
    return lastDetRow


def create_totals_sheet(id, workbook):
    arr = utils.createFamEstDetails(id)
    worksheet = workbook.add_worksheet('Totals')
    # create top row with countries
    baseEsts = BaseEst.objects.filter(application__family=id)
    countries = baseEsts.order_by('application__country') \
        .distinct('application__country') \
        .values(country=F('application__country__long_name'),
                country_id=F('application__country'))
    min_year = baseEsts.aggregate(Min('date'))['date__min'].year
    max_year = baseEsts.aggregate(Max('date'))['date__max'].year
    country_arr = ['']
    country_lookup_arr = [0]
    num_country = 0
    for i, country in enumerate(countries):
        country_arr.append(country['country'])
        country_lookup_arr.append(country['country_id'])
        num_country += 1
    new_arr = [country_arr]
    year = min_year
    column_arr = [0] * (num_country + 2)
    year_lookup_arr = [0]
    col_counter = 1
    while year <= max_year:
        new_column_arr = deepcopy(column_arr)
        new_column_arr[0] = year
        new_arr.append(new_column_arr)
        year_lookup_arr.append(year)
        col_counter += 1
        year += 1
    for x in arr:
        row = country_lookup_arr.index(x['country'])
        column = year_lookup_arr.index(x['year'])
        new_arr[column][row] = x['total_cost_sum'].quantize(Decimal('.01'))

    # totals
    total_row = utils.get_totals_per_year(id)
    new_arr[0].append('Total')
    for t in total_row:
        column = year_lookup_arr.index(t['year'])
        new_arr[column][num_country + 1] = t['total_cost_sum'].quantize(Decimal('.01'))

    currency_format_even = workbook.add_format({'num_format': '[$$-409]#,##0.00',
                                                'bg_color': 'white'})
    currency_format_odd = workbook.add_format({'num_format': '[$$-409]#,##0.00',
                                               'bg_color': '#c8c7c8'})
    total_row = workbook.add_format({'num_format': '[$$-409]#,##0.00',
                                     'top': True, 'bottom': True,
                                     'bg_color': 'white',
                                     'underline': True,
                                     })
    header_format = workbook.add_format({'bold': True, 'bg_color': '#494349',
                                         'font_color': "white"})

    worksheet.set_column(0, 0, 22)
    worksheet.set_column(1, max_year - min_year + 1, 10)

    for col_index, col in enumerate(new_arr):
        for row_index, row in enumerate(col):
            if row_index > 0:
                if row_index == num_country + 1:
                    worksheet.write(row_index, col_index,
                                    new_arr[col_index][row_index], total_row)
                elif row_index % 2 == 0:
                    worksheet.write(row_index, col_index,
                                    new_arr[col_index][row_index], currency_format_even)
                else:
                    worksheet.write(row_index, col_index,
                                    new_arr[col_index][row_index], currency_format_odd)
            else:
                if col_index > 0:
                    worksheet.write(row_index, col_index,
                                    new_arr[col_index][row_index], header_format)
                else:
                    worksheet.write(0, 0, 'Total Cost Estimate', header_format)
    family = Family.objects.get(id=id)
    chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
    chart.set_size({'width': 750, 'height': 580})
    chart.set_x_axis({'name': 'year'})
    chart.set_y_axis({'name': 'Total Cost (USD)'})
    chart.set_title({'name': 'Total Cost Estimate for Patent Family ' + family.family_name})
    worksheet.insert_chart(num_country + 3, 1, chart)
    row_index = 1  # skip header row
    while row_index <= num_country:
        country_color = Country.objects.get(id=country_lookup_arr[row_index]).color
        chart.add_series({
            'categories': ['Totals', 0, 1, 0, max_year - min_year],
            'values': ['Totals', row_index, 1, row_index, max_year - min_year + 1],
            'name': ['Totals', row_index, 0, row_index, 0],
            'fill': {'color': country_color},
            'gap': 30,
        })
        row_index += 1


def createCustomApplDetails(worksheet, custom_appl_details, row):
    newRow = row
    if custom_appl_details:
        if custom_appl_details.num_indep_claims:
            worksheet.write(newRow, 2, 'Indep Claims')
            worksheet.write(newRow, 3, custom_appl_details.num_indep_claims)
            newRow += 1
        if custom_appl_details.num_claims:
            worksheet.write(newRow, 2, 'Claims')
            worksheet.write(newRow, 3, custom_appl_details.num_claims)
            newRow += 1
        if custom_appl_details.num_drawings:
            worksheet.write(newRow, 2, 'Drawings')
            worksheet.write(newRow, 3, custom_appl_details.num_drawings)
            newRow += 1
        if custom_appl_details.num_pages_drawings:
            worksheet.write(newRow, 2, 'Pages Drawings')
            worksheet.write(newRow, 3, custom_appl_details.num_pages_drawings)
            newRow += 1
        if custom_appl_details.num_pages_claims:
            worksheet.write(newRow, 2, 'Pages Claims')
            worksheet.write(newRow, 3, custom_appl_details.num_pages_claims)
            newRow += 1
        if custom_appl_details.num_pages_description:
            worksheet.write(newRow, 2, 'Pages Description')
            worksheet.write(newRow, 3, custom_appl_details.num_pages_description)
            newRow += 1
        if custom_appl_details.entity_size:
            worksheet.write(newRow, 2, 'Entity Size')
            worksheet.write(newRow, 3, custom_appl_details.entity_size.entity_size)
            newRow += 1
    if newRow > row:
        return newRow - 1
    else:
        return newRow
