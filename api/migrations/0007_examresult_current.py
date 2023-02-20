# Generated by Django 4.1.4 on 2023-02-20 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_examresultdetail_examresult"),
    ]

    operations = [
        migrations.AddField(
            model_name="examresult",
            name="current",
            field=models.ForeignKey(
                default=11,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="current",
                to="api.topic",
            ),
            preserve_default=False,
        ),
    ]
