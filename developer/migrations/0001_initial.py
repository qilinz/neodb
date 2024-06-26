# Generated by Django 3.2.19 on 2023-06-28 05:09

import django.core.validators
import django.db.models.deletion
import markdownx.models
import oauth2_provider.generators
import oauth2_provider.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "client_id",
                    models.CharField(
                        db_index=True,
                        default=oauth2_provider.generators.generate_client_id,
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "redirect_uris",
                    models.TextField(
                        blank=True, help_text="Allowed URIs list, space separated"
                    ),
                ),
                (
                    "post_logout_redirect_uris",
                    models.TextField(
                        blank=True,
                        help_text="Allowed Post Logout URIs list, space separated",
                    ),
                ),
                (
                    "client_type",
                    models.CharField(
                        choices=[
                            ("confidential", "Confidential"),
                            ("public", "Public"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "authorization_grant_type",
                    models.CharField(
                        choices=[
                            ("authorization-code", "Authorization code"),
                            ("implicit", "Implicit"),
                            ("password", "Resource owner password-based"),
                            ("client-credentials", "Client credentials"),
                            ("openid-hybrid", "OpenID connect hybrid"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "client_secret",
                    oauth2_provider.models.ClientSecretField(
                        blank=True,
                        db_index=True,
                        default=oauth2_provider.generators.generate_client_secret,
                        help_text="Hashed on Save. Copy it now if this is a new secret.",
                        max_length=255,
                    ),
                ),
                ("skip_authorization", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "algorithm",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "No OIDC support"),
                            ("RS256", "RSA with SHA-2 256"),
                            ("HS256", "HMAC with SHA-2 256"),
                        ],
                        default="",
                        max_length=5,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="minimum two characters, words and -_. only, no special characters",
                                regex="^\\w[\\w_\\-. ]*\\w$",
                            )
                        ],
                    ),
                ),
                (
                    "description",
                    markdownx.models.MarkdownxField(blank=True, default=""),
                ),
                ("url", models.URLField(blank=True, null=True)),
                ("is_official", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="developer_application",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
