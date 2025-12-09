from models.basemodel import BaseModel
from peewee import *
from playhouse.postgres_ext import *

class Visitantes(BaseModel):
    nombre = CharField(null=False)
    email = CharField(unique=True, null=True)
    altura = IntegerField(null=True)  # en centímetros
    fecha_registro = DateTimeField(null=True)
    preferencias = BinaryJSONField(null=True, default={
        "tipo_favorito": "",
        "restricciones": [],
        "historial_visitas": [
            # ejemplo:
            # {"fecha": "2024-06-15", "atracciones_visitadas": 8},
            # {"fecha": "2024-08-20", "atracciones_visitadas": 12}
        ]
    })
