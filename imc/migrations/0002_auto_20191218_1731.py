# Generated by Django 3.0 on 2019-12-18 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
