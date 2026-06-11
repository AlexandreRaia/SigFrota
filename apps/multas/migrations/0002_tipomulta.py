import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multas', '0001_initial'),
    ]

    operations = [
        # 1. Criar TipoMulta
        migrations.CreateModel(
            name='TipoMulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo',    models.CharField(max_length=20, unique=True, verbose_name='Código DENATRAN')),
                ('descricao', models.CharField(max_length=200, verbose_name='Descrição')),
                ('natureza',  models.CharField(
                    choices=[
                        ('LEVE',       'Leve'),
                        ('MEDIA',      'Média'),
                        ('GRAVE',      'Grave'),
                        ('GRAVISSIMA', 'Gravíssima'),
                    ],
                    max_length=12,
                    verbose_name='Natureza',
                )),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
            options={
                'verbose_name':        'Tipo de Multa',
                'verbose_name_plural': 'Tipos de Multa',
                'ordering':            ['codigo'],
            },
        ),

        # 2. Remover campo CharField tipo_infracao antigo
        migrations.RemoveField(model_name='multa', name='tipo_infracao'),

        # 3. Remover codigo_denatran (agora faz parte do TipoMulta)
        migrations.RemoveField(model_name='multa', name='codigo_denatran'),

        # 4. Adicionar FK tipo_infracao → TipoMulta
        migrations.AddField(
            model_name='multa',
            name='tipo_infracao',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='multas',
                to='multas.tipomulta',
                verbose_name='Tipo de Infração',
            ),
        ),
    ]
