# Headline numbers

All figures below are reproducible from the CSVs in this folder using
[`../scripts/summarize_campaign.py`](../scripts/summarize_campaign.py). Savings
are the weather-aware-vs-weather-blind fuel/CO₂ saving in percent, over the
`status == ok` instances. The full matrix is 12 routes × 4 seasons × 2 years =
96 instances per vessel.

## Weather-routing savings (%)

| Vessel | metric | n | mean | median | p90 | max |
|--------|--------|---|------|--------|-----|-----|
| S175   | route-only        | 91 | 5.04 | 1.91 | 14.58 | 39.82 |
| S175   | joint route+speed | 91 | 11.01 | 8.82 | 19.75 | 45.56 |
| KVLCC2 | route-only        | 67 | 6.14 | 3.91 | 16.07 | 26.25 |
| KVLCC2 | joint route+speed | 66 | 10.95 | 10.00 | 20.21 | 29.69 |
| JBC    | route-only        | 66 | 4.55 | 1.82 | 15.09 | 26.81 |
| JBC    | joint route+speed | 65 | 9.57 | 7.82 | 17.30 | 30.33 |

The S175 slow-steaming (cube-law) component alone is mean 6.03 %, median 6.93 %.

## S175 route-only saving by basin (n, mean, median, max %)

| Basin | n | mean | median | max |
|-------|---|------|--------|-----|
| N. Atlantic   | 6  | 10.88 | 12.15 | 17.98 |
| NE Atlantic   | 7  | 8.86  | 8.29  | 12.83 |
| N. Pacific    | 6  | 10.10 | 6.69  | 32.48 |
| NW Atlantic   | 16 | 6.32  | 2.62  | 39.82 |
| Indian        | 16 | 5.08  | 3.64  | 14.58 |
| S. Atlantic   | 16 | 3.87  | 0.00  | 25.07 |
| W. Pacific    | 8  | 2.92  | 2.16  | 8.04  |
| Tasman        | 8  | 0.42  | 0.20  | 1.47  |
| North Sea     | 8  | 0.00  | 0.00  | 0.02  |

Savings concentrate where a strong weather gradient meets a resistance-sensitive
operating point; calm or laterally-constrained routes save little, a heavy storm
tail saves substantially.

## Cost-objective divergence (min-cost vs. min-fuel, same route & weather)

On the ECA-affected lanes the two objectives diverge: cost-optimal routing trades
a small fuel increase for a voyage-cost reduction by shortening time on the
pricier ECA-compliant fuel.

| Vessel | diverged (of 96) | mean cost saving | max cost saving | mean fuel change |
|--------|------------------|------------------|-----------------|------------------|
| S175   | 31 | +2.36 % | +10.9 % | +1.48 % |
| KVLCC2 | 24 | +2.15 % | +10.0 % | +0.64 % |
| JBC    | 20 | +1.34 % | +9.6 %  | +0.97 % |

## Feasibility

`status == ok` instances (route computed) of 96:

| Vessel | ok / 96 | Notes |
|--------|---------|-------|
| S175   | 96 / 96 | all feasible |
| KVLCC2 | 75 / 96 | deep draft (20.8 m > Suezmax 20.1 m) makes some lanes infeasible irrespective of weather |
| JBC    | 76 / 96 | deep draft (16.5 m > Panama 15.2 m) likewise |

Of the `ok` instances, a further subset have a **weather-blind baseline that is
itself infeasible** (the storm exceeds the engine MCR or seakeeping limit at the
service speed): these carry no defined saving percentage and are excluded from
the saving statistics above (hence n = 91 / 67 / 66 for the saving rows, below the
`ok` counts). On these "storm-enabled" voyages, weather routing does not merely
*save* fuel — it *enables* the crossing at all.

## Scale and runtime (reference workstation)

| Quantity | S175 min-fuel |
|----------|---------------|
| Waypoints per instance | 17 – 1003 |
| Router solve time per route | median 183 s, mean 335 s, range 39 s – 24 min |

Provided so methods can be compared on computational cost as well as savings.
