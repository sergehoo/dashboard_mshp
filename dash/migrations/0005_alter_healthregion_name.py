# Generated by Django 4.2.15 on 2024-10-02 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0004_rename_poles_regionaux_polesregionaux'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthregion',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]