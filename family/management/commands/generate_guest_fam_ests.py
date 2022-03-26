import datetime
import io

from django.core.management import BaseCommand

from application.models import ApplDetails
from characteristics.models import ApplType, Country, DocFormat, EntitySize, Language
from famform.models import ApplOptions, CustomApplDetails, CustomApplOptions, EPMethodCustomization, FamEstFormData, \
    PCTMethodCustomization
from family import createPDF, createXLSX
from family.models import Family
from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.generate_guest_fam_ests()
        self.stdout.write(self.style.SUCCESS('Successfully ran generate guest fam ests'))

    def generate_guest_fam_ests(self):
        countries = Country.objects.filter(active_bool=True).exclude(country='EP')
        user = User.objects.get(username='guest')
        applTypeUtility = ApplType.objects.get(application_type='utility')
        applTypeEp = ApplType.objects.get(application_type='ep')
        # countryEp = Country.objects.get(country='EP')
        for country in countries:
            fam = Family.objects.create(
                user=user,
                family_name=country.long_name + ' Patent Estimate',
                family_no='INV-001-' + country.country
            )
            fam.save()
            # if country == countryEp:
            #     init_appl_type = applTypeEp
            # else:
            init_appl_type = applTypeUtility

            if EntitySize.objects.filter(country=country, default_bool=True).exists():
                default_entity_size = EntitySize.objects.get(country=country, default_bool=True)
            else:
                default_entity_size = None
            default_language = country.get_languages().get(appl_type=init_appl_type, default=True).language
            init_appl_details = ApplDetails.objects.create(
                num_indep_claims=2,
                num_claims=10,
                num_claims_multiple_dependent=0,
                num_drawings=5,
                num_pages_claims=2,
                num_pages_description=10,
                num_pages_drawings=5,
                entity_size=default_entity_size,
                language=default_language
            )
            default_doc_format = country.get_country_formats().get(appl_type=init_appl_type, default=True).doc_format
            init_appl_options = CustomApplOptions.objects.create(
                request_examination_early_bool=False,
                doc_format=default_doc_format
            )
            pct_custom_appl_details = CustomApplDetails.objects.create(
                num_indep_claims=2,
                num_claims=10,
                num_claims_multiple_dependent=0,
                num_drawings=5,
                num_pages_claims=2,
                num_pages_description=10,
                num_pages_drawings=5,
            )
            pct_appl_options = CustomApplOptions.objects.create(
                request_examination_early_bool=False,
                doc_format=default_doc_format
            )
            pct_method_customization = PCTMethodCustomization.objects.create(
                custom_appl_details=pct_custom_appl_details,
                custom_appl_options=pct_appl_options
            )
            ep_custom_appl_details = CustomApplDetails.objects.create(
                num_indep_claims=2,
                num_claims=10,
                num_claims_multiple_dependent=0,
                num_drawings=5,
                num_pages_claims=2,
                num_pages_description=10,
                num_pages_drawings=5,
            )
            ep_appl_options = CustomApplOptions.objects.create(
                request_examination_early_bool=False,
                doc_format=default_doc_format
            )
            ep_method_customization = EPMethodCustomization.objects.create(
                custom_appl_details=ep_custom_appl_details,
                custom_appl_options=ep_appl_options
            )
            famEstData = FamEstFormData.objects.create(
                family=fam,
                user=user,
                init_appl_filing_date=datetime.datetime.now(),
                init_appl_details=init_appl_details,
                init_appl_country=country,
                init_appl_type=init_appl_type,
                init_appl_options=init_appl_options,
                pct_method=False,
                pct_method_customization=pct_method_customization,
                pct_country=country,
                isa_country=country,
                isa_entity_size=default_entity_size,
                ep_method=False,
                ep_method_customization=ep_method_customization,
            )
            famEstData.save()
            famEstData.generate_family_options()
            output = io.BytesIO()
            createXLSX.create_workbook(output, fam.id)
            with open('staticfiles/free_estimates/excel/' + str(country.country) + '.xlsx', 'wb') as file:
                file.write(output.getbuffer())
            pdf_output = createPDF.generate_pdf_report(fam.id)
            with open('staticfiles/free_estimates/pdf/' + str(country.country) + '.pdf', 'wb') as file:
                file.write(pdf_output.getbuffer())
            file.close()
