
# Generated by Django 2.1.7 on 2019-03-04 18:31


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_articulo', models.CharField(max_length=45)),
                ('codigo_articulo', models.CharField(max_length=45)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('precio_unidad', models.FloatField()),
                ('is_activate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_Categoria', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='articulo',
            name='id_categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articulos.Categoria'),
        ),
    ]
