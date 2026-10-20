import csv
import os
import hashlib
import hmac
import secrets
import random
import string
from getpass import getpass
from datetime import datetime

class Expediente:

    def __init__(
        self,
        codigo,
        dni,
        remitente,
        sede,
        asunto,
        fecha,
        documento,
        estado="Pendiente"
    ):

        self.codigo = codigo
        self.dni = dni
        self.remitente = remitente
        self.sede = sede
        self.asunto = asunto
        self.fecha = fecha
        self.documento = documento
        self.estado = estado

    def __str__(self):

        return (
            f"Código: {self.codigo}\n"
            f"DNI: {self.dni}\n"
            f"Remitente: {self.remitente}\n"
            f"Sede: {self.sede}\n"
            f"Asunto: {self.asunto}\n"
            f"Fecha: {self.fecha}\n"
            f"Documento: {self.documento}\n"
            f"Estado: {self.estado}"
        )   
    
    def cambiar_estado(self, nuevo_estado):

        if nuevo_estado in ESTADOS_VALIDOS:
            self.estado = nuevo_estado
            return True
        return False

    def resumen(self):
        return (
            f"{self.codigo} | "
            f"{self.remitente} | "
            f"{self.estado}"
        )

    def to_dict(self):

        return {
            "codigo": self.codigo,
            "dni": self.dni,
            "remitente": self.remitente,
            "sede": self.sede,
            "asunto": self.asunto,
            "fecha": self.fecha,
            "documento": self.documento,
            "estado": self.estado
        }

    @classmethod
    def from_dict(cls, datos):

        return cls(
            datos["codigo"],
            datos["dni"],
            datos["remitente"],
            datos["sede"],
            datos["asunto"],
            datos["fecha"],
            datos["documento"],
            datos["estado"]
        )

class MesaPartes:

    def __init__(self):

        self.expedientes = cargar_expedientes()

    def total_expedientes(self):

        return len(self.expedientes)

    def menu(self):
        """Inicia el menú interno autenticado usando la lista de esta instancia."""
        menu(self.expedientes)


    
ARCHIVO = "expedientes.csv"
ARCHIVO_BITACORA = "bitacora.txt"
ARCHIVO_USUARIOS = "usuarios.csv"
ROLES_VALIDOS = {"administrador", "operador"}
ESTADOS_VALIDOS = {"Pendiente", "En Proceso", "Atendido", "Observado", "Archivado"}


# ==================================
# FUNCIONES DE ARCHIVO
# ==================================
def generar_codigo_expediente(expedientes):

    while True:

        anio = datetime.now().year

        numero = "".join(
            random.choices("0123456789", k=6)
        )

        codigo = f"EXP-{anio}-{numero}"

        existe = any(
            expediente.codigo == codigo
            for expediente in expedientes
        )

        if not existe:
            return codigo
def cargar_expedientes():
    expedientes = []

    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, mode="r", newline="", encoding="utf-8") as archivo:
                lector = csv.DictReader(archivo)

                for fila in lector:
                    expediente = Expediente.from_dict(fila)

                    expedientes.append(expediente)

        except Exception as e:
            print(f"\nError al leer archivo: {e}")

    return expedientes


def guardar_expedientes(expedientes):

    try:
            with open(ARCHIVO, mode="w", newline="", encoding="utf-8") as archivo:

                campos = ["codigo", "dni", "remitente","sede","asunto", "fecha", "documento", "estado"]

                escritor = csv.DictWriter(
                    archivo,
                    fieldnames=campos
                )

                escritor.writeheader()

                escritor.writerows(
                    [expediente.to_dict() for expediente in expedientes]
                )
            return True

    except Exception as e:
        print(f"\nError al guardar archivo: {e}")
        return False
    
