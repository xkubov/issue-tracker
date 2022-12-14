# Generated by Django 4.1.3 on 2022-11-17 09:45

from django.db import migrations


def create_default_categories(apps, _):
    """
    Creates default categories during migration.
    """

    # Fetch expected Category model.
    cls = apps.get_model("issues", "Category")
    cls(name="documentation").save()
    cls(name="feature").save()
    cls(name="improvement").save()
    cls(name="bug").save()


class Migration(migrations.Migration):

    dependencies = [
        ("issues", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]
