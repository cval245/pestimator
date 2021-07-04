from django.db import models
from django.conf import settings

# class FamilyManager(models.Manager):

    # def select_all_fam_ests(self, user):
    #     families = self.filter(user=user)
    #     # BaseEst.objects.filter(application__in)
    #     # all_fam_ests = []
    #     # for fam_count, fam in enumerate(families):    
    #     #     appls = fam.baseapplication_set.all()
    #     #     all_ests = 0
    #     #     for count, appl in enumerate(appls):
    #     #         if count == 0:
    #     #             all_ests = appl.select_ests()
    #     #         else:
    #     #             est = appl.select_ests()
    #     #             all_ests = all_ests.union(est)
    #     #     a = {'family_id': fam.id, 'queryset': all_ests}
    #     #     all_fam_ests.append(a)
    #     # print('all_fam_ests', all_fam_ests)
    #     return families


# Create your models here.
class Family(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    family_name = models.TextField()
    family_no = models.CharField(default='', max_length=20)

    # objects = FamilyManager()

    def __str__(self):
        return self.family_name

    def create_appls(self, famOptions):
        from application.models import BaseApplication
        bob = famOptions.apploptions_set.all()
        for x in bob:
            BaseApplication.objects.create_full(options=x, user=self.user, family_id=self.id)
               
    def select_all_fam_ests(self):
        appls = self.baseapplication_set.all()
        all_ests = []
        for appl in appls:
            est = appl.select_ests()
            all_ests.append(est)
        return all_ests