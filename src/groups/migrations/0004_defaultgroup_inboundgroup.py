# Generated by Django 5.0.4 on 2025-05-21 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0003_alter_group_date_alter_group_guide_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DefaultGroup",
            fields=[],
            options={
                "verbose_name": "Group (Default)",
                "verbose_name_plural": "Groups (Default)",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("groups.group",),
        ),
        migrations.CreateModel(
            name="InboundGroup",
            fields=[],
            options={
                "verbose_name": "Group (Inbound)",
                "verbose_name_plural": "Groups (Inbound)",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("groups.group",),
        ),
    ]
