# Generated by Django 4.1.4 on 2023-01-17 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_result_current_question_number_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="result",
            name="current_question_number",
        ),
        migrations.RemoveField(
            model_name="result",
            name="current_question_result",
        ),
        migrations.RemoveField(
            model_name="student",
            name="question_list",
        ),
    ]
