# Generated by Django 5.1 on 2024-08-14 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_hash_linkmapping_shortcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmapping',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
