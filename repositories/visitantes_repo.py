from models.visitantes_model import Visitantes
from models.tickets_model import Tickets
from peewee import *
from datetime import datetime

class VisitantesRepo:
    # --- Creación ---
    @staticmethod
    def crear_visitante(nombre, email=None, altura=None, fecha_registro=None, preferencias_json=None):
        return Visitantes.create(
            nombre=nombre,
            email=email,
            altura=altura,
            fecha_registro=fecha_registro if fecha_registro else datetime.now(),
            preferencias=preferencias_json if preferencias_json else {
                "tipo_favorito": "",
                "restricciones": [],
                "historial_visitas": []
            }
        )

    # --- Lectura ---
    @staticmethod
    def obtener_todos():
        return list(Visitantes.select())

    @staticmethod
    def get_by_id(visitante_id):
        return Visitantes.get_or_none(Visitantes.id == visitante_id)

    @staticmethod
    def tickets_del_visitante(visitante_id):
        return list(Tickets.select().where(Tickets.visitante == visitante_id))

    # --- Eliminación ---
    @staticmethod
    def eliminar(visitante_id):
        try:
            visitante = Visitantes.get_or_none(Visitantes.id == visitante_id)
            if visitante:
                Tickets.delete().where(Tickets.visitante == visitante).execute()
                visitante.delete_instance()
                return True
            return False
        except Exception as e:
            print(f"Error eliminando visitante: {e}")
            return False
