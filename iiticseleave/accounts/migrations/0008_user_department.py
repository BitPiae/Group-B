# Generated by Django 2.0.1 on 2018-03-15 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20180315_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(default='CSE', max_length=5),
        ),
    ]
