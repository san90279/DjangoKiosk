# Generated by Django 2.1 on 2018-08-31 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='m_invoice',
            name='FeeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='FeeItem.M_FeeItem'),
        ),
        migrations.AlterField(
            model_name='m_invoice',
            name='Status',
            field=models.CharField(choices=[('0', '作廢'), ('1', '已使用'), ('2', '未使用')], max_length=10),
        ),
    ]
