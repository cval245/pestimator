from application.models import BaseUtilityApplication

from application.models.usOfficeAction import USOfficeAction


class USUtilityApplication(BaseUtilityApplication):
    class Meta:
        abstract = False

    def _generate_oa(self, date_request_examination, oas_in):

        ordered_oa = self._create_ordered_oa(oas_in=oas_in)
        date_prev = date_request_examination
        oa_array = []
        prev_oa = None
        final_oa_bool = False
        for oa in ordered_oa:
            date_oa = date_prev + oa.date_diff
            created_oa = USOfficeAction.objects.create(
                application=self,
                oa_final_bool=final_oa_bool,
                oa_prev=prev_oa,
                date_office_action=date_oa)
            created_oa.generate_ests()
            oa_array.append(created_oa)
            date_prev = date_oa
            prev_oa = created_oa
            if final_oa_bool is False:
                final_oa_bool = True
            else:
                final_oa_bool = False

        return oa_array