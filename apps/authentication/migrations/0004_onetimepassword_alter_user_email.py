# Generated by Django 4.2.7 on 2023-12-09 19:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0003_printer"),
    ]

    operations = [
        migrations.CreateModel(
            name="OneTimePassword",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("otp", models.CharField(blank=True, max_length=5)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("expiry_date", models.DateTimeField(auto_now=True)),
                ("dummy", models.CharField(max_length=5)),
                ("is_expired", models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
