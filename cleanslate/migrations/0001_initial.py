# Generated by Django 3.0b1 on 2019-10-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PetitionTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('doctype', models.CharField(max_length=255)),
                ('data', models.BinaryField()),
            ],
        ),
    ]
