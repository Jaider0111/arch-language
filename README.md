# team-D-p3 — Modelado arquitectónico del Sistema de Coordinación Nacional (NCS)

Lenguaje del Laboratorio 4 adaptado por el equipo D, modelo conjunto `sos.arch` (escrito en el lenguaje base, así que corre igual con el lenguaje de cualquier equipo),
modelos del NCS antes (`ncs-e1.arch`) y después (`ncs-e2.arch`) de la Entrega 2,
transformaciones y artefactos generados.

## Ejecución

```bash
docker build -t lssa-team-d .
docker run --rm -v "$PWD:/app" lssa-team-d                      # los tres modelos de models/
docker run --rm -v "$PWD:/app" lssa-team-d invalid/c6-layers.arch  # un modelo mal formado
```

Sin argumentos se procesan todos los modelos de `models/`. Los artefactos quedan en
`out/<modelo>/`: `connectors.md`, `view.mmd` (Mermaid) y `analysis.md`.

## Estructura

| Archivo | Contenido |
|---------|-----------|
| `arch.tx` | Gramática (M2). Adaptaciones del equipo marcadas `[D]` |
| `metamodel.py` | Restricciones C1–C7 |
| `transformations.py` | Tabla de conectores, vista C&C y análisis |
| `generation.py` | Lee cada modelo, verifica la conformidad y aplica las transformaciones |
| `models/` | `sos.arch` (conjunto), `ncs-e1.arch`, `ncs-e2.arch` |
| `invalid/` | Un modelo mal formado por restricción agregada o adaptada, y los mensajes esperados |
| `out/` | Artefactos generados |
| `tools/gen_models.py` | Ayuda que escribió los modelos a partir de las tablas de la Entrega 2 |
| `team-D-p3.pdf` | Informe de la entrega |

## Adaptaciones del lenguaje

| Adaptación | Dónde | Para qué |
|------------|-------|----------|
| `domain` en componentes | Gramática, C4 | La regla de datos por dominio del NCS (Entrega 1) |
| `event_capacity`, `event_load`, `instances` | Gramática | Calcular la absorción de un rezago (D-QS10) y las réplicas de un servicio escalado (D-QS1) |
| Presupuesto por factor (`= valor`) | Gramática | Un presupuesto es un término del escenario, no una propiedad del elemento: el NCS tiene 230 s en M4 y 15 s en M3 |
| `beta` en un factor simple | Gramática, análisis | Componente con `instances` ≥ 2 y fracción de causa común, sin duplicar el componente |
| Métrica `deadline` | Análisis | Suma de presupuestos; un grupo trabaja en paralelo y cuenta su máximo (M4) |
| Métrica `recovery` con `backlog` | Análisis | Tiempo = rezago / Σ(capacidad × instancias − carga) |

## Restricciones

| ID | Restricción | Origen | Modelo rechazado |
|----|-------------|--------|------------------|
| C1–C3 | Sin cambios (Laboratorio 4) | — | — |
| C4 (adaptada) | Un almacén T4 solo se accede por dependencia desde componentes de su dominio; sin dominio, rige la regla del Laboratorio 4 | Regla de datos por dominio del NCS | `c4-domain.arch`, `c4-lab4-rule.arch` |
| C5 (extendida) | Cada factor tiene la propiedad que su métrica necesita, incluidas `deadline` y `recovery` | U5, Lectura 2, §4.2 | `c5-deadline.arch`, `c5-recovery.arch` |
| C6 (nueva, estilo) | Ningún componente T1 se une directamente a un almacén T4 | Estilo **en capas** del NCS (Entrega 1, §5) | `c6-layers.arch` |
| C7 (nueva, estilo) | Ningún comando de control cruza la frontera de un constituyente | SoS **reconocido**: estilo jerárquico solo donde la autoridad es real (Entrega 1, nivel global) | `c7-command.arch` |

## Convenciones

- Identificadores: `SoS-K5` se escribe `SoS_K5` y `D-K1` se escribe `D_K1`, porque el guion no es válido en un identificador (como `K2a′` → `K2a2` en el Laboratorio 4).
- Los componentes de frontera de los otros constituyentes aparecen en los modelos del NCS como en `sos.arch`. En `ncs-e2.arch`, los conectores globales entrantes pasan por el Balanceador de Entrada (`X -> BEN -> NCG`), como dice la sección 7.3 de la Entrega 2; su ID, naturaleza, acoplamiento y acuerdo son los de `sos.arch`.
- Un par solicitud/respuesta se clasifica como bloqueante en sus dos conectores. D-K1, que en la Entrega 2 es bloqueante para solicitudes y sumidero para eventos, se clasifica como bloqueante (la más restrictiva).
- Disponibilidad de 99,9 % (L17) en cada elemento que entra en una cadena. `event_capacity` = 3 veces la carga normal (L19), repartida entre los consumidores del Bus: Carga 1,5 → 4,5 eventos/s y Tránsito 20 → 60 eventos/s.
- `sos.arch` usa solo el lenguaje base. Los presupuestos de M4 van en ms y cada tramo lo lleva un elemento distinto, como K18 lleva la etapa 4 en el Laboratorio 4: RGW 200 s, SoS-K5 40 s, NCG 230 s, SoS-K32 10 s y CGW 300 s. CGW representa a los cuatro consumidores, que tienen el mismo presupuesto y trabajan en paralelo. M3 no cabe en el lenguaje base (RGW y NCG necesitarían un segundo valor): se analiza en los modelos del NCS con la métrica `deadline`. Los modelos del NCS repiten esas latencias en los elementos de frontera, que se escriben como en `sos.arch`.
- En `ncs-e1.arch`, el tramo del NCS en M4 toma el resultado de `DQS10` en ese mismo modelo (7.033 s). M3 no se puede escribir porque SoS-K36 todavía no existe.

## Resultados

| Escenario | Antes (e1) | Después (e2) | Entrega 2 | Diferencia |
|-----------|-----------|--------------|-----------|------------|
| D-QS1 | 99,30 %, no cumple | 99,95 %, cumple | 99,30 % → 99,95 % | Ninguna |
| D-QS1 con balanceadores | — | 99,55 %, no cumple | No calculado | La Entrega 2 no contó los 4 balanceadores que la cadena atraviesa, cada uno sin copia |
| D-QS10 | 7.032,6 s, no cumple | 189,8 s, cumple | ≈ 7.030 s → ≈ 190 s | Redondeo |
| SoS-QS1 (M4), `sos.arch` | — | 780.000 ms, cumple | 780 s | Ninguna; lenguaje base |
| SoS-QS1 (M4), modelos del NCS | 7.573 s, no cumple | 780 s, cumple | Sin cifra → 780 s | La Entrega 2 no dio cifra para la estructura de partida |
| SoS-QS1 (M3), modelos del NCS | No aplica (SoS-K36 no existe) | 55 s, cumple | 55 s | Ninguna; no se puede escribir en `sos.arch` con el lenguaje base |
