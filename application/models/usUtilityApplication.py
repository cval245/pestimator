from application.models import BaseUtilityApplication


class USUtilityApplication(BaseUtilityApplication):

    class Meta:
        abstract = False


    def _generate_oa(self, date_request_examination, oas_in):
        ordered_oa = []
        oa_first = [x for x in oas_in if x.oa_prev is None]
        ordered_oa.append(oa_first[0])
        prev_oa = oa_first[0]
        # order array
        complete = False
        while complete is False:
            oa_x = [x for x in oas_in if x.oa_prev == prev_oa]
            if len(oa_x) != 0:
                prev_oa = oa_x[0]
                ordered_oa.append(oa_x[0])
            else:
                complete = True

        date_prev = date_request_examination
        oa_array = []
        prev_oa = None
        final_oa_bool = False
        for oa in ordered_oa:
            date_oa = date_prev + oa.date_diff
            from application.models.usOfficeAction import USOfficeAction
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