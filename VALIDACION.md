# Validación del metamodelo del Laboratorio 4 para el CPMS

Insumos: `LAB4.zip` (paquete del Laboratorio 4: ERTMS), `team-A-p1.pdf`, `team-A-p2.pdf`, enunciados del Laboratorio 4 y de la Entrega 3.

**Aclaración sobre el zip.** `LAB4.zip` contiene el paquete del laboratorio sobre el ERTMS (`arch.tx`, `metamodel.py`, `transformations.py`, `ertms-l1.arch`, `ertms-l3.arch`). No contiene nada específico del NCS ni de un equipo D. Lo usé como metamodelo de referencia. Si el equipo D adaptó algo para el NCS, no está en el zip.

## 1. Resultado

Todos los conceptos del metamodelo aplican al CPMS. El modelo del Caribe (`cpms-l1.arch`: 44 componentes propios + 4 gateways vecinos, 107 conectores) conforma con el metamodelo y reproduce las cifras de las Entregas 1 y 2. Hacen falta cuatro adaptaciones al lenguaje y cuatro restricciones nuevas derivadas de estilos.

## 2. Validación elemento por elemento

| Elemento del Lab 4 | ¿Aplica al CPMS? | Evidencia | Ajuste |
|---|---|---|---|
| `Constituent` + dueño | Sí | E1 §3.1: seis constituyentes con dueño | El modelo declara cinco: el Pacífico no tiene conectores con el Caribe |
| `Component` con tier T1–T5 | Sí | E1 §4.2.6: 6 / 7 / 12 / 9 / 10 = 44 | Ninguno. El modelo reproduce los 44 |
| `kind` (4 valores) | Sí | E1 «Tipo»: Software, Hardware y software, Hardware, Físico | Ninguno |
| `nature` (4 valores) | Sí | Se usan las cuatro: 36 flujos de datos, 12 comandos, 22 dependencias, 18 eventos (internos) | Ninguno |
| `coupling` (3 valores) | Sí | E2 §4.1 usa exactamente bloqueante / suministro / sumidero | Ninguno en el lenguaje. Internos 22 / 60 / 6 (igual que E2). Los 19 globales siguen ahora el `sos.arch` del equipo D (16 bloqueantes / 0 suministro / 3 sumidero), no el 8 / 9 / 2 de E2 §4.1: hay que decidirlo con D |
| `Link` con camino `A -> B -> C` | Aplica, no se usa | Los 107 conectores son de un solo salto (E1 §4.3: pares a/b) | Ninguno |
| Unidireccionalidad (gramática) | Sí | E1 §4.3: «todos los conectores internos son unidireccionales» | Ninguno |
| Frontera **derivada** | Sí | Salen exactamente los 19 SoS-K del Caribe. A-K70..A-K88 dan «No», como en E1 | Ninguno |
| `agreement` obligatorio en frontera (C3) | Sí | E1 §3.3: los globales «solo pueden cambiarse por acuerdo» | Los 19 acuerdos globales se tomaron literalmente del `sos.arch` del equipo D (acuerdo v4). Las versiones v1..v4 no se representan |
| `availability` / `latency` | Parcial | L9–L11 se mapean directo. Las latencias de E2 son timeouts anidados, no presupuestos que se suman | Ver [A2] y §5 |
| `Analysis` con `Single` | Sí | Cadena C1 (A-QS2) | Se añade `value` por factor [A3] |
| `Group` con β | Parcial | E2 usa pares de T2.1, T2.5, T3.6, T3.9 sin duplicar el componente | Se añade `Replicated` [A4] |
| C1 enlace con ≥ 2 componentes | Sí | Se cumple | Ninguno |
| C2 un solo origen por comando | Sí | Se cumple | Ninguno |
| C3 frontera con acuerdo | Sí | Se cumple en los 19 | Ninguno |
| C4 almacén con un solo usuario | Sí | A-K58..A-K65: ocho almacenes, un dueño cada uno. T4.8 (histórico) se alimenta por evento y C4 no lo toca | Ninguno |
| C5 propiedad requerida | Sí | Ver [A2], [A3] | Extendida a `utilization` y a `value` |

## 3. Comprobaciones cruzadas con tus entregas

