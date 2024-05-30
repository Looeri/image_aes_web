# Generated by Django 5.0.4 on 2024-05-07 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='image_encrpto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plainimage', models.ImageField(upload_to='image:plain')),
                ('key', models.BinaryField(max_length=256)),
                ('cryptoimage', models.ImageField(upload_to='image:crypto')),
                ('preview', models.ImageField(blank=True, upload_to='image:preview')),
            ],
        ),
    ]
