from application.models import BaseApplication


class ProvApplication(BaseApplication):
    class Meta:
        abstract = False

    def generate_dates(self, options):
        # generate filing estimates
        print('generate_dates')
        self._generate_filing_est()
