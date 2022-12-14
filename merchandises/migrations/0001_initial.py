# Generated by Django 3.2.15 on 2022-08-24 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('name', models.CharField(max_length=500)),
                ('released_at', models.DateTimeField(default=None, null=True)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('commission_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='merchandises', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MerchContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('language', models.CharField(choices=[('ko', 'Korean'), ('en', 'English'), ('zh', 'Chinese')], default='Korean', max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField(blank=True, max_length=10000, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('merchendise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='merchandises.merchandise')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
