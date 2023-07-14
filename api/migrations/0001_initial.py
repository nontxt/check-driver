# Generated by Django 4.2.3 on 2023-07-14 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('api_key', models.CharField(unique=True)),
                ('check_type', models.CharField(choices=[('kit', 'kitchen'), ('cli', 'client')])),
                ('point_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('kit', 'kitchen'), ('cli', 'client')])),
                ('order', models.JSONField()),
                ('status', models.CharField(choices=[('n', 'new'), ('r', 'rendered'), ('p', 'printed')])),
                ('pdf_file', models.FileField(blank=True, upload_to='pdf/')),
                ('printer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='api.printer')),
            ],
        ),
    ]