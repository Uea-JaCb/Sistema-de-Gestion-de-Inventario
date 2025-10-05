# ===============================================
# Archivo principal de la aplicación
# Descripción: Interfaz gráfica con Tkinter para
# gestionar el inventario de productos.
# ===============================================

import tkinter as tk
from tkinter import ttk, messagebox
from Producto import Producto
from Inventario import Inventario

# Información del estudiante
NOMBRE = "Johanna Gamboa Luna - Johao Caicedo Bautista"
CARRERA = "Ingeniería en Tecnologías de la Información"
PARALELO = "A"


class App:
    def __init__(self):
        # Intentar cargar el inventario al iniciar
        self.inventario = Inventario()
        try:
            self.inventario.cargar('inventario.json')
        except Exception as e:
            messagebox.showerror("Error al Cargar", f"No se pudo cargar inventario.json: {str(e)}")
            self.inventario = Inventario()

        # ---------- CONFIGURACIÓN DE VENTANA PRINCIPAL ----------
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("500x420")  # Tamaño fijo
        # Posición centrada
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"500x420+{x}+{y}")
        self.root.configure(bg="#35444f")

        # ---------- ENCABEZADO ----------
        header = tk.Frame(self.root, bg="#42afa6", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="Universidad Estatal Amazónica", fg="white",
                 bg="#42afa6", font=("Helvetica", 14, "bold")).pack()

        # ---------- LOGO ----------
        logo_frame = tk.Frame(self.root, bg="#35444f")
        logo_frame.pack(pady=5)
        try:
            logo = tk.PhotoImage(file="uea_logo.png")
            logo_label = tk.Label(logo_frame, image=logo, bg="#35444f")
            logo_label.photo = logo
            logo_label.pack()
        except tk.TclError:
            tk.Label(logo_frame, text="Escudo UEA", fg="#d6df7b", bg="#35444f",
                     font=("Helvetica", 10, "italic")).pack()

        # ---------- INFORMACIÓN DEL ESTUDIANTE ----------
        info_frame = tk.Frame(self.root, bg="#2f3b44", padx=15, pady=10)
        info_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(info_frame, text=f"Nombre: {NOMBRE}", bg="#2f3b44", fg="white").pack()
        tk.Label(info_frame, text=f"Carrera: {CARRERA}", bg="#2f3b44", fg="white").pack()
        tk.Label(info_frame, text=f"Paralelo: {PARALELO}", bg="#2f3b44", fg="white").pack()

        # ---------- MENÚ ----------
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=file_menu)
        file_menu.add_command(label="Productos", command=self.abrir_productos)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.salir)

        # Atajo para salir
        self.root.bind("<Escape>", lambda e: self.salir())

        self.root.mainloop()

    # ---------- FUNCIONES PRINCIPALES ----------
    def salir(self):
        """Guarda el inventario antes de salir del programa."""
        self.inventario.guardar('inventario.json')
        self.root.quit()

    def abrir_productos(self):
        """Abre la ventana de gestión de productos."""
        productos_window = tk.Toplevel(self.root)
        productos_window.title("Gestión de Productos")
        # Tamaño y ubicación
        screen_width = productos_window.winfo_screenwidth()
        screen_height = productos_window.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 450) // 2
        productos_window.geometry(f"600x450+{x}+{y}")
        productos_window.configure(bg="#35444f")
        productos_window.transient(self.root)
        productos_window.grab_set()

        # Contenedor principal
        main_frame = tk.Frame(productos_window, bg="#35444f")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # ---------- TREEVIEW ----------
        self.tree = ttk.Treeview(main_frame, columns=('ID', 'Nombre', 'Cantidad', 'Precio'),
                                 show='headings', style="Custom.Treeview")
        self.tree.heading('ID', text='ID', anchor="w")
        self.tree.heading('Nombre', text='Nombre', anchor="w")
        self.tree.heading('Cantidad', text='Cantidad', anchor="w")
        self.tree.heading('Precio', text='Precio', anchor="w")
        self.tree.column('ID', width=60)
        self.tree.column('Nombre', width=200)
        self.tree.column('Cantidad', width=100)
        self.tree.column('Precio', width=100)
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Estilo visual
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#ffffff", foreground="#000000",
                        fieldbackground="#ffffff")
        style.map('Custom.Treeview', background=[('selected', '#42afa6')],
                  foreground=[('selected', 'white')])

        # Configurar expansión
        main_frame.grid_rowconfigure(0, weight=1)
        for i in range(4):
            main_frame.grid_columnconfigure(i, weight=1)

        self.actualizar_lista()

        # ---------- BOTONES ----------
        btn_frame = tk.Frame(main_frame, bg="#35444f")
        btn_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        tk.Button(btn_frame, text="⏩ Ingresar Producto", command=self.ingresar_producto,
                  bg="#ffffff", fg="#35444f").grid(row=0, column=0, sticky="ew", padx=(10, 5))
        tk.Button(btn_frame, text="✏️ Modificar Producto", command=self.modificar_producto,
                  bg="#ffffff", fg="#35444f").grid(row=0, column=1, sticky="ew", padx=(5, 5))
        tk.Button(btn_frame, text="❌ Eliminar Producto", command=self.eliminar_producto,
                  bg="#ff4d4d", fg="white").grid(row=0, column=2, sticky="ew", padx=(5, 5))
        tk.Button(btn_frame, text="♻️ Listar Productos", command=self.actualizar_lista,
                  bg="#ffffff", fg="#35444f").grid(row=0, column=3, sticky="ew", padx=(5, 10))

        # Atajos
        productos_window.bind("<Delete>", lambda e: self.eliminar_producto())
        productos_window.bind("<d>", lambda e: self.eliminar_producto())

    # ---------- CRUD ----------
    def actualizar_lista(self):
        """Actualiza la lista de productos en pantalla."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.inventario.mostrar_todos():
            self.tree.insert('', 'end', values=(
                p.get_id(), p.get_nombre(), p.get_cantidad(), f"${p.get_precio():.2f}"))

    def ingresar_producto(self):
        """Abre el formulario para ingresar un nuevo producto."""
        self._mostrar_form("Ingresar Producto", self._agregar)

    def modificar_producto(self):
        """Abre el formulario para modificar un producto seleccionado."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto.")
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        precio = float(item['values'][3].replace('$', ''))
        self._mostrar_form("Modificar Producto", self._modificar,
                           id=id, valores=(id, item['values'][1], item['values'][2], precio))

    def eliminar_producto(self):
        """Elimina el producto seleccionado."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto.")
            return
        item = self.tree.item(selected[0])
        id = item['values'][0]
        try:
            self.inventario.eliminar_producto(id)
            self.actualizar_lista()
            messagebox.showinfo("Éxito", "Producto eliminado.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ---------- FORMULARIO ----------
    def _mostrar_form(self, titulo, callback, id=None, valores=None):
        """Formulario para ingresar o modificar productos."""
        form = tk.Toplevel(self.root)
        form.title(titulo)
        x = self.root.winfo_x() + (self.root.winfo_width() - 350) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 250) // 2
        form.geometry(f"350x250+{x}+{y}")
        form.configure(bg="#35444f")
        form.transient(self.root)
        form.grab_set()

        form_frame = tk.Frame(form, bg="#2f3b44", padx=15, pady=15)
        form_frame.pack(expand=True)

        # Entradas
        tk.Label(form_frame, text="ID:", bg="#2f3b44", fg="white").grid(row=0, column=0, pady=5, sticky="e")
        entry_id = tk.Entry(form_frame)
        entry_id.grid(row=0, column=1, pady=5)
        if id:
            entry_id.insert(0, valores[0])
            entry_id.config(state='disabled')

        tk.Label(form_frame, text="Nombre:", bg="#2f3b44", fg="white").grid(row=1, column=0, pady=5, sticky="e")
        entry_nombre = tk.Entry(form_frame)
        entry_nombre.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Cantidad:", bg="#2f3b44", fg="white").grid(row=2, column=0, pady=5, sticky="e")
        entry_cantidad = tk.Entry(form_frame)
        entry_cantidad.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Precio:", bg="#2f3b44", fg="white").grid(row=3, column=0, pady=5, sticky="e")
        entry_precio = tk.Entry(form_frame)
        entry_precio.grid(row=3, column=1, pady=5)

        if valores:
            entry_nombre.insert(0, valores[1])
            entry_cantidad.insert(0, valores[2])
            entry_precio.insert(0, f"${valores[3]:.2f}")

        # Guardar datos
        def submit():
            try:
                # Validar campos vacíos
                if not entry_id.get().strip() and not id:
                    raise ValueError("Debe ingresar un ID numérico.")
                if not entry_nombre.get().strip():
                    raise ValueError("Debe ingresar un nombre.")
                if not entry_cantidad.get().strip():
                    raise ValueError("Debe ingresar una cantidad.")
                if not entry_precio.get().strip():
                    raise ValueError("Debe ingresar un precio.")

                pid = int(entry_id.get()) if not id else id
                nombre = entry_nombre.get()
                cantidad = int(entry_cantidad.get())
                precio_texto = entry_precio.get().replace('$', '').strip()
                precio = float(precio_texto)

                if cantidad < 0 or precio < 0:
                    raise ValueError("Cantidad y precio deben ser positivos.")

                callback(pid, nombre, cantidad, precio)
                form.destroy()
                self.actualizar_lista()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(form_frame, text="Guardar", command=submit,
                  bg="#4CAF50", fg="white").grid(row=4, column=1, pady=10)

    # ---------- FUNCIONES CRUD INTERNAS ----------
    def _agregar(self, id, nombre, cantidad, precio):
        """Agrega un nuevo producto."""
        try:
            producto = Producto(id, nombre, cantidad, precio)
            self.inventario.agregar_producto(producto)
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _modificar(self, id, nombre, cantidad, precio):
        """Modifica un producto existente."""
        try:
            self.inventario.modificar_producto(id, nombre, cantidad, precio)
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


# ---------- EJECUCIÓN ----------
if __name__ == "__main__":
    App()

