# Generated by Django 4.1.4 on 2022-12-08 01:18

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
            ],
        ),

    ]
