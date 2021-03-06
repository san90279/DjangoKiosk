# Generated by Django 2.1 on 2018-08-31 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Menu', '0003_auto_20180723_1329'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='M_Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InvoiceNo', models.CharField(max_length=20, unique=True)),
                ('Status', models.CharField(choices=[('0', '作廢'), ('1', '已使用')], max_length=10)),
                ('Amount', models.IntegerField(null=True)),
                ('CreateDate', models.DateTimeField(auto_now=True)),
                ('EditDate', models.DateTimeField(null=True)),
                ('Creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('Editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Editor', to=settings.AUTH_USER_MODEL)),
                ('FeeID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Menu.M_Menu')),
            ],
        ),
    ]
