from django.db import models
from characteristics.models import Country, ApplType
from relativedeltafield import RelativeDeltaField

# Create your models here.
class BaseTransform(models.Model):
    date_diff = RelativeDeltaField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class DefaultFilingTransform(models.Model):
    date_diff = RelativeDeltaField()
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)

class CustomFilingTransform(BaseTransform):
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    prev_appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE,
                                       null=True, related_name='prev_appl_type')

class PublicationTransform(BaseTransform):
    pass

class OATransform(BaseTransform):
    # oa_num = models.IntegerField()
    pass

class USOATransform(OATransform):
    final_oa_bool = models.BooleanField(default=False)
    pass

class AllowanceTransform(BaseTransform):
    pass

class IssueTransform(BaseTransform):
    pass

# oa_group
# class OAGroupTransform(BaseTransform):
#     pass

class CountryOANum(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    oa_total = models.IntegerField()



class DefaultCountryOANum(models.Model):
    oa_total = models.IntegerField()

class BaseDefaultTransform(models.Model):
    date_diff = RelativeDeltaField()
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)


class DefaultPublTransform(BaseDefaultTransform):
    pass

class DefaultOATransform(BaseDefaultTransform):
    pass

class DefaultAllowanceTransform(BaseDefaultTransform):
    pass

class DefaultIssueTransform(BaseDefaultTransform):
    pass
