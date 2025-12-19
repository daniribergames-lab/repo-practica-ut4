from database import inicializar_base
from repositories.visitantes_repo import VisitantesRepo
from repositories.atracciones_repo import AtraccionesRepo
from repositories.tickets_repo import TicketsRepo
from models.visitantes import Visitantes
from models.atracciones import Atracciones
from models.tickets import Tickets
from peewee import IntegrityError
from datetime import datetime, date

TIPOS_ATRACCION_VALIDOS = ["extrema", "familiar", "infantil", "acuatica"]
TIPOS_TICKET_VALIDOS = ["general", "colegio", "empleado"]
METODOS_PAGO_VALIDOS = ["tarjeta", "efectivo", "bizum"]
RESTRICCIONES_VALIDAS = ["problemas cardiacos", "vertigo", "embarazo"]
CARACTERISTICAS_VALIDAS = ["looping", "caida libre", "giro 360"]

# ------------------ INIT DB ------------------

def init_db():
    inicializar_base([Visitantes, Atracciones, Tickets])
    print("Base de datos inicializada correctamente.")

# ------------------ CREAR ------------------

def menu_crear():
    while True:
        print("\n--- CREAR ---")
        print("1. Crear visitante")
        print("2. Crear atracción")
        print("3. Crear ticket")
        print("0. Volver")

        op = input("Opción: ")

        if op == '1':
            nombre = input("Nombre: ")
            email = input("Email: ")
            altura = input("Altura (cm): ")

            while True:
                tipo_favorito = input(
                    "Tipo favorito (extrema | familiar | infantil | acuatica): "
                ).lower()

                if tipo_favorito in TIPOS_ATRACCION_VALIDOS:
                    break
                else:
                    print("Tipo no válido. Intente de nuevo.")

            restricciones = []

            while True:
                r = input(
                    "Añadir restricción (problemas cardiacos | vertigo | embarazo) "
                    "(enter para terminar): "
                ).strip().lower()

                if not r:
                    break

                if r in RESTRICCIONES_VALIDAS:
                    if r not in restricciones:
                        restricciones.append(r)
                    else:
                        print("Restricción ya añadida.")
                else:
                    print("Restricción no válida.")
            
            preferencias = {
                "tipo_favorito": tipo_favorito,
                "restricciones": restricciones,
                "historial_visitas": []
            }

            try:
                v = VisitantesRepo.crear_visitante(
                    nombre,
                    email,
                    int(altura) if altura else None,
                    preferencias_json=preferencias
                )
                print(f"Visitante creado con ID {v.id}")
            except IntegrityError:
                print("Error: email duplicado.")

        elif op == '2':
            nombre = input("Nombre: ")

            while True:
                tipo = input(
                    "Tipo (extrema | familiar | infantil | acuatica): "
                ).lower()

                if tipo in TIPOS_ATRACCION_VALIDOS:
                    break
                else:
                    print("Tipo no válido. Intente de nuevo.")

            altura_minima = input("Altura mínima: ")

            caracteristicas = []

            while True:
                c = input(
                    "Añadir característica (looping | caida libre | giro 360) "
                    "(enter para terminar): "
                ).strip().lower()

                if not c:
                    break

                if c in CARACTERISTICAS_VALIDAS:
                    if c not in caracteristicas:
                        caracteristicas.append(c)
                    else:
                        print("Característica ya añadida.")
                else:
                    print("Característica no válida.")

            mantenimiento = []

            while True:
                m = input(
                    "Añadir mantenimiento (HH:MM-HH:MM) (enter para terminar): "
                ).strip()

                if not m:
                    break

                mantenimiento.append(m)

            detalles = {
                "duracion_segundos": int(input("Duración (seg): ") or 0),
                "capacidad_por_turno": int(input("Capacidad: ") or 0),
                "intensidad": int(input("Intensidad: ") or 0),
                "caracteristicas": caracteristicas,
                "horarios": {
                    "apertura": "10:00",
                    "cierre": "22:00",
                    "mantenimiento": mantenimiento
                }
            }

            try:
                a = AtraccionesRepo.crear_atraccion(
                    nombre,
                    tipo,
                    int(altura_minima) if altura_minima else None,
                    detalles
                )
                print(f"Atracción creada con ID {a.id}")
            except IntegrityError:
                print("Error: nombre duplicado.")

        elif op == '3':
            visitante_id = input("ID visitante: ")
            atraccion_id = input("ID atracción (enter si es general): ")

            while True:
                fecha_input = input("Fecha de visita (YYYY-MM-DD): ").strip()

                if not fecha_input:
                    print("La fecha es obligatoria.")
                    continue

                try:
                    fecha_visita = datetime.strptime(fecha_input, "%Y-%m-%d").date()

                    if fecha_visita < date.today():
                        print("La fecha no puede ser anterior a hoy.")
                        continue

                    break
                except ValueError:
                    print("Formato incorrecto. Use YYYY-MM-DD.")

            while True:
                tipo_ticket = input(
                    "Tipo de ticket (general | colegio | empleado): "
                ).lower()

                if tipo_ticket in TIPOS_TICKET_VALIDOS:
                    break
                else:
                    print("Tipo de ticket no válido.")

            while True:
                metodo_pago = input(
                    "Método de pago (tarjeta | efectivo | bizum): "
                ).strip().lower()

                if not metodo_pago:
                    print("El método de pago es obligatorio.")
                    continue

                if metodo_pago in METODOS_PAGO_VALIDOS:
                    break
                else:
                    print("Método de pago no válido.")

            descuentos = []

            if tipo_ticket == "colegio":
                descuentos.append("estudiante")

            detalles = {
                "precio": float(input("Precio: ")),
                "descuentos_aplicados": descuentos,
                "servicios_extra": [],
                "metodo_pago": metodo_pago
            }

            t = TicketsRepo.crear_ticket(
                visitante_id=int(visitante_id),
                fecha_visita=fecha_visita,
                tipo_ticket=tipo_ticket,
                detalles_compra_json=detalles,
                atraccion_id=int(atraccion_id) if atraccion_id else None
            )

            if t:
                print(f"Ticket creado con ID {t.id}")
            else:
                print("Error creando ticket.")

        elif op == '0':
            break

        else:
            print("Opción no válida.")

