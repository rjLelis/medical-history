# Generated by Django 3.0 on 2019-12-23 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imc', '0005_auto_20191223_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imc',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imc', to='imc.Profile', unique=True),
        ),
    ]
