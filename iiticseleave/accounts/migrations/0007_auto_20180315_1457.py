# Generated by Django 2.0.1 on 2018-03-15 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180315_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='designation',
            field=models.IntegerField(choices=[(0, 'Associate Professor'), (1, 'Assistant Professor'), (2, 'Professor'), (3, 'Other')], default=3),
        ),
    ]