def registrar_bitacora(accion, codigo):

    print(">>> BITACORA EJECUTADA <<<")

    with open(
        ARCHIVO_BITACORA,
        "a",
        encoding="utf-8"
    ) as archivo:

        fecha_hora = datetime.now()

        archivo.write(
            f"{fecha_hora} - "
            f"{accion} - "
            f"{codigo}\n"
        )
# ==================================
# VALIDACIONES
# ==================================

def validar_codigo(codigo, expedientes):

    codigo = codigo.strip()

    if not codigo:
        print("Error: el código es obligatorio.")
        return False

    if not codigo.isalnum():
        print("Error: el código debe ser alfanumérico.")
        return False

    if len(codigo) < 5 or len(codigo) > 10:
        print("Error: el código debe tener entre 5 y 10 caracteres.")
        return False

    for expediente in expedientes:
        if expediente.codigo.strip().casefold() == codigo.casefold():
            print("Error: el código ya existe.")
            return False

    return True


def validar_remitente(remitente):

    if not remitente.strip():
        print("Error: el remitente es obligatorio.")
        return False

    if len(remitente) > 100:
        print("Error: máximo 100 caracteres.")
        return False

    return True


def validar_asunto(asunto):

    if not asunto.strip():
        print("Error: el asunto es obligatorio.")
        return False

    if len(asunto) > 200:
        print("Error: máximo 200 caracteres.")
        return False

    return True


def validar_fecha(fecha):

    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True

    except ValueError:
        print("Error: fecha inválida. Use DD/MM/AAAA.")
        return False
    
def validar_dni(dni):

    if dni == "":
        print("❌ El DNI es obligatorio.")
        return False

    if not dni.isdigit():
        print("❌ El DNI solo debe contener números.")
        return False

    if len(dni) != 8:
        print("❌ El DNI debe tener exactamente 8 dígitos.")
        return False

    return True

# ==================================
# REGISTRAR EXPEDIENTE
# ==================================
def menu_inicial():

    while True:

        print("\n" + "=" * 45)
        print("       MESA DE PARTES DIGITAL")
        print("=" * 45)
        print("1. Administrador")
        print("2. Usuario")
        print("0. Salir")
        print("=" * 45)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":

            usuario = iniciar_sesion()

            if usuario and usuario["rol"] == "administrador":
                sistema = MesaPartes()
                menu(sistema.expedientes, usuario)

        elif opcion == "2":

            sistema = MesaPartes()
            menu_usuario(sistema.expedientes)

        elif opcion == "0":

            print("Gracias por utilizar el sistema.")
            break

        else:

            print("❌ Opción inválida.")

def menu_usuario(expedientes):

    while True:

        print("\n" + "=" * 40)
        print("      PORTAL DEL USUARIO")
        print("=" * 40)
        print("1. Registrar expediente")
        print("2. Seguimiento por código")
        print("3. Seguimiento por DNI")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            registrar_expediente(expedientes)

        elif opcion == "2":
            seguimiento_tramite(expedientes)

        elif opcion == "3":
            seguimiento_por_dni(expedientes)

        elif opcion == "0":
            break

        else:
            print("❌ Opción inválida.")

