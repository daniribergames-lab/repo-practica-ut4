from models.atracciones_model import Atracciones
from peewee import *

class AtraccionesRepo:
    # --- Creación ---
    @staticmethod
    def crear_atraccion(nombre, tipo=None, altura_minima=None, detalles_json=None):
        return Atracciones.create(
            nombre=nombre,
            tipo=tipo,
            altura_minima=altura_minima,
            detalles=detalles_json
        )

    # --- Lectura ---
    @staticmethod
    def obtener_todas():
        return list(Atracciones.select())

    @staticmethod
    def obtener_activas():
        return list(Atracciones.select().where(Atracciones.activa == True))

    @staticmethod
    def get_by_id(atraccion_id):
        return Atracciones.get_or_none(Atracciones.id == atraccion_id)

    # --- Actualización ---
    @staticmethod
    def cambiar_estado(atraccion_id, estado):
        atraccion = Atracciones.get_or_none(Atracciones.id == atraccion_id)
        if atraccion:
            atraccion.activa = estado
            atraccion.save()
            return atraccion
        return None

    # --- Eliminación ---
    @staticmethod
    def eliminar(atraccion_id):
        try:
            atraccion = Atracciones.get_or_none(Atracciones.id == atraccion_id)
            if atraccion:
                atraccion.delete_instance()
                return True
            return False
        except Exception as e:
            print(f"Error eliminando atracción: {e}")
            return False
