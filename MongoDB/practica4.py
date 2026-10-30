import pymongo
from pymongo import MongoClient
from datetime import datetime
import pprint

def main():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['DBTechWorld']

        #limpiar colecciones
        db.productos.drop()
        db.clientes.drop()
        db.ventas.drop()

        #TAREA 1 
        clientes =  [
            {
                "nombre": "Ana García",
                "email": "ana@techworld.com",
                "ciudad": "Madrid",
                "premium": True,
                "fecha_registro": datetime(2023, 12, 1)
            },
            {
                "nombre": "Carlos López", 
                "email": "carlos@techworld.com",
                "ciudad": "Barcelona",
                "premium": False,
                "fecha_registro": datetime(2024, 1, 15)
            },
            {
                "nombre": "María Rodríguez",
                "email": "maria@techworld.com", 
                "ciudad": "Madrid",
                "premium": True,
                "fecha_registro": datetime(2023, 11, 20)
            }
        ]

        ventas = [
            {
                "producto_id": 1,
                "cliente_email": "ana@techworld.com",
                "cantidad": 1,
                "total": 1500,
                "fecha": datetime(2024, 3, 15),
                "ciudad": "Madrid"
            },
            {
                "producto_id": 2,
                "cliente_email": "carlos@techworld.com", 
                "cantidad": 2,
                "total": 1598,
                "fecha": datetime(2024, 3, 16),
                "ciudad": "Barcelona"
            },
            {
                "producto_id": 3,
                "cliente_email": "maria@techworld.com",
                "cantidad": 1, 
                "total": 599,
                "fecha": datetime(2024, 3, 17),
                "ciudad": "Madrid"
            }
        ]

        productos = [
            {
                "_id": 1,
                "nombre": "Laptop Gaming Pro",
                "categoria": "computadoras",
                "precio": 1500,
                "stock": 8,
                "marca": "ASUS",
                "tags": ["gaming", "portatil", "rendimiento"],
                "fecha_ingreso": datetime(2024, 1, 10),
                "activo": True
            },
            {
                "_id": 2,
                "nombre": "Smartphone Galaxy",
                "categoria": "moviles", 
                "precio": 799,
                "stock": 25,
                "marca": "Samsung",
                "tags": ["android", "5G", "camara"],
                "fecha_ingreso": datetime(2024, 2, 15),
                "activo": True
            },
            {
                "_id": 3,
                "nombre": "Tablet iPad",
                "categoria": "tablets",
                "precio": 599,
                "stock": 15,
                "marca": "Apple",
                "tags": ["apple", "creatividad", "portatil"],
                "fecha_ingreso": datetime(2024, 1, 25),
                "activo": True
            },
			{
				"_id": 4,
				"nombre": "Auriculares Bluetooth",
				"categoria": "audio",
				"precio": 299,
				"stock": 0,
				"marca": "Sony", 
				"tags": ["audio", "inalambrico", "calidad"],
				"fecha_ingreso": datetime(2024, 3, 1),
				"activo": False
			}
        ]
        resultado_insertar_productos = db.productos.insert_many(productos)
        resultado_insertar_clientes = db.clientes.insert_many(clientes)
        resultado_insertar_ventas = db.ventas.insert_many(ventas)
        #print(f"{len(resultado_insertar_productos.inserted_ids)} productos insertados")
        #print(f"{len(resultado_insertar_clientes.inserted_ids)} clientes insertados")
        #print(f"{len(resultado_insertar_ventas.inserted_ids)} ventas insertadas")

        #TAREA 2: CONSULTAS
        print("Ejercicio 1")
        todos_productos = db.productos.find()
        print("\nTodos los productos:")
        for producto in todos_productos:
            pprint.pprint(f"Producto: {producto['nombre']}, Marca: {producto['marca']}, Precio: {producto['precio']}") 


        #productos activos
        print(" ")
        print("Ejercicio 2")
        productos_activos = db.productos.find({"activo": True})
        print("\nProductos activos:")
        for producto in productos_activos:
            pprint.pprint(f"Producto: {producto['nombre']}, Stock: {producto['stock']}, Activo: {producto['activo']}")

        #productos por categoria
        print(" ")
        print("Ejercicio 3")
        productos_computadoras = db.productos.find({"categoria": "computadoras"})
        for producto in productos_computadoras:
            pprint.pprint(f"Producto: {producto['nombre']}, Precio: {producto['precio']}, Marca: {producto['marca']}")

        print(" ")
        print("Ejercicio 4") #premium si >500€
        productos_premium= db.productos.find({"precio": {"$gt": 500}})
        for producto in productos_premium:
            pprint.pprint(f"Producto: {producto['nombre']}, Precio: {producto['precio']}, Marca: {producto['marca']}")

        print(" ")
        print("Ejercicio 5") #clientes premium
        clientes_premium = db.clientes.find({"premium": True})
        for cliente in clientes_premium:
            pprint.pprint(f"Cliente: {cliente['nombre']}, Email: {cliente['email']}, Premium: {cliente['premium']}")

        #TAREA 3: ACTUALIZACIONES
        print(" ")
        print("Ejercicio 6") #actualizar sprecio
        db.productos.update_one({"nombre": "Auriculares Bluetooth"}, {"$set": {"precio": 249}})
        producto_actualizado = db.productos.find_one({"nombre": "Auriculares Bluetooth"})
        pprint.pprint(f"Producto actualizado: {producto_actualizado['nombre']}, Precio: {producto_actualizado['precio']}")

        print(" ")
        print("Ejercicio 7") #actualizar activo y stock
        db.productos.update_many({"activo": False}, {"$set": {"activo": True, "stock": 10}})
        productos_inactivos = db.productos.find({"activo": False})
        for producto in productos_inactivos: #deberia imprimir vacio
            pprint.pprint(f"Producto: {producto['nombre']}, Activo: {producto['activo']}, Stock: {producto['stock']}")

        print(" ")
        print("Ejercicio 8") #descuento 10% apple
        db.productos.update_many({"marca": "Apple"}, {"$set": {"descuento": 10}})
        productos_apple = db.productos.find({"marca": "Apple"})
        for producto in productos_apple:
            pprint.pprint(f"Producto: {producto['nombre']}, Precio: {producto['precio']}, Marca: {producto['marca']}")

        print(" ")
        print("Ejercicio 9") #incrememtar en 5 aquellos con stock menor a 10
        productos_stock_menor_10 = db.productos.find({"stock": {"$lt": 10}})
        for producto in productos_stock_menor_10:
                    pprint.pprint(f"Producto: {producto['nombre']}, Stock: {producto['stock']}")
        
        db.productos.update_many({"stock": {"$lt": 10}}, {"$inc": {"stock": 5}})
        for producto in productos_stock_menor_10:
            pprint.pprint(f"Producto: {producto['nombre']}, Stock: {producto['stock']}")


        #TAREA 4: INDICES
        print(" ")
        print("Ejercicio 10") #indice en campo nombre - producto
        db.productos.create_index("nombre")

   
        print(" ")
        print("Ejercicio 11") #índice compuesto con categoría ascendente y precio descendente - produto
        db.productos.create_index([("categoria", pymongo.ASCENDING), ("precio", pymongo.DESCENDING)])
       
        print(" ")
        print("Ejercicio 12") #índice único en email - cliente
        db.clientes.create_index("email", unique=True)      
      
        print(" ")
        print("Ejercicio 13") #Ver indices d productos
        for index in db.productos.list_indexes():
            pprint.pprint(index)

        #TAREA 5: AGREGACIONES
        print(" ")
        print("Ejercicio 14") 
        pipeline_categorias = [
            {
                "$group":{
                    "_id": "$categoria",
                    "totalProductos": {"$sum": 1},
                    "precioMedio": {"$avg": "$precio"},
                    "stockTotal": {"$sum": "$stock"},
                    "precioMaximo": {"$max": "$precio"},
                    "productos": {"$push": "nombre"}
                }
            },
            {
                "$sort": {"totalProductos": -1}
            }
        ]
        resultado_categorias = list(db.productos.aggregate(pipeline_categorias))
        for categoria in resultado_categorias:
            print(f" - {categoria['_id']} : {categoria['totalProductos']}"),
            print(f"   Precio medio: {categoria['precioMedio']}"),
            print(f"   Stock total: {categoria['stockTotal']}"),
            print(f"   Precio máximo: {categoria['precioMaximo']}"),
            print(f"   Productos: {categoria['productos']}")

        print(" ")
        print("Ejercicio 15") 
        pipeline_ventas_productos = [
            {
                "$lookup": {
                    "from": "productos",
                    "localField": "producto_id",
                    "foreignField": "_id",
                    "as": "producto"
                }
            },
            {
                "$unwind": "$producto"
            },
            {
                "$project": {
                    "_id": 0,
                    "cliente": "$cliente_email",
                    "producto": "$producto.nombre",
                    "categoria": "$producto.categoria",
                    "marca": "$producto.marca",
                    "cantidad": 1,
                    "total": 1,
                    "ciudad": 1
                }
            }
        ]
        resultado_ventas_productos = list(db.ventas.aggregate(pipeline_ventas_productos))
        for venta in resultado_ventas_productos:
            pprint.pprint(venta)

        print(" ")
        print("Ejercicio 16")
        pipeline_ventas_ciudad = [
            {
                "$group": {
                    "_id": "$ciudad",
                    "totalVentas": {"$sum": "$total"},
                    "totalTransacciones": {"$sum": 1},
                    "promedioVenta": {"$avg": "$total"}
                }
            },
            {
                "$sort": {"totalVentas": -1}
            }
        ]
        resultado_ventas_ciudad = list(db.ventas.aggregate(pipeline_ventas_ciudad))
        for ciudad in resultado_ventas_ciudad:
            print(f" - {ciudad['_id']}")
            print(f"   Total de ventas: {ciudad['totalVentas']} euros")
            print(f"   Cantidad de transacciones: {ciudad['totalTransacciones']}")
            print(f"   Promedio por transacción: {ciudad['promedioVenta']} euros")

        #TAREA 6: BORRADOS
        print(" ")
        print("Ejercicio 17")
        nuevo_producto = {
            "nombre": "Producto temporal",
            "categoria": "otros",
            "precio": 10,
            "stock": 1,
            "marca": "TechWorld",
            "activo": True
        }
        resultado_insertar = db.productos.insert_one(nuevo_producto)
        resultado_borrar = db.productos.delete_one({"_id": resultado_insertar.inserted_id})
        print(f"Producto insertado y borrado: {resultado_borrar.deleted_count}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client in locals():
            client.close()

if __name__ == "__main__":
    main()
