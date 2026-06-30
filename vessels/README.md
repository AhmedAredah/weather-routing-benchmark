# Vessels

Three standard benchmark hulls spanning the merchant-fleet block-coefficient
range, so that savings can be shown to be a property of the weather and route
rather than of a single vessel.

| File | Vessel | Type | L_pp | Beam | Draft | Displacement | Cᵦ | MCR | Propeller |
|------|--------|------|------|------|-------|--------------|----|-----|-----------|
| `s175_containership.dat` | **S175** | containership | 175 m | 25.4 m | 9.5 m | 24 053 m³ | 0.572 | 14.85 MW | D 5.0 m, P/D 0.95, Z 5 |
| `kvlcc2_tanker.dat` | **KVLCC2** | VLCC tanker | 320 m | 58.0 m | 20.8 m | 312 621 m³ | 0.810 | 30.0 MW | D 9.86 m, P/D 0.72, Z 4 |
| `jbc_bulkcarrier.dat` | **JBC** | capesize bulk carrier | 280 m | 45.0 m | 16.5 m | 178 370 m³ | 0.858 | 16.5 MW | D 8.12 m, P/D 0.75, Z 5 |

- **S175** — the standard ITTC/SR-108 container-ship hull form.
- **KVLCC2** — the MOERI/KRISO VLCC, a SIMMAN manoeuvring/CFD benchmark hull.
- **JBC** (Japan Bulk Carrier) — the NMRI Tokyo-2015 CFD-workshop capesize hull.

The tanker and bulk-carrier machinery ratings are class-representative two-stroke
engines, and their load-dependent specific-fuel-consumption shape is scaled from
the S175 reference; the hull and propeller geometry are from the published
benchmark definitions.

## File format (`.dat`)

A tab-separated ShipNetSim vessel record. The two leading `#` lines are the
header legend; the data line carries, in order: an ID and a placeholder path;
maximum speed (knots); waterline and between-perpendiculars length; beam;
fore/aft draft; displacement (m³); above-waterline and frontal areas; block,
midship, waterplane and prismatic coefficients; fuel-tank specification; the
engine power–RPM–efficiency curve (Tier II / Tier III); gearbox and shaft
efficiencies; and the propeller particulars (diameter, pitch ratio, blade count,
expanded-area ratio). See the ShipNetSim documentation
(<https://github.com/VTTI-CSM/ShipNetSim>) for the full field specification.
