# Tarea_C6T1# Ejecutador de Problemas — Fernando Vaca
### Modularidad mediante Funciones y Procedimientos

---

## ¿Cómo ejecutar?

```bash
python3 fernando_vaca_funciones.py
```

Al iniciar, aparece un menú interactivo donde puedes elegir el problema a ejecutar (1–5) o ejecutarlos todos con la opción 6.

**Requisitos:** Python 3.10+ y la librería `numpy` (`pip install numpy`).

---

## Estructura del proyecto

```
fernando_vaca_funciones.py   ← Código fuente principal con menú y los 5 problemas
README.md                    ← Este archivo
```

---

## Problema 1 — Control de Temperatura en un Edificio Inteligente

### Funciones implementadas

| Función / Procedimiento | Tipo | Descripción |
|---|---|---|
| `leer_sensores_temperatura(zonas)` | Función | Simula la lectura de sensores físicos por zona, retornando temperaturas actuales |
| `calcular_temperatura_optima(zona, hora, ocupacion, temp_exterior)` | Función | Calcula la temperatura ideal combinando hora del día, ocupación y clima exterior |
| `enviar_ajuste_temperatura(zona, temp_actual, temp_objetivo)` | Procedimiento | Decide si activar calefacción o refrigeración según la diferencia de temperaturas |
| `registrar_consumo_energia(zona, temp_actual, temp_objetivo)` | Función | Estima el consumo en kWh usando la fórmula `0.5 × Δtemp²` |

### Impacto en rendimiento
Separar la lectura de sensores del cálculo y del envío de señales permite reemplazar cada módulo de forma independiente (p. ej., conectar sensores reales sin tocar la lógica de control). Al procesar cada zona en una iteración única, el sistema escala linealmente O(n) con el número de zonas.

---

## Problema 2 — Gestión de Inventario en un Almacén

### Funciones implementadas

| Función / Procedimiento | Tipo | Descripción |
|---|---|---|
| `registrar_entrada_producto(producto, cantidad, costo)` | Función | Añade stock al inventario y recalcula el costo promedio ponderado |
| `registrar_salida_producto(producto, cantidad)` | Función | Descuenta stock validando disponibilidad previa; retorna True/False |
| `calcular_nivel_optimo_inventario(producto, demanda_diaria, tiempo_reposicion)` | Procedimiento | Calcula el punto de reorden: `demanda × tiempo + stock_seguridad` |
| `generar_alertas_reabastecimiento()` | Función | Recorre el inventario y reporta productos bajo el mínimo establecido |

### Impacto en rendimiento
Mantener un único diccionario compartido como fuente de verdad evita sincronización entre estructuras. La validación en `registrar_salida_producto` antes de modificar el estado previene inconsistencias sin necesidad de transacciones complejas.

---

## Problema 3 — Sistema de Navegación para un Vehículo Autónomo

### Funciones implementadas

| Función / Procedimiento | Tipo | Descripción |
|---|---|---|
| `leer_sensores_proximidad(num_sensores)` | Función | Genera lecturas de distancia a obstáculos en N ángulos alrededor del vehículo |
| `calcular_ruta_optima(origen, destino, obstaculos)` | Procedimiento | Navega hacia el destino paso a paso desviándose de obstáculos conocidos |
| `detectar_evitar_obstaculos(sensores, distancia_segura)` | Función | Identifica obstáculos dentro de la zona de peligro y determina la maniobra de evasión |
| `ajustar_velocidad(velocidad_actual, densidad_trafico, distancia_obstaculo)` | Procedimiento | Limita la velocidad según el tráfico y la proximidad del obstáculo más cercano |

### Impacto en rendimiento
Separar la lectura de sensores, la planificación de ruta y el control de velocidad en funciones independientes facilita la ejecución paralela en un sistema embebido real (los sensores pueden leerse en un hilo dedicado mientras la planificación corre en otro). Cada función tiene responsabilidad única, reduciendo el acoplamiento.

---

## Problema 4 — Optimización de la Producción en una Fábrica

### Funciones implementadas

| Función / Procedimiento | Tipo | Descripción |
|---|---|---|
| `monitorear_estado_maquinas(ids_maquinas)` | Función | Lee temperatura, vibración y horas de uso, clasificando el estado como NORMAL / ADVERTENCIA / CRÍTICO |
| `planificar_mantenimiento_preventivo(estados)` | Procedimiento | Agrupa las máquinas por nivel de urgencia y genera el plan de mantenimiento priorizado |
| `analizar_rendimiento_produccion(producidas, objetivo)` | Función | Calcula el porcentaje de eficiencia real vs. objetivo por máquina |
| `ajustar_programacion_produccion(demanda, eficiencias)` | Procedimiento | Asigna la demanda pendiente a la máquina más eficiente disponible |

### Impacto en rendimiento
El monitoreo y la planificación están desacoplados: el sistema puede monitorear continuamente sin bloquear la planificación. Calcular la eficiencia antes de asignar producción garantiza que los recursos se dirijan siempre a la máquina óptima, minimizando desperdicio.

---

## Problema 5 — Sistema de Riego Automatizado para Agricultura

### Funciones implementadas

| Función / Procedimiento | Tipo | Descripción |
|---|---|---|
| `leer_sensores_humedad(secciones)` | Función | Retorna el porcentaje de humedad actual del suelo por sección del campo |
| `consultar_prevision_meteorologica()` | Función | Simula la respuesta de una API meteorológica con lluvia esperada, temperatura máxima y humedad ambiental |
| `calcular_cantidad_riego(humedad_actual, humedad_objetivo, area_m2, prevision)` | Procedimiento | Determina los litros necesarios; devuelve 0 si se espera lluvia suficiente (≥10 mm) |
| `controlar_valvulas_riego(secciones_riego)` | Función | Abre o cierra cada válvula según el volumen calculado, mostrando la duración estimada |

### Impacto en rendimiento
Consultar la previsión meteorológica antes de calcular el riego evita activar válvulas innecesariamente, ahorrando agua y energía. La modularidad permite sustituir `consultar_prevision_meteorologica` por una llamada real a una API REST (como OpenWeatherMap) sin modificar las demás funciones.

---

## Principios de modularidad aplicados

- **Responsabilidad única:** cada función realiza exactamente una tarea.
- **Reutilización:** las funciones de lectura de sensores pueden usarse en cualquier problema sin modificación.
- **Separación lectura/lógica/acción:** leer datos → calcular → actuar, siguiendo el patrón de tres capas.
- **Sin efectos secundarios innecesarios:** las funciones retornan valores; los procedimientos modifican el estado de forma explícita y documentada.