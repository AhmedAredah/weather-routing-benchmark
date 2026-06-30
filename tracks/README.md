# Per-instance tracks and profiles

Exemplar voyage geometry behind the figures in the accompanying paper, provided
so others can overlay, re-plot, or re-score the routes. Three instance types are
included.

## Route tracks — `*_tracks.csv`

The competing routes for an instance, as ordered waypoints.

| Column | Meaning |
|--------|---------|
| `series` | which route: `blind` (weather-blind baseline), `aware`/`mesh` (weather-aware), `gc` (great circle) |
| `idx` | waypoint index along the series |
| `lon`, `lat` | waypoint position (decimal degrees) |

Instances: `NewYork_Colon_2022-01-15` (max-saving winter crossing),
`Rotterdam_NewYork_2023-04-15`, `Santos_CapeTown_2023-04-15`.

## Significant-wave-height fields — `*_hs.csv`

The ERA5 significant-wave-height field sampled over the instance's area of
interest, for the mid-voyage time, to shade the route maps.

| Column | Meaning |
|--------|---------|
| `lon`, `lat` | grid-cell centre (decimal degrees) |
| `hs` | significant wave height (m) |

## Powering profiles — `*_profile.csv`

Leg-by-leg state along the Yokohama → Long Beach spring crossing (the campaign's
max-saving instance), one file per regime: `blind`, `aware`, `mesh`, `geo`
(great circle), `speedopt` (speed-optimized schedule), and `speedopt_pareto`.

| Column | Units | Meaning |
|--------|-------|---------|
| `leg` | — | leg index |
| `cum_dist_km` | km | cumulative distance from origin |
| `lon`, `lat` | deg | position |
| `Hs_m` | m | significant wave height encountered |
| `wind_mps` | m/s | wind speed |
| `curr_mps` | m/s | surface current speed |
| `V_service_mps` | m/s | service (commanded) speed-through-water |
| `V_achievable_mps` | m/s | speed achievable under the engine/seakeeping limits |
| `SOG_mps` | m/s | speed over ground |
| `brakePower_kW` | kW | required engine brake power |
| `feasible` | 0/1 | whether the leg is within all feasibility limits |
