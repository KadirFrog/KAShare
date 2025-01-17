# Generated by Django 5.0.6 on 2024-06-29 09:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=100)),
                ('test_date', models.DateField()),
                ('related_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classtests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
