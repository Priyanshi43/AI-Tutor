# Generated by Django 5.2.3 on 2025-06-29 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0003_remove_quizattempt_correct_option_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='correct_answer',
            field=models.CharField(default='A', max_length=1),
        ),
    ]
