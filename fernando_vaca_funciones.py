"""
=============================================================================
EJECUTADOR DE PROBLEMAS - Fernando Vaca
Modularidad mediante Funciones y Procedimientos
=============================================================================
"""

import random
import math
from datetime import datetime


# =============================================================================
#        PROBLEMA 1: Control de Temperatura en un Edificio Inteligente
# =============================================================================

def leer_sensores_temperatura(zonas: list[str]) -> dict:
    """
    Lee los datos de temperatura actual de cada zona del edificio.
    Simula la lectura de sensores físicos retornando valores aleatorios
    dentro de rangos realistas.

    Args:
        zonas: Lista con los nombres de las zonas del edificio.
    Returns:
        Diccionario {zona: temperatura_actual}.
    """
    return {zona: round(random.uniform(15.0, 35.0), 1) for zona in zonas}


def calcular_temperatura_optima(zona: str, hora: int, ocupacion: int, temp_exterior: float) -> float:
    """
    Calcula la temperatura óptima para una zona según hora, ocupación
    y condiciones climáticas externas.

    Lógica:
    - Horario nocturno (22-6h): temperatura de ahorro energético.
    - Alta ocupación: temperatura más fresca para mayor confort.
    - Temperatura exterior alta: se reduce la temperatura objetivo.

    Args:
        zona: Nombre de la zona.
        hora: Hora actual (0-23).
        ocupacion: Número de personas en la zona.
        temp_exterior: Temperatura exterior en °C.
    Returns:
        Temperatura óptima objetivo en °C.
    """
    # Base: temperatura de confort estándar
    temp_base = 22.0

    # Ajuste por horario (modo ahorro nocturno)
    if hora >= 22 or hora < 6:
        temp_base -= 3.0   # Reducir consumo por la noche

    # Ajuste por ocupación (más personas → más calor corporal → bajar temp)
    if ocupacion > 10:
        temp_base -= 1.5
    elif ocupacion == 0:
        temp_base -= 2.0   # Zona vacía: modo ahorro

    # Ajuste por temperatura exterior
    if temp_exterior > 30:
        temp_base -= 1.0   # Clima caluroso: refrescar más
    elif temp_exterior < 5:
        temp_base += 1.0   # Clima frío: calentar más

    return round(temp_base, 1)


def enviar_ajuste_temperatura(zona: str, temp_actual: float, temp_objetivo: float) -> None:
    """
    Procedimiento que envía señales de ajuste al sistema de
    calefacción/refrigeración según la diferencia de temperaturas.

    Args:
        zona: Nombre de la zona a ajustar.
        temp_actual: Temperatura actual medida en la zona.
        temp_objetivo: Temperatura objetivo calculada.
    """
    diferencia = temp_objetivo - temp_actual

    if diferencia > 1.0:
        print(f"  [{zona}] → CALEFACCIÓN activada | Actual: {temp_actual}°C | Objetivo: {temp_objetivo}°C")
    elif diferencia < -1.0:
        print(f"  [{zona}] → REFRIGERACIÓN activada | Actual: {temp_actual}°C | Objetivo: {temp_objetivo}°C")
    else:
        print(f"  [{zona}] ✓ Temperatura estable | {temp_actual}°C (objetivo: {temp_objetivo}°C)")


def registrar_consumo_energia(zona: str, temp_actual: float, temp_objetivo: float) -> float:
    """
    Registra y calcula el consumo de energía estimado basado en la
    diferencia entre la temperatura actual y la objetivo.

    Fórmula simplificada: consumo proporcional al cuadrado de la diferencia.

    Args:
        zona: Nombre de la zona.
        temp_actual: Temperatura actual.
        temp_objetivo: Temperatura objetivo.
    Returns:
        Consumo estimado en kWh.
    """
    diferencia = abs(temp_objetivo - temp_actual)
    consumo_kwh = round(0.5 * (diferencia ** 2), 3)
    print(f"  [{zona}] Consumo estimado: {consumo_kwh} kWh")
    return consumo_kwh


