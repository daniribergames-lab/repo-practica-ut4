from models.atracciones import Atracciones
from models.visitantes import Visitantes
from models.tickets import Tickets
from peewee import *
from datetime import date
from playhouse.postgres_ext import *

class AtraccionesRepo:
    # --- Creación ---
    @staticmethod
    def crear_atraccion(nombre, tipo=None, altura_minima=None, detalles_json=None, activa=True, fecha_inauguracion=None):
        return Atracciones.create(
            nombre=nombre,
            tipo=tipo,
            altura_minima=altura_minima,
            detalles=detalles_json if detalles_json else {
                "duracion_segundos": 0,
                "capacidad_por_turno": 0,
                "intensidad": 0,
                "caracteristicas": [],
                "horarios": {
                    "apertura": "10:00",
                    "cierre": "22:00",
                    "mantenimiento": []
                }
            },
            activa=activa,
            fecha_inauguracion=fecha_inauguracion if fecha_inauguracion else date.today()
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

# --- Consultas ---
    @staticmethod
    def atracciones_por_intensidad_mayor_a(intensidad_minima):
        return list(
            Atracciones.select()
            .where(Atracciones.detalles['intensidad'].cast('int') > intensidad_minima)
        )

    @staticmethod
    def atracciones_por_duracion_mayor_a(duracion_segundos):
        return list(
            Atracciones.select()
            .where(Atracciones.detalles['duracion_segundos'].cast('int') > duracion_segundos)
        )

    @staticmethod
    def atracciones_con_caracteristicas(caracteristica1, caracteristica2):
        return list(
            Atracciones.select()
            .where(
                Atracciones.detalles['caracteristicas'].contains([caracteristica1]) &
                Atracciones.detalles['caracteristicas'].contains([caracteristica2])
            )
        )

    @staticmethod
    def atracciones_con_mantenimiento_programado():
        from peewee import fn
        return list(
            Atracciones.select().where(
                fn.jsonb_array_length(
                    Atracciones.detalles['horarios']['mantenimiento']
                    .cast('jsonb')
                ) > 0
            )
        )

    # --- JSONB ---
    @staticmethod
    def agregar_caracteristica(atraccion_id, caracteristica):
        atraccion = Atracciones.get_or_none(Atracciones.id == atraccion_id)
        if not atraccion:
            return 0

        caracteristicas = atraccion.detalles.get('caracteristicas', [])
        if caracteristica in caracteristicas:
            return 0

        caracteristicas.append(caracteristica)
        atraccion.detalles['caracteristicas'] = caracteristicas
        return atraccion.save()
    
    # --- CONSULTAS ÚTILES ---
    @staticmethod
    def top_5_atracciones_mas_vendidas():
        return (
            Atracciones
            .select(
                Atracciones,
                fn.COUNT(Tickets.id).alias('ventas')
            )
            .join(Tickets)
            .where(Tickets.atraccion.is_null(False))
            .group_by(Atracciones.id)
            .order_by(fn.COUNT(Tickets.id).desc())
            .limit(5)
        )

    @staticmethod
    def atracciones_compatibles_para_visitante(visitante_id):
        visitante = Visitantes.get_or_none(Visitantes.id == visitante_id)
        if not visitante:
            return []

        tipo = visitante.preferencias.get('tipo_favorito')

        return Atracciones.select().where(
            (Atracciones.activa == True) &
            (Atracciones.tipo == tipo) &
            (Atracciones.altura_minima <= visitante.altura)
        )
