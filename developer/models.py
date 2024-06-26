from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField
from oauth2_provider.models import AbstractApplication

from journal.models.renderers import render_md


class Application(AbstractApplication):
    name = models.CharField(
        max_length=255,
        blank=False,
        validators=[
            RegexValidator(
                regex=r"^\w[\w_\-. ]*\w$",
                message=_(
                    "minimum two characters, words and -_. only, no special characters"
                ),
            ),
        ],
    )
    description = MarkdownxField(default="", blank=True)
    url = models.URLField(null=True, blank=True)
    is_official = models.BooleanField(default=False)
    unique_together = [["user", "name"]]
    redirect_uris = models.TextField(
        blank=False,
        help_text=_("Allowed URIs list, space separated, at least one URI is required"),
    )

    def description_html(self):
        return render_md(self.description)
