# Generated by Django 4.2.6 on 2023-11-11 11:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pigeon_package_main_app", "0006_rename_project_packageinvitation_package"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="textfile",
            name="font_size",
        ),
    ]