import tkinter as tk
from tkinter import messagebox, ttk

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class MainView:
    """Vista principal con información del restaurante, usuarios y gestión de productos."""

    def __init__(self, root: tk.Tk, restaurante, usuario, archivo: ArchivoServicio | None = None) -> None:
        self.root = root
        self.restaurante = restaurante
        self.usuario = usuario
        self.archivo = archivo or ArchivoServicio()
        self.usuario_seleccionado = None

        self.frame = ttk.Frame(root, padding=16)
        self.frame.pack(fill="both", expand=True)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)

        ttk.Label(self.frame, text=f"Bienvenido, {usuario.nombre}", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )
        ttk.Label(self.frame, text=f"Usuario: {usuario.identificacion} | Rol: {usuario.rol}").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )

        self.panel_resumen = ttk.Frame(self.frame)
        self.panel_resumen.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 12))
        self.panel_resumen.columnconfigure(0, weight=1)
        self.panel_resumen.columnconfigure(1, weight=1)
        self.panel_resumen.columnconfigure(2, weight=1)

        ttk.Label(self.panel_resumen, text="Productos", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(self.panel_resumen, text="Usuarios", font=("Segoe UI", 11, "bold")).grid(row=0, column=1, sticky="w")
        ttk.Label(self.panel_resumen, text="Categorías", font=("Segoe UI", 11, "bold")).grid(row=0, column=2, sticky="w")

        self.productos_listbox = tk.Listbox(self.panel_resumen, width=34, height=10)
        self.productos_listbox.grid(row=1, column=0, padx=(0, 12), sticky="nsew")

        self.usuarios_listbox = tk.Listbox(self.panel_resumen, width=34, height=10)
        self.usuarios_listbox.grid(row=1, column=1, padx=(0, 12), sticky="nsew")

        self.categorias_listbox = tk.Listbox(self.panel_resumen, width=24, height=10)
        self.categorias_listbox.grid(row=1, column=2, sticky="nsew")

        self.productos_panel = ttk.LabelFrame(self.frame, text="Gestión de productos")
        self.productos_panel.grid(row=3, column=0, sticky="nsew", padx=(0, 12), pady=(0, 8))
        self.productos_panel.columnconfigure(0, weight=1)

        self.productos_form = ttk.Frame(self.productos_panel, padding=10)
        self.productos_form.grid(row=0, column=0, sticky="nsew")
        self.productos_form.columnconfigure(1, weight=1)

        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()

        self._agregar_campo_producto("Código", self.codigo_var, 0)
        self._agregar_campo_producto("Nombre", self.nombre_var, 1)
        self._agregar_campo_producto("Categoría", self.categoria_var, 2)
        self._agregar_campo_producto("Precio", self.precio_var, 3)
        self._agregar_campo_producto("Stock", self.stock_var, 4)

        self.acciones_producto = ttk.Frame(self.productos_panel)
        self.acciones_producto.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.acciones_producto.columnconfigure((0, 1, 2, 3, 4), weight=1)

        ttk.Button(self.acciones_producto, text="Registrar", command=self._registrar_producto).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(self.acciones_producto, text="Consultar", command=self._consultar_producto).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(self.acciones_producto, text="Actualizar", command=self._actualizar_producto).grid(row=0, column=2, sticky="ew", padx=4)
        ttk.Button(self.acciones_producto, text="Eliminar", command=self._eliminar_producto).grid(row=0, column=3, sticky="ew", padx=4)
        ttk.Button(self.acciones_producto, text="Limpiar", command=self._limpiar_producto).grid(row=0, column=4, sticky="ew", padx=(4, 0))

        self.productos_tree = ttk.Treeview(
            self.productos_panel,
            columns=("codigo", "nombre", "categoria", "precio", "stock"),
            show="headings",
            height=8,
        )
        self.productos_tree.heading("codigo", text="Código")
        self.productos_tree.heading("nombre", text="Nombre")
        self.productos_tree.heading("categoria", text="Categoría")
        self.productos_tree.heading("precio", text="Precio")
        self.productos_tree.heading("stock", text="Stock")
        self.productos_tree.column("codigo", width=80, anchor="center")
        self.productos_tree.column("nombre", width=160)
        self.productos_tree.column("categoria", width=120)
        self.productos_tree.column("precio", width=90, anchor="e")
        self.productos_tree.column("stock", width=80, anchor="center")
        self.productos_tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.usuarios_panel = ttk.LabelFrame(self.frame, text="Información de usuarios")
        self.usuarios_panel.grid(row=3, column=1, sticky="nsew", pady=(0, 8))
        self.usuarios_panel.columnconfigure(0, weight=1)

        self.tree_usuarios = ttk.Treeview(
            self.usuarios_panel,
            columns=("identificacion", "nombre", "correo", "rol"),
            show="headings",
            height=8,
        )
        self.tree_usuarios.heading("identificacion", text="Identificación")
        self.tree_usuarios.heading("nombre", text="Nombre")
        self.tree_usuarios.heading("correo", text="Correo")
        self.tree_usuarios.heading("rol", text="Rol")
        self.tree_usuarios.column("identificacion", width=110, anchor="center")
        self.tree_usuarios.column("nombre", width=120)
        self.tree_usuarios.column("correo", width=180)
        self.tree_usuarios.column("rol", width=80, anchor="center")
        self.tree_usuarios.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.root.bind("<Escape>", self._limpiar_producto)

        self._cargar_productos()
        self._cargar_usuarios()
        self._cargar_categorias()
        self._cargar_treeview_usuarios()

    def _agregar_campo_producto(self, texto: str, variable: tk.StringVar, fila: int) -> None:
        ttk.Label(self.productos_form, text=f"{texto}:").grid(row=fila, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(self.productos_form, textvariable=variable, width=28).grid(row=fila, column=1, sticky="ew", pady=6)

    def _registrar_producto(self) -> None:
        try:
            producto = Producto(
                self.codigo_var.get().strip(),
                self.nombre_var.get().strip(),
                self.categoria_var.get().strip(),
                float(self.precio_var.get().strip()),
                int(self.stock_var.get().strip()),
            )
        except ValueError as error:
            messagebox.showerror("Validación", str(error))
            return

        if self.restaurante.buscar_producto_por_codigo(producto.codigo) is not None:
            messagebox.showwarning("Duplicado", f"El código '{producto.codigo}' ya existe.")
            return

        self.restaurante.registrar_producto(producto)
        self.archivo.guardar_productos(self.restaurante.listar_productos())
        self._cargar_productos()
        self._limpiar_producto()
        messagebox.showinfo("Registro", f"Producto registrado: {producto.codigo}")

    def _consultar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Consulta", "Ingrese el código del producto a consultar.")
            return

        producto = self.restaurante.buscar_producto_por_codigo(codigo)
        if producto is None:
            messagebox.showinfo("Consulta", "No se encontró el producto.")
            return

        self.codigo_var.set(producto.codigo)
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(f"{producto.precio}")
        self.stock_var.set(str(producto.stock))

    def _actualizar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Actualización", "Ingrese el código para actualizar un producto.")
            return

        if self.restaurante.buscar_producto_por_codigo(codigo) is None:
            messagebox.showwarning("Actualización", "El producto no existe.")
            return

        try:
            nombre = self.nombre_var.get().strip()
            categoria = self.categoria_var.get().strip()
            precio = float(self.precio_var.get().strip())
            stock = int(self.stock_var.get().strip())
        except ValueError:
            messagebox.showerror("Validación", "Precio debe ser numérico y stock debe ser entero.")
            return

        if self.restaurante.actualizar_producto(codigo, nombre, categoria, precio, stock):
            self.archivo.guardar_productos(self.restaurante.listar_productos())
            self._cargar_productos()
            self._limpiar_producto()
            messagebox.showinfo("Actualización", "Producto actualizado correctamente.")

    def _eliminar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Eliminación", "Ingrese el código del producto a eliminar.")
            return

        if self.restaurante.buscar_producto_por_codigo(codigo) is None:
            messagebox.showwarning("Eliminación", "El producto no existe.")
            return

        if messagebox.askyesno("Confirmación", f"¿Desea eliminar el producto {codigo}?"):
            self.restaurante.eliminar_producto(codigo)
            self.archivo.guardar_productos(self.restaurante.listar_productos())
            self._cargar_productos()
            self._limpiar_producto()
            messagebox.showinfo("Eliminación", "Producto eliminado correctamente.")

    def _limpiar_producto(self, event=None) -> None:
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")

    def _cargar_productos(self) -> None:
        self.productos_listbox.delete(0, tk.END)
        self.productos_tree.delete(*self.productos_tree.get_children())
        for producto in self.restaurante.listar_productos():
            self.productos_listbox.insert(tk.END, f"{producto.codigo} - {producto.nombre} - Stock: {producto.stock}")
            self.productos_tree.insert(
                "",
                tk.END,
                values=(producto.codigo, producto.nombre, producto.categoria, f"{producto.precio:.2f}", producto.stock),
            )

    def _cargar_usuarios(self) -> None:
        self.usuarios_listbox.delete(0, tk.END)
        for usuario in self.restaurante.listar_usuarios():
            self.usuarios_listbox.insert(tk.END, f"{usuario.identificacion} - {usuario.nombre} - {usuario.rol}")

    def _cargar_categorias(self) -> None:
        self.categorias_listbox.delete(0, tk.END)
        for categoria in sorted(self.restaurante.obtener_categorias()):
            self.categorias_listbox.insert(tk.END, categoria)

    def _cargar_treeview_usuarios(self) -> None:
        self.tree_usuarios.delete(*self.tree_usuarios.get_children())
        for usuario in self.restaurante.listar_usuarios():
            self.tree_usuarios.insert(
                "",
                tk.END,
                values=(usuario.identificacion, usuario.nombre, usuario.correo, usuario.rol),
            )
