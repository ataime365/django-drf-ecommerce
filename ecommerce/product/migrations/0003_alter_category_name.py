# Generated by Django 4.1.1 on 2023-11-19 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_category_level_category_lft_category_rght_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
