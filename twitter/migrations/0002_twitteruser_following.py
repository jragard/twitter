# Generated by Django 2.1.4 on 2018-12-13 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='following',
            field=models.ManyToManyField(related_name='_twitteruser_following_+', to='twitter.TwitterUser'),
        ),
    ]