def ejecutar_problema1():
    zonas = ["Oficina-A", "Sala-Reuniones", "Recepción", "Almacén", "Cafetería"]
    hora_actual = datetime.now().hour
    temp_exterior = round(random.uniform(5.0, 38.0), 1)

    print(f"\n  Hora: {hora_actual:02d}:00 | Temp. exterior: {temp_exterior}°C")
    print("  " + "-" * 56)

    temperaturas = leer_sensores_temperatura(zonas)
    consumo_total = 0.0

    for zona in zonas:
        ocupacion = random.randint(0, 20)
        temp_actual = temperaturas[zona]
        temp_objetivo = calcular_temperatura_optima(zona, hora_actual, ocupacion, temp_exterior)
        enviar_ajuste_temperatura(zona, temp_actual, temp_objetivo)
        consumo_total += registrar_consumo_energia(zona, temp_actual, temp_objetivo)

    print(f"\n  ⚡ Consumo total estimado del edificio: {round(consumo_total, 3)} kWh")


# =============================================================================
#                PROBLEMA 2: Gestión de Inventario en un Almacén
# =============================================================================

# Inventario global del almacén (simulado)
inventario: dict = {}


def registrar_entrada_producto(producto: str, cantidad: int, costo_unitario: float) -> None:
    """
    Registra la entrada de un producto al almacén, actualizando
    el inventario y el costo promedio ponderado.

    Args:
        producto: Nombre del producto.
        cantidad: Unidades que ingresan.
        costo_unitario: Costo por unidad en USD.
    """
    if producto in inventario:
        # Actualiza stock y calcula nuevo costo promedio ponderado
        stock_anterior = inventario[producto]["stock"]
        costo_anterior = inventario[producto]["costo_promedio"]
        nuevo_stock = stock_anterior + cantidad
        nuevo_costo = ((stock_anterior * costo_anterior) + (cantidad * costo_unitario)) / nuevo_stock
        inventario[producto]["stock"] = nuevo_stock
        inventario[producto]["costo_promedio"] = round(nuevo_costo, 2)
    else:
        # Primera entrada: crea el registro del producto
        inventario[producto] = {
            "stock": cantidad,
            "costo_promedio": costo_unitario,
            "stock_minimo": max(5, cantidad // 4)   # 25% del primer lote como mínimo
        }
    print(f"  [ENTRADA] {producto}: +{cantidad} unidades | Stock actual: {inventario[producto]['stock']}")


def registrar_salida_producto(producto: str, cantidad: int) -> bool:
    """
    Registra la salida de un producto del almacén.
    Verifica disponibilidad antes de descontar el stock.

    Args:
        producto: Nombre del producto.
        cantidad: Unidades que salen.
    Returns:
        True si la operación fue exitosa, False si no hay stock suficiente.
    """
    if producto not in inventario:
        print(f"  [ERROR] Producto '{producto}' no encontrado en inventario.")
        return False

    if inventario[producto]["stock"] < cantidad:
        print(f"  [ERROR] Stock insuficiente de '{producto}': {inventario[producto]['stock']} < {cantidad}")
        return False

    inventario[producto]["stock"] -= cantidad
    print(f"  [SALIDA] {producto}: -{cantidad} unidades | Stock actual: {inventario[producto]['stock']}")
    return True


def calcular_nivel_optimo_inventario(producto: str, demanda_diaria: float, tiempo_reposicion: int) -> float:
    """
    Procedimiento que calcula el nivel óptimo de inventario usando
    la fórmula del punto de reorden: demanda_diaria × tiempo_reposición + stock_seguridad.

    Args:
        producto: Nombre del producto.
        demanda_diaria: Unidades consumidas por día en promedio.
        tiempo_reposicion: Días que tarda en llegar el reabastecimiento.
    Returns:
        Punto de reorden recomendado en unidades.
    """
    stock_seguridad = demanda_diaria * 2   # 2 días de seguridad
    punto_reorden = (demanda_diaria * tiempo_reposicion) + stock_seguridad
    print(f"  [ÓPTIMO] {producto}: Punto de reorden = {punto_reorden:.1f} unidades")
    return punto_reorden


def generar_alertas_reabastecimiento() -> list[str]:
    """
    Revisa todo el inventario y genera alertas para los productos
    cuyo stock está por debajo del mínimo establecido.

    Returns:
        Lista de productos que necesitan reabastecimiento.
    """
    alertas = []
    for producto, datos in inventario.items():
        if datos["stock"] <= datos["stock_minimo"]:
            alertas.append(producto)
            print(f"  ⚠ ALERTA: '{producto}' bajo mínimo | Stock: {datos['stock']} | Mínimo: {datos['stock_minimo']}")
    if not alertas:
        print("  ✓ Todos los productos tienen stock suficiente.")
    return alertas


def ejecutar_problema2():
    global inventario
    inventario = {}   # Reinicia para cada ejecución

    # Entradas iniciales
    registrar_entrada_producto("Tornillos M8",   500, 0.05)
    registrar_entrada_producto("Placas Acero",    80, 12.50)
    registrar_entrada_producto("Cable 2.5mm",    200, 1.80)
    registrar_entrada_producto("Conectores USB",  60, 3.20)

    print()
    # Salidas simuladas
    registrar_salida_producto("Tornillos M8",  480)   # Deja stock bajo
    registrar_salida_producto("Placas Acero",   75)   # Deja stock bajo
    registrar_salida_producto("Cable 2.5mm",    50)
    registrar_salida_producto("Conectores USB", 100)  # Stock insuficiente

    print()
    # Niveles óptimos
    calcular_nivel_optimo_inventario("Tornillos M8",  50, 3)
    calcular_nivel_optimo_inventario("Placas Acero",   8, 7)

    print()
    # Alertas
    generar_alertas_reabastecimiento()


# =============================================================================
#           PROBLEMA 3: Sistema de Navegación para un Vehículo Autónomo
# =============================================================================

def leer_sensores_proximidad(num_sensores: int = 8) -> dict:
    """
    Lee datos de sensores de proximidad y cámaras del vehículo.
    Simula distancias en metros a obstáculos en diferentes ángulos.

    Args:
        num_sensores: Número de sensores distribuidos alrededor del vehículo.
    Returns:
        Diccionario {angulo_grados: distancia_metros}.
    """
    angulos = [i * (360 // num_sensores) for i in range(num_sensores)]
    return {angulo: round(random.uniform(0.5, 20.0), 2) for angulo in angulos}


def calcular_ruta_optima(origen: tuple, destino: tuple, obstaculos: list[tuple]) -> list[tuple]:
    """
    Procedimiento que calcula la ruta óptima entre origen y destino
    usando una versión simplificada de navegación por waypoints,
    desviándose de obstáculos conocidos.

    Args:
        origen: Coordenadas (x, y) de inicio.
        destino: Coordenadas (x, y) de llegada.
        obstaculos: Lista de coordenadas de obstáculos conocidos.
    Returns:
        Lista de waypoints (x, y) que forman la ruta.
    """
    ruta = [origen]
    x_act, y_act = origen
    x_dest, y_dest = destino

    # Navegación por pasos hacia el destino evitando obstáculos
    for _ in range(10):
        if abs(x_act - x_dest) < 1 and abs(y_act - y_dest) < 1:
            break

        # Calcula dirección hacia el destino
        dx = 1 if x_dest > x_act else (-1 if x_dest < x_act else 0)
        dy = 1 if y_dest > y_act else (-1 if y_dest < y_act else 0)
        siguiente = (x_act + dx, y_act + dy)

        # Evita obstáculos: si el siguiente paso es obstáculo, desviarse
        if siguiente in obstaculos:
            siguiente = (x_act + dy, y_act - dx)   # Giro 90° a la derecha

        ruta.append(siguiente)
        x_act, y_act = siguiente

    ruta.append(destino)
    return ruta


def detectar_evitar_obstaculos(sensores: dict, distancia_segura: float = 2.0) -> dict:
    """
    Detecta obstáculos cercanos y determina la dirección de evasión.

    Args:
        sensores: Diccionario {angulo: distancia} de los sensores.
        distancia_segura: Distancia mínima en metros para considerar peligro.
    Returns:
        Diccionario con obstáculos detectados y la acción recomendada.
    """
    obstaculos_detectados = {}
    for angulo, distancia in sensores.items():
        if distancia < distancia_segura:
            # Determina acción según la posición del obstáculo
            if 315 <= angulo or angulo <= 45:
                accion = "FRENAR/GIRAR"
            elif 45 < angulo <= 135:
                accion = "GIRAR IZQUIERDA"
            elif 135 < angulo <= 225:
                accion = "REVERSA"
            else:
                accion = "GIRAR DERECHA"
            obstaculos_detectados[angulo] = {"distancia": distancia, "accion": accion}

    return obstaculos_detectados


def ajustar_velocidad(velocidad_actual: float, densidad_trafico: str, distancia_obstaculo: float) -> float:
    """
    Procedimiento que ajusta la velocidad del vehículo según el tráfico
    y la proximidad de obstáculos.

    Args:
        velocidad_actual: Velocidad actual en km/h.
        densidad_trafico: 'bajo', 'medio' o 'alto'.
        distancia_obstaculo: Distancia al obstáculo más cercano en metros.
    Returns:
        Nueva velocidad recomendada en km/h.
    """
    velocidad_max = {"bajo": 80.0, "medio": 50.0, "alto": 30.0}
    vel_max = velocidad_max.get(densidad_trafico, 50.0)

    # Reduce velocidad si hay obstáculos cercanos
    if distancia_obstaculo < 5.0:
        vel_max = min(vel_max, distancia_obstaculo * 3)   # Proporcional a distancia

    nueva_velocidad = min(velocidad_actual, vel_max)
    print(f"  Velocidad: {velocidad_actual} → {round(nueva_velocidad, 1)} km/h | Tráfico: {densidad_trafico} | Obstáculo a {distancia_obstaculo}m")
    return round(nueva_velocidad, 1)


def ejecutar_problema3():
    # Lectura de sensores
    sensores = leer_sensores_proximidad()
    print(f"  Sensores de proximidad: {sensores}")

    # Detección de obstáculos
    print()
    obstaculos = detectar_evitar_obstaculos(sensores, distancia_segura=3.0)
    if obstaculos:
        for angulo, info in obstaculos.items():
            print(f"  ⚠ Obstáculo a {angulo}° → {info['distancia']}m → Acción: {info['accion']}")
    else:
        print("  ✓ Sin obstáculos en zona de peligro.")

    # Ruta óptima
    print()
    origen  = (0, 0)
    destino = (5, 5)
    obs_conocidos = [(2, 2), (3, 3)]
    ruta = calcular_ruta_optima(origen, destino, obs_conocidos)
    print(f"  Ruta calculada ({len(ruta)} waypoints): {ruta}")

    # Ajuste de velocidad
    print()
    dist_min = min(sensores.values())
    ajustar_velocidad(60.0, "medio", dist_min)


# =============================================================================
#           PROBLEMA 4: Optimización de la Producción en una Fábrica
# =============================================================================

# Estado de las máquinas de la fábrica
maquinas: dict = {}


def monitorear_estado_maquinas(ids_maquinas: list[str]) -> dict:
    """
    Monitorea el estado actual de cada máquina en la fábrica.
    Retorna métricas clave: temperatura, vibración, horas de uso y estado.

    Args:
        ids_maquinas: Lista de identificadores de máquinas.
    Returns:
        Diccionario con el estado de cada máquina.
    """
    estados = {}
    for maq_id in ids_maquinas:
        horas_uso = random.randint(0, 2000)
        temp = round(random.uniform(40.0, 95.0), 1)
        vibracion = round(random.uniform(0.1, 5.0), 2)

        # Determina estado según parámetros
        if temp > 85 or vibracion > 4.0 or horas_uso > 1800:
            estado = "CRÍTICO"
        elif temp > 70 or vibracion > 2.5 or horas_uso > 1200:
            estado = "ADVERTENCIA"
        else:
            estado = "NORMAL"

        estados[maq_id] = {
            "temperatura": temp,
            "vibracion": vibracion,
            "horas_uso": horas_uso,
            "estado": estado
        }
        print(f"  [{maq_id}] Estado: {estado} | Temp: {temp}°C | Vibr: {vibracion} | Horas: {horas_uso}")

    maquinas.update(estados)
    return estados


def planificar_mantenimiento_preventivo(estados: dict) -> None:
    """
    Procedimiento que planifica el mantenimiento preventivo basado
    en el estado de las máquinas, priorizando las más críticas.

    Args:
        estados: Diccionario con el estado actual de las máquinas.
    """
    prioridad = {"CRÍTICO": [], "ADVERTENCIA": [], "NORMAL": []}

    for maq_id, datos in estados.items():
        prioridad[datos["estado"]].append(maq_id)

    print()
    for nivel, maquinas_nivel in prioridad.items():
        if maquinas_nivel:
            print(f"  [{nivel}] Mantenimiento requerido: {', '.join(maquinas_nivel)}")


def analizar_rendimiento_produccion(unidades_producidas: dict, unidades_objetivo: dict) -> dict:
    """
    Analiza el rendimiento de producción comparando lo producido
    contra el objetivo, calculando eficiencia por máquina.

    Args:
        unidades_producidas: {maquina: unidades_reales}.
        unidades_objetivo: {maquina: unidades_esperadas}.
    Returns:
        Diccionario con el porcentaje de eficiencia por máquina.
    """
    eficiencias = {}
    for maq_id in unidades_producidas:
        objetivo = unidades_objetivo.get(maq_id, 1)
        eficiencia = (unidades_producidas[maq_id] / objetivo) * 100
        eficiencias[maq_id] = round(eficiencia, 1)
        estado = "✓" if eficiencia >= 85 else "⚠"
        print(f"  {estado} [{maq_id}] Eficiencia: {eficiencias[maq_id]}% ({unidades_producidas[maq_id]}/{objetivo} uds)")
    return eficiencias


def ajustar_programacion_produccion(demanda: dict, eficiencias: dict) -> None:
    """
    Procedimiento que ajusta la programación de producción en función
    de la demanda actual y la eficiencia de cada máquina.

    Args:
        demanda: {producto: unidades_requeridas}.
        eficiencias: {maquina: porcentaje_eficiencia}.
    """
    print()
    for producto, unidades in demanda.items():
        # Asigna a la máquina más eficiente disponible
        mejor_maquina = max(eficiencias, key=eficiencias.get)
        ajuste = math.ceil(unidades / (eficiencias[mejor_maquina] / 100))
        print(f"  [AJUSTE] {producto}: {unidades} uds requeridas → Asignar {ajuste} a {mejor_maquina} ({eficiencias[mejor_maquina]}% efic.)")


def ejecutar_problema4():
    ids = ["MAQ-01", "MAQ-02", "MAQ-03", "MAQ-04"]
    estados = monitorear_estado_maquinas(ids)

    planificar_mantenimiento_preventivo(estados)

    print()
    producidas = {m: random.randint(60, 120) for m in ids}
    objetivos  = {m: 100 for m in ids}
    eficiencias = analizar_rendimiento_produccion(producidas, objetivos)

    demanda = {"Producto-X": 200, "Producto-Y": 350, "Producto-Z": 150}
    ajustar_programacion_produccion(demanda, eficiencias)


# =============================================================================
#           PROBLEMA 5: Sistema de Riego Automatizado para Agricultura
# =============================================================================

def leer_sensores_humedad(secciones: list[str]) -> dict:
    """
    Lee los datos de humedad del suelo de cada sección del campo.
    Simula lecturas de sensores capacitivos de humedad (0-100%).

    Args:
        secciones: Lista de nombres de secciones del campo.
    Returns:
        Diccionario {seccion: porcentaje_humedad}.
    """
    return {sec: round(random.uniform(10.0, 90.0), 1) for sec in secciones}


def consultar_prevision_meteorologica() -> dict:
    """
    Consulta las previsiones meteorológicas para los próximos días.
    Simula datos de una API meteorológica.

    Returns:
        Diccionario con previsión de lluvia, temperatura y humedad ambiental.
    """
    prevision = {
        "lluvia_proximas_24h": random.choice([True, False]),
        "mm_lluvia_esperados": round(random.uniform(0, 30), 1),
        "temperatura_max": round(random.uniform(18, 42), 1),
        "humedad_ambiental": round(random.uniform(20, 90), 1)
    }
    print(f"  Previsión: Lluvia={'Sí' if prevision['lluvia_proximas_24h'] else 'No'} | "
          f"{prevision['mm_lluvia_esperados']}mm | "
          f"Temp.máx: {prevision['temperatura_max']}°C")
    return prevision


def calcular_cantidad_riego(humedad_actual: float, humedad_objetivo: float,
                             area_m2: float, prevision: dict) -> float:
    """
    Procedimiento que calcula la cantidad óptima de agua a aplicar
    considerando la humedad del suelo, el área y la previsión de lluvia.

    Fórmula: litros = deficit_humedad * area * factor_evaporacion

    Args:
        humedad_actual: Humedad actual del suelo en %.
        humedad_objetivo: Humedad deseada del suelo en %.
        area_m2: Área de la sección en m².
        prevision: Datos meteorológicos de la previsión.
    Returns:
        Litros de agua recomendados (0 si se espera lluvia suficiente).
    """
    # Si se espera lluvia suficiente, no regar
    if prevision["lluvia_proximas_24h"] and prevision["mm_lluvia_esperados"] >= 10:
        return 0.0

    deficit = max(0, humedad_objetivo - humedad_actual)
    factor_evaporacion = 1.2 if prevision["temperatura_max"] > 35 else 1.0
    litros = (deficit / 100) * area_m2 * 10 * factor_evaporacion   # 10L por m² por punto de humedad
    return round(litros, 1)


def controlar_valvulas_riego(secciones_riego: dict) -> None:
    """
    Controla la apertura y cierre de válvulas de riego en cada sección
    del campo según el volumen de agua calculado.

    Args:
        secciones_riego: Diccionario {seccion: litros_a_aplicar}.
    """
    for seccion, litros in secciones_riego.items():
        if litros > 0:
            duracion_min = round(litros / 20, 1)   # Flujo: 20 L/min
            print(f"  💧 [{seccion}] Válvula ABIERTA | {litros}L | Duración: {duracion_min} min")
        else:
            print(f"  ✓ [{seccion}] Válvula CERRADA (lluvia esperada o humedad suficiente)")


def ejecutar_problema5():
    secciones = ["Sector-Norte", "Sector-Sur", "Sector-Este", "Sector-Oeste", "Invernadero"]
    humedad_objetivo = 60.0
    area_por_seccion = 500.0   # m²

    # Lecturas de humedad
    humedades = leer_sensores_humedad(secciones)
    print(f"  Humedad del suelo: {humedades}")

    # Previsión meteorológica
    print()
    prevision = consultar_prevision_meteorologica()

    # Cálculo y control de riego
    print()
    plan_riego = {}
    for seccion in secciones:
        litros = calcular_cantidad_riego(humedades[seccion], humedad_objetivo, area_por_seccion, prevision)
        plan_riego[seccion] = litros

    controlar_valvulas_riego(plan_riego)
    total = sum(plan_riego.values())
    print(f"\n  💧 Total agua a usar: {total} litros")


# =============================================================================
#                                   MENÚ PRINCIPAL
# =============================================================================

def mostrar_menu():
    print("\n" + "╔" + "═" * 60 + "╗")
    print("║" + " " * 60 + "║")
    print("║     Bienvenido al Ejecutador de Problemas de           ║")
    print("║                  Fernando Vaca 🎓                      ║")
    print("║" + " " * 60 + "║")
    print("╠" + "═" * 60 + "╣")
    print("║                                                          ║")
    print("║   [1]  Problema 1 - Control de Temperatura              ║")
    print("║   [2]  Problema 2 - Gestión de Inventario               ║")
    print("║   [3]  Problema 3 - Navegación Vehículo Autónomo        ║")
    print("║   [4]  Problema 4 - Optimización de Producción          ║")
    print("║   [5]  Problema 5 - Sistema de Riego Automatizado       ║")
    print("║   [6]  Ejecutar TODOS los problemas                     ║")
    print("║   [0]  Salir                                            ║")
    print("║                                                          ║")
    print("╚" + "═" * 60 + "╝")


PROBLEMAS = {
    "1": ("Control de Temperatura en Edificio Inteligente",    ejecutar_problema1),
    "2": ("Gestión de Inventario en un Almacén",               ejecutar_problema2),
    "3": ("Navegación para Vehículo Autónomo",                 ejecutar_problema3),
    "4": ("Optimización de la Producción en una Fábrica",      ejecutar_problema4),
    "5": ("Sistema de Riego Automatizado para Agricultura",    ejecutar_problema5),
}


def ejecutar_problema(opcion: str):
    titulo, funcion = PROBLEMAS[opcion]
    print("\n" + "=" * 62)
    print(f"  PROBLEMA {opcion}: {titulo}")
    print("=" * 62)
    funcion()
    print("=" * 62)


def main():
    while True:
        mostrar_menu()
        opcion = input("\n  ➤ Ingresa el número del problema: ").strip()

        if opcion in PROBLEMAS:
            ejecutar_problema(opcion)
        elif opcion == "6":
            for key in PROBLEMAS:
                ejecutar_problema(key)
        elif opcion == "0":
            print("\n  ¡Hasta luego, Querido Usuario\n")
            break
        else:
            print("\n  ⚠  Opción inválida. Por favor ingresa un número del 0 al 6.")

        input("\n  Presiona ENTER para volver al menú...")


if __name__ == "__main__":
    main()