from models.basemodel import BaseModel
from peewee import *
from playhouse.postgres_ext import *
from datetime import datetime, date
from models.atracciones import Atracciones
from models.visitantes import Visitantes

class Tickets(BaseModel):
    visitante = ForeignKeyField(Visitantes, backref='tickets')
    atraccion = ForeignKeyField(Atracciones, backref='tickets', null=True)  # Null si vale para cualquier atracción
    fecha_compra = DateTimeField(default=datetime.now)
    fecha_visita = DateField(null=True)
    tipo_ticket = CharField(null=True)  # "general", "colegio", "empleado"
    detalles_compra = BinaryJSONField(null=True, default={
        "precio": 0.0,
        "descuentos_aplicados": [],
        "servicios_extra": [],
        "metodo_pago": ""
    })
    usado = BooleanField(default=False)
    fecha_uso = DateTimeField(null=True)
