# Generated by Django 2.1 on 2018-10-23 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Deal', '0003_m_v_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='m_dealmaster',
            name='Cashier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
