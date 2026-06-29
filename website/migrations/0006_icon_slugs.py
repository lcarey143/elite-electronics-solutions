# Generated manually for icon slug fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_hero_commercial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutcard",
            name="icon",
            field=models.CharField(
                default="shield",
                help_text='Icon key, e.g. "shield", "cctv", "fire"',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="icon",
            field=models.CharField(
                default="cctv",
                help_text="Icon key when no project photo is uploaded",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="icon",
            field=models.CharField(
                default="cctv",
                help_text='Icon key, e.g. "cctv", "access", "fire"',
                max_length=20,
            ),
        ),
    ]
