# Generated by Django 3.0.7 on 2020-06-08 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0007_auto_20200608_1326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booked',
            options={'verbose_name_plural': 'Book'},
        ),
        migrations.AlterField(
            model_name='booked',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.signup_model'),
        ),
    ]
