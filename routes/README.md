# Routes

`campaign_routes.csv` is the canonical 12-route manifest. The benchmark driver
crosses each route with the four seasonal dates (15 Jan / 15 Apr / 15 Jul /
15 Oct) and both years (2022, 2023) to form the 96-instance set per vessel.

## Columns

```
name, basin, lengthClass,
startLon, startLat, goalLon, goalLat,   # endpoints (decimal degrees)
speedMps,                               # service speed (6.0 m/s)
minLon, maxLon, minLat, maxLat,         # ERA5 area-of-interest bbox, or "auto"
useMesh,                                # 1 = lateral ocean mesh enabled
[meshSpacingKm, meshHalfWidthKm]        # optional; defaults 40 km / 400 km
```

- **`auto` bbox** — the area of interest is derived from the great-circle path
  plus the mesh half-width, so the fetched ERA5 grid always covers the route
  including its high-latitude apex and the mesh's lateral detour room. All four
  ocean-crossings use `auto`.
- **Antimeridian** — a row whose `minLon > maxLon` signals a bbox that wraps
  across the dateline (e.g. Yokohama → Long Beach); the field is fetched in two
  halves and merged onto a continuous 0–360° axis.
- **Mesh parameters** — the four ocean-crossings (rows 9–12) use coarser mesh
  spacing (80 km) and a wider half-width (1000 km) to keep a 6000–9000 km corridor
  tractable; a convergence study shows 80 km spacing is within 0.006 % of 40 km
  and the half-width saturates near 1000 km. Coastal/basin rows use the 40 km /
  200–400 km defaults.

## Route table

| # | Route | Basin | Class | Start (lon, lat) | Goal (lon, lat) | Mesh |
|---|-------|-------|-------|------------------|-----------------|------|
| 1 | Antwerpen → Zeebrugge | North Sea | coastal | 4.40, 51.22 | 3.20, 51.33 | off |
| 2 | Santos → Paranaguá | S. Atlantic | coastal | −46.31, −23.96 | −48.51, −25.50 | on |
| 3 | New York → Boston | NW Atlantic | coastal | −74.01, 40.71 | −71.06, 42.36 | on |
| 4 | Brisbane → Newcastle | Tasman | regional | 153.03, −27.47 | 151.78, −32.93 | off |
| 5 | Rotterdam → Algeciras | NE Atlantic | regional | 4.48, 51.92 | −5.45, 36.14 | on |
| 6 | New York → Colón | NW Atlantic | basin | −74.01, 40.71 | −79.91, 9.35 | on |
| 7 | Colombo → Jeddah | Indian | basin | 79.85, 6.93 | 39.17, 21.49 | on |
| 8 | Singapore → Busan | W. Pacific | basin | 103.82, 1.35 | 129.08, 35.18 | on |
| 9 | Rotterdam → New York | N. Atlantic | ocean | 4.48, 51.92 | −74.01, 40.71 | on |
| 10 | Santos → Cape Town | S. Atlantic | ocean | −46.31, −23.96 | 18.42, −33.92 | on |
| 11 | Cape Town → Mumbai | Indian | ocean | 18.42, −33.92 | 72.88, 19.08 | on |
| 12 | Yokohama → Long Beach | N. Pacific | ocean | 139.64, 35.44 | −118.19, 33.77 | on |