| Dato | Entregas | Modelo | Resultado |
|---|---|---|---|
| Componentes por tier | 6 / 7 / 12 / 9 / 10 (E1) | 6 / 7 / 12 / 9 / 10 | Coincide |
| Conectores internos / globales | 88 / 19 | 88 / 19 | Coincide |
| Acoplamiento interno | 22 / 60 / 6 (E2 §4.1) | 22 / 60 / 6 | Coincide |
| Acoplamiento global | 8 / 9 / 2 (E2 §4.1) | 16 / 0 / 3 (según `sos.arch`) | No coincide con E2: las 9 respuestas/avisos (K1b, K10b, K12b, K21b, K24b, K25b, K26b, K31b, K32) se clasifican distinto. Decidir con D |
| Conectores internos que tocan T3 | 63 (E1 §4.2.6) | 63 | Coincide |
| Conectores de T2.1 | 38 (E1 §6.2) | 38 | Coincide |
| Cada SoS-K lo sirve un solo A-K | A-K70..A-K88 (E1 §4.3) | 19 de 19, una vez cada uno, misma naturaleza y sentido opuesto en el gateway | Coincide |
| Disponibilidad C1 antes (A-QS2) | 99,84 % (13,8 h/año) | 99,8425 % (13,8 h/año) | Coincide |
| SoS-QS1 M3 / M4 | 55 s / 780 s | 55 / 780 (`sos-qs1-demo.arch`) | Coincide |
| A-QS4 antes | T2.5 no escala | 20 / 10 = 200 %, hacen falta 2 instancias | Coherente con E2 |
| A-QS6 tasa programada | 1,5 / 2 por s | 75 % | Coincide |

**Compatibilidad hacia atrás.** Con la gramática adaptada, `ertms-l1.arch` y `ertms-l3.arch` dan los mismos resultados del laboratorio (99,64 % y 1000 ms; 850 ms) y la misma tabla de conectores.

## 4. Adaptaciones al lenguaje

### Gramática

- **[A1] Identificadores de las entregas** (`T2.1`, `A-K70`, `SoS-K12a`, `A-K85'`). Se conserva la convención de E1 y E2, y la trazabilidad es directa. El gateway del Caribe se llama `CPMS-GW` porque en `sos.arch` los seis equipos tienen un «T2.1» y los nombres deben ser únicos. Su etiqueta es «T2.1 Caribbean Port Gateway».
- **[A2] `capacity`, `load`, `instances` y la métrica `utilization`.** Los necesitan A-QS4 (L2 × L8 = 20 eventos/s contra 10 por instancia) y A-QS6 (1,5 consultas/s contra el tope de 2 de P7). Son los «capacity, load» que pide la Entrega 3.
- **[A3] `value` por factor** (`RGW value 30`). Sin esto un elemento solo puede tener un presupuesto, pero SoS-QS1 usa `Road Gateway` con 30 s en M3 y 200 s en M4.
- **[A4] `Replicated`** (`T3.6 replicas 2 beta 0.05`). E2 aplica β a pares de T2.1, T2.5, T3.6 y T3.9 sin añadir componentes. `Group` obliga a dos componentes distintos, lo que cambiaría la estructura de E1 (44 componentes).

### Restricciones nuevas, derivadas de estilos de E1

| | Estilo (E1) | Regla | Rechaza |
|---|---|---|---|
| **C6** | SoS reconocido; jerárquico solo interno (§5.5) | Ningún conector de frontera lleva `control_command` | `c6-command-across-boundary` |
| **C7** | Patrón gateway (§3.2, §3.5) | Todo enlace de frontera empieza y termina en un componente T2 | `c7-boundary-link-not-at-gateway` |
| **C8** | Jerárquico y lazo de control (§5.2) | Un equipo T5 recibe comandos de un único origen | `c8-equipment-with-two-authorities` |
| **C9** | Orientado a eventos / publicar-suscribir | Una `event_notification` nunca es bloqueante | `c9-event-with-blocking-coupling` |

Cada una tiene su modelo mal formado en `ill-formed/`, junto con uno por cada C1–C5 y uno de referencia desconocida. Los diez se rechazan antes de generar ningún artefacto. Ejemplo (C8): `T5.1: equipment commanded by several authorities ['T3.10', 'T5.8']`.

C6, C7 y C8 son específicas de un SoS reconocido con gateways. El ERTMS las incumple a propósito (K2b y K6 llevan comandos entre constituyentes, K1 cruza en T5, K13 cruza en T1 y T3, OBU recibe órdenes de RAD y STM). Si se quiere un lenguaje común para los seis equipos, C6 y C7 son candidatas a restricción conjunta.

## 5. Lo que el lenguaje no puede analizar (para «Observaciones» de la Entrega 3)

