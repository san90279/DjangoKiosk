# Generated by Django 2.1 on 2018-08-27 02:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Station', '0001_initial'),
        ('Deal', '0001_initial'),
        ('Invoice', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FeeItem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='m_dealmaster',
            name='InvoiceNo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Invoice.M_Invoice'),
        ),
        migrations.AddField(
            model_name='m_dealmaster',
            name='StationID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Station.M_Station'),
        ),
        migrations.AddField(
            model_name='m_dealdetail',
            name='Creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='CreatorDetail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='m_dealdetail',
            name='Editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='EditorDetail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='m_dealdetail',
            name='FeeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='FeeItem.M_FeeItem'),
        ),
        migrations.AddField(
            model_name='m_dealdetail',
            name='MasterID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Deal.M_DealMaster'),
        ),
    ]
