# Generated by Django 2.1 on 2018-10-06 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_auto_20180923_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestador',
            name='telefone',
            field=models.CharField(default=55555, max_length=15, verbose_name='Telefone'),
            preserve_default=False,
        ),
    ]
