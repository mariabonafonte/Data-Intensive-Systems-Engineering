import redis

#Connect to Redis server
r = redis.Redis(host='localhost', port=6379, db=0)
r.flushdb()

# Set a key-value pair
r.set('estudiante', 'María')

# Get the value of the key
value = r.get('estudiante')
print(value.decode('utf-8'))  # Output: María

r.hset('estudiante:1', mapping={'nombre': 'María', 'edad': 21})

print("El estudiante 1 se llama " + r.hget('estudiante:1', 'nombre').decode('utf-8'))  # Output: El estudiante 1 se llama María
print("El estudiante 1 tiene " + r.hget('estudiante:1', 'edad').decode('utf-8') + " años")  # Output: El estudiante 1 tiene 21 años

estudiante_1 = r.hgetall('estudiante:1')
print(type(estudiante_1)) 
print(estudiante_1)  # Output: {b'nombre': b'Mar\xeda', b'edad': b'21'}
print(estudiante_1.get(b'nombre'))# Output: María
print(estudiante_1.get(b'edad'))  # Output: 21


r.set('estudiante:2', 'Juan')
