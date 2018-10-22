# Generated by Django 2.1 on 2018-10-22 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataEntrada', models.DateField()),
                ('dataSaida', models.DateField()),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Consulta_Agenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataconsultada', models.DateTimeField(auto_now_add=True)),
                ('agenda', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='agenda.Agenda')),
            ],
        ),
        migrations.CreateModel(
            name='Entre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('descricao', models.TextField()),
                ('criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
