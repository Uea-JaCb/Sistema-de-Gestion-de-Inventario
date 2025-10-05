# ===============================================
# Clase: Inventario
# Descripción: Gestiona los productos mediante una colección (diccionario)
# Incluye persistencia en archivo JSON.
# ===============================================

import json
from Producto import Producto

class Inventario:
    def __init__(self):
        # Diccionario: clave = ID del producto, valor = objeto Producto
        self._productos = {}

    # ---------- MÉTODOS CRUD ----------
    def agregar_producto(self, producto):
        """Agrega un producto al inventario verificando que no se repita el ID."""
        if producto.get_id() in self._productos:
            raise ValueError("El ID del producto ya existe.")
        self._productos[producto.get_id()] = producto

    def eliminar_producto(self, id):
        """Elimina un producto según su ID."""
        if id in self._productos:
            del self._productos[id]
        else:
            raise ValueError("Producto no encontrado.")

    def modificar_producto(self, id, nombre, cantidad, precio):
        """Modifica los datos de un producto existente."""
        if id in self._productos:
            producto = self._productos[id]
            producto.set_nombre(nombre)
            producto.set_cantidad(cantidad)
            producto.set_precio(precio)
        else:
            raise ValueError("Producto no encontrado.")

    def mostrar_todos(self):
        """Retorna todos los productos en forma de lista."""
        return list(self._productos.values())

    # ---------- PERSISTENCIA EN ARCHIVO ----------
    def guardar(self, archivo):
        """Guarda el inventario en un archivo JSON."""
        data = {str(id): {
            'nombre': p.get_nombre(),
            'cantidad': p.get_cantidad(),
            'precio': p.get_precio()
        } for id, p in self._productos.items()}
        with open(archivo, 'w') as f:
            json.dump(data, f)

    def cargar(self, archivo):
        """Carga los productos desde un archivo JSON."""
        try:
            with open(archivo, 'r') as f:
                data = json.load(f)
                self._productos = {
                    int(id): Producto(int(id), d['nombre'], d['cantidad'], float(d['precio']))
                    for id, d in data.items()
                }
        except FileNotFoundError:
            self._productos = {}  # Si no existe el archivo, inicia vacío
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error al cargar {archivo}: {str(e)}")
            self._productos = {}
