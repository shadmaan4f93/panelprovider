# Generated by Django 3.0.1 on 2019-12-20 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20191220_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panelprovider',
            name='code',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]