# Generated by Django 5.0.4 on 2025-05-21 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0002_group_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="group",
            name="guide",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="groups.guide",
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="tax_threshold",
            field=models.DecimalField(decimal_places=2, default=70, max_digits=10),
        ),
    ]
