# Generated by Django 2.1.3 on 2018-12-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deal', '0004_auto_20181023_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='m_dealmaster',
            name='IsOutsidePay',
            field=models.BooleanField(default=False),
        ),
    ]