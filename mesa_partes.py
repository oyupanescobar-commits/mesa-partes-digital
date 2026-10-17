import csv
import os
from datetime import datetime

ARCHIVO = "expedientes.csv"


# ==================================
# FUNCIONES DE ARCHIVO
# ==================================

def cargar_expedientes():
    expedientes = []

    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, mode="r", newline="", encoding="utf-8") as archivo:
                lector = csv.DictReader(archivo)

                for fila in lector:
                    expedientes.append(fila)

        except Exception as e:
            print(f"\nError al leer archivo: {e}")

    return expedientes


def guardar_expedientes(expedientes):

    try:
        with open(ARCHIVO, mode="w", newline="", encoding="utf-8") as archivo:

            campos = ["codigo", "remitente", "asunto", "fecha"]

            escritor = csv.DictWriter(
                archivo,
                fieldnames=campos
            )

            escritor.writeheader()
            escritor.writerows(expedientes)

        return True

    except Exception as e:
        print(f"\nError al guardar archivo: {e}")
        return False


# ==================================
# VALIDACIONES
# ==================================

def validar_codigo(codigo, expedientes):

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
        if expediente["codigo"] == codigo:
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


# ==================================
# REGISTRAR EXPEDIENTE
# ==================================

def registrar_expediente(expedientes):

    print("\n===== REGISTRO DE EXPEDIENTE =====")

    while True:
        codigo = input("Código: ").strip()

        if validar_codigo(codigo, expedientes):
            break

    while True:
        remitente = input("Remitente: ").strip()

        if validar_remitente(remitente):
            break

    while True:
        asunto = input("Asunto: ").strip()

        if validar_asunto(asunto):
            break

    while True:
        fecha = input("Fecha (DD/MM/AAAA): ").strip()

        if validar_fecha(fecha):
            break

    expediente = {
        "codigo": codigo,
        "remitente": remitente,
        "asunto": asunto,
        "fecha": fecha
    }

    expedientes.append(expediente)

    if guardar_expedientes(expedientes):
        print("\n✅ Expediente registrado correctamente.")


# ==================================
# BUSCAR EXPEDIENTE
# ==================================

def buscar_expediente(expedientes):

    print("\n===== BÚSQUEDA =====")

    codigo = input("Ingrese código: ").strip()

    for expediente in expedientes:

        if expediente["codigo"] == codigo:

            print("\nEXPEDIENTE ENCONTRADO")
            print("-" * 40)
            print("Código:", expediente["codigo"])
            print("Remitente:", expediente["remitente"])
            print("Asunto:", expediente["asunto"])
            print("Fecha:", expediente["fecha"])

            return

    print("\nNo se encontró el expediente.")


# ==================================
# ORDENAR EXPEDIENTES
# ==================================

def ordenar_expedientes(expedientes):

    print("\n===== ORDENAMIENTO =====")
    print("1. Por código")
    print("2. Por remitente")
    print("3. Por fecha")

    opcion = input("Seleccione: ")

    if opcion == "1":

        expedientes.sort(
            key=lambda x: x["codigo"]
        )

    elif opcion == "2":

        expedientes.sort(
            key=lambda x: x["remitente"].lower()
        )

    elif opcion == "3":

        expedientes.sort(
            key=lambda x: datetime.strptime(
                x["fecha"],
                "%d/%m/%Y"
            )
        )

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
        print("Código    :", expediente["codigo"])
        print("Remitente :", expediente["remitente"])
        print("Asunto    :", expediente["asunto"])
        print("Fecha     :", expediente["fecha"])

    print("-" * 50)
    print(f"Total de expedientes: {len(expedientes)}")

def modificar_expediente(expedientes):

    print("\n===== MODIFICAR EXPEDIENTE =====")

    codigo = input("Ingrese código del expediente: ").strip()

    for expediente in expedientes:

        if expediente["codigo"] == codigo:

            print("\nExpediente encontrado")

            nuevo_remitente = input(
                f"Nuevo remitente [{expediente['remitente']}]: "
            ).strip()

            nuevo_asunto = input(
                f"Nuevo asunto [{expediente['asunto']}]: "
            ).strip()

            nueva_fecha = input(
                f"Nueva fecha [{expediente['fecha']}]: "
            ).strip()

            if nuevo_remitente:
                expediente["remitente"] = nuevo_remitente

            if nuevo_asunto:
                expediente["asunto"] = nuevo_asunto

            if nueva_fecha:
                if validar_fecha(nueva_fecha):
                    expediente["fecha"] = nueva_fecha

            guardar_expedientes(expedientes)

            print("\n✅ Expediente modificado correctamente.")
            return

    print("\n❌ Expediente no encontrado.")

def eliminar_expediente(expedientes):

    print("\n===== ELIMINAR EXPEDIENTE =====")

    codigo = input("Ingrese código del expediente: ").strip()

    for expediente in expedientes:

        if expediente["codigo"] == codigo:

            print("\nExpediente encontrado")
            print(f"Código: {expediente['codigo']}")
            print(f"Remitente: {expediente['remitente']}")
            print(f"Asunto: {expediente['asunto']}")

            confirmar = input(
                "\n¿Desea eliminarlo? (S/N): "
            ).upper()

            if confirmar == "S":

                expedientes.remove(expediente)

                guardar_expedientes(expedientes)

                print("\n✅ Expediente eliminado correctamente.")

            else:

                print("\nOperación cancelada.")

            return

    print("\n❌ Expediente no encontrado.")
# ==================================
# MENÚ PRINCIPAL
# ==================================

def menu():

    expedientes = cargar_expedientes()

    while True:

        print("\n")
        print("=" * 40)
        print("      MESA DE PARTES DIGITAL")
        print("=" * 40)
        print("1. Registrar expediente")
        print("2. Buscar expediente")
        print("3. Ordenar expedientes")
        print("4. Reporte de expedientes")
        print("5. Modificar expedientes")
        print("6. Eliminar expedientes")
        print("7. Salir")

        opcion = input("\nSeleccione una opción: ")

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

            guardar_expedientes(expedientes)

            print("\nGracias por usar el sistema.")
            break

# ==================================
# PROGRAMA PRINCIPAL
# ==================================

if __name__ == "__main__":
    menu()