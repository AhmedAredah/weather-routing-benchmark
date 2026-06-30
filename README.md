# Weather-Routing Benchmark

**A multi-basin, multi-vessel, instance-matched benchmark for ship weather-routing and speed-optimization research.**

[![License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21052776.svg)](https://doi.org/10.5281/zenodo.21052776)
[![Paper](https://img.shields.io/badge/Paper-under%20review-orange.svg)](#citation)

---

## Why this benchmark exists

Reported fuel and CO₂ savings from ship weather routing span an enormous range
(≈1–49 %) across the literature, yet **no two studies measure them on a common
footing** — baselines, vessels, routes, weather years, and reporting statistics
all differ. Surveys of the field have explicitly called for *standardized
benchmark instances to facilitate comparison between methods*
(Zis et al., 2020, *Ocean Engineering*).

This repository provides exactly that: a **fixed, openly documented instance
set** — 12 routes spanning every major ocean basin, crossed with four seasons
and two years (96 voyage instances), run on three standard benchmark hulls under
identical real ERA5 weather against a **single well-defined weather-blind
baseline**. Every result is priced from a **first-principles** naval-architecture
model (not a vessel-specific performance curve), so the savings are reproducible
from published hull and engine particulars and transfer across vessels.

Use it to **place a new router on a shared scale**: score your route through the
same physics, or compare your savings against the same baseline on the same
instances.

---

## At a glance

| | |
|---|---|
| **Routes** | 12 (coastal → ocean-crossing), every major basin |
| **Seasons × years** | DJF / MAM / JJA / SON × 2022, 2023 |
| **Instances per vessel** | 96 (12 × 4 × 2) |
| **Vessels** | S175 containership, KVLCC2 VLCC tanker, JBC capesize bulk carrier (Cᵦ 0.57 → 0.86) |
| **Objectives** | minimum fuel, minimum voyage cost (ECA fuel-switching) |
| **Weather** | ECMWF ERA5 reanalysis (10 m wind 0.25°, waves 0.5°, hourly) |
| **Baseline** | weather-blind (calm-optimal) route scored under the same real weather |
| **Total instances** | 96 × 3 vessels × 2 objectives = 576 priced voyages |

---

## Repository layout

```
weather-routing-benchmark/
├── routes/
│   ├── campaign_routes.csv      # the 12-route manifest (ports, coords, AOI, mesh params)
│   └── README.md                # human-readable route table
├── vessels/
│   ├── s175_containership.dat   # hull + engine + propeller particulars
│   ├── kvlcc2_tanker.dat
│   ├── jbc_bulkcarrier.dat
│   └── README.md                # particulars table + format notes
├── results/
│   ├── results_<vessel>_minfuel.csv   # 96 instances, minimum-fuel objective
│   ├── results_<vessel>_mincost.csv   # 96 instances, minimum-cost objective (ECA)
│   ├── DATA_DICTIONARY.md             # every column defined
│   └── SUMMARY.md                     # headline numbers (reproducible from the CSVs)
├── tracks/
│   ├── *_tracks.csv             # per-instance route geometry (lon/lat waypoints)
│   ├── *_hs.csv                 # significant-wave-height field along the route
│   ├── *_profile.csv            # speed / power / fuel profile along an exemplar voyage
│   └── README.md
└── scripts/
    └── summarize_campaign.py    # canonical metric definitions; regenerates SUMMARY.md
```

---

## The instance set

Each **instance** is a (route × seasonal date × year) triple. The four seasonal
dates are mid-season representatives (15 Jan / 15 Apr / 15 Jul / 15 Oct), crossed
with 2022 and 2023. The 12 routes (`routes/campaign_routes.csv`):

| # | Route | Basin | Class | ~Distance |
|---|-------|-------|-------|-----------|
| 1 | Antwerpen → Zeebrugge | North Sea | coastal | 85 km |
| 2 | Santos → Paranaguá | S. Atlantic | coastal | 285 km |
| 3 | New York → Boston | NW Atlantic | coastal | 404 km |
| 4 | Brisbane → Newcastle | Tasman | regional | 693 km |
| 5 | Rotterdam → Algeciras | NE Atlantic | regional | 2 489 km |
| 6 | New York → Colón | NW Atlantic | basin | 3 686 km |
| 7 | Colombo → Jeddah | Indian | basin | 5 228 km |
| 8 | Singapore → Busan | W. Pacific | basin | 4 673 km |
| 9 | Rotterdam → New York | N. Atlantic | ocean | 6 247 km |
| 10 | Santos → Cape Town | S. Atlantic | ocean | 6 994 km |
| 11 | Cape Town → Mumbai | Indian | ocean | ~7 000 km |
| 12 | Yokohama → Long Beach | N. Pacific | ocean | 10 065 km |

Vessels (full particulars in `vessels/`):

| Vessel | Type | L_pp | Beam | Draft | Cᵦ | MCR |
|--------|------|------|------|-------|----|-----|
| **S175** | containership | 175 m | 25.4 m | 9.5 m | 0.572 | 14.85 MW |
| **KVLCC2** | VLCC tanker | 320 m | 58.0 m | 20.8 m | 0.810 | 30.0 MW |
| **JBC** | capesize bulk carrier | 280 m | 45.0 m | 16.5 m | 0.858 | 16.5 MW |

---

## Baseline and metrics

The benchmark is built around **one** fixed baseline so that savings are
comparable across methods:

- **Weather-blind baseline** — the calm-water-optimal (least-fuel-at-service-speed)
  route, scored under the *same* real ERA5 weather it would actually meet. This is
  the route a router that ignores weather would sail.

Two headline savings are reported against it (definitions in
[`scripts/summarize_campaign.py`](scripts/summarize_campaign.py)):

- **Route-only saving** — fuel saved by deviating the *track* around weather at the
  fixed service speed:
  `100 × (baseline − min(weather-aware, mesh)) / baseline`.
- **Joint route + speed saving** — additionally optimizing the per-leg speed
  schedule under a 5 % ETA slack:
  `100 × (baseline − min(speed-optimized variants)) / baseline`.

Instances whose weather-blind baseline is itself physically infeasible (engine
MCR or seakeeping limit exceeded in the storm) carry no defined percentage and
are held out of the saving statistics — a documented, deliberate part of the
design (see `results/SUMMARY.md`).

---

## Headline results

Weather-routing fuel/CO₂ saving vs. the weather-blind baseline
(percentages; `status==ok` instances). Full breakdown in
[`results/SUMMARY.md`](results/SUMMARY.md).

| Vessel | metric | n | mean | median | p90 | max |
|--------|--------|---|------|--------|-----|-----|
| S175   | route-only        | 91 | 5.04 | 1.91 | 14.58 | 39.82 |
| S175   | joint route+speed | 91 | 11.01 | 8.82 | 19.75 | 45.56 |
| KVLCC2 | route-only        | 67 | 6.14 | 3.91 | 16.07 | 26.25 |
| KVLCC2 | joint route+speed | 66 | 10.95 | 10.00 | 20.21 | 29.69 |
| JBC    | route-only        | 66 | 4.55 | 1.82 | 15.09 | 26.81 |
| JBC    | joint route+speed | 65 | 9.57 | 7.82 | 17.30 | 30.33 |

**Scale / runtime** (S175, min-fuel): the search visits 17–1003 waypoints per
instance and solves in a median **183 s** per route (mean 335 s, range 39 s –
24 min) on a commodity workstation — provided so methods can be compared on
runtime as well as savings.

---

## How to use it

**Compare a new router on a common footing:**

1. Take the 12 routes and the (season × year) dates from `routes/campaign_routes.csv`.
2. Run your router on the same instances with the same vessels (`vessels/`).
3. Either (a) report your savings against the **same weather-blind baseline** the
   results CSVs already contain, or (b) export your chosen tracks and score them
   through an identical physics model for a track-only comparison.
4. Use the metric definitions in `scripts/summarize_campaign.py` verbatim so the
   numbers line up.

**Reuse the priced results directly:** `results/*.csv` give per-instance fuel,
cost, duration, mean speed, and runtime for the baseline, weather-aware,
lateral-mesh, and speed-optimized variants under both objectives — ready for
secondary analysis (intensity, abatement, sensitivity, fleet scaling).

---

## Provenance and reproduction

- **Generated by** the open-source **ShipNetSim** maritime simulator
  (<https://github.com/VTTI-CSM/ShipNetSim>) using a first-principles vessel
  model: Holtrop–Mennen calm-water resistance, Lang–Mao spectral added
  resistance, Fujiwara wind resistance, a Wageningen B-series propeller operating
  point, and a load-dependent specific-fuel-consumption map, with in-search engine
  (MCR), IMO MSC.1/Circ.1228 seakeeping, under-keel-clearance, and current-triangle
  feasibility gates.
- **Metocean inputs:** ECMWF ERA5 reanalysis (Copernicus Climate Data Store
  `reanalysis-era5-single-levels`; 10 m winds on the 0.25° grid, significant wave
  height and mean wave period on the 0.5° grid, hourly); bathymetry from GMRT;
  coastlines from Natural Earth. The min-cost objective additionally uses 2024
  Ship & Bunker bunker prices.
- The raw metocean fields are **not** redistributed here (they are freely
  available from the sources above); this repository contains the routing
  instances, vessel definitions, priced results, and exemplar tracks.

---

## Citation

If you use this benchmark, please cite the accompanying paper and this dataset.

> Aredah, A. and Rakha, H. A. (2026). *Energy- and emission-optimal ship routing
> from a first-principles vessel model under real metocean conditions.* (Under
> review.)

A machine-readable citation is in [`CITATION.cff`](CITATION.cff). This dataset is
permanently archived on Zenodo with the concept DOI
[**10.5281/zenodo.21052776**](https://doi.org/10.5281/zenodo.21052776) (always
resolves to the latest version):

> Aredah, A. and Rakha, H. A. (2026). *Weather-Routing Benchmark: a multi-basin,
> multi-vessel instance set for ship weather-routing and speed-optimization
> research* (v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.21052776

---

## License

- **Data** (routes, vessels, results, tracks): [Creative Commons Attribution 4.0
  International (CC BY 4.0)](LICENSE).
- **Scripts** (`scripts/`): same license; reuse freely with attribution.

You are free to share and adapt the material for any purpose, including
commercially, provided you give appropriate credit.

---

## Contact

Ahmed Aredah · Texas A&M Transportation Institute / Virginia Tech ·
`ahmed.aredah@gmail.com`
