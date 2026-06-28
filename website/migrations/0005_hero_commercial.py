# Generated manually for hero commercial fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_videos"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="hero_commercial_url",
            field=models.URLField(
                blank=True,
                help_text="YouTube URL for the featured commercial at the top of the home page",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="hero_commercial_title",
            field=models.CharField(
                blank=True,
                default="Watch Our Commercial",
                max_length=120,
            ),
        ),
    ]
