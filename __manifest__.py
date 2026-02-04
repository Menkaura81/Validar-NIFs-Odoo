{
    "name": "Validacion NIF",
    "author": "Alcalink",
    "summary": "Valida NIFs desde archivos CSV",
    "version": "1.2",
    "installable": True,
    "license": "LGPL-3",
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/nif_validator_views.xml",
    ],
}