# ------------------ LEER ------------------

def menu_leer():
    while True:
        print("\n--- LEER ---")
        print("1. Ver visitantes")
        print("2. Ver atracciones")
        print("3. Ver tickets")
        print("4. Tickets de un visitante")
        print("5. Tickets de una atracción")
        print("6. Visitantes con ticket para atracción")
        print("7. Atracciones activas")
        print("0. Volver")

        op = input("Opción: ")

        if op == '1':
            for v in VisitantesRepo.obtener_todos():
                print(v.id, v.nombre)

        elif op == '2':
            for a in AtraccionesRepo.obtener_todas():
                print(a.id, a.nombre)

        elif op == '3':
            for t in TicketsRepo.obtener_todos():
                print(t.id, t.tipo_ticket)

        elif op == '4':
            vid = input("ID visitante: ")
            for t in TicketsRepo.tickets_por_visitante(vid):
                print(t.id)

        elif op == '5':
            aid = input("ID atracción: ")
            for t in TicketsRepo.tickets_por_atraccion(aid):
                print(t.id)

        elif op == '6':
            aid = input("ID atracción: ")
            for v in TicketsRepo.visitantes_con_ticket_para_atraccion(aid):
                print(v.id, v.nombre)

        elif op == '7':
            for a in AtraccionesRepo.obtener_activas():
                print(a.id, a.nombre)

        elif op == '0':
            break

        else:
            print("Opción no válida.")

# ------------------ ACTUALIZAR ------------------

def menu_actualizar():
    while True:
        print("\n--- ACTUALIZAR ---")
        print("1. Marcar ticket como usado")
        print("2. Cambiar estado de atracción")
        print("0. Volver")

        op = input("Opción: ")

        if op == '1':
            tid = input("ID ticket: ")
            t = TicketsRepo.marcar_usado(tid)
            print("Ticket actualizado." if t else "No encontrado.")

        elif op == '2':
            aid = input("ID atracción: ")
            estado = input("¿Activar? (si/no): ").lower() == 's'
            a = AtraccionesRepo.cambiar_estado(aid, estado)
            print("Estado actualizado." if a else "No encontrada.")

        elif op == '0':
            break

        else:
            print("Opción no válida.")

# ------------------ ELIMINAR ------------------

def menu_eliminar():
    while True:
        print("\n--- ELIMINAR ---")
        print("1. Eliminar visitante")
        print("2. Eliminar atracción")
        print("0. Volver")

        op = input("Opción: ")

        if op == '1':
            vid = input("ID visitante: ")
            print("Eliminado." if VisitantesRepo.eliminar(vid) else "No encontrado.")

        elif op == '2':
            aid = input("ID atracción: ")
            print("Eliminada." if AtraccionesRepo.eliminar(aid) else "No encontrada.")

        elif op == '0':
            break

        else:
            print("Opción no válida.")

# ------------------ CONSULTAS ------------------

