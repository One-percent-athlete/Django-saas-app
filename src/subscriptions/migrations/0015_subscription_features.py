# Generated by Django 5.0.7 on 2024-09-03 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0014_alter_subscriptionprice_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='features',
            field=models.TextField(blank=True, help_text='Features for pricing, seperated by new line', null=True),
        ),
    ]
