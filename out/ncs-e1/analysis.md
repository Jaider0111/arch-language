# Analysis of NCS

## DQS1 (Scenario D-QS1)

| Factor | Unavailability | Share |
|--------|----------------|-------|
| NCG | 0.1000 % | 14 % |
| TRA | 0.1000 % | 14 % |
| ADU | 0.1000 % | 14 % |
| RSK | 0.1000 % | 14 % |
| CAR | 0.1000 % | 14 % |
| RMDB | 0.1000 % | 14 % |
| EXDB | 0.1000 % | 14 % |

Chain availability: **99.30 %** (61.1 h/year); target 99.9: **NOT met**

## DQS10 (Scenario D-QS10)

| Consumer | Capacity (events/s × instances) | Load (events/s) | Spare (events/s) |
|----------|----------------------------------|-----------------|------------------|
| CAR | 4.5 × 1 | 1.5 | 3 |
| TRS | 60 × 1 | 20 | 40 |
| **Total** | | | **43** |

Recovery time: **7032.6 s** (302400 events / 43 events/s); target 230: **NOT met**

## SoSQS1M4 (Scenario SoS-QS1 (M4))

| Stage | Budget |
|-------|--------|
| RGW | 200 s |
| SoS_K5 | 40 s |
| NCG | 7033 s |
| CGW (300 s) ‖ PGW (300 s) ‖ LGW (300 s) ‖ FGW (300 s) | 300 s (maximum, in parallel) |

Composed deadline: **7573 s**; target 900: **NOT met**
