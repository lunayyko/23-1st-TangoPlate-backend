# Generated by Django 3.2.6 on 2021-08-11 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewimage',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.review'),
        ),
    ]