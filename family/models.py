from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models import Max


class Family(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    family_name = models.TextField()
    family_no = models.CharField(default='', max_length=20)
    unique_display_no = models.IntegerField()

    # objects = FamilyManager()

    def __str__(self):
        return self.family_nama

    @property
    def get_fam_est_form_data_udn(self):
        return self.famestformdata.unique_display_no

    def save(self, *args, **kwargs):
        if self.pk == None:
            # get all pervious families by user
            max_udn = Family.objects.filter(user=self.user).aggregate(max_udn=Max('unique_display_no'))
            if max_udn['max_udn'] is not None:
                self.unique_display_no = max_udn['max_udn'] + 1
            else:
                self.unique_display_no = 1
        return super(Family, self).save(*args, **kwargs)

    def create_appls(self, famOptions):
        from application.models import BaseApplication
        bob = famOptions.apploptions_set.all()
        for x in bob:
            BaseApplication.objects.create_full(options=x, user=self.user,
                                                family_id=self.id)

        # subtract one from user accounts
        self.user.userprofile.estimates_remaining = self.user.userprofile.estimates_remaining - 1
        self.user.userprofile.save()
               
    def select_all_fam_ests(self):
        appls = self.baseapplication_set.all()
        all_ests = []
        for appl in appls:
            est = appl.select_ests()
            all_ests.append(est)
        return all_ests