# ===============================================
# Clase: Producto
# Descripción: Representa un producto dentro del inventario
# ===============================================

class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        # Atributos encapsulados
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # ---------- MÉTODOS GET ----------
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # ---------- MÉTODOS SET ----------
    def set_nombre(self, nombre):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = nombre

    def set_cantidad(self, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = cantidad

    def set_precio(self, precio):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = precio

    # ---------- REPRESENTACIÓN ----------
    def __str__(self):
        """Devuelve una representación en texto del producto."""
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: {self._precio}"
