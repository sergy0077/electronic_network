# Generated by Django 4.2.8 on 2023-12-24 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrepreneur',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, related_name='entrepreneurs', to='electronics.product'),
        ),
        migrations.AlterField(
            model_name='factory',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='factories', to='electronics.product'),
        ),
    ]
