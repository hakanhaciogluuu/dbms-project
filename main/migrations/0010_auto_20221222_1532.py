# Generated by Django 3.2.9 on 2022-12-22 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0009_auto_20221220_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urunfotograf',
            name='urun',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.urun'),
        ),
        migrations.CreateModel(
            name='Sepet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miktar', models.IntegerField()),
                ('urun', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.urun')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
