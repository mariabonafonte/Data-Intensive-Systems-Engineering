import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.flushdb()
def ejercicio1():
    r.hset("equipo:1", mapping={
        "nombre": "Leones FC", 
        "ciudad": "Madrid", 
        "entrenador": "Carlos Ruiz", 
        "fundacion":1920
    })
    r.hset("equipo:2", mapping={
            "nombre": "Aguilas Deportivas", 
            "ciudad": "Barcelona", 
            "entrenador": "Ana Martinez", 
            "fundacion":1935
    })
    r.hset("equipo:3", mapping={
                "nombre": "Tiburones FC", 
                "ciudad": "Valencia", 
                "entrenador": "David Gonzalez", 
                "fundacion":1948
    })

    for i in range(1, 4):
        print(r.hgetall(f"equipo:{i}"))
    
def ejercicio2():
    r.zadd("clasificacion", {"equipo:1": 0, "equipo:2": 0, "equipo:3": 0})

def ejercicio3():
        r.hset("jugador:1", mapping={
            "nombre": "Luis Torres", 
            "edad": 25, 
            "posicion": "delantero", 
            "equipo": "equipo:1"
        })

        r.hset("jugador:2", mapping={
            "nombre": "María Rodriguez", 
            "edad": 28, 
            "posicion": "centrocampista", 
            "equipo": "equipo:2"
        })

        r.hset("jugador:3", mapping={
            "nombre": "Javier Lopez", 
            "edad": 22, 
            "posicion": "defensa", 
            "equipo": "equipo:3"
        })
        r.hset("jugador:4", mapping={
            "nombre": "Sofía García", 
            "edad": 26, 
            "posicion": "delantero", 
            "equipo": "equipo:1"
        })
        for i in range(1, 5):
                print(r.hgetall(f"jugador:{i}"))

def ejercicio4():
    r.zadd("goleadores", {"jugador:1": 0, "jugador:2": 0, "jugador:3": 0, "jugador:4": 0})

def ejercicio5():
    r.rpush("partidos", "partido:1", "partido:2", "partido:3")

    r.hset("partido:1", mapping={
        "local": "equipo:1", 
        "visitante": "equipo:2", 
        "resultado": "2-1",
        #"fecha": ""
    })
    r.hset("partido:2", mapping={
        "local": "equipo:3", 
        "visitante": "equipo:1", 
        "resultado": "0-0",
        #"fecha": ""
    })
    r.hset("partido:3", mapping={
        "local": "equipo:2", 
        "visitante": "equipo:3", 
        "resultado": "3-2",
        #"fecha": ""
    })

def ejercicio6():
     r.zincrby("clasificacion",4.0, "equipo:1")
     r.zincrby("clasificacion", 3.0, "equipo:2")
     r.zincrby("clasificacion", 1.0, "equipo:3")

def ejercicio7():
    r.zincrby("goleadores", 2.0, "jugador:1") 
    r.zincrby("goleadores", 3.0, "jugador:2")
    r.zincrby("goleadores", 1.0, "jugador:4")

def ejercicio8(): 
    r.hset("partido:4", mapping={
        "local": "equipo:1", 
        "visitante": "equipo:3", 
        #"resultado": "2-1",
        "fecha": "21-10-1026"
    })
    r.hset("partido:5", mapping={
        "local": "equipo:2", 
        "visitante": "equipo:1", 
        #"resultado": "0-0",
        "fecha": "28-10-2026"
    })

    r.rpush("calendario", "partido:4", "partido:5")

def ejercicio9():
    print("\nCLASIFICACIÓN DE LA LIGA")
    clasificacion = r.zrevrange("clasificacion", 0, -1, withscores=True)
    
    for i, (equipo_id, puntos) in enumerate(clasificacion, 1):
        nombre_equipo = r.hget(equipo_id, "nombre")
        print(f"{i}. {nombre_equipo} - {int(puntos)} puntos")

    print("\nTOP 3 GOLEADORES")
    top_goleadores = r.zrevrange("goleadores", 0, 2, withscores=True)
    
    for i, (jugador_id, goles) in enumerate(top_goleadores, 1):
        jugador = r.hgetall(jugador_id)
        nombre_equipo = r.hget(jugador["equipo"], "nombre")
        print(f"{i}. {jugador['nombre']} ({nombre_equipo}, {jugador['posicion']}) - {int(goles)} goles")

    print("\nHISTORIAL DE PARTIDOS")
    historial = r.lrange("partidos", 0, -1)
    
    for partido_id in historial:
        partido = r.hgetall(partido_id)
        local = r.hget(partido["local"], "nombre")
        visitante = r.hget(partido["visitante"], "nombre")
        print(f"{local} {partido['resultado']} {visitante}")
     

def ejercicio10():
    r.rpush("traspaso", "14-10-2026:jugador:4:equipo:1:equipo:2")
    r.hset("jugador:4", mapping={
                 "equipo": "equipo:2"
             })
    print(r.hgetall("jugador:4"))
     

if __name__ == "__main__":
    ejercicio1()
    ejercicio2()
    ejercicio3()
    ejercicio4()
    ejercicio5()
    ejercicio6()
    ejercicio7()
    ejercicio8()
    ejercicio9()
    ejercicio10()