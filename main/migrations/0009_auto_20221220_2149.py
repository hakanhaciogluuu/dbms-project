# Generated by Django 3.2.9 on 2022-12-20 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20221220_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urun',
            name='image',
        ),
        migrations.AddField(
            model_name='urunfotograf',
            name='urun',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.urun'),
        ),
    ]
