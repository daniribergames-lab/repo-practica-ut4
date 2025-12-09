from models.basemodel import BaseModel
from peewee import *
from playhouse.postgres_ext import *
from datetime import date

class Atracciones(BaseModel):
    nombre = CharField(unique=True, null=False)
    tipo = CharField(null=True)  # "extrema", "familiar", "infantil", "acuatica"
    altura_minima = IntegerField(null=True)  # en cm
    detalles = BinaryJSONField(null=True, default={
        "duracion_segundos": 0,
        "capacidad_por_turno": 0,
        "intensidad": 0,
        "caracteristicas": [],
        "horarios": {
            "apertura": "10:00",
            "cierre": "22:00",
            "mantenimiento": []
        }
    })
    activa = BooleanField(default=True)
    fecha_inauguracion = DateField(default=date.today)
