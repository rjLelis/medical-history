# Generated by Django 3.0 on 2019-12-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imc', '0008_profile_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imc',
            name='classificacao',
            field=models.CharField(choices=[('PP', 'Muito abaixo do peso'), ('P', 'Abaixo do peso'), ('M', 'Peso normal'), ('G', 'Obesidade'), ('GG', 'Acima do peso'), ('XG', 'Obesidade II (severa)'), ('XGG', 'Obesidade III (mórbida)')], default='M', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='imc',
            name='imc',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]