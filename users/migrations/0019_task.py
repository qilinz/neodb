# Generated by Django 4.2.8 on 2024-01-08 03:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0018_apidentity_anonymous_viewable"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=20)),
                (
                    "state",
                    models.IntegerField(
                        choices=[
                            (0, "Pending"),
                            (1, "Started"),
                            (2, "Complete"),
                            (3, "Failed"),
                        ],
                        default=0,
                    ),
                ),
                ("metadata", models.JSONField(default=dict)),
                ("message", models.TextField(default="")),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("edited_time", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["user", "type"], name="users_task_user_id_e29f34_idx"
                    )
                ],
            },
        ),
    ]
