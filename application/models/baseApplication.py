from django.conf import settings
from django.db import models
from djmoney.money import Money

from application import utils as applUtils
from application.models import ApplDetails
from application.models.managers import ApplManager
from application.utils import convert_class_applType
from characteristics.enums import TranslationRequirements
from characteristics.models import Country
from estimation import utils
from famform.models import ApplOptions
from family.models import Family


class BaseApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.TextField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    date_filing = models.DateField()
    details = models.OneToOneField(ApplDetails, on_delete=models.CASCADE)
    prior_appl = models.ForeignKey("self", models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_option = models.OneToOneField(ApplOptions, on_delete=models.CASCADE)

    objects = ApplManager()

    class Meta:
        abstract = False

    def get_appl_type(self):
        return applUtils.convert_class_applType(self)

    def generate_dates(self, options):
        # generate filing estimates
        self._generate_filing_est()

        # generate publication date and estimates
        self._generate_publication(options.publoptions.date_diff)
        # calc last oa
        last_date = self.date_filing

    def _generate_publication(self, publication_diff_from_filing):
        from application.models.publication import Publication
        publ = Publication.objects.create(
            application=self,
            date_publication=self.date_filing + publication_diff_from_filing)
        publ.generate_ests()
        return publ
        # create a publication instance

    def _generate_translation_est(self):
        # take previous appl country
        # translate to new
        if (self.prior_appl):
            prev_language = self.prior_appl.details.language
            language = self.details.language

            from estimation.models import TranslationEstTemplate
            if self.appl_option.translation_implemented.get_enum() is TranslationRequirements.FULL_TRANSLATION:
                start = TranslationEstTemplate.objects.filter(start_language=prev_language)
                if start.filter(end_language=language).exists():
                    translation_est = start.get(end_language=language)
                else:
                    from estimation.models import DefaultTranslationEstTemplate
                    translation_est = DefaultTranslationEstTemplate.objects.first()

                num_words = language.words_per_page * self.details.num_pages_description
                translation_cost = num_words * translation_est.cost_per_word

                date = self.date_filing + translation_est.date_diff
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=date,
                    law_firm_cost=Money(0, 'USD')
                )

                from estimation.models import BaseEst
                BaseEst.objects.create(
                    official_cost=translation_cost,
                    date=date,
                    law_firm_est=lawFirmEst,
                    application=self,
                    translation_bool=True)

    def _generate_filing_est(self):

        # create translation ests
        # no need to include in the same est templates
        # can leave on its own
        self._generate_translation_est()

        from estimation.models import FilingEstimateTemplate
        filing_templates = FilingEstimateTemplate.objects.filter(
            country=self.country,
            appl_type=convert_class_applType(self),
        )
        templates = utils.filter_conditions(filing_templates, self)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            from estimation.models import FilingEstimate
            est = FilingEstimate.objects.create_complex_and_simple_est(
                application=self,
                law_firm_est=lawFirmEst,
                est_template=e,
            )
            ests.append(est)

        return ests
