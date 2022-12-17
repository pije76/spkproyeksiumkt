# Generated by Django 3.2.6 on 2022-12-17 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyek', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kegiatan', models.CharField(blank=True, max_length=255, null=True)),
                ('kode', models.CharField(blank=True, choices=[('-', '-'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('AA', 'AA')], default='-', max_length=255, null=True)),
                ('duration', models.FloatField(blank=True, null=True)),
                ('predecessor', models.CharField(blank=True, choices=[('-', '-'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], default='-', max_length=255, null=True)),
                ('earliest_start', models.FloatField(blank=True, null=True, verbose_name='ES')),
                ('earliest_finish', models.FloatField(blank=True, null=True, verbose_name='EF')),
                ('latest_start', models.FloatField(blank=True, null=True, verbose_name='LS')),
                ('latest_finish', models.FloatField(blank=True, null=True, verbose_name='LF')),
                ('slack_time', models.FloatField(blank=True, null=True, verbose_name='Slack')),
                ('critical', models.CharField(blank=True, max_length=255, null=True)),
                ('successors', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'CPM',
                'verbose_name_plural': 'CPM',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minggu', models.IntegerField(blank=True, null=True, verbose_name='Minggu')),
                ('progress_rencana', models.FloatField(blank=True, null=True, verbose_name='Progress Rencana')),
                ('progress_aktual', models.FloatField(blank=True, null=True, verbose_name='Progress Aktual')),
                ('acwp', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Actual Cost of Work Planned')),
                ('bcwp', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Budgeted Cost of Work Planned ')),
                ('bcws', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Budgeted Cost of Work Schedule')),
                ('cost_variance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cost Variance')),
                ('cost_performance_index', models.FloatField(blank=True, null=True, verbose_name='Cost Performance Index')),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedule',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Kegiatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_kegiatan', models.CharField(max_length=255, null=True, verbose_name='Nama Kegiatan')),
                ('kode', models.CharField(blank=True, choices=[('-', '-'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('AA', 'AA')], default='-', max_length=255, null=True)),
                ('bobot_kegiatan', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Bobot Kegiatan')),
                ('biaya_kegiatan', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='Biaya Kegiatan')),
                ('predecessor', models.CharField(blank=True, choices=[('-', '-'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], default='-', max_length=255, null=True)),
                ('hubungan_keterkaitan', models.CharField(blank=True, choices=[('', '-'), ('S-S', 'Start to Start'), ('F-S', 'Finish to Start'), ('F-F', 'Finish to Finish')], default='ss', max_length=255, null=True)),
                ('duration', models.FloatField(blank=True, null=True)),
                ('proyek', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='proyek.proyek')),
            ],
            options={
                'verbose_name': 'Kegiatan',
                'verbose_name_plural': 'Kegiatan',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PERT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.FloatField(blank=True, null=True)),
                ('optimistic_time', models.FloatField(blank=True, null=True, verbose_name='Optimistic Time')),
                ('most_likely_time', models.FloatField(blank=True, null=True, verbose_name='Most Likely Time')),
                ('pessimistic_time', models.FloatField(blank=True, null=True, verbose_name='Pessimistic Time')),
                ('standar_deviasi', models.FloatField(blank=True, null=True, verbose_name='Standar Deviasi')),
                ('varians_kegiatan', models.FloatField(blank=True, null=True, verbose_name='Varians Kegiatan')),
                ('kegiatan', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='kegiatan.kegiatan')),
            ],
            options={
                'verbose_name': 'PERT',
                'verbose_name_plural': 'PERT',
                'ordering': ('id',),
            },
        ),
    ]