def registrar_expediente(expedientes):

    print("\n===== REGISTRO DE EXPEDIENTE =====")
    codigo = generar_codigo_expediente(expedientes)
    print(f"\n📄 Código generado: {codigo}")
    while True:

        dni = input(
            "DNI (8 dígitos): "
        ).strip()

        if validar_dni(dni):
            break

    while True:

        print("\n===== SEDE =====")
        print("1. Trujillo")
        print("2. Lima")
        print("3. Cajamarca")
        print("4. Chimbote")
        print("0. Volver")

        opcion_sede = input(
            "Seleccione una sede: "
        )

        if opcion_sede == "0":
            return

        elif opcion_sede == "1":
            sede = "Trujillo"
            break

        elif opcion_sede == "2":
            sede = "Lima"
            break

        elif opcion_sede == "3":
            sede = "Cajamarca"
            break

        elif opcion_sede == "4":
            sede = "Chimbote"
            break

        else:
            print("❌ Opción inválida.")

    while True:
        remitente = input("Remitente: ").strip()

        if validar_remitente(remitente):
            break

    while True:
        asunto = input("Asunto: ").strip()

        if validar_asunto(asunto):
            break

    while True:
        fecha = input(
            "Fecha (DD/MM/AAAA): "
        ).strip()

        if validar_fecha(fecha):
            break

    while True:

        documento = input(
            "Nombre del documento: "
        ).strip()

        if documento == "":
            print("❌ Debe ingresar un documento.")
            continue

        break

    expediente = Expediente(
        codigo,
        dni,
        remitente,
        sede,
        asunto,
        fecha,
        documento
    )

    expedientes.append(expediente)

    if guardar_expedientes(expedientes):

        registrar_bitacora(
            "REGISTRO",
            codigo
        )

        registrar_bitacora(
            "DOCUMENTO_ADJUNTO",
            documento
        )

        print("\n✅ Expediente registrado correctamente.")
    else:
        expedientes.pop()
        print("\n❌ No se pudo guardar el expediente; no quedó registrado en memoria.") 
           
# ==================================
# BUSCAR EXPEDIENTE
# ==================================

def buscar_expediente(expedientes):

    while True:

        print("\n===== BÚSQUEDA =====")
        print("1. Buscar por código")
        print("2. Buscar por DNI")
        print("3. Buscar por remitente")
        print("4. Buscar por sede")
        print("5. Buscar por asunto")
        print("6. Buscar por fecha")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            buscar_por_codigo(expedientes)

        elif opcion == "2":
            buscar_por_dni(expedientes)

        elif opcion == "3":
            buscar_por_remitente(expedientes)

        elif opcion == "4":
            buscar_por_sede(expedientes)

        elif opcion == "5":
            buscar_por_asunto(expedientes)

        elif opcion == "6":
            buscar_por_fecha(expedientes)

        elif opcion == "0":
            return

        else:
            print("\n❌ Opción inválida.")


# ==================================
# ORDENAR EXPEDIENTES
# ==================================

def ordenar_expedientes(expedientes):

    print("\n===== ORDENAMIENTO =====")
    print("1. Por código")
    print("2. Por remitente")
    print("3. Por fecha")
    print("4. Volver")

    opcion = input("Seleccione: ")

    if opcion == "1":

        expedientes.sort(
            key=lambda x: x.codigo
        )

    elif opcion == "2":

        expedientes.sort(
            key=lambda x: x.remitente.lower()
        )

    elif opcion == "3":

        expedientes.sort(
            key=lambda x: datetime.strptime(
                x.fecha,
                "%d/%m/%Y"
            )
        )
    elif opcion == "4":
            print("\nVolviendo al menú principal...")
            return

    else:
        print("Opción inválida.")
        return

    guardar_expedientes(expedientes)

    print("\n✅ Expedientes ordenados correctamente.")


# ==================================
# REPORTE
# ==================================

def mostrar_reporte(expedientes):

    print("\n===== REPORTE DE EXPEDIENTES =====")

    if len(expedientes) == 0:
        print("No existen expedientes registrados.")
        return

    for expediente in expedientes:

        print("-" * 50)
        print("Código    :", expediente.codigo)
        print("DNI       :", expediente.dni)
        print("Remitente :", expediente.remitente)
        print("Sede      :", expediente.sede)
        print("Asunto    :", expediente.asunto)
        print("Fecha     :", expediente.fecha)
        print("Documento :", expediente.documento)
        print("Estado    :", expediente.estado)
        print("-" * 50)
        print(f"Total de expedientes: {len(expedientes)}")

