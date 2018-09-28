# Generated by Django 2.1 on 2018-09-26 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('cnpj', models.IntegerField()),
                ('inscricaoestadual', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('site', models.CharField(max_length=50)),
                ('cep', models.IntegerField()),
                ('endereco', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('bairro', models.CharField(max_length=20)),
                ('telefone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Condicao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condicao', models.CharField(max_length=15)),
            ],
        ),
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
                ('foto', models.ImageField(blank=True, null=True, upload_to='clients_photos')),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('capacidade', models.IntegerField()),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Condicao')),
            ],
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiposervico', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TipoSala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='sala',
            name='tipo',
            field=models.ManyToManyField(blank=True, to='home.TipoSala'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='contato',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Contato'),
        ),
    ]