| Escenario | Qué falta |
|---|---|
| A-QS1 (400 registros en ≤ 200 s) | Volumen y tasa de drenaje: 400 / 200 = 2 registros/s. Solo existe carga contra capacidad |
| A-QS2 (timeouts 2,2 / 2,5 / 3 s) | Timeouts, reintentos y la regla «cada timeout externo supera la suma de los internos». El análisis de latencia solo suma. Tampoco hay p95 |
| A-QS3 (0 % de eventos falsificados) | Seguridad no se mide con disponibilidad, latencia ni utilización. Solo se podría presupuestar el sobrecosto de 35 ms |
| A-QS5 (despliegue < 2 semanas, v1/v2) | Versiones de contrato y tiempos de cambio |
| A-QS6 (reconciliar 120 citas en 60 s) | Igual que A-QS1: volumen / tasa. La detección (3P = 180 s) sí se puede expresar con `value` |
| SoS-QS1 M4 | `máx(consumidores)` en paralelo. Se escribe con un solo consumidor porque los cuatro valen 300 s |
| SoS-QS1 M1 y M2 | Regla de despacho (P5) y error de ETA p95 (±30 min): comportamiento y percentiles |

## 6. Hallazgos en las entregas que el modelo dejó ver

1. **E2 §7.3 está incompleto para armar `cpms-l3.arch`.** Lista A-K85', A-K89, A-K76', A-K90 y A-K88'. La figura 7.1 menciona A-K85' y A-K89 a A-K98. El §6.2 dice que los conectores nuevos T2.1 → T3.6 / T3.8 / T3.12 arrancan «desde A-K89», que ya es T2.8 → T2.1. El conector T3.8 → T3.6 (ETA) no tiene número. Hay que definir A-K91..A-K98 antes de modelar la estructura resultante.
2. **E2 «antes» ya usa pares redundantes.** El 99,84 % de A-QS2 supone dos réplicas de T2.1, T3.6 y T3.9, pero E1 tiene una sola instancia de cada una. El modelo lo expresa en el análisis con `replicas 2`, no en la estructura. Conviene confirmarlo con el equipo.
3. **Fórmula de β.** E2 escribe `β·U + (1−β)·U²` y el laboratorio usa `β·U + ((1−β)·U)ⁿ`. Dan lo mismo hasta 99,99748 % por par y 99,8425 % / 99,9924 % en la cadena. Explicarlo en una línea si algún evaluador lo pregunta.
4. **E2 no fija una meta de disponibilidad para C1.** El modelo usa 99,9 % como supuesto, y solo el valor calculado se compara con E2.
5. **Cifras de E1 §7 con error de una unidad.** T3.6 tiene 13 conectores (E1 dice 12), T3.10 tiene 7 (dice 8), y T2.1 integra los 19 globales con A-K70..A-K88 (E1 escribe «13 conectores, A-K46 a A-K58»).

## 7. Archivos

| Archivo | Contenido |
|---|---|
| `arch.tx`, `metamodel.py` | Gramática adaptada y restricciones C1–C9 |
| `transformations.py` | Tabla de conectores, vista Mermaid, análisis (disponibilidad, latencia, utilización) y `summary.md`, que reproduce los conteos de E1 y E2 |
| `generation.py`, `Dockerfile` | Sin cambios salvo el modelo por defecto |
| `cpms-l1.arch`, `cpms-l3.arch` | Estructura de partida (E1 + propiedades de E2) y estructura resultante (E2 §7), con los nombres del `sos.arch` |
| `sos-qs1-demo.arch` | Fragmento que prueba M3 y M4 (M3 no cabe en `sos.arch`, ver §9). No es el `sos.arch` conjunto |
| `ill-formed/` | Diez modelos rechazados |
| `out/cpms-l1/`, `out/cpms-l3/`, `out/sos-qs1-demo/` | Artefactos generados |

Ejecución: `docker build -t lssa-lab4 .` y `docker run --rm -v "$PWD:/app" lssa-lab4 cpms-l1.arch`. Yo lo corrí con Python 3.13 y textX 4.3.0 directamente, **no con Docker**.

## 8. Pendiente

- Acordar con el equipo D (y los demás) el acoplamiento de las 9 respuestas globales (§9).
- Confirmar y modelar A-K91..A-K98 (E2 §7 solo define A-K89 y A-K90; propuesta en comentario al final de `cpms-l3.arch`).
- Incluir el `sos.arch` conjunto, idéntico en los seis equipos, en el zip. Hoy se usa el del equipo D como referencia.
- Probar con Docker.
- El informe en PDF de la Entrega 3 (vence el viernes 6 de noviembre, 23:59).

