import mysql.connector #type: ignore
import getpass


HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "1234"
DATABASE = "clubciencias"


# --- codigo que se me recomento pa que funcionara mejor ---


def crear_conexion(con_db=True):
    db_to_use = DATABASE if con_db else None
   
    conexion = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=db_to_use
    )
    return conexion


def ejecutar_consulta(sql, parametros=None, fetch=False):
    conexion = crear_conexion(con_db=True)
    cursor = conexion.cursor(dictionary=fetch)
   
    cursor.execute(sql, parametros)
   
    if fetch:
        resultado = cursor.fetchall()
    else:
        resultado = None
        conexion.commit()
       
    cursor.close()
    conexion.close()
    return resultado


def inicializar_db():
    sql = """
    CREATE TABLE IF NOT EXISTS registros (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
        Contrasena TEXT NOT NULL,
        Email VARCHAR(100) UNIQUE,
        Telefono VARCHAR(20),
        Direccion VARCHAR(255)
    );
    """
    ejecutar_consulta(sql)
    print("Tabla 'registros' lista para la entrega.")


# --- FUNCIONALIDADES INDISPENSABLES QUE USTED DIJO EN EL CLASSROOM ---


def registrarse():
    print("--- 1. REGISTRO DE CUENTA Y DATOS PERSONALES ---")
    nombre = input("Usuario (obligatorio): ").strip()
    clave = input("Contraseña (obligatorio): ").strip()
    email = input("Email (obligatorio): ").strip()
    telefono = input("Teléfono: ").strip()
    direccion = input("Dirección: ").strip()
   
    sql = """
    INSERT INTO registros (Nombre_usuario, Contrasena, Email, Telefono, Direccion)
    VALUES (%s, %s, %s, %s, %s)
    """
    parametros = (nombre, clave, email, telefono, direccion)
   
    ejecutar_consulta(sql, parametros)
    print(f"Registro completo! Usuario '{nombre}' creado.")


def iniciar_sesion():
    print("--- 2. INICIO DE SESIÓN ---")
    nombre = input("Tu Usuario: ").strip()
    clave = input("Tu Contraseña: ").strip()
   
    sql = "SELECT id, Nombre_usuario FROM registros WHERE Nombre_usuario = %s AND Contrasena = %s"
    parametros = (nombre, clave)
   
    usuarios = ejecutar_consulta(sql, parametros, fetch=True)
   
    if usuarios:
        usuario = usuarios[0]
        print(f"Bienvenido, {usuario['Nombre_usuario']}! Sesión iniciada.")
        return usuario
    else:
        print("Error: Usuario o clave mal.")
        return None


def consultar_datos_personales(user_id):
    print("--- 3. CONSULTA DE DATOS ---")
   
    sql = "SELECT Nombre_usuario, Email, Telefono, Direccion FROM registros WHERE id = %s"
   
    datos = ejecutar_consulta(sql, (user_id,), fetch=True)


    if datos:
        datos = datos[0]
        print(f"Usuario: {datos['Nombre_usuario']}")
        print(f"Email: {datos['Email']}")
        print(f"Teléfono: {datos['Telefono'] or 'N/A'}")
        print(f"Dirección: {datos['Direccion'] or 'N/A'}")
    else:
        print("No se encontraron tus datos.")


def modificar_datos(usuario_activo):
    print("--- 4. MODIFICAR DATOS ---")
    print("Dejá el campo vacío si no querés modificarlo.")
   
    nuevo_email = input("Nuevo Email: ").strip()
    nuevo_telefono = input("Nuevo Teléfono: ").strip()
    nueva_direccion = input("Nueva Dirección: ").strip()
   
    if nuevo_email:
        sql = "UPDATE registros SET Email = %s WHERE id = %s"
        ejecutar_consulta(sql, (nuevo_email, usuario_activo['id']))
    if nuevo_telefono:
        sql = "UPDATE registros SET Telefono = %s WHERE id = %s"
        ejecutar_consulta(sql, (nuevo_telefono, usuario_activo['id']))
    if nueva_direccion:
        sql = "UPDATE registros SET Direccion = %s WHERE id = %s"
        ejecutar_consulta(sql, (nueva_direccion, usuario_activo['id']))


    print(f"Datos actualizados para {usuario_activo['Nombre_usuario']}!")


def eliminar_usuario(usuario_activo):
    print("--- 5. ELIMINAR CUENTA ---")
    confirmacion = input("¿Estás seguro? Escribí 'SI' para confirmar: ").strip().upper()
   
    if confirmacion == 'SI':
        sql = "DELETE FROM registros WHERE id = %s"
        ejecutar_consulta(sql, (usuario_activo['id'],))
        print(f"Cuenta de '{usuario_activo['Nombre_usuario']}' eliminada permanentemente.")
        return True
    else:
        print("Eliminación cancelada.")
    return False


# --- MENÚ DESPUES DEL INICIO DE SESIÓN ---


def menu_usuario(usuario_activo):
    # Usamos una variable de control
    sesion_activa = True
    while sesion_activa:
        print("--- MENÚ DE SESIÓN ---")
        print("1. Consultar mis Datos Personales")
        print("2. Modificar mis Datos Personales")
        print("3. Eliminar mi Cuenta")
        print("4. Cerrar Sesión")
        opcion = input("Elegí qué hacer (1-4): ").strip()


        if opcion == '1':
            consultar_datos_personales(usuario_activo['id'])
        elif opcion == '2':
            modificar_datos(usuario_activo)
        elif opcion == '3':
            if eliminar_usuario(usuario_activo):
                return
        elif opcion == '4':
            print("Sesión cerrada.")
            sesion_activa = False # Esto hace que el bucle 'while' termine
        else:
            print("Opción no válida.")


# --- BUCLE PRINCIPAL (MAIN) ---


inicializar_db()
usuario_logueado = None
programa_activo = True # Nueva variable de control para el bucle principal


while programa_activo:
    if usuario_logueado:
        menu_usuario(usuario_logueado)
        usuario_logueado = None
        continue


    print("\n=========================")
    print("  sistema de cuentas")
    print("=========================")
    print("1. Registrarse (Crear Cuenta)")
    print("2. Iniciar Sesión")
    print("3. Salir del Programa")
    print("=========================")
   
    opcion = input("Elegí qué hacer (1-3): ").strip()


    if opcion == '1':
        registrarse()
    elif opcion == '2':
        usuario_logueado = iniciar_sesion()
    elif opcion == '3':
        print("Programa finalizado")
        programa_activo = False # Esto hace que el bucle 'while' termine
    else:
        print("Opción no válida.")
    