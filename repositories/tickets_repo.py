from models.tickets_model import Tickets
from models.visitantes_model import Visitantes
from models.atracciones_model import Atracciones
from peewee import *
from datetime import datetime

class TicketsRepo:
    # --- Creación ---
    @staticmethod
    def crear_ticket(visitante_id, fecha_compra=None, fecha_visita=None, tipo_ticket=None, detalles_compra_json=None, atraccion_id=None):
        visitante = Visitantes.get_or_none(Visitantes.id == visitante_id)
        atraccion = Atracciones.get_or_none(Atracciones.id == atraccion_id) if atraccion_id else None
        if not visitante:
            return None
        return Tickets.create(
            visitante=visitante,
            atraccion=atraccion,
            fecha_compra=fecha_compra if fecha_compra else datetime.now(),
            fecha_visita=fecha_visita,
            tipo_ticket=tipo_ticket,
            detalles_compra=detalles_compra_json if detalles_compra_json else {
                "precio": 0.0,
                "descuentos_aplicados": [],
                "servicios_extra": [],
                "metodo_pago": ""
            }
        )

    # --- Lectura ---
    @staticmethod
    def obtener_todos():
        return list(Tickets.select())

    @staticmethod
    def tickets_por_visitante(visitante_id):
        return list(Tickets.select().where(Tickets.visitante == visitante_id))

    @staticmethod
    def tickets_por_atraccion(atraccion_id):
        return list(Tickets.select().where(Tickets.atraccion == atraccion_id))

    @staticmethod
    def visitantes_con_ticket_para_atraccion(atraccion_id):
        return list(
            Visitantes.select()
            .join(Tickets, on=(Tickets.visitante == Visitantes.id))
            .where(
                (Tickets.atraccion == atraccion_id) |
                (Tickets.atraccion.is_null(True))
            )
        )

    # --- Actualización ---
    @staticmethod
    def marcar_usado(ticket_id):
        ticket = Tickets.get_or_none(Tickets.id == ticket_id)
        if ticket:
            ticket.usado = True
            ticket.fecha_uso = datetime.now()
            ticket.save()
            return ticket
        return None

# --- Consultas ---
    @staticmethod
    def tickets_tipo_y_precio_menor_a(tipo, precio_maximo):
        return list(
            Tickets.select()
            .where(
                (Tickets.tipo_ticket == tipo) &
                (Tickets.detalles_compra['precio'].cast('float') < precio_maximo)
            )
        )

    @staticmethod
    def tickets_con_descuento(descuento):
        return list(
            Tickets.select()
            .where(
                Tickets.detalles_compra['descuentos_aplicados'].contains([descuento])
            )
        )