# Generated by Django 5.2.3 on 2025-07-01 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0006_alter_anuncio_condicao_alter_anuncio_marca_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuncio',
            name='marca',
            field=models.CharField(choices=[('Samsung', 'Samsung'), ('Xiaomi', 'Xiaomi'), ('Apple', 'Apple')], default=' ', max_length=20),
        ),
        migrations.AlterField(
            model_name='anuncio',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
