from models.visitantes import Visitantes
from models.tickets import Tickets
from peewee import *
from datetime import datetime, date
from playhouse.postgres_ext import *

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

# --- Consultas ---
    @staticmethod
    def visitantes_preferencia_extrema():
        return list(
            Visitantes.select()
            .where(Visitantes.preferencias['tipo_favorito'] == 'extrema')
        )

    @staticmethod
    def visitantes_con_restriccion(restriccion):
        return list(
            Visitantes.select()
            .where(
                Visitantes.preferencias['restricciones'].contains([restriccion])
            )
        )
    
    # --- JSONB ---
    @staticmethod
    def eliminar_restriccion(visitante_id, restriccion):
        visitante = Visitantes.get_or_none(Visitantes.id == visitante_id)
        if not visitante:
            return 0

        restricciones = visitante.preferencias.get("restricciones", [])
        if restriccion not in restricciones:
            return 0

        nuevas = [r for r in restricciones if r != restriccion]
        visitante.preferencias["restricciones"] = nuevas
        return visitante.save()

    @staticmethod
    def agregar_visita_historial(visitante_id, fecha, atracciones_visitadas):
        visitante = Visitantes.get_or_none(Visitantes.id == visitante_id)
        if not visitante:
            return 0

        fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)
        historial = visitante.preferencias.get("historial_visitas", [])

        nueva_visita = {
            "fecha": fecha_str,
            "atracciones_visitadas": atracciones_visitadas
        }

        historial.append(nueva_visita)
        visitante.preferencias["historial_visitas"] = historial

        return visitante.save()
    
    # --- CONSULTAS ÚTILES ---
    @staticmethod
    def visitantes_ordenados_por_tickets():
        return (
            Visitantes
            .select(
                Visitantes,
                fn.COUNT(Tickets.id).alias('total_tickets')
            )
            .join(Tickets, JOIN.LEFT_OUTER)
            .group_by(Visitantes.id)
            .order_by(fn.COUNT(Tickets.id).desc())
        )

    @staticmethod
    def visitantes_gasto_mayor_a(cantidad):
        return (
            Visitantes
            .select(
                Visitantes,
                fn.SUM(
                    Tickets.detalles_compra['precio'].cast('float')
                ).alias('total_gastado')
            )
            .join(Tickets)
            .group_by(Visitantes.id)
            .having(
                fn.SUM(
                    Tickets.detalles_compra['precio'].cast('float')
                ) > cantidad
            )
        )