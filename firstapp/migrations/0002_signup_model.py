# Generated by Django 3.0.4 on 2020-05-08 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='signup_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.IntegerField()),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/%y/%m/%d')),
                ('age', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('occupation', models.CharField(blank=True, max_length=250, null=True)),
                ('gender', models.CharField(max_length=250, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Detail',
            },
        ),
    ]