def modificar_expediente(expedientes):

    print("\n===== MODIFICAR EXPEDIENTE =====")

    codigo = input("Ingrese código (0 para volver): ").strip()
    if codigo == "0":
        return

    expediente = next(
        (item for item in expedientes if item.codigo == codigo),
        None
    )

    if expediente is None:
        print("\n❌ Expediente no encontrado.")
        return

    print("\nExpediente encontrado")
    nuevo_remitente = input(
        f"Nuevo remitente [{expediente.remitente}] (Enter para mantener): "
    ).strip()
    nuevo_asunto = input(
        f"Nuevo asunto [{expediente.asunto}] (Enter para mantener): "
    ).strip()
    nueva_fecha = input(
        f"Nueva fecha [{expediente.fecha}] (Enter para mantener): "
    ).strip()

    if nuevo_remitente and not validar_remitente(nuevo_remitente):
        print("No se guardaron los cambios.")
        return
    if nuevo_asunto and not validar_asunto(nuevo_asunto):
        print("No se guardaron los cambios.")
        return
    if nueva_fecha and not validar_fecha(nueva_fecha):
        print("No se guardaron los cambios.")
        return

    # El cambio de estado es una operación separada y exclusiva del administrador.
    original_remitente = expediente.remitente
    original_asunto = expediente.asunto
    original_fecha = expediente.fecha

    if nuevo_remitente:
        expediente.remitente = nuevo_remitente
    if nuevo_asunto:
        expediente.asunto = nuevo_asunto
    if nueva_fecha:
        expediente.fecha = nueva_fecha

    if guardar_expedientes(expedientes):
        registrar_bitacora("MODIFICACION", codigo)
        print("\n✅ Expediente modificado correctamente.")
    else:

        expediente.remitente = original_remitente
        expediente.asunto = original_asunto
        expediente.fecha = original_fecha

        print(
            "\n❌ No se pudieron guardar los cambios; "
            "se restauraron los datos en memoria."
        )

def eliminar_expediente(expedientes):

    print("\n===== ELIMINAR EXPEDIENTE =====")

    codigo = input(
            "Ingrese código (0 para volver): "
    ).strip()
    
    if codigo == "0":
            return

    for expediente in expedientes:

        if expediente.codigo == codigo:

            print("\nExpediente encontrado")
            print(f"Código: {expediente.codigo}")
            print(f"Remitente: {expediente.remitente}")
            print(f"Asunto: {expediente.asunto}")

            confirmar = input(
                "\n¿Desea eliminarlo? (S/N): "
            ).upper()

            if confirmar == "S":

                indice = expedientes.index(expediente)
                expedientes.pop(indice)

                if guardar_expedientes(expedientes):
                    registrar_bitacora("ELIMINACION", codigo)
                    print("\n✅ Expediente eliminado correctamente.")
                else:
                    expedientes.insert(indice, expediente)
                    print("\n❌ No se pudo guardar la eliminación; el expediente se conservó.")

            else:

                print("\nOperación cancelada.")

            return
        

    print("\n❌ Expediente no encontrado.")

def buscar_por_codigo(expedientes):

    codigo = input(
        "\nCódigo (0 para volver): "
    ).strip()

    if codigo == "0":
        return

    for expediente in expedientes:

        if expediente.codigo == codigo:

            print("\n✅ Expediente encontrado")
            print("-" * 40)
            print("Código:", expediente.codigo)
            print("DNI:", expediente.dni)
            print("Remitente:", expediente.remitente)
            print("Sede:", expediente.sede)
            print("Asunto:", expediente.asunto)
            print("Fecha:", expediente.fecha)

            return

    print("\n❌ No encontrado.")

def buscar_por_remitente(expedientes):

    remitente = input(
        "\nRemitente (0 para volver): "
    ).strip().lower()

    if remitente == "0":
        return

    encontrados = False

    for expediente in expedientes:

        if remitente in expediente.remitente.lower():

            print("-" * 40)
            print("Código:", expediente.codigo)
            print("DNI:", expediente.dni)
            print("Remitente:", expediente.remitente)
            print("Sede:", expediente.sede)
            print("Asunto:", expediente.asunto)
            print("Fecha:", expediente.fecha)

            encontrados = True

    if not encontrados:
        print("\n❌ No se encontraron resultados.")

