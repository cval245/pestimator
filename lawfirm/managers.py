from django.db import models
from django.utils.text import slugify


class LawFirmManager(models.Manager):

    def create_with_slug(self, lawfirm):
        slug = slugify(lawfirm)

        lawfirm = self.create(
            name=lawfirm.name,
            slug=slug,
            country=lawfirm.country,
            website=lawfirm.website,
            email=lawfirm.email,
            phone=lawfirm.phone,
            long_description=lawfirm.long_description
        )

        return lawfirm
