from application.models import BaseIssue


class Issue(BaseIssue):

    class Meta:
        abstract = False