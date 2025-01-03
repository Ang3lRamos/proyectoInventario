import sqlite3
import csv

# Inicializar la base de datos y crear las tablas necesarias
def initialize_database():
    # Conectarse a la base de datos SQLite
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Crear la tabla de usuarios si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL,
        contraseña TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    ''')

    # Crear la tabla de productos si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        cantidad INTEGER NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Asegurarse de que los cambios sean confirmados y cerrar la conexión
    conn.commit()
    conn.close()

# Funciones de usuarios
def agregar_usuario(nombre_usuario, contraseña, rol):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Asegurarse de que el nombre de usuario no esté duplicado
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario=?", (nombre_usuario,))
    if cursor.fetchone():
        conn.close()
        return False  # Si ya existe, no agregamos el usuario

    # Si no existe, agregarlo a la base de datos
    cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña, rol) VALUES (?, ?, ?)", (nombre_usuario, contraseña, rol))
    
    conn.commit()
    conn.close()
    return True

def obtener_usuarios():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    
    # Obtener todos los usuarios
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    
    conn.close()
    return usuarios

def editar_usuario(user_id, nuevo_nombre, nueva_contraseña, nuevo_rol):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE usuarios
                      SET nombre_usuario = ?, contraseña = ?, rol = ?
                      WHERE id = ?''', (nuevo_nombre, nueva_contraseña, nuevo_rol, user_id))
    
    conn.commit()
    conn.close()

def eliminar_usuario(user_id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
    
    conn.commit()
    conn.close()

def exportar_usuarios_a_csv():
    usuarios = obtener_usuarios()
    with open('usuarios.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nombre de Usuario', 'Contraseña', 'Rol'])  # Cabeceras del CSV
        for usuario in usuarios:
            writer.writerow(usuario)  # Escribir cada usuario en el CSV

# Funciones de productos
def agregar_producto(nombre, precio, stock):
    try:
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()

        # Verificar si el producto ya existe
        cursor.execute("SELECT * FROM productos WHERE nombre=?", (nombre,))
        if cursor.fetchone():
            raise Exception(f"El producto {nombre} ya existe en la base de datos.")

        # Insertar el producto en la base de datos
        cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
                       (nombre, precio, stock))  # Elimina la columna "cantidad" extra
        conn.commit()
        return True  # Devuelve True si la inserción es exitosa
    except sqlite3.Error as e:
        print(f"Error al agregar el producto: {e}")
        return False  # Devuelve False si hay un error
    finally:
        conn.close()



def obtener_productos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def editar_producto(product_id, nuevo_nombre, nueva_descripcion, nuevo_precio, nueva_cantidad):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE productos
                      SET nombre = ?, descripcion = ?, precio = ?, cantidad = ?
                      WHERE id = ?''', 
                   (nuevo_nombre, nueva_descripcion, nuevo_precio, nueva_cantidad, product_id))
    conn.commit()
    conn.close()

def eliminar_producto(product_id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

# Función para descontar inventario cuando un vendedor realiza una venta
def descontar_producto(producto_id, cantidad):
    try:
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()

        # Actualizar el stock del producto
        cursor.execute('''
            UPDATE productos
            SET cantidad = cantidad - ?
            WHERE id = ? AND cantidad >= ?
        ''', (cantidad, producto_id, cantidad))
        
        conn.commit()
        success = cursor.rowcount > 0  # Verifica si se actualizó alguna fila
        conn.close()
        return success
    except Exception as e:
        print(f"Error al descontar producto: {e}")
        return False
