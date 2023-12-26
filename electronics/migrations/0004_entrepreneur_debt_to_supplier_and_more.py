# Generated by Django 4.2.8 on 2023-12-26 15:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0003_supplier_debt_to_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrepreneur',
            name='debt_to_supplier',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='entrepreneur',
            name='network_object',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='electronics.networkobject'),
        ),
        migrations.AddField(
            model_name='entrepreneur',
            name='previous_supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplied_entrepreneurs', to='electronics.supplier'),
        ),
        migrations.AddField(
            model_name='factory',
            name='debt_to_supplier',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='factory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='factory',
            name='previous_supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplied_factories', to='electronics.supplier'),
        ),
        migrations.AddField(
            model_name='factory',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factories', to='electronics.supplier'),
        ),
        migrations.AlterField(
            model_name='entrepreneur',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='entrepreneurs', to='electronics.product'),
        ),
        migrations.AlterField(
            model_name='entrepreneur',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entrepreneurs', to='electronics.supplier'),
        ),
        migrations.AlterField(
            model_name='factory',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='networkobject',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_network_objects', to='electronics.supplier'),
        ),
        migrations.AlterField(
            model_name='product',
            name='debt_to_supplier',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplied_products', to='electronics.supplier'),
        ),
        migrations.CreateModel(
            name='RetailNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('house_number', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('debt_to_supplier', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('network_object', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='electronics.networkobject')),
                ('previous_supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplied_retail_networks', to='electronics.supplier')),
                ('products', models.ManyToManyField(blank=True, related_name='retail_networks', to='electronics.product')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='retail_networks', to='electronics.supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]