def ejecutar_consultas():
    """Implementa el menú interactivo para las 8 consultas de 2.5 puntos."""
    while True:
        print("\n--- MENÚ DE CONSULTAS (2.5 PUNTOS) ---")
        print("1. Visitantes con preferencia 'extrema'")
        print("2. Atracciones con intensidad mayor a 7")
        print("3. Tickets 'colegio' con precio < 30€")
        print("4. Atracciones con duración > 120 segundos")
        print("5. Visitantes con restricción 'problemas cardiacos'")
        print("6. Atracciones con 'looping' y 'caida libre'")
        print("7. Tickets con descuento 'estudiante'")
        print("8. Atracciones con mantenimiento programado")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("\nConsulta 1: Visitantes con preferencia 'extrema'")
            visitantes = VisitantesRepo.visitantes_preferencia_extrema()
            if visitantes:
                for v in visitantes:
                    print(f"ID: {v.id}, Nombre: {v.nombre}, Preferencia: {v.preferencias.get('tipo_favorito')}")
            else:
                print("No se encontraron visitantes con preferencia extrema.")

        elif opcion == '2':
            print("\nConsulta 2: Atracciones con intensidad > 7")
            atracciones = AtraccionesRepo.atracciones_por_intensidad_mayor_a(7)
            if atracciones:
                for a in atracciones:
                    print(f"ID: {a.id}, Nombre: {a.nombre}, Intensidad: {a.detalles.get('intensidad')}")
            else:
                print("No se encontraron atracciones con intensidad > 7.")
        
        elif opcion == '3':
            print("\nConsulta 3: Tickets 'colegio' con precio < 30€")
            tickets = TicketsRepo.tickets_tipo_y_precio_menor_a('colegio', 30.0)
            if tickets:
                for t in tickets:
                    precio = t.detalles_compra.get('precio', 0.0)
                    print(f"ID Ticket: {t.id}, Tipo: {t.tipo_ticket}, Precio: {precio}€")
            else:
                print("No se encontraron tickets 'colegio' por menos de 30€.")

        elif opcion == '4':
            print("\nConsulta 4: Atracciones con duración > 120 segundos")
            atracciones = AtraccionesRepo.atracciones_por_duracion_mayor_a(120)
            if atracciones:
                for a in atracciones:
                    print(f"ID: {a.id}, Nombre: {a.nombre}, Duración: {a.detalles.get('duracion_segundos')} segundos")
            else:
                print("No se encontraron atracciones con duración mayor a 120 segundos.")

        elif opcion == '5':
            print("\nConsulta 5: Visitantes con restricción 'problemas_cardiacos'")
            visitantes = VisitantesRepo.visitantes_con_restriccion('problemas_cardiacos')
            if visitantes:
                for v in visitantes:
                    print(f"ID: {v.id}, Nombre: {v.nombre}, Restricciones: {v.preferencias.get('restricciones')}")
            else:
                print("No se encontraron visitantes con esa restricción.")

        elif opcion == '6':
            print("\nConsulta 6: Atracciones con 'looping' y 'caida libre'")
            atracciones = AtraccionesRepo.atracciones_con_caracteristicas('looping', 'caida libre')
            if atracciones:
                for a in atracciones:
                    carac = a.detalles.get('caracteristicas', [])
                    print(f"ID: {a.id}, Nombre: {a.nombre}, Características: {', '.join(carac)}")
            else:
                print("No se encontraron atracciones con ambas características.")

        elif opcion == '7':
            print("\nConsulta 7: Tickets con descuento 'estudiante'")
            tickets = TicketsRepo.tickets_con_descuento('estudiante')
            if tickets:
                for t in tickets:
                    desc = t.detalles_compra.get('descuentos_aplicados', [])
                    print(f"ID Ticket: {t.id}, Descuentos: {', '.join(desc)}")
            else:
                print("No se encontraron tickets con descuento 'estudiante'.")

        elif opcion == '8':
            print("\nConsulta 8: Atracciones con mantenimiento programado")
            atracciones = AtraccionesRepo.atracciones_con_mantenimiento_programado()
            if atracciones:
                for a in atracciones:
                    mant = a.detalles.get('horarios', {}).get('mantenimiento', [])
                    print(f"ID: {a.id}, Nombre: {a.nombre}, Mantenimiento: {', '.join(mant)}")
            else:
                print("No se encontraron atracciones con mantenimiento programado.")

        elif opcion == '0':
            break

        else:
            print("Opción no válida. Intente de nuevo.")

# ------------------ MENÚ PRINCIPAL ------------------

def menu_principal():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Crear")
        print("2. Leer")
        print("3. Actualizar")
        print("4. Eliminar")
        print("5. Consultas")
        print("0. Salir")

        op = input("Opción: ")

        if op == '1':
            menu_crear()
        elif op == '2':
            menu_leer()
        elif op == '3':
            menu_actualizar()
        elif op == '4':
            menu_eliminar()
        elif op == '5':
            ejecutar_consultas()
        elif op == '0':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida.")

# ------------------ MAIN ------------------

if __name__ == "__main__":
    init_db()
    menu_principal()
