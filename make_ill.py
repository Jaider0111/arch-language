import sys
src = open('models/cpmscpms-l1.arch', encoding='utf-8').read()

def mutate(name, old, new):
    assert src.count(old) == 1, (name, src.count(old))
    open(f'models/cpms/ill-formed/{name}.arch', 'w', encoding='utf-8').write(src.replace(old, new))

# Constraints of Laboratory 4 (C1-C5) and reference
mutate('c1-link-with-one-component',
       ': T2.5 -> T5.4\n', ': T5.4\n')
mutate('c2-command-with-two-sources',
       'carries "Órdenes de trabajo para grúas" : T3.10 -> T2.4',
       'carries "Órdenes de trabajo para grúas" : T3.10 -> T2.4, T3.5 -> T2.4')
mutate('c3-boundary-without-agreement',
       '    agreement "Contrato de levante aduanero (v1)" availability 99.95\n    : CGW -> NCG\n',
       '    availability 99.95\n    : CGW -> NCG\n')
mutate('c4-store-shared',
       'carries "Registros de cambio de custodia" : T3.8 -> T4.4',
       'carries "Registros de cambio de custodia" : T3.8 -> T4.1')
mutate('c5-analysis-without-property',
       'component NCG\n', 'component NCG\n') if False else None
mutate('c5-analysis-without-property',
       'in NCS  tier T2 kind software availability 99.90', 'in NCS  tier T2 kind software')
mutate('reference-unknown-component',
       'carries "Solicitud de atraque para una escala" : T3.1 -> T3.2',
       'carries "Solicitud de atraque para una escala" : T3.1 -> T3.99')
# Constraints added for the CPMS
mutate('c6-command-across-boundary',
       'connector SoS_K1b nature data_flow coupling blocking',
       'connector SoS_K1b nature control_command coupling blocking')
mutate('c7-boundary-link-not-at-gateway',
       'availability 99.95\n    : RGW -> CGW\nconnector SoS_K1b',
       'availability 99.95\n    : RGW -> T3.6\nconnector SoS_K1b')
mutate('c8-equipment-with-two-authorities',
       '// Datos de campo hacia el sistema\n',
       '// Datos de campo hacia el sistema\nconnector A-K99 nature control_command coupling supply\n    carries "Orden directa a la grúa de muelle, saltando el lazo de control" : T3.10 -> T5.1\n')
mutate('c9-event-with-blocking-coupling',
       'connector A-K22 nature event_notification coupling supply',
       'connector A-K22 nature event_notification coupling blocking')
