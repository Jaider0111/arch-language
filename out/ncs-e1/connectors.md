# Connectors of NCS

| ID | Source → Target | Nature | Coupling | Information carried | Boundary |
|----|-----------------|--------|----------|---------------------|----------|
| D_K1 | National Coordination Gateway → Traductor de Mensajes Externos | Data flow | Blocking | Mensajes entrantes validados contra el CDM, con identidad del remitente | No |
| D_K2 | Traductor de Mensajes Externos → National Coordination Gateway | Data flow | Blocking | Respuestas en CDM: certificados de levante y estados consolidados | No |
| D_K3 | Traductor de Mensajes Externos → Bus de Eventos | Event notification | Sink | Hechos operacionales: arribos, manifiestos, custodias, posiciones | No |
| D_K4a | Traductor de Mensajes Externos → Servicio de Aduana | Dependency | Blocking | Solicitud de trámite de levante | No |
| D_K4b | Servicio de Aduana → Traductor de Mensajes Externos | Data flow | Blocking | Resultado y certificado de levante | No |
| D_K5a | Traductor de Mensajes Externos → Servicio de Carga | Dependency | Blocking | Consulta de estado, con el constituyente solicitante | No |
| D_K5b | Servicio de Carga → Traductor de Mensajes Externos | Data flow | Blocking | Estado de la carga, solo si el solicitante participa en ella | No |
| D_K6 | Bus de Eventos → Servicio de Carga | Event notification | Sink | Arribos, manifiestos, custodias y decisiones de levante | No |
| D_K7 | Servicio de Carga → Historial de Carga DB | Dependency | Blocking | Lectura y escritura de la historia de cada carga | No |
| D_K8 | Servicio de Carga → Repositorio de Manifiestos DB | Dependency | Blocking | Lectura y escritura de manifiestos | No |
| D_K9 | Bus de Eventos → Servicio de Tránsito | Event notification | Supply | Posiciones, estado de tránsito y eventos de viaje | No |
| D_K10 | Servicio de Tránsito → Historial de Posiciones DB | Dependency | Blocking | Lectura y escritura de posiciones | No |
| D_K11 | Servicio de Tránsito → Bus de Eventos | Event notification | Sink | Alertas por desvío, detención prolongada o sello comprometido | No |
| D_K12a | Servicio de Carga → Servicio de Tránsito | Dependency | Blocking | Consulta de la última posición del vehículo que lleva una carga | No |
| D_K12b | Servicio de Tránsito → Servicio de Carga | Data flow | Blocking | Última posición registrada | No |
| D_K13 | Bus de Eventos → Consola del Centro de Coordinación | Event notification | Sink | Alertas operacionales y de tránsito | No |
| D_K14a | Consola del Centro de Coordinación → Servicio de Carga | Dependency | Blocking | Consulta del historial y estado de una carga | No |
| D_K14b | Servicio de Carga → Consola del Centro de Coordinación | Data flow | Blocking | Historia completa y estado consolidado | No |
| D_K15a | Servicio de Aduana → Servicio de Riesgo | Dependency | Blocking | Solicitud de evaluación de riesgo | No |
| D_K15b | Servicio de Riesgo → Servicio de Aduana | Data flow | Blocking | Perfil de riesgo calculado y control sugerido | No |
| D_K16a | Servicio de Riesgo → Servicio de Carga | Dependency | Blocking | Solicitud de manifiesto y composición del embarque | No |
| D_K16b | Servicio de Carga → Servicio de Riesgo | Data flow | Blocking | Manifiesto y actores involucrados | No |
| D_K17 | Servicio de Riesgo → Expediente Aduanero DB | Dependency | Blocking | Lectura de antecedentes, sanciones e historial de inspecciones | No |
| D_K18a | Consola Aduanera → Servicio de Aduana | Dependency | Blocking | Consulta de los casos pendientes de revisión | No |
| D_K18b | Servicio de Aduana → Consola Aduanera | Data flow | Blocking | Casos pendientes, con su evaluación de riesgo y antecedentes | No |
| D_K19 | Consola Aduanera → Servicio de Aduana | Control command | Blocking | Decisión del funcionario: levante, escáner o inspección física | No |
| D_K20 | Servicio de Aduana → Expediente Aduanero DB | Dependency | Blocking | Lectura y escritura del expediente | No |
| D_K21 | Servicio de Aduana → Adaptador de Escáneres | Control command | Blocking | Orden de inspección no intrusiva | No |
| D_K22 | Adaptador de Escáneres → Escáner de Inspección No Intrusiva | Control command | Blocking | Instrucción en el protocolo del fabricante | No |
| D_K23 | Escáner de Inspección No Intrusiva → Adaptador de Escáneres | Data flow | Blocking | Imagen y lectura técnica | No |
| D_K24 | Adaptador de Escáneres → Servicio de Aduana | Data flow | Blocking | Resultado estandarizado de la inspección | No |
| D_K25a | Aplicación del Inspector → Servicio de Aduana | Dependency | Blocking | Consulta de las órdenes de inspección física asignadas | No |
| D_K25b | Servicio de Aduana → Aplicación del Inspector | Data flow | Blocking | Órdenes de inspección física asignadas | No |
| D_K26 | Aplicación del Inspector → Servicio de Aduana | Data flow | Blocking | Hallazgos y verificación del sello | No |
| D_K27 | Servicio de Aduana → Bus de Eventos | Event notification | Sink | Decisión de levante emitida | No |
| SoS_K5 | Road Gateway → National Coordination Gateway | Event notification | Sink | Custodia recibida por el transportador; v3: ETA al despachar | Yes |
| SoS_K6 | Road Gateway → National Coordination Gateway | Event notification | Supply | Posición del vehículo, estado del tránsito y eventos en ruta | Yes |
| SoS_K8 | Pacific Port Gateway → National Coordination Gateway | Event notification | Sink | Arribo/zarpe de motonave y manifiesto en puertos del Pacífico | Yes |
| SoS_K9a | Pacific Port Gateway → National Coordination Gateway | Dependency | Blocking | Solicitud de validación de levante previa a la salida por portería | Yes |
| SoS_K9b | National Coordination Gateway → Pacific Port Gateway | Data flow | Blocking | Estado de levante: concedido, inspección requerida o retenido | Yes |
| SoS_K11 | Caribbean Port Gateway → National Coordination Gateway | Event notification | Sink | Arribo/zarpe de motonave y manifiesto en puertos del Caribe | Yes |
| SoS_K12a | Caribbean Port Gateway → National Coordination Gateway | Dependency | Blocking | Solicitud de validación de levante previa a la salida por portería | Yes |
| SoS_K12b | National Coordination Gateway → Caribbean Port Gateway | Data flow | Blocking | Estado de levante: concedido, inspección requerida o retenido | Yes |
| SoS_K13 | Rail Gateway → National Coordination Gateway | Event notification | Sink | Custodia recibida por el concesionario y composición del tren | Yes |
| SoS_K14 | Rail Gateway → National Coordination Gateway | Event notification | Supply | Posición del convoy, estado del corredor y eventos de vía | Yes |
| SoS_K15 | Fluvial Gateway → National Coordination Gateway | Event notification | Sink | Custodia recibida por el operador fluvial | Yes |
| SoS_K16 | Fluvial Gateway → National Coordination Gateway | Event notification | Supply | Posición de barcaza o remolcador y estado de navegación | Yes |
| SoS_K17a | Road Gateway → National Coordination Gateway | Dependency | Blocking | Consulta de estado consolidado de la carga en la que participa el transportador | Yes |
| SoS_K17b | National Coordination Gateway → Road Gateway | Data flow | Blocking | Estado consolidado limitado a su carga; v3: posición y ETA estimadas | Yes |
| SoS_K18a | Rail Gateway → National Coordination Gateway | Dependency | Blocking | Consulta de estado consolidado de la carga en la que participa el concesionario | Yes |
| SoS_K18b | National Coordination Gateway → Rail Gateway | Data flow | Blocking | Estado consolidado limitado a su carga; v3: posición y ETA estimadas | Yes |
| SoS_K19a | Fluvial Gateway → National Coordination Gateway | Dependency | Blocking | Consulta de estado consolidado de la carga en la que participa el operador fluvial | Yes |
| SoS_K19b | National Coordination Gateway → Fluvial Gateway | Data flow | Blocking | Estado consolidado limitado a su carga; v3: posición y ETA estimadas | Yes |
| SoS_K20a | Pacific Port Gateway → National Coordination Gateway | Dependency | Blocking | Consulta de estado consolidado de la carga en la que participa el operador portuario | Yes |
| SoS_K20b | National Coordination Gateway → Pacific Port Gateway | Data flow | Blocking | Estado consolidado limitado a su carga; v3: posición y ETA estimadas | Yes |
| SoS_K21a | Caribbean Port Gateway → National Coordination Gateway | Dependency | Blocking | Consulta de estado consolidado de la carga en la que participa el operador portuario | Yes |
| SoS_K21b | National Coordination Gateway → Caribbean Port Gateway | Data flow | Blocking | Estado consolidado limitado a su carga; v3: posición y ETA estimadas | Yes |
