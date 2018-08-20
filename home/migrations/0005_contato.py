# Generated by Django 2.1 on 2018-08-17 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=35)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('site', models.CharField(max_length=40, null=True)),
                ('celular', models.IntegerField()),
                ('telefone1', models.IntegerField(null=True)),
                ('telefone2', models.IntegerField(null=True)),
                ('foto', models.ImageField(null=True, upload_to='')),
            ],
        ),
    ]
