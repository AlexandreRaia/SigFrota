from django.db import migrations

TIPOS = [
    ("500-20", "Dirigir sem possuir CNH",                     "GRAVISSIMA"),
    ("501-00", "Dirigir com CNH vencida há mais de 30 dias",  "GRAVISSIMA"),
    ("504-50", "Dirigir segurando celular",                   "GRAVISSIMA"),
    ("516-91", "Dirigir sob influência de álcool",            "GRAVISSIMA"),
    ("518-51", "Excesso de velocidade até 20%",               "MEDIA"),
    ("518-52", "Excesso de velocidade de 20% a 50%",          "GRAVE"),
    ("518-53", "Excesso de velocidade acima de 50%",          "GRAVISSIMA"),
    ("520-70", "Ultrapassagem em local proibido",             "GRAVISSIMA"),
    ("545-21", "Estacionar sobre faixa de pedestres",         "GRAVE"),
    ("554-14", "Estacionar em local proibido",                "MEDIA"),
    ("572-00", "Parar sobre faixa de pedestres",              "GRAVE"),
    ("574-61", "Transitar em faixa exclusiva de ônibus",      "GRAVE"),
    ("583-50", "Desobedecer rodízio/restrição de circulação", "MEDIA"),
    ("605-01", "Avançar sinal vermelho",                      "GRAVISSIMA"),
    ("659-92", "Conduzir veículo sem cinto de segurança",     "GRAVE"),
    ("676-91", "Transportar criança sem cadeirinha",          "GRAVISSIMA"),
    ("736-62", "Uso de película irregular",                   "GRAVE"),
    ("745-50", "Transitar com veículo sem licenciamento",     "GRAVISSIMA"),
    ("757-90", "Veículo licenciado em desacordo",             "GRAVISSIMA"),
    ("763-31", "Dirigir falando ao celular",                  "MEDIA"),
]


def seed(apps, schema_editor):
    TipoMulta = apps.get_model('multas', 'TipoMulta')
    for codigo, descricao, natureza in TIPOS:
        TipoMulta.objects.get_or_create(
            codigo=codigo,
            defaults={"descricao": descricao, "natureza": natureza},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('multas', '0002_tipomulta'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
