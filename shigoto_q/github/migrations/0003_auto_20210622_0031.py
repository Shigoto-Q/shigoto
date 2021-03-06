# Generated by Django 3.1.7 on 2021-06-22 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("github", "0002_githubprofile_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repository",
            name="repo_author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="github.githubprofile",
            ),
        ),
    ]
