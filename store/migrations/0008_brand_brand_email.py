# Generated by Django 3.0.5 on 2023-03-17 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_productv'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='Brand_Email',
            field=models.EmailField(default='default', max_length=100),
        ),
    ]