# Generated by Django 2.2.6 on 2019-12-17 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20191123_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]