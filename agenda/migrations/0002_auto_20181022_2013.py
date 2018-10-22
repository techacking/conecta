# Generated by Django 2.1 on 2018-10-22 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        ('agenda', '0001_initial'),
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta_agenda',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Cliente'),
        ),
        migrations.AddField(
            model_name='agenda',
            name='pedido',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.Pedido'),
        ),
        migrations.AddField(
            model_name='agenda',
            name='sala',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Sala'),
        ),
    ]