# Analysis of CPMS

## ExitAvailability (Scenario A-QS2)

| Factor | Unavailability | Share |
|--------|----------------|-------|
| T3.6 × 2 (β = 0.05) | 0.0025 % | 33 % |
| T3.9 × 2 (β = 0.05) | 0.0025 % | 33 % |
| CGW × 2 (β = 0.05) | 0.0025 % | 33 % |

Chain availability: **99.9924 %** (0.7 h/year); target 99.9: **met**

## FieldEventLoad (Scenario A-QS4)

| Element | Load | Capacity per instance | Instances | Utilization | Instances needed |
|---------|------|-----------------------|-----------|-------------|------------------|
| T2.5 | 20 | 10 | 2 | 100 % | 2 |

Bottleneck utilization: **100 %**; target 100: **met**

## ConsolidatedStateQueries (Scenario A-QS6)

| Element | Load | Capacity per instance | Instances | Utilization | Instances needed |
|---------|------|-----------------------|-----------|-------------|------------------|
| SoS_K21a | 1.5 | 2 | 1 | 75 % | 1 |

Bottleneck utilization: **75 %**; target 100: **met**

## FieldEventAvailability (Scenario A-QS4 (pair))

| Factor | Unavailability | Share |
|--------|----------------|-------|
| T2.5 × 2 (β = 0.05) | 0.0051 % | 100 % |

Chain availability: **99.9949 %** (0.4 h/year); target 99.99: **met**

## SoSQS1M4 (Scenario SoS-QS1 (M4))

| Stage | Budget |
|-------|--------|
| RGW | 200000 |
| SoS_K5 | 40000 |
| NCG | 230000 |
| SoS_K32 | 10000 |
| CGW | 300000 |

Chain latency: **780000**; target 900000: **met**

