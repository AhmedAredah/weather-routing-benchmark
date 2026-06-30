# Results — data dictionary

Each `results_<vessel>_<objective>.csv` holds **96 rows**, one per voyage instance
(12 routes × 4 seasons × 2 years). Fuel is in kilograms; CO₂ follows by the
fuel's carbon factor (HFO C_F = 3.12 g CO₂ / g fuel). `NA` = not applicable /
not produced for that instance (e.g. mesh columns on a mesh-off route).

| # | Column | Units | Meaning |
|---|--------|-------|---------|
| 1 | `route` | — | Route name, e.g. `NewYork->Colon` |
| 2 | `basin` | — | Ocean basin label |
| 3 | `lengthClass` | — | `coastal` / `regional` / `basin` / `ocean` |
| 4 | `date` | ISO date | Departure date (mid-season representative) |
| 5 | `season` | — | `DJF` / `MAM` / `JJA` / `SON` |
| 6 | `year` | — | 2022 or 2023 |
| 7 | `distKm` | km | Great-circle / corridor distance |
| 8 | `speedMps` | m/s | Service speed (fixed-speed runs); 6.0 m/s |
| 9 | `geoFuelKg` | kg | Fuel on the geodesic path, calm-water reference |
| 10 | `gcFuelKg` | kg | Fuel on the great-circle path under real weather |
| 11 | `calmPathRealFuelKg` | kg | **Baseline**: calm-optimal (weather-blind) route scored under real weather |
| 12 | `realFuelKg` | kg | Weather-aware HVG-corridor route, fixed speed |
| 13 | `benefitKg` | kg | `calmPathRealFuelKg − realFuelKg` |
| 14 | `benefitPct` | % | Route-only saving from the corridor route |
| 15 | `meshFuelKg` | kg | Weather-aware route with the lateral ocean mesh, fixed speed |
| 16 | `meshGainPct` | % | Saving from the mesh route vs. baseline |
| 17 | `currentEffectPct` | % | Modelled effect of surface currents on fuel (where evaluated) |
| 18 | `wps` | count | Number of waypoints in the returned route (search scale) |
| 19 | `fetchS` | s | Wall-clock to fetch/prepare the ERA5 field (not the router) |
| 20 | `routeS` | s | **Router solve time** (the weather-aware search) |
| 21 | `status` | — | `ok` if the instance was computed; otherwise an infeasibility tag |
| 22 | `speedOptFuelKg` | kg | Speed-optimized schedule on the corridor route |
| 23 | `speedOptDurationH` | h | Duration of that schedule |
| 24 | `speedOptMeanMps` | m/s | Distance-weighted mean speed of that schedule |
| 25 | `meshSpeedOptFuelKg` | kg | Speed-optimized schedule on the mesh route |
| 26 | `meshSpeedOptDurationH` | h | Duration |
| 27 | `meshSpeedOptMeanMps` | m/s | Mean speed |
| 28 | `calmSpeedOptFuelKg` | kg | Speed-optimized schedule on the calm/baseline path |
| 29 | `awareSpeedOptFuelKg` | kg | Speed-optimized schedule on the weather-aware route |
| 30 | `etaSlack` | fraction | ETA slack allowed for speed optimization (0.05 = 5 %) |
| 31 | `speedSet` | m/s | Discrete speed buckets, e.g. `5.0\|5.5\|6.0\|6.5\|7.0` |
| 32 | `speedOptCostUSD` | USD | Voyage cost of the corridor speed-optimized schedule |
| 33 | `meshSpeedOptCostUSD` | USD | Voyage cost, mesh speed-optimized |
| 34 | `calmSpeedOptCostUSD` | USD | Voyage cost, calm/baseline speed-optimized |
| 35 | `awareSpeedOptCostUSD` | USD | Voyage cost, weather-aware speed-optimized |

## Derived headline metrics

Computed exactly as in [`../scripts/summarize_campaign.py`](../scripts/summarize_campaign.py):

- **Route-only saving (%)** = `100 × (calmPathRealFuelKg − min(realFuelKg, meshFuelKg)) / calmPathRealFuelKg`
- **Joint route+speed saving (%)** = `100 × (calmPathRealFuelKg − min(speedOptFuelKg, meshSpeedOptFuelKg, awareSpeedOptFuelKg)) / calmPathRealFuelKg`

Only `status == ok` rows enter the statistics; instances whose weather-blind
baseline is itself infeasible (storm exceeds engine/seakeeping limits) carry no
defined percentage and are excluded — see [`SUMMARY.md`](SUMMARY.md).

## Objectives

- `*_minfuel.csv` — search minimizes **fuel mass**.
- `*_mincost.csv` — search minimizes **voyage cost** with MARPOL Annex VI
  emission-control-area (ECA) fuel switching active; outside-vs-inside-ECA fuel
  price differences make the cost-optimal route diverge from the fuel-optimal one
  on the ECA-affected lanes.
