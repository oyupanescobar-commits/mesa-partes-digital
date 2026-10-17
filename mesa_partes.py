import csv
import os
from datetime import datetime

ARCHIVO = "expedientes.csv"
ARCHIVO_BITACORA = "bitacora.txt"


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

            campos = ["codigo", "dni", "remitente","sede","asunto", "fecha", "documento", "estado"]

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

def registrar_expediente(expedientes):

    print("\n===== REGISTRO DE EXPEDIENTE =====")

    while True:
        codigo = input(
            "Ingrese código (0 para volver): "
        ).strip()

        if codigo == "0":
            return

        if validar_codigo(codigo, expedientes):
            break

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

    expediente = {
        "codigo": codigo,
        "dni": dni,
        "remitente": remitente,
        "sede": sede,
        "asunto": asunto,
        "fecha": fecha,
        "documento": documento,
        "estado": "pendiente",
    }

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
        print("Código    :", expediente["codigo"])
        print("DNI       :", expediente["dni"])
        print("Remitente :", expediente["remitente"])
        print("Sede      :", expediente["sede"])
        print("Asunto    :", expediente["asunto"])
        print("Fecha     :", expediente["fecha"])
        print("Documento :", expediente["documento"])
        print("Estado    :", expediente["estado"])

    print("-" * 50)
    print(f"Total de expedientes: {len(expedientes)}")

def modificar_expediente(expedientes):

    print("\n===== MODIFICAR EXPEDIENTE =====")

    codigo = input(
            "Ingrese código (0 para volver): "
    ).strip()
    
    if codigo == "0":
            return
    
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
            registrar_bitacora(
                            "MODIFICACION",
                            codigo
                        )

            print("\n✅ Expediente modificado correctamente.")
            return
        
        print("\n===== NUEVO ESTADO =====")
        print("1. Pendiente")
        print("2. En Proceso")
        print("3. Atendido")
        print("4. Observado")
        print("5. Archivado")

    opcion_estado = input(
    "Seleccione un estado: "
)
    if opcion_estado == "1":
        expediente["estado"] = "Pendiente"

    elif opcion_estado == "2":
        expediente["estado"] = "En Proceso"

    elif opcion_estado == "3":
        expediente["estado"] = "Atendido"

    elif opcion_estado == "4":
        expediente["estado"] = "Observado"

    elif opcion_estado == "5":
        expediente["estado"] = "Archivado"

    print("\n❌ Expediente no encontrado.")

def eliminar_expediente(expedientes):

    print("\n===== ELIMINAR EXPEDIENTE =====")

    codigo = input(
            "Ingrese código (0 para volver): "
    ).strip()
    
    if codigo == "0":
            return

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

                registrar_bitacora(
                            "ELIMINACION",
                            codigo
                        )

                print("\n✅ Expediente eliminado correctamente.")

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

        if expediente["codigo"] == codigo:

            print("\n✅ Expediente encontrado")
            print("-" * 40)
            print("Código:", expediente["codigo"])
            print("DNI:", expediente["dni"])
            print("Remitente:", expediente["remitente"])
            print("Sede:", expediente["sede"])
            print("Asunto:", expediente["asunto"])
            print("Fecha:", expediente["fecha"])

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

        if remitente in expediente["remitente"].lower():

            print("-" * 40)
            print("Código:", expediente["codigo"])
            print("DNI:", expediente["dni"])
            print("Remitente:", expediente["remitente"])
            print("Sede:", expediente["sede"])
            print("Asunto:", expediente["asunto"])
            print("Fecha:", expediente["fecha"])

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

        if asunto in expediente["asunto"].lower():

            print("-" * 40)
            print("Código:", expediente["codigo"])
            print("DNI:", expediente["dni"])
            print("Remitente:", expediente["remitente"])
            print("Sede:", expediente["sede"])
            print("Asunto:", expediente["asunto"])
            print("Fecha:", expediente["fecha"])

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

        if expediente["fecha"] == fecha:

            print("-" * 40)
            print("Código:", expediente["codigo"])
            print("DNI:", expediente["dni"])
            print("Remitente:", expediente["remitente"])
            print("Sede:", expediente["sede"])
            print("Asunto:", expediente["asunto"])
            print("Fecha:", expediente["fecha"])

            encontrados = True

    if not encontrados:
        print("\n❌ No se encontraron resultados.")

def buscar_por_dni(expedientes):

    dni = input(
        "\nIngrese DNI: "
    ).strip()

    for expediente in expedientes:

        if expediente["dni"] == dni:

            print("\n✅ Expediente encontrado")
            print("-" * 40)
            print("Código:", expediente["codigo"])
            print("DNI:", expediente["dni"])
            print("Remitente:", expediente["remitente"])
            print("Sede:", expediente["sede"])
            print("Estado:", expediente["estado"])

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

        estado = expediente["estado"]

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
            x["fecha"],
            "%d/%m/%Y"
        )
    )

    mas_antiguo = ordenados[0]
    mas_reciente = ordenados[-1]

    print("\nExpediente más antiguo:")
    print(
        f"{mas_antiguo['codigo']} - "
        f"{mas_antiguo['fecha']}"
    )

    print("\nExpediente más reciente:")
    print(
        f"{mas_reciente['codigo']} - "
        f"{mas_reciente['fecha']}"
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
                    f"{expediente['codigo']}\n"
                )

                archivo.write(
                    f"Remitente: "
                    f"{expediente['remitente']}\n"
                )

                archivo.write(
                    f"Asunto: "
                    f"{expediente['asunto']}\n"
                )

                archivo.write(
                    f"Fecha: "
                    f"{expediente['fecha']}\n"
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

        if expediente["sede"] == sede:

            print("-" * 50)
            print("Código    :", expediente["codigo"])
            print("DNI       :", expediente["dni"])
            print("Remitente :", expediente["remitente"])
            print("Sede      :", expediente["sede"])
            print("Asunto    :", expediente["asunto"])
            print("Fecha     :", expediente["fecha"])
            print("Documento :", expediente["documento"])
            print("Estado    :", expediente["estado"])

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

        if expediente["codigo"] == codigo:

            print("\n✅ EXPEDIENTE ENCONTRADO")
            print("-" * 50)
            print("Código    :", expediente["codigo"])
            print("DNI       :", expediente["dni"])
            print("Remitente :", expediente["remitente"])
            print("Sede      :", expediente["sede"])
            print("Estado    :", expediente["estado"])
            print("Fecha     :", expediente["fecha"])

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

        if expediente["dni"] == dni:

            print("-" * 50)
            print("Código    :", expediente["codigo"])
            print("Estado    :", expediente["estado"])
            print("Asunto    :", expediente["asunto"])
            print("Fecha     :", expediente["fecha"])

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
        print("7. Estadisticas de expedientes")
        print("8. Seguimiento de trámite")
        print("9. Exportar reporte TXT")
        print("10. Salir")

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
            mostrar_estadisticas(expedientes)

        elif opcion == "8":
            menu_seguimiento(expedientes)

        elif opcion == "9" :
            exportar_reporte_txt(expedientes)

        elif opcion == "10":
            guardar_expedientes(expedientes)

            print("\nGracias por usar el sistema.")
            break

# ==================================
# PROGRAMA PRINCIPAL
# ==================================

if __name__ == "__main__":
    menu()