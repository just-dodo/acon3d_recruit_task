# Generated by Django 4.1 on 2022-08-29 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("merchandises", "0004_merchcontent_unique_content_for_each_lang"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="merchcontent",
            name="unique_content_for_each_lang",
        ),
        migrations.RenameField(
            model_name="merchcontent",
            old_name="merchendise",
            new_name="merchandise",
        ),
        migrations.AddConstraint(
            model_name="merchcontent",
            constraint=models.UniqueConstraint(
                fields=("merchandise", "language"), name="unique_content_for_each_lang"
            ),
        ),
    ]