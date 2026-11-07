# Analysis of CPMS

## ExitAvailability (Scenario A-QS2)

| Factor | Unavailability | Share |
|--------|----------------|-------|
| T3.6 | 0.0500 % | 17 % |
| T3.9 | 0.0500 % | 17 % |
| CGW | 0.0500 % | 17 % |
| SoS_K12a | 0.0500 % | 17 % |
| NCG | 0.1000 % | 33 % |

Chain availability: **99.7003 %** (26.2 h/year); target 99.9: **NOT met**

## ExitAvailabilityD2Before (Scenario A-QS2 (D2 before))

| Factor | Unavailability | Share |
|--------|----------------|-------|
| T3.6 × 2 (β = 0.05) | 0.0025 % | 2 % |
| T3.9 × 2 (β = 0.05) | 0.0025 % | 2 % |
| CGW × 2 (β = 0.05) | 0.0025 % | 2 % |
| SoS_K12a | 0.0500 % | 32 % |
| NCG | 0.1000 % | 63 % |

Chain availability: **99.8425 %** (13.8 h/year); target 99.9: **NOT met**

## FieldEventLoad (Scenario A-QS4)

| Element | Load | Capacity per instance | Instances | Utilization | Instances needed |
|---------|------|-----------------------|-----------|-------------|------------------|
| T2.5 | 20 | 10 | 1 | 200 % | 2 |

Bottleneck utilization: **200 %**; target 100: **NOT met**

## ConsolidatedStateQueries (Scenario A-QS6)

| Element | Load | Capacity per instance | Instances | Utilization | Instances needed |
|---------|------|-----------------------|-----------|-------------|------------------|
| SoS_K21a | 1.5 | 2 | 1 | 75 % | 1 |

Bottleneck utilization: **75 %**; target 100: **met**

## SoSQS1M4 (Scenario SoS-QS1 (M4))

| Stage | Budget |
|-------|--------|
| RGW | 200000 |
| SoS_K5 | 40000 |
| NCG | 230000 |
| SoS_K32 | 10000 |
| CGW | 300000 |

Chain latency: **780000**; target 900000: **met**

