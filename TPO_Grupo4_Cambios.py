def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def es_numero_valido(cadena): 
    return cadena.isdigit()


def es_fecha_valida(fecha_str):
    partes = fecha_str.split("/")
    if len(partes) != 3:
        return False
    
    dia_str, mes_str, anio_str = partes
    if not (es_numero_valido(dia_str) and es_numero_valido(mes_str) and es_numero_valido(anio_str)):
        return False
    
    dia, mes, anio = int(dia_str), int(mes_str), int(anio_str)
    
    if mes < 1 or mes > 12:
        return False
    
    dias_por_mes = [31, 29 if es_bisiesto(anio) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if dia < 1 or dia > dias_por_mes[mes - 1]:
        return False
    
    return True

def solicitar_fecha_valida():
    fecha = input("Introduce la fecha del espectáculo (DD/MM/AAAA): ")
    while not es_fecha_valida(fecha):
        print("Fecha no válida. Por favor, ingrese una fecha válida.")
        fecha = input("Introduce la fecha del espectáculo (DD/MM/AAAA): ")
    return fecha

def cargar_espectaculos():
    nombres = []
    fechas = []
    asientos_list = []
    
    n = int(input("Introduce la cantidad de espectáculos: "))
    for i in range(n):
        nombre = input(f"Introduce el nombre del espectáculo {i + 1}: ")
        fecha = solicitar_fecha_valida()
        filas = int(input("Introduce el número de filas de asientos: "))
        columnas = int(input("Introduce el número de asientos por fila: "))
        asientos = [[0] * columnas for _ in range(filas)]  # 0 = libre, 1 = ocupado
        
        nombres.append(nombre)
        fechas.append(fecha)
        asientos_list.append(asientos)
    
    return nombres, fechas, asientos_list

def mostrar_asientos(asientos, nombre, fecha):
    print(f"Asientos para el espectáculo '{nombre}' en la fecha {fecha}:")
    for fila in asientos:
        linea = ""
        for asiento in fila:
            linea += str(asiento) + " "
        print(linea.strip())  

def calcular_precio(fila, precio):
    if fila < 3:  # Si la fila está entre las primeras 3
        return precio * 1.4  # 40% más caro
    else:
        return precio

def reservar_entrada(asientos, nombre, fecha, precio_butaca):
    while True:
        mostrar_asientos(asientos, nombre, fecha)  # Mostrar la sala antes de la reserva con nombre y fecha
        fila = seleccionar_numero(0,len(asientos)-1, "Introduzca el numero de fila") #con la funcion que agregue, no te deja elegir una fila 
        columna = seleccionar_numero(0, len(asientos[0])-1,"Introduzca el número de asiento: " ) #o asiento que no exista
        
        if asientos[fila][columna] == 0:  # Si el asiento está libre
            precio_butaca = calcular_precio(fila,precio_butaca)
            print(f"El precio de la butaca es de: {precio_butaca} pesos.")
            confirmar = input("¿Desea confirmar la reserva? (si/no): ")
            if confirmar.lower() == 'si':
                asientos[fila][columna] = 1  # Reservar el asiento
                print("Reserva exitosa.")
                break
            else:
                print("Reserva cancelada.")
        else:
            print("El asiento ya está ocupado. Elige otro asiento.")
   

def cancelar_reserva(asientos, fila, columna):
    if asientos[fila][columna] == 1:  # Si el asiento está ocupado
        asientos[fila][columna] = 0  # Liberar el asiento
        print("Reserva cancelada.")
    else:
        print("El asiento ya estaba libre.")


def seleccionar_numero(inicio,fin,texto):  #PARA VALIDAR INGRESO DE NROS
    n=int(input(texto))
    while n < inicio or n > fin:
        n=int(input(texto))
    return n


def diccionario_espectaculos(nombre_espectaculo, matriz_asientos):
    dic_asientos = {}
    
    for i, asientos in enumerate(matriz_asientos):
        libres = sum(fila.count(0) for fila in asientos)
        ocupados = sum(fila.count(1) for fila in asientos)
        
        dic_asientos[nombre_espectaculo[i]] = {"Libres": libres, "Ocupados": ocupados} #agrega los espectaculos al diccionario
    
    return dic_asientos




def main():
    PRECIO_BASE = 50000
    nombres, fechas, asientos_list = cargar_espectaculos()
    
    while True:
        print("\n--- Gestión de Entradas ---")
        print("1. Mostrar asientos disponibles")
        print("2. Reservar entrada")
        print("3. Cancelar reserva")
        print("4. Consultar disponibilidad")
        print("5. Salir")
        opcion = seleccionar_numero(1,5,"Selecciona una opción: ")
         
        if opcion == 5:
            break
        
        elif opcion == 4:  
            espectaculos= diccionario_espectaculos(nombres, asientos_list)
            for nombre, disponibilidad in espectaculos.items():
                print(f"\nEspectáculo: {nombre}")
                print(f"Asientos libres: {disponibilidad['Libres']}")
                print(f"Asientos ocupados: {disponibilidad['Ocupados']}")
          
        for i, nombre in enumerate(nombres):
            print(f"{i + 1}. {nombre} - {fechas[i]}")
        
        espectaculo_index = int(input("Selecciona el número del espectáculo: ")) - 1
        
        if 0 <= espectaculo_index < len(nombres):
            nombre = nombres[espectaculo_index]
            fecha = fechas[espectaculo_index]
            asientos = asientos_list[espectaculo_index]
            
            if opcion == 1:
                mostrar_asientos(asientos, nombre, fecha)
            elif opcion == 2:
                reservar_entrada(asientos, nombre, fecha, PRECIO_BASE)
            elif opcion == 3:
                fila = int(input("Introduce el número de fila: "))
                columna = int(input("Introduce el número de asiento: "))
                cancelar_reserva(asientos, fila, columna)
            
        else:
            print("Espectáculo no encontrado.")

    
                
if __name__ == "__main__":
    main()
