
from repositories.atracciones_repo import AtraccionesRepo
from repositories.visitantes_repo import VisitantesRepo
from repositories.tickets_repo import TicketsRepo
from models.visitantes import Visitantes 
from models.atracciones import Atracciones
from models.tickets import Tickets
from database import db 
from peewee import fn
from datetime import datetime



def ejecutar_consultas():
    """Implementa el menú interactivo para las 8 consultas de 2.5 puntos."""
    while True:
        print("\n--- MENÚ DE CONSULTAS (2.5 PUNTOS) ---")
        print("1. Visitantes con preferencia 'extrema'")
        print("2. Atracciones con intensidad mayor a 7")
        print("3. Tickets 'colegio' con precio < 30€")
        print("4. Atracciones con duración > 120 segundos")
        print("5. Visitantes con restricción 'problemas_cardiacos'")
        print("6. Atracciones con 'looping' y 'caída libre'")
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
            print("\nConsulta 6: Atracciones con 'looping' y 'caída libre'")
            atracciones = AtraccionesRepo.atracciones_con_caracteristicas('looping', 'caída libre')
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


def menu_principal():
    """Muestra el menú principal y gestiona las opciones de la aplicación."""
    
    while True:
        print("\n--- SISTEMA DE GESTIÓN PARQUE DE ATRACCIONES ---")
        print("1. Gestión de Visitantes (CRUD)")
        print("2. Gestión de Atracciones (CRUD)")
        print("3. Gestión de Tickets (CRUD)")
        print("4. CONSULTAS (2.5 Puntos)")
        print("5. Consultas Útiles (3 Puntos)") 
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '4':
            ejecutar_consultas() 
        elif opcion == '5':
            print("\nConsultas Útiles (3 Puntos) pendientes de implementar.")
        elif opcion == '0':
            print("Cerrando el sistema. Hasta pronto!")
            break
        elif opcion in ('1', '2', '3'):
            print(f"Opción {opcion} (CRUD) pendiente de implementación.")
        else:
            print("Opción no válida. Intente de nuevo.")



if __name__ == '__main__':
    try:
        db.connect()
        db.create_tables([Visitantes, Atracciones, Tickets])
        print("Conexión a la base de datos exitosa. Tablas verificadas/creadas.")
    except Exception as e:
        print(f"Error al iniciar la DB. Asegúrate que la base de datos esté corriendo: {e}")

    menu_principal()
    
    if not db.is_closed():
        db.close()