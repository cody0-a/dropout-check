# Generated by Django 5.1.4 on 2025-01-18 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_dropoutsummary_is_dropout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='student',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='user',
        ),
        migrations.RenameField(
            model_name='dropout',
            old_name='date',
            new_name='year',
        ),
        migrations.RemoveField(
            model_name='dropout',
            name='DropOut_case',
        ),
        migrations.RemoveField(
            model_name='schoolname',
            name='established',
        ),
        migrations.RemoveField(
            model_name='student',
            name='cgpa',
        ),
        migrations.RemoveField(
            model_name='student',
            name='department',
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('staff', 'Staff'), ('principal', 'Principal')], default='12/01/2017', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dropout',
            name='dropout_reason',
            field=models.CharField(choices=[('Academic', 'Academic'), ('Financial', 'Financial'), ('Health', 'Health'), ('Personal', 'Personal'), ('Marriage', 'Marriage'), ('Distance', 'Distance'), ('Death', 'Death'), ('Other', 'Other')], default='Academic', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dropout',
            name='semester',
            field=models.CharField(choices=[('1st Semester', '1st Semester'), ('2nd Semester', '2nd Semester')], default='1st Semester', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='image/default.jpg', height_field=400, upload_to='photos/', width_field=300),
        ),
        migrations.CreateModel(
            name='SchoolAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wereda_name', models.CharField(max_length=100)),
                ('street_name', models.CharField(default='Unknown', max_length=100)),
                ('city', models.CharField(default='Unknown', max_length=100)),
                ('state', models.CharField(default='Unknown', max_length=100)),
                ('region', models.CharField(max_length=64)),
                ('zone_id', models.CharField(max_length=64)),
                ('school_code', models.CharField(max_length=64)),
                ('SchoolName', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='school_address_name', to='account.schoolname')),
            ],
        ),
        migrations.AlterField(
            model_name='schoolname',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.schooladdress'),
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.DeleteModel(
            name='Parent',
        ),
    ]
