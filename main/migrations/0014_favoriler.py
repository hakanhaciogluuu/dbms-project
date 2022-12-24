# Generated by Django 3.2.9 on 2022-12-23 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0013_yorum_yorum_urun'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favoriler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urun', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.urun')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]