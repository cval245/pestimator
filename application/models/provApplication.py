from application.models import BaseApplication


class ProvApplication(BaseApplication):
    class Meta:
        abstract = False

    def generate_dates(self, options):
        # generate filing estimates
        self._generate_filing_est()
