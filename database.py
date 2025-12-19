from peewee import *
import envyte

db = PostgresqlDatabase(
    envyte.get("DATABASE"),
    host=envyte.get("HOST"),
    port=int(envyte.get("PORT")),
    user=envyte.get("USER"),
    password=envyte.get("PASSWORD")
)

def inicializar_base(tablas, reiniciar=True):
    if reiniciar:
        db.drop_tables(tablas[::-1], safe=True)
        db.create_tables(tablas, safe=True)
    else:
        db.create_tables(tablas, safe=True)