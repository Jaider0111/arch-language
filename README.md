# Lenguaje de descripción arquitectónica del CPMS (Entrega 3, equipo A)

Modelos y transformaciones del **Caribbean Port Management System (CPMS)**, constituyente `CPS` del SoS de transporte y comercio exterior. Parte del lenguaje del Laboratorio 4 (gramática textX, restricciones C1–C5 y transformaciones) y lo adapta al CPMS.

## Contenido

| Archivo / carpeta | Descripción |
|---|---|
| `arch.tx` | Gramática (M2) con las adaptaciones [A1]–[A4] |
| `metamodel.py` | Restricciones C1–C5 del laboratorio y C6–C9 derivadas de los estilos de la Entrega 1 |
| `transformations.py` | Tabla de conectores, vista C&C (Mermaid), resumen estructural y análisis de escenarios |
| `generation.py` | Programa de generación: carga un modelo, lo valida y escribe los artefactos en `out/<modelo>/` |
| `Dockerfile` | Imagen con Python 3.11 y textX 4.3.0 |
| `cpms-l1.arch` | Modelo de la estructura de partida (Entrega 1 con las propiedades de la Entrega 2) |
| `cpms-l3.arch` | Modelo de la estructura resultante (Entrega 2, §7) |
| `sos-qs1-demo.arch` | Fragmento con M3 y M4 de SoS-QS1 (M3 usa un presupuesto por factor) |
| `ill-formed/` | Diez modelos mal formados que el lenguaje rechaza, uno por restricción C1–C9 y una referencia desconocida |
| `make_ill.py` | Genera `ill-formed/` a partir de `cpms-l1.arch` |
| `out/` | Artefactos generados de cada modelo: `connectors.md`, `view.mmd`, `summary.md`, `analysis.md` |
| `VALIDACION.md` | Validación de los elementos del metamodelo frente al CPMS y al `sos.arch`, límites del lenguaje y pendientes |

### Restricciones

| ID | Regla |
|---|---|
| C1 | Todo enlace une al menos dos componentes |
| C2 | Un comando de control tiene un solo origen |
| C3 | Todo conector de frontera tiene acuerdo |
| C4 | Un almacén de datos (T4) lo consulta por dependencia un solo componente |
| C5 | Cada factor de un análisis es válido para su métrica y el elemento trae la propiedad que necesita |
| C6 | Ningún comando de control cruza la frontera (el SoS es reconocido, no dirigido) |
| C7 | Todo enlace de frontera empieza y termina en un componente T2 (patrón gateway) |
| C8 | Un equipo físico (T5) recibe comandos de un solo origen (estilo jerárquico y lazo de control) |
| C9 | Una notificación de evento nunca es bloqueante (estilo orientado a eventos) |

## Uso con Docker

Todos los comandos se ejecutan dentro de esta carpeta (`cpms/`).

Construir la imagen:

```bash
docker build -t lssa-cpms .
```

Generar los artefactos de un modelo (se escriben en `out/<modelo>/`):

```bash
docker run --rm -v "$PWD:/app" lssa-cpms cpms-l1.arch
docker run --rm -v "$PWD:/app" lssa-cpms cpms-l3.arch
docker run --rm -v "$PWD:/app" lssa-cpms sos-qs1-demo.arch
```

Comprobar que un modelo mal formado es rechazado (termina con error y con el mensaje de la restricción):

```bash
docker run --rm -v "$PWD:/app" lssa-cpms ill-formed/c6-command-across-boundary.arch
```

Probar los diez de una vez:

```bash
for f in ill-formed/*.arch; do
  echo "== $f"; docker run --rm -v "$PWD:/app" lssa-cpms "$f" 2>&1 | tail -1
done
```

Regenerar `ill-formed/` desde `cpms-l1.arch` (cambia la entrada de la imagen):

```bash
docker run --rm -v "$PWD:/app" --entrypoint python lssa-cpms make_ill.py
```

En Windows con PowerShell, `$PWD` funciona igual; en `cmd` usa `%cd%`.

## Uso sin Docker

```bash
pip install textX==4.3.0
python generation.py cpms-l1.arch
python generation.py cpms-l3.arch
```

## Resultados esperados

| Modelo | Escenario | Resultado | Meta |
|---|---|---|---|
| `cpms-l1.arch` | A-QS2 disponibilidad de la salida | 99,7003 % (26,2 h/año) | 99,9 % (supuesto) |
| `cpms-l1.arch` | A-QS4 utilización de T2.5 | 200 % | 100 % |
| `cpms-l1.arch` | A-QS6 consultas de SoS_K21a | 75 % | 100 % |
| `cpms-l1.arch` | SoS-QS1 (M4) | 780 s | 900 s |
| `cpms-l3.arch` | A-QS2 disponibilidad de la salida | 99,9924 % (0,7 h/año) | 99,9 % (supuesto) |
| `cpms-l3.arch` | A-QS4 utilización de T2.5 | 100 % | 100 % |
| `cpms-l3.arch` | A-QS4 disponibilidad del par de T2.5 | 99,9949 % | 99,99 % (supuesto) |
| `cpms-l3.arch` | A-QS6 consultas de SoS_K21a | 75 % | 100 % |
| `cpms-l3.arch` | SoS-QS1 (M4) | 780 s | 900 s |

Los valores de latencia de `.arch` están en milisegundos (como en `sos.arch`); `analysis.md` los muestra en esa unidad (780000 = 780 s).

## Convenciones de los modelos

- Los componentes internos conservan el identificador de la Entrega 1 (`T1.1` … `T5.10`) y los conectores internos `A-K1` … `A-K89` (con `'` para los modificados, por ejemplo `A-K85'`).
- Los componentes de frontera y los conectores globales se escriben como en `sos.arch`: constituyentes `CPS`, `RTS`, `RLS`, `FTS`, `NCS`; gateways `CGW` (T2.1), `RGW`, `LGW`, `FGW`, `NCG`; conectores `SoS_K…` con pares `a`/`b` para solicitud y respuesta.
- Un conector es de frontera si un enlace suyo une componentes de constituyentes distintos (se deriva, no se declara).
- Disponibilidad en %, tasas en eventos o solicitudes por segundo, latencias en milisegundos.