def buscar_por_asunto(expedientes):

    asunto = input(
        "\nAsunto (0 para volver): "
    ).strip().lower()

    if asunto == "0":
        return

    encontrados = False

    for expediente in expedientes:

        if asunto in expediente.asunto.lower():

            print("-" * 40)
            print("Código:", expediente.codigo)
            print("DNI:", expediente.dni)
            print("Remitente:", expediente.remitente)
            print("Sede:", expediente.sede)
            print("Asunto:", expediente.asunto)
            print("Fecha:", expediente.fecha)

            encontrados = True

    if not encontrados:
        print("\n❌ No se encontraron resultados.")

def buscar_por_fecha(expedientes):

    fecha = input(
        "\nFecha (DD/MM/AAAA): "
    ).strip()

    if fecha == "0":
        return

    encontrados = False

    for expediente in expedientes:

        if expediente.fecha == fecha:

            print("-" * 40)
            print("Código:", expediente.codigo)
            print("DNI:", expediente.dni)
            print("Remitente:", expediente.remitente)
            print("Sede:", expediente.sede)
            print("Asunto:", expediente.asunto)
            print("Fecha:", expediente.fecha)

            encontrados = True

    if not encontrados:
        print("\n❌ No se encontraron resultados.")

def buscar_por_dni(expedientes):

    dni = input(
        "\nIngrese DNI: "
    ).strip()

    for expediente in expedientes:

        if expediente.dni == dni:

            print("\n✅ Expediente encontrado")
            print("-" * 40)
            print("Código:", expediente.codigo)
            print("DNI:", expediente.dni)
            print("Remitente:", expediente.remitente)
            print("Sede:", expediente.sede)
            print("Estado:", expediente.estado)

            return

    print("\n❌ No se encontró el expediente.")
def mostrar_estadisticas(expedientes):

    print("\n===== ESTADÍSTICAS =====")

    

    total = len(expedientes)

    print(f"\nTotal de expedientes: {total}")

    if total == 0:
        return
    estados = {}

    for expediente in expedientes:

        estado = expediente.estado

        if estado in estados:
            estados[estado] += 1
        else:
            estados[estado] = 1

    print("\nExpedientes por estado:")

    for estado, cantidad in estados.items():

        print(
            f"{estado}: {cantidad}"
        )
    ordenados = sorted(
        expedientes,
        key=lambda x: datetime.strptime(
            x.fecha,
            "%d/%m/%Y"
        )
    )

    mas_antiguo = ordenados[0]
    mas_reciente = ordenados[-1]

    print("\nExpediente más antiguo:")
    print(
        f"{mas_antiguo.codigo} - "
        f"{mas_antiguo.fecha}"
    )

    print("\nExpediente más reciente:")
    print(
        f"{mas_reciente.codigo} - "
        f"{mas_reciente.fecha}"
    )

def exportar_reporte_txt(expedientes):

    with open(
        "reporte_expedientes.txt",
        "w",
        encoding="utf-8"
    ) as archivo:

        archivo.write("=" * 50 + "\n")
        archivo.write("REPORTE DE EXPEDIENTES\n")
        archivo.write("=" * 50 + "\n\n")

        if len(expedientes) == 0:

            archivo.write(
                "No existen expedientes registrados.\n"
            )

        else:

            for expediente in expedientes:

                archivo.write(
                    f"Código: "
                    f"{expediente.codigo}\n"
                )

                archivo.write(
                    f"Remitente: "
                    f"{expediente.remitente}\n"
                )

                archivo.write(
                    f"Asunto: "
                    f"{expediente.asunto}\n"
                )

                archivo.write(
                    f"Fecha: "
                    f"{expediente.fecha}\n"
                )

                archivo.write("-" * 50 + "\n")

    print(
        "\n✅ Reporte exportado correctamente."
    )

