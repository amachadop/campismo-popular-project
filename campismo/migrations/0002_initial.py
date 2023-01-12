# Generated by Django 4.1.4 on 2023-01-04 01:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campismo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='valoracioncampismo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_valoracion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservaexcursion',
            name='instancia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instancia_reserva', to='campismo.instanciaexcursion'),
        ),
        migrations.AddField(
            model_name='reservaexcursion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_excursion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservacampismo',
            name='campismo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='campismo_reserva', to='campismo.campismo'),
        ),
        migrations.AddField(
            model_name='reservacampismo',
            name='habitacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='habitacion_reserva', to='campismo.habitacioncampismo'),
        ),
        migrations.AddField(
            model_name='reservacampismo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_reserva', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='instanciaexcursion',
            name='excursion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='excursion_instancia', to='campismo.excursion'),
        ),
        migrations.AddField(
            model_name='habitacioncampismo',
            name='campismo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campismo_habitacion', to='campismo.campismo'),
        ),
        migrations.AddField(
            model_name='comentarioexcursion',
            name='excursion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='excursion_comentario', to='campismo.excursion'),
        ),
        migrations.AddField(
            model_name='comentarioexcursion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_comentario_excursion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campismo',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campismo_provincia', to='campismo.provincia'),
        ),
    ]
