from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.models import TagBase, GenericTaggedItemBase


class GuardedTag(TagBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class TaggedWhatever(GenericTaggedItemBase):
    tag = models.ForeignKey(
        GuardedTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
