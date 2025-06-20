# Generated by Django 5.2.3 on 2025-06-14 06:40

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='equipment',
            field=models.TextField(help_text='ノートPC、外付けモニター、ヘッドセットなど', verbose_name='設備'),
        ),
        migrations.AlterField(
            model_name='space',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, help_text='半個室: 500円、完全個室: 1000円（設備は共通）', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='時間単価（円）'),
        ),
    ]
