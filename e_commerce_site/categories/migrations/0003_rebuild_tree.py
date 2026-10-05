from django.db import migrations


def rebuild_tree(apps, schema_editor):
    from categories.models import Category

    Category.objects.rebuild()


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_alter_category_options_category_level_category_lft_and_more"),
    ]

    operations = [
        migrations.RunPython(rebuild_tree, migrations.RunPython.noop),
    ]
