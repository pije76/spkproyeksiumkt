# Generated by Django 3.2.6 on 2022-12-17 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nama Lengkap'),
        ),
    ]