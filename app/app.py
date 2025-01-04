import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog, ttk
from database import initialize_database, agregar_usuario, editar_usuario, eliminar_usuario, exportar_usuarios_a_csv, obtener_usuarios, agregar_producto, obtener_productos, editar_producto, eliminar_producto, descontar_producto

# Inicializar la base de datos
initialize_database()

# Función para actualizar la lista de usuarios
def actualizar_lista_usuarios():
    usuarios = obtener_usuarios()  # Obtener usuarios desde la base de datos
    lista_usuarios.delete(0, tk.END)  # Limpiar la lista actual
    for usuario in usuarios:
        lista_usuarios.insert(tk.END, f"ID: {usuario[0]} - Nombre: {usuario[1]} - Contraseña: {usuario[2]} - Rol: {usuario[3]}")  # Agregar cada usuario a la lista
def actualizar_lista_productos():
    productos = obtener_productos()
    lista_productos.delete(0, tk.END)
    for producto in productos:
        lista_productos.insert(tk.END, f"ID: {producto[0]} - Nombre: {producto[1]} - Precio: {producto[2]} - Stock: {producto[3]}")
# Función para mostrar el formulario de agregar usuario
def mostrar_formulario_agregar_usuario():
    # Mostrar campos para ingresar nombre de usuario y contraseña
    nombre_usuario = simpledialog.askstring("Agregar Usuario", "Nombre de usuario:")
    if not nombre_usuario:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de usuario.")
        return

    contraseña = simpledialog.askstring("Agregar Usuario", "Contraseña:", show="*")
    if not contraseña:
        messagebox.showwarning("Advertencia", "Por favor, ingrese una contraseña.")
        return

    # Crear una ventana emergente para seleccionar el rol
    def elegir_rol():
        # Recuperamos el rol elegido y asignamos el usuario
        rol = seleccion_rol.get()
        if agregar_usuario(nombre_usuario, contraseña, rol):
            messagebox.showinfo("Éxito", f"Usuario {nombre_usuario} agregado como {rol}.")
            actualizar_lista_usuarios()
            ventana_rol.destroy()  # Cerrar la ventana de rol
        else:
            messagebox.showerror("Error", "El nombre de usuario ya existe. Intente con otro.")

    # Crear la ventana emergente para seleccionar el rol
    ventana_rol = tk.Toplevel(root)
    ventana_rol.title("Seleccionar Rol")
    ventana_rol.geometry("300x150")

    # Crear el Combobox para seleccionar el rol
    rol_label = tk.Label(ventana_rol, text="Selecciona el rol:")
    rol_label.pack(pady=10)
    seleccion_rol = ttk.Combobox(ventana_rol, values=["Administrador", "Vendedor"], state="readonly")
    seleccion_rol.set("Vendedor")  # Valor predeterminado
    seleccion_rol.pack(pady=5)

    # Botón para confirmar el rol
    boton_confirmar = tk.Button(ventana_rol, text="Confirmar Rol", command=elegir_rol)
    boton_confirmar.pack(pady=10)

# Función para editar un usuario
def editar_usuario_gui():
    try:
        user_id = int(simpledialog.askstring("Editar Usuario", "Ingrese el ID del usuario a editar:"))
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
        return
    
    usuarios = obtener_usuarios()
    usuario_existente = next((u for u in usuarios if u[0] == user_id), None)
    
    if usuario_existente:
        nuevo_nombre = simpledialog.askstring("Editar Usuario", f"Nuevo nombre de usuario ({usuario_existente[1]}):")
        nueva_contraseña = simpledialog.askstring("Editar Usuario", f"Nueva contraseña:")

        # Crear la ventana para elegir el nuevo rol
        def elegir_nuevo_rol():
            nuevo_rol = seleccion_rol.get()  # Obtener el valor seleccionado en el Combobox
            
            if nuevo_rol not in ["Administrador", "Vendedor"]:
                messagebox.showwarning("Advertencia", "Por favor, seleccione un rol válido.")
                return
            
            if nuevo_nombre and nueva_contraseña:
                editar_usuario(user_id, nuevo_nombre, nueva_contraseña, nuevo_rol)
                messagebox.showinfo("Éxito", "Usuario editado exitosamente.")
                actualizar_lista_usuarios()
                ventana_rol.destroy()  # Cerrar la ventana de rol
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

        # Crear la ventana emergente para seleccionar el rol
        ventana_rol = tk.Toplevel(root)
        ventana_rol.title("Seleccionar Nuevo Rol")
        ventana_rol.geometry("300x150")

        rol_label = tk.Label(ventana_rol, text="Selecciona el nuevo rol:")
        rol_label.pack(pady=10)

        # Crear el Combobox para seleccionar el rol
        seleccion_rol = ttk.Combobox(ventana_rol, values=["Administrador", "Vendedor"], state="readonly")
        seleccion_rol.set(usuario_existente[3])  # Establecer el rol actual como valor predeterminado
        seleccion_rol.pack(pady=5)

        # Botón para confirmar el nuevo rol
        boton_confirmar = tk.Button(ventana_rol, text="Confirmar Rol", command=elegir_nuevo_rol)
        boton_confirmar.pack(pady=10)

    else:
        messagebox.showerror("Error", "Usuario no encontrado.")

# Función para eliminar un usuario
def eliminar_usuario_gui():
    try:
        user_id = int(simpledialog.askstring("Eliminar Usuario", "Ingrese el ID del usuario a eliminar:"))
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
        return
    
    usuarios = obtener_usuarios()
    usuario_existente = next((u for u in usuarios if u[0] == user_id), None)
    
    if usuario_existente:
        confirmar = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar al usuario {usuario_existente[1]}?")
        if confirmar:
            eliminar_usuario(user_id)
            messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
            actualizar_lista_usuarios()
    else:
        messagebox.showerror("Error", "Usuario no encontrado.")

# Función para exportar usuarios a CSV
def exportar_usuarios_gui():
    exportar_usuarios_a_csv()

# Función para cerrar sesión
def cerrar_sesion():
    respuesta = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?")
    if respuesta:
        root.destroy()  # Cerrar la ventana actual
        mostrar_inicio_sesion()  # Mostrar la ventana de inicio de sesión

# Función para manejar el cierre de la ventana
def confirmar_cierre():
    respuesta = messagebox.askyesno("Cerrar Aplicación", "¿Deseas exportar los usuarios antes de cerrar?")
    if respuesta:  # Si el usuario acepta exportar
        exportar_usuarios_gui()  # Exportamos los usuarios
    root.destroy()  # Cerramos la aplicación

# Función para iniciar sesión
def iniciar_sesion():
    username = entry_usuario.get()
    password = entry_contraseña.get()

    usuarios = obtener_usuarios()
    usuario = next((u for u in usuarios if u[1] == username and u[2] == password), None)

    if usuario:
        rol = usuario[3]
        root.destroy()  # Cerrar la ventana de inicio de sesión
        abrir_ventana_principal(rol)  # Abrir la ventana principal según el rol
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Función para abrir la ventana de inicio de sesión
def mostrar_inicio_sesion():
    global root
    root = tk.Tk()
    root.title("Inicio de Sesión")
    root.geometry("400x300")

    tk.Label(root, text="Usuario:").pack(pady=10)
    global entry_usuario
    entry_usuario = tk.Entry(root)
    entry_usuario.pack(pady=5)

    tk.Label(root, text="Contraseña:").pack(pady=10)
    global entry_contraseña
    entry_contraseña = tk.Entry(root, show="*")
    entry_contraseña.pack(pady=5)

    boton_iniciar = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion)
    boton_iniciar.pack(pady=20)

    root.mainloop()

# Función para abrir la ventana principal
def abrir_ventana_principal(rol):
    global root
    root = tk.Tk()
    root.title("Gestión de Usuarios y Productos")
    root.geometry("600x400")

    # Lista de usuarios
    global lista_usuarios
    lista_usuarios = tk.Listbox(root, width=80, height=15)
    lista_usuarios.pack(pady=20)

    # Lista de productos
    global lista_productos
    lista_productos = tk.Listbox(root, width=80, height=15)
    lista_productos.pack(pady=20)

    # Botones de acción
    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=10)

    if rol == "Administrador":
        boton_agregar = tk.Button(frame_botones, text="Agregar Usuario", width=20, command=mostrar_formulario_agregar_usuario)
        boton_agregar.grid(row=0, column=0, padx=10)

        boton_editar = tk.Button(frame_botones, text="Editar Usuario", width=20, command=editar_usuario_gui)
        boton_editar.grid(row=0, column=1, padx=10)

        boton_eliminar = tk.Button(frame_botones, text="Eliminar Usuario", width=20, command=eliminar_usuario_gui)
        boton_eliminar.grid(row=1, column=0, padx=10)

        boton_agregar_producto = tk.Button(frame_botones, text="Agregar Producto", width=20, command=mostrar_formulario_agregar_producto)
        boton_agregar_producto.grid(row=1, column=1, padx=10)

        boton_editar_producto = tk.Button(frame_botones, text="Editar Producto", width=20, command=editar_producto_gui)
        boton_editar_producto.grid(row=2, column=0, padx=10)

        boton_eliminar_producto = tk.Button(frame_botones, text="Eliminar Producto", width=20, command=eliminar_producto_gui)
        boton_eliminar_producto.grid(row=3, column=1, padx=10)

    if rol == "Vendedor":
        boton_vender_producto = tk.Button(frame_botones, text="Vender Producto", width=20, command=vender_producto)
        boton_vender_producto.grid(row=2, column=0, padx=10)

    # Botón para exportar usuarios
    boton_exportar = tk.Button(frame_botones, text="Exportar Usuarios", width=20, command=exportar_usuarios_a_csv)
    boton_exportar.grid(row=2, column=1, padx=10)

    # Botón para cerrar sesión
    boton_cerrar_sesion = tk.Button(frame_botones, text="Cerrar Sesión", width=20, command=cerrar_sesion)
    boton_cerrar_sesion.grid(row=3, column=0, columnspan=2, pady=10)

    # Cargar la lista inicial de usuarios
    actualizar_lista_usuarios()

    # Cargar la lista de productos
    actualizar_lista_productos()

    # Establecer el manejador para el cierre de la ventana
    root.protocol("WM_DELETE_WINDOW", confirmar_cierre)

    # Ejecutar la interfaz gráfica
    root.mainloop()

# Función para mostrar el formulario de agregar producto
def mostrar_formulario_agregar_producto():
    # Solicitar el nombre del producto
    nombre_producto = simpledialog.askstring("Agregar Producto", "Nombre del producto:")
    if not nombre_producto:
        messagebox.showwarning("Advertencia", "Por favor, ingrese el nombre del producto.")
        return

    try:
        # Solicitar el precio del producto
        precio = float(simpledialog.askstring("Agregar Producto", "Precio del producto:"))
        if precio <= 0:
            raise ValueError("El precio debe ser un número positivo.")
    except (ValueError, TypeError):
        messagebox.showwarning("Advertencia", "Por favor, ingrese un precio válido.")
        return

    try:
        # Solicitar la cantidad en stock
        stock = int(simpledialog.askstring("Agregar Producto", "Cantidad en stock:"))
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
    except (ValueError, TypeError):
        messagebox.showwarning("Advertencia", "Por favor, ingrese una cantidad válida.")
        return

    # Llamar a la función de agregar producto con los parámetros adecuados
    if agregar_producto(nombre_producto, precio, stock):
        messagebox.showinfo("Éxito", f"Producto '{nombre_producto}' agregado exitosamente.")
        actualizar_lista_productos()  # Actualizar la lista de productos en la interfaz
    else:
        messagebox.showerror("Error", "No se pudo agregar el producto. Intente nuevamente.")




# Función para actualizar la lista de productos
def actualizar_lista_productos():
    productos = obtener_productos()  # Obtener productos desde la base de datos
    lista_productos.delete(0, tk.END)  # Limpiar la lista actual
    for producto in productos:
        lista_productos.insert(tk.END, f"ID: {producto[0]} - Nombre: {producto[1]} - Precio: {producto[2]} - Stock: {producto[3]}")  # Agregar cada producto a la lista

# Función para vender un producto
def vender_producto():
    try:
        producto_id = int(simpledialog.askstring("Vender Producto", "Ingrese el ID del producto a vender:"))
    except (ValueError, TypeError):  # Manejo de errores más robusto
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
        return

    productos = obtener_productos()
    producto_existente = next((p for p in productos if p[0] == producto_id), None)

    if producto_existente:
        cantidad = simpledialog.askinteger("Vender Producto", f"Ingrese la cantidad a vender de {producto_existente[1]}:")

        if cantidad is not None and cantidad > 0:
            # Validar que la cantidad a vender no supere el stock disponible
            if cantidad <= producto_existente[3]:  # producto_existente[3] es el stock
                if descontar_producto(producto_id, cantidad):
                    messagebox.showinfo("Éxito", f"Se han vendido {cantidad} unidad(es) de {producto_existente[1]}.")
                    actualizar_lista_productos()  # Actualizar la lista de productos en la interfaz
                else:
                    messagebox.showerror("Error", "Error al actualizar el inventario.")
            else:
                messagebox.showwarning("Advertencia", "Stock insuficiente. No puede vender más de lo que hay disponible.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una cantidad válida.")
    else:
        messagebox.showerror("Error", "Producto no encontrado.")

def editar_producto_gui():
    try:
        producto_id = int(simpledialog.askstring("Editar Producto", "Ingrese el ID del producto a editar:"))
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
        return

    productos = obtener_productos()
    producto_existente = next((p for p in productos if p[0] == producto_id), None)

    if producto_existente:
        nuevo_nombre = simpledialog.askstring("Editar Producto", f"Nuevo nombre del producto ({producto_existente[1]}):")
        
        try:
            nuevo_precio = float(simpledialog.askstring("Editar Producto", f"Nuevo precio del producto ({producto_existente[2]}):"))
            if nuevo_precio <= 0:
                raise ValueError("El precio debe ser positivo.")
        except (ValueError, TypeError):
            messagebox.showwarning("Advertencia", "Por favor, ingrese un precio válido.")
            return

        try:
            nuevo_stock = int(simpledialog.askstring("Editar Producto", f"Nuevo stock del producto ({producto_existente[3]}):"))
            if nuevo_stock < 0:
                raise ValueError("El stock no puede ser negativo.")
        except (ValueError, TypeError):
            messagebox.showwarning("Advertencia", "Por favor, ingrese un stock válido.")
            return

        # Editar el producto en la base de datos
        editar_producto(producto_id, nuevo_nombre, nuevo_precio, nuevo_stock)
        messagebox.showinfo("Éxito", "Producto editado exitosamente.")
        actualizar_lista_productos()
    else:
        messagebox.showerror("Error", "Producto no encontrado.")

def eliminar_producto_gui():
    try:
        producto_id = int(simpledialog.askstring("Eliminar Producto", "Ingrese el ID del producto a eliminar:"))
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
        return

    productos = obtener_productos()
    producto_existente = next((p for p in productos if p[0] == producto_id), None)

    if producto_existente:
        confirmar = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar el producto '{producto_existente[1]}'?")
        if confirmar:
            eliminar_producto(producto_id)
            messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
            actualizar_lista_productos()
    else:
        messagebox.showerror("Error", "Producto no encontrado.")

# Mostrar la ventana de inicio de sesión
mostrar_inicio_sesion()
