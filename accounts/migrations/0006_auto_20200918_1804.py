# Generated by Django 3.1.1 on 2020-09-18 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200918_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='like_music',
            field=models.CharField(choices=[('Pop', 'Pop'), ('Rock', 'Rock'), ('Folk', 'Folk'), ('Jazz', 'Jazz'), ('Blues', 'Blues'), ('None', 'None')], default='None', max_length=20),
        ),
    ]