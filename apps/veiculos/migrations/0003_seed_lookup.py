"""
0003_seed_lookup — popula TipoVeiculo, Marca e Modelo.
"""
from django.db import migrations


TIPOS = [
    "Automóvel",
    "Caminhão",
    "Caminhonete / Pickup",
    "Microônibus",
    "Motocicleta",
    "Máquina / Equipamento",
    "Ônibus",
    "Utilitário",
    "Van",
]

# (marca, tipo_padrão, [modelos])
SEED = [
    ("Chevrolet", "Automóvel", [
        ("Onix", "Automóvel"), ("Onix Plus", "Automóvel"), ("Tracker", "Automóvel"),
        ("Spin", "Automóvel"), ("Equinox", "Automóvel"), ("Montana", "Caminhonete / Pickup"),
        ("S10", "Caminhonete / Pickup"), ("Trailblazer", "Automóvel"),
        ("Blazer", "Automóvel"), ("Cruze", "Automóvel"),
    ]),
    ("Citroën", "Automóvel", [
        ("C3", "Automóvel"), ("C4 Cactus", "Automóvel"), ("Aircross", "Automóvel"),
        ("Berlingo", "Utilitário"), ("Jumper", "Van"),
    ]),
    ("Fiat", "Automóvel", [
        ("Argo", "Automóvel"), ("Cronos", "Automóvel"), ("Fastback", "Automóvel"),
        ("Mobi", "Automóvel"), ("Uno", "Automóvel"), ("Palio", "Automóvel"),
        ("Siena", "Automóvel"), ("Toro", "Caminhonete / Pickup"),
        ("Strada", "Caminhonete / Pickup"), ("Dobló", "Utilitário"),
        ("Ducato", "Van"), ("Fiorino", "Utilitário"), ("Pulse", "Automóvel"),
    ]),
    ("Ford", "Automóvel", [
        ("Ka", "Automóvel"), ("Territory", "Automóvel"), ("Bronco Sport", "Automóvel"),
        ("Ranger", "Caminhonete / Pickup"), ("Transit", "Van"),
        ("Cargo 815", "Caminhão"), ("Cargo 1119", "Caminhão"),
    ]),
    ("Honda", "Automóvel", [
        ("City", "Automóvel"), ("City Hatchback", "Automóvel"), ("Civic", "Automóvel"),
        ("HR-V", "Automóvel"), ("CR-V", "Automóvel"), ("WR-V", "Automóvel"),
        ("Fit", "Automóvel"),
    ]),
    ("Hyundai", "Automóvel", [
        ("HB20", "Automóvel"), ("HB20S", "Automóvel"), ("Creta", "Automóvel"),
        ("Tucson", "Automóvel"), ("Santa Fe", "Automóvel"),
    ]),
    ("Iveco", "Van", [
        ("Daily 35-150", "Van"), ("Daily 55-170", "Van"), ("Daily 70-170", "Caminhão"),
        ("Tector 240E28", "Caminhão"), ("Stralis", "Caminhão"),
    ]),
    ("Mercedes-Benz", "Van", [
        ("Sprinter 311", "Van"), ("Sprinter 415", "Van"), ("Sprinter 515", "Van"),
        ("Accelo 815", "Caminhão"), ("Accelo 1016", "Caminhão"),
        ("Atego 1719", "Caminhão"), ("Atego 2426", "Caminhão"),
        ("Axor 2535", "Caminhão"), ("OF 1519", "Ônibus"), ("LO 916", "Microônibus"),
    ]),
    ("Nissan", "Automóvel", [
        ("Kicks", "Automóvel"), ("Versa", "Automóvel"), ("Frontier", "Caminhonete / Pickup"),
        ("Sentra", "Automóvel"),
    ]),
    ("Peugeot", "Automóvel", [
        ("208", "Automóvel"), ("2008", "Automóvel"), ("3008", "Automóvel"),
        ("Partner", "Utilitário"), ("Boxer", "Van"),
    ]),
    ("Renault", "Automóvel", [
        ("Kwid", "Automóvel"), ("Sandero", "Automóvel"), ("Logan", "Automóvel"),
        ("Duster", "Automóvel"), ("Oroch", "Caminhonete / Pickup"),
        ("Kangoo", "Utilitário"), ("Master", "Van"),
    ]),
    ("Scania", "Caminhão", [
        ("P 310", "Caminhão"), ("P 360", "Caminhão"), ("G 410", "Caminhão"),
        ("R 450", "Caminhão"), ("K 360", "Ônibus"),
    ]),
    ("Toyota", "Automóvel", [
        ("Corolla", "Automóvel"), ("Corolla Cross", "Automóvel"), ("Yaris", "Automóvel"),
        ("RAV4", "Automóvel"), ("Hilux", "Caminhonete / Pickup"),
        ("Hilux SW4", "Automóvel"), ("Etios", "Automóvel"),
    ]),
    ("Volkswagen", "Automóvel", [
        ("Gol", "Automóvel"), ("Polo", "Automóvel"), ("Virtus", "Automóvel"),
        ("T-Cross", "Automóvel"), ("Taos", "Automóvel"), ("Nivus", "Automóvel"),
        ("Saveiro", "Caminhonete / Pickup"), ("Amarok", "Caminhonete / Pickup"),
    ]),
    ("Volkswagen Caminhões", "Caminhão", [
        ("Delivery 6.160", "Caminhão"), ("Delivery 9.170", "Caminhão"),
        ("Constellation 17.280", "Caminhão"), ("Constellation 24.280", "Caminhão"),
        ("Worker 13.180", "Caminhão"),
    ]),
    ("Yamaha", "Motocicleta", [
        ("Factor 150", "Motocicleta"), ("Fazer 250", "Motocicleta"),
        ("XTZ 150", "Motocicleta"), ("NMax 160", "Motocicleta"),
    ]),
    ("Honda Motos", "Motocicleta", [
        ("CG 160 Fan", "Motocicleta"), ("CG 160 Start", "Motocicleta"),
        ("Pop 110i", "Motocicleta"), ("Biz 125", "Motocicleta"),
        ("PCX 150", "Motocicleta"), ("CB 300R", "Motocicleta"),
    ]),
    ("Caterpillar", "Máquina / Equipamento", [
        ("Retroescavadeira 416", "Máquina / Equipamento"),
        ("Motoniveladora 120", "Máquina / Equipamento"),
        ("Pá Carregadeira 924", "Máquina / Equipamento"),
    ]),
    ("JCB", "Máquina / Equipamento", [
        ("Retroescavadeira 3CX", "Máquina / Equipamento"),
        ("Pá Carregadeira 457", "Máquina / Equipamento"),
    ]),
    ("Marcopolo", "Ônibus", [
        ("Volare W8", "Microônibus"), ("Volare W9", "Microônibus"),
        ("Ideale 770", "Ônibus"), ("Paradiso G8", "Ônibus"),
    ]),
]


def seed(apps, schema_editor):
    TipoVeiculoDB = apps.get_model("veiculos", "TipoVeiculo")
    MarcaDB       = apps.get_model("veiculos", "Marca")
    ModeloDB      = apps.get_model("veiculos", "Modelo")

    # Cria tipos
    tipos = {}
    for nome in TIPOS:
        obj, _ = TipoVeiculoDB.objects.get_or_create(nome=nome)
        tipos[nome] = obj

    # Cria marcas e modelos
    for marca_nome, _, modelos in SEED:
        marca_obj, _ = MarcaDB.objects.get_or_create(nome=marca_nome)
        for mod_nome, tipo_nome in modelos:
            ModeloDB.objects.get_or_create(
                marca=marca_obj,
                nome=mod_nome,
                defaults={"tipo_veiculo": tipos.get(tipo_nome)},
            )


class Migration(migrations.Migration):

    dependencies = [
        ("veiculos", "0002_lookup_tables"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