## Modelo «después»: `cpms-l3.arch` (Entrega 2, §7)

Se obtiene editando `cpms-l1.arch`, como `ertms-l3.arch` en el Lab 3. Aplicado: T2.8 y T2.9, A-K85', A-K89, A-K76', A-K90, A-K88', y `instances 2` en T2.1, T2.5, T3.6 y T3.9. No se modelan A-K91..A-K98 (la Entrega 2 solo define A-K89 y A-K90); las propuestas de numeración están como comentario al final del archivo.

| Métrica | l1 (antes) | l3 (después) | Entrega 2 |
|---|---|---|---|
| A-QS2 disponibilidad de la salida | 99,7003 % (26,2 h/año) | 99,9924 % (0,7 h/año) | 99,992 % después |
| A-QS2 con los pares que la Entrega 2 ya supone en «antes» | 99,8425 % (`ExitAvailabilityD2Before`) | n/a | 99,84 % antes |
| A-QS4 utilización de T2.5 | 200 % (necesita 2 instancias) | 100 % | 20 ev/s, 2 instancias |
| A-QS4 disponibilidad del par T2.5 | n/a | 99,9949 % | 99,9949 % |
| A-QS6 consultas SoS-K21a | 75 % | 75 % | 1,5 de 2 consultas/s |

Conteo l3: 46 componentes del CPMS (9 en T2), 91 conectores internos (22 modificados o nuevos respecto a l1: 4 nuevos + A-K85' que reemplaza a A-K85 + A-K88' con dos enlaces), 19 globales.

Hallazgo: el «antes» de la Entrega 2 (99,84 %) ya incluye pares redundantes que la Entrega 1 no tiene; con una sola instancia, el estado de partida real es 99,70 %.

## 9. Referencia: `sos.arch` del equipo D (NCS)

Se recibió después de la validación inicial de los elementos (§§1–7), que se hizo contra el Lab 4 y las entregas 1 y 2. Se usó así:

- **Carga:** `sos.arch` carga sin cambios con la gramática del Lab 4 y con la gramática adaptada, y cumple C1–C9. No hace falta modificarlo para que coincida con los elementos del CPMS.
- **Estructura:** los 19 conectores globales del Caribe están en `sos.arch` (K1a/b, K10a/b, K11, K12a/b, K21a/b, K24a/b, K25a/b, K26a/b, K29, K31a/b, K32) con la misma naturaleza y dirección que en el modelo del CPMS.
- **Cambios que se hicieron al modelo del CPMS a partir de él:**
  1. Nombres como en `sos.arch`: constituyentes `CPS`, `RTS`, `RLS`, `FTS`, `NCS` (con sus etiquetas y dueños), gateways `CGW`, `RGW`, `LGW`, `FGW`, `NCG` y conectores `SoS_K…`. Los identificadores internos (`T2.1`, `A-K…`) no cambian.
  2. Los 19 acuerdos globales son los textos de `sos.arch` (acuerdo v4).
  3. El acoplamiento de los 19 globales es el de `sos.arch`: 16 bloqueantes, 0 suministro y 3 sumidero. **Contradice E2 §4.1 (8 / 9 / 2)** en K1b, K10b, K12b, K21b, K24b, K25b, K26b, K31b y K32. Decisión pendiente con D.
  4. SoS-QS1 (M4) se incluye en l1 y l3 con la misma cadena y presupuestos que `sos.arch` (RGW 200 s, SoS_K5 40 s, NCG 230 s, SoS_K32 10 s, CGW 300 s): 780 s, meta 900 s. Para eso los modelos incluyen el conector `SoS_K5` (RGW → NCG), que no es del CPMS pero es parte de la cadena, y la latencia de K32 (10 s).
- **Comprobación automática:** en los dos modelos, los 20 conectores `SoS_K` coinciden con `sos.arch` en origen, destino, naturaleza, acoplamiento, acuerdo y latencia, y los cinco gateways coinciden en constituyente, tier y latencia.
- **No cubre `sos.arch`:** M3 (visibilidad del peaje) necesita un presupuesto distinto para RGW (30 s frente a 200 s en M4); con un solo valor por componente, `sos.arch` solo puede analizar M4. Tampoco lleva disponibilidad, por lo que no hay análisis de A-QS2 sobre él.
