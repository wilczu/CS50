# Generated by Django 3.1.1 on 2020-10-07 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='listingID',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='userID',
            new_name='user',
        ),
    ]
