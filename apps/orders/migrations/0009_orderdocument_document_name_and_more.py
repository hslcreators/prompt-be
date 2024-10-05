# Generated by Django 4.2.7 on 2024-10-05 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0008_orderdocument_remove_order_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderdocument",
            name="document_name",
            field=models.CharField(default="R"),
        ),
        migrations.AlterField(
            model_name="orderdocument",
            name="document",
            field=models.BinaryField(blank=True, null=True),
        ),
    ]