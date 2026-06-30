# Scripts

## `summarize_campaign.py`

The canonical metric definitions for the benchmark. It computes the route-only
and joint route+speed savings from a results CSV and prints pooled, per-basin and
per-season statistics. Reuse it verbatim so your numbers are defined identically
to ours.

### Reproduce the headline numbers

```bash
# route-only saving (S175): n=91, mean 5.04, median 1.91, p90 14.58, max 39.82
python3 scripts/summarize_campaign.py --csv results/results_s175_minfuel.csv --metric combined

# joint route+speed saving (S175): n=91, mean 11.01, median 8.82, max 45.56
python3 scripts/summarize_campaign.py --csv results/results_s175_minfuel.csv --metric combined_speedopt

# repeat for results/results_{kvlcc2,jbc}_minfuel.csv
```

Useful `--metric` values: `combined` (route-only), `combined_speedopt` (joint
route+speed), `slow_steaming` (cube-law speed component), or any raw CSV column
(e.g. `benefitPct`, `meshGainPct`). Only `status == ok` rows are counted; the
script is pure Python 3 (standard library) and needs no dependencies.
