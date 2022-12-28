# Generated by Django 3.2.9 on 2022-12-27 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20221227_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='siparisurun',
            name='status',
            field=models.CharField(choices=[('hazirlaniyor', 'hazirlaniyor'), ('teslim_edildi', 'teslim_edildi')], default='hazirlaniyor', max_length=20),
        ),
        migrations.AddField(
            model_name='yorum',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='yorum',
            name='image',
            field=models.ImageField(null=True, upload_to='yorumlar'),
        ),
        migrations.AddField(
            model_name='yorum',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.DeleteModel(
            name='YorumFotograf',
        ),
    ]