def buscar_por_sede(expedientes):

    print("\n===== BÚSQUEDA POR SEDE =====")
    print("1. Trujillo")
    print("2. Lima")
    print("3. Cajamarca")
    print("4. Chimbote")
    print("0. Volver")

    opcion = input("Seleccione una sede: ")

    if opcion == "0":
        return

    elif opcion == "1":
        sede = "Trujillo"

    elif opcion == "2":
        sede = "Lima"

    elif opcion == "3":
        sede = "Cajamarca"

    elif opcion == "4":
        sede = "Chimbote"

    else:
        print("❌ Opción inválida.")
        return

    encontrados = False

    for expediente in expedientes:

        if expediente.sede == sede:

            print("-" * 50)
            print("Código    :", expediente.codigo)
            print("DNI       :", expediente.dni)
            print("Remitente :", expediente.remitente)
            print("Sede      :", expediente.sede)
            print("Asunto    :", expediente.asunto)
            print("Fecha     :", expediente.fecha)
            print("Documento :", expediente.documento)
            print("Estado    :", expediente.estado)

            encontrados = True

    if not encontrados:
        print("\n❌ No se encontraron expedientes.")

def seguimiento_tramite(expedientes):

    print("\n===== SEGUIMIENTO DE TRÁMITE =====")

    codigo = input(
        "Ingrese código del expediente (0 para volver): "
    ).strip()

    if codigo == "0":
        return

    for expediente in expedientes:

        if expediente.codigo == codigo:

            print("\n✅ EXPEDIENTE ENCONTRADO")
            print("-" * 50)
            print("Código    :", expediente.codigo)
            print("DNI       :", expediente.dni)
            print("Remitente :", expediente.remitente)
            print("Sede      :", expediente.sede)
            print("Estado    :", expediente.estado)
            print("Fecha     :", expediente.fecha)

            registrar_bitacora(
                "CONSULTA_ESTADO",
                codigo
            )

            return

    print("\n❌ No se encontró el expediente.")

def seguimiento_por_dni(expedientes):

    print("\n===== SEGUIMIENTO POR DNI =====")

    dni = input(
        "Ingrese DNI (0 para volver): "
    ).strip()

    if dni == "0":
        return

    encontrados = False

    for expediente in expedientes:

        if expediente.dni == dni:

            print("-" * 50)
            print("Código    :", expediente.codigo)
            print("Estado    :", expediente.estado)
            print("Asunto    :", expediente.asunto)
            print("Fecha     :", expediente.fecha)

            encontrados = True

    if not encontrados:
        print("\n❌ No existen expedientes para ese DNI.")

def menu_seguimiento(expedientes):

    while True:

        print("\n===== SEGUIMIENTO =====")
        print("1. Consultar por código")
        print("2. Consultar por DNI")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            seguimiento_tramite(expedientes)

        elif opcion == "2":
            seguimiento_por_dni(expedientes)

        elif opcion == "0":
            return

        else:
            print("❌ Opción inválida.")

# ==================================
# USUARIOS Y PERMISOS INTERNOS
# ==================================

def _hash_password(password, salt=None):
    """Devuelve sal y hash PBKDF2; nunca guarda contraseñas en texto claro."""
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 200_000)
    return salt, digest.hex()


def cargar_usuarios():
    usuarios = []
    if os.path.exists(ARCHIVO_USUARIOS):
        try:
            with open(ARCHIVO_USUARIOS, "r", newline="", encoding="utf-8") as archivo:
                for fila in csv.DictReader(archivo):
                    if fila.get("rol") in ROLES_VALIDOS:
                        usuarios.append(fila)
        except (OSError, csv.Error) as error:
            print(f"Error al leer usuarios: {error}")
    return usuarios


