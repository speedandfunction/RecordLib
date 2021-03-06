# Generated by Django 3.0b1 on 2019-10-31 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleanslate', '0004_auto_20191030_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='expungementpetitiontemplate',
            name='default',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='sealingpetitiontemplate',
            name='default',
            field=models.BooleanField(null=True),
        ),
        migrations.AddConstraint(
            model_name='expungementpetitiontemplate',
            constraint=models.UniqueConstraint(condition=models.Q(default=True), fields=('default',), name='unique_default_expungement_petition'),
        ),
        migrations.AddConstraint(
            model_name='sealingpetitiontemplate',
            constraint=models.UniqueConstraint(condition=models.Q(default=True), fields=('default',), name='unique_default_sealing_petition'),
        ),
    ]
