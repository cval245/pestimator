from django.db import models


class FilingTransformManager(models.Manager):

    def calc_filing_date_for_appl_option(self, appl_type, country, prev_appl_type,
                                         prev_date, prev_appl_option):
        if self.filter(appl_type=appl_type, country=country, prev_appl_type=prev_appl_type).exists():
            cFilTrans = self.get(appl_type=appl_type, country=country, prev_appl_type=prev_appl_type)
            if cFilTrans.trans_complex_time_condition is None:
                return cFilTrans.date_diff + prev_date
            else:
                new_date = cFilTrans.trans_complex_time_condition.calc_complex_time_conditions(prev_date=prev_date,
                                                                                               filing_transform=cFilTrans,
                                                                                               prev_appl_option=prev_appl_option)
                return new_date
        else:
            # default Transform objects
            from transform.models import DefaultFilingTransform
            dFilTrans = DefaultFilingTransform.objects.get(appl_type=appl_type)
            return prev_date + dFilTrans.date_diff