def guardar_usuarios(usuarios):
    try:
        temporal = ARCHIVO_USUARIOS + ".tmp"
        with open(temporal, "w", newline="", encoding="utf-8") as archivo:
            campos = ["usuario", "sal", "hash_password", "rol", "activo"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(usuarios)
        os.replace(temporal, ARCHIVO_USUARIOS)
        return True
    except OSError as error:
        print(f"Error al guardar usuarios: {error}")
        return False


def crear_usuario(usuarios, nombre, password, rol):
    nombre = nombre.strip()
    if not nombre or any(u["usuario"].casefold() == nombre.casefold() for u in usuarios):
        print("El nombre de usuario está vacío o ya existe.")
        return False
    if len(password) < 12:
        print("La contraseña debe tener al menos 12 caracteres.")
        return False
    if rol not in ROLES_VALIDOS:
        print("Rol inválido.")
        return False
    sal, hash_password = _hash_password(password)
    usuarios.append({"usuario": nombre, "sal": sal, "hash_password": hash_password,
                     "rol": rol, "activo": "1"})
    if guardar_usuarios(usuarios):
        registrar_bitacora("CREACION_USUARIO", nombre)
        return True
    usuarios.pop()
    return False


def preparar_administrador_inicial():
    usuarios = cargar_usuarios()
    if usuarios:
        return usuarios
    print("\nPrimera ejecución: cree la cuenta del administrador principal.")
    while True:
        nombre = input("Usuario administrador: ").strip()
        clave = getpass("Contraseña (mínimo 12 caracteres): ")
        confirmar = getpass("Repita la contraseña: ")
        if clave != confirmar:
            print("Las contraseñas no coinciden.")
            continue
        if crear_usuario(usuarios, nombre, clave, "administrador"):
            print("Cuenta de administrador creada.")
            return cargar_usuarios()
        print("No se pudo crear la cuenta. Inténtelo nuevamente.")


def iniciar_sesion():
    usuarios = preparar_administrador_inicial()
    while True:
        print("\n===== INICIO DE SESIÓN INTERNO =====")
        nombre = input("Usuario (0 para salir): ").strip()
        if nombre == "0":
            return None
        clave = getpass("Contraseña: ")
        for usuario in usuarios:
            if usuario["usuario"].casefold() == nombre.casefold() and usuario.get("activo") == "1":
                _, hash_intento = _hash_password(clave, usuario["sal"])
                if hmac.compare_digest(hash_intento, usuario["hash_password"]):
                    registrar_bitacora("INICIO_SESION", usuario["usuario"])
                    return {"usuario": usuario["usuario"], "rol": usuario["rol"]}
        print("Credenciales incorrectas o cuenta inactiva.")


def cambiar_estado_expediente(expedientes, usuario):
    """Único punto de cambio de estado; exige rol administrador."""

    if not usuario or usuario.get("rol") != "administrador":

        print(
            "Acceso denegado: "
            "solo el administrador puede cambiar estados."
        )

        registrar_bitacora(
            "CAMBIO_ESTADO_DENEGADO",
            usuario.get("usuario", "desconocido")
            if usuario else "sin_sesion"
        )

        return

    codigo = input(
        "Código del expediente (0 para volver): "
    ).strip()

    if codigo == "0":
        return

    expediente = next(
        (
            item
            for item in expedientes
            if item.codigo.casefold() == codigo.casefold()
        ),
        None
    )

    if expediente is None:
        print("Expediente no encontrado.")
        return

    print(
        f"Estado actual: {expediente.estado}"
    )

    opciones = {
        "1": "Pendiente",
        "2": "En Proceso",
        "3": "Atendido",
        "4": "Observado",
        "5": "Archivado"
    }

    for clave, estado in opciones.items():

        print(f"{clave}. {estado}")

    print("0. Cancelar")

    opcion = input(
        "Nuevo estado: "
    ).strip()

    if opcion == "0":

        print("Operación cancelada.")
        return

    if opcion not in opciones:

        print("Opción de estado inválida.")
        return

    anterior = expediente.estado
    nuevo = opciones[opcion]

    if anterior == nuevo:

        print(
            "El expediente ya tiene ese estado."
        )

        return

    expediente.estado = nuevo

    if guardar_expedientes(expedientes):

        try:

            registrar_bitacora(
                f"CAMBIO_ESTADO:{anterior}->{nuevo};"
                f"USUARIO:{usuario['usuario']}",
                codigo
            )

        except OSError as error:

            print(
                f"Advertencia: el estado se guardó, "
                f"pero falló la bitácora: {error}"
            )

        print(
            "Estado actualizado correctamente."
        )

    else:

        expediente.estado = anterior

        print(
            "No se pudo guardar el estado; "
            "se restauró el valor anterior."
        )
def administrar_usuarios(usuario):
    if not usuario or usuario.get("rol") != "administrador":
        print("Acceso denegado: solo el administrador puede administrar cuentas.")
        return
    usuarios = cargar_usuarios()
    nombre = input("Nuevo nombre de usuario (0 para volver): ").strip()
    if nombre == "0":
        return
    clave = getpass("Contraseña inicial (mínimo 12 caracteres): ")
    rol = input("Rol (administrador/operador): ").strip().lower()
    if crear_usuario(usuarios, nombre, clave, rol):
        print("Usuario creado correctamente.")
    else:
        print("No se pudo crear el usuario.")


# ==================================
# MENÚ PRINCIPAL
# ==================================

def menu(expedientes=None, usuario=None):
    """Menú interno. Las funciones administrativas verifican el rol también."""
    if expedientes is None:
        expedientes = cargar_expedientes()
    if usuario is None:
        usuario = iniciar_sesion()
    if usuario is None:
        print("Sesión no iniciada.")
        return

    while True:
        print("\n" + "=" * 40)
        print("      MESA DE PARTES DIGITAL")
        print(f"Usuario: {usuario['usuario']} | Rol: {usuario['rol']}")
        print("=" * 40)
        print("1. Registrar expediente")
        print("2. Buscar expediente")
        print("3. Ordenar expedientes")
        print("4. Reporte de expedientes")
        print("5. Modificar datos del expediente (sin cambiar estado)")
        print("6. Eliminar expediente")
        print("7. Estadísticas de expedientes")
        print("8. Seguimiento interno")
        print("9. Exportar reporte TXT")
        if usuario["rol"] == "administrador":
            print("11. Cambiar estado de expediente (administrador)")
            print("12. Crear cuenta interna")
        print("10. Cerrar sesión")
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            registrar_expediente(expedientes)
        elif opcion == "2":
            buscar_expediente(expedientes)
        elif opcion == "3":
            ordenar_expedientes(expedientes)
        elif opcion == "4":
            mostrar_reporte(expedientes)
        elif opcion == "5":
            modificar_expediente(expedientes)
        elif opcion == "6":
            eliminar_expediente(expedientes)
        elif opcion == "7":
            mostrar_estadisticas(expedientes)
        elif opcion == "8":
            menu_seguimiento(expedientes)
        elif opcion == "9":
            exportar_reporte_txt(expedientes)
        elif opcion == "11" and usuario["rol"] == "administrador":
            cambiar_estado_expediente(expedientes, usuario)
        elif opcion == "12" and usuario["rol"] == "administrador":
            administrar_usuarios(usuario)
        elif opcion == "10":
            try:
                registrar_bitacora("CIERRE_SESION", usuario["usuario"])
            except OSError:
                pass
            print("Sesión cerrada.")
            return
        else:
            print("Opción inválida o permiso insuficiente.")

# ==================================
# PROGRAMA PRINCIPAL
# ==================================

if __name__ == "__main__":
    menu_inicial()