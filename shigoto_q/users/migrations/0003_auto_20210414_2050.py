# Generated by Django 3.1.7 on 2021-04-14 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("djstripe", "0007_2_4"),
        ("users", "0002_auto_20210408_1403"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                help_text="Stripe Customer Object",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="djstripe.customer",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="subscription",
            field=models.ForeignKey(
                blank=True,
                help_text="Stripe Subscripton Object",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="djstripe.subscription",
            ),
        ),
    ]
