# Analysis of NCS

## DQS1 (Scenario D-QS1)

| Factor | Unavailability | Share |
|--------|----------------|-------|
| NCG × 2 (β = 0.1) | 0.0101 % | 20 % |
| TRA × 2 (β = 0.1) | 0.0101 % | 20 % |
| ADU × 2 (β = 0.1) | 0.0101 % | 20 % |
| RSK × 2 (β = 0.1) | 0.0101 % | 20 % |
| EXDB, EXDB2 (β = 0.1) | 0.0101 % | 20 % |

Chain availability: **99.95 %** (4.4 h/year); target 99.9: **met**

## DQS1Balancers (Scenario D-QS1 (with balancers))

| Factor | Unavailability | Share |
|--------|----------------|-------|
| BEN | 0.1000 % | 22 % |
| NCG × 2 (β = 0.1) | 0.0101 % | 2 % |
| BTR | 0.1000 % | 22 % |
| TRA × 2 (β = 0.1) | 0.0101 % | 2 % |
| BAD | 0.1000 % | 22 % |
| ADU × 2 (β = 0.1) | 0.0101 % | 2 % |
| BRI | 0.1000 % | 22 % |
| RSK × 2 (β = 0.1) | 0.0101 % | 2 % |
| EXDB, EXDB2 (β = 0.1) | 0.0101 % | 2 % |

Chain availability: **99.55 %** (39.4 h/year); target 99.9: **NOT met**

## DQS10 (Scenario D-QS10)

| Consumer | Capacity (events/s × instances) | Load (events/s) | Spare (events/s) |
|----------|----------------------------------|-----------------|------------------|
| CAR | 4.5 × 2 | 1.5 | 7.5 |
| TRS | 60 × 2 | 20 | 100 |
| **Total** | | | **107.5** |

Recovery time: **189.8 s** (20400 events / 107.5 events/s); target 230: **met**

## SoSQS1M4 (Scenario SoS-QS1 (M4))

| Stage | Budget |
|-------|--------|
| RGW | 200 s |
| SoS_K5 | 40 s |
| NCG | 230 s |
| SoS_K32 | 10 s |
| CGW (300 s) ‖ PGW (300 s) ‖ LGW (300 s) ‖ FGW (300 s) | 300 s (maximum, in parallel) |

Composed deadline: **780 s**; target 900: **met**

## SoSQS1M3 (Scenario SoS-QS1 (M3))

| Stage | Budget |
|-------|--------|
| RGW | 30 s |
| SoS_K36 | 10 s |
| NCG | 15 s |

Composed deadline: **55 s**; target 60: **met**
