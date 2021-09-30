# from django.db.models.signals import post_save
#
# from account.models import UserProfile
# from user.models import User
#
# def first_estimate_free(sender, instance, **kwargs):
#     print('some infor', instance, sender)
#     UserProfile.objects.create(user=instance, estimates_remaining=1)
#
# post_save.connect(first_estimate_free, sender=User)
