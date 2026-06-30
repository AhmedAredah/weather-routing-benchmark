#!/usr/bin/env python3
"""summarize_campaign.py — turn a multi-route/multi-season campaign CSV
(plan §17, emitted by tests/test_routing_campaign.cpp) into a savings
DISTRIBUTION: pooled and per-basin / per-season / per-length-class summary
statistics (n, mean, median, p90, min, max) of the weather-routing benefit,
plus an optional histogram + CDF figure for the paper.

Only status==ok rows are aggregated; other statuses are counted and reported so
failures are never silently dropped. "NA" / blank numeric cells are skipped.

Usage (stdlib-only for the table; matplotlib optional, only for --fig):
    python summarize_campaign.py --csv /tmp/campaign_results.csv \
        [--metric benefitPct] [--fig campaign_distribution.png]

Project standard for the optional plotting dep is uv (never conda):
    uv venv --python 3.12 .venv
    uv pip install --python .venv/bin/python matplotlib
    .venv/bin/python summarize_campaign.py --csv /tmp/campaign_results.csv \
        --fig campaign_distribution.png
"""
import argparse
import csv
import math
import statistics
import sys
from collections import defaultdict


def to_float(s):
    """Parse a CSV cell to float, or None for NA/blank/non-numeric."""
    if s is None:
        return None
    s = s.strip()
    if s == "" or s.upper() == "NA":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def combined_benefit(row):
    """The OPERATIONAL weather-routing benefit: the weather-blind path vs the
    BEST weather-aware route the system produces (mesh when enabled, else
    no-mesh), both under real weather on the same corridor. This is the right
    headline: the bare `benefitPct` column is the NO-MESH benefit, which is ~0
    wherever the base HVG corridor offers no lateral alternative — the mesh is
    what supplies that freedom, so the no-mesh column understates by design."""
    cb = to_float(row.get("calmPathRealFuelKg"))
    real = to_float(row.get("realFuelKg"))
    mesh = to_float(row.get("meshFuelKg"))
    if cb is None or cb <= 0.0:
        return None
    # Best feasible weather-aware route: the no-mesh corridor and/or the mesh,
    # whichever the system produced (on severe-storm instances the bare corridor
    # can fail while the mesh still routes, so realFuel may be absent).
    cands = [x for x in (real, mesh) if x is not None]
    if not cands:
        return None
    return 100.0 * (cb - min(cands)) / cb


def combined_speedopt_benefit(row):
    """JOINT route+speed-opt benefit (Phase 3B): the weather-blind FIXED-speed
    baseline vs the best speed-opt route the system produced (bare corridor
    Pareto, mesh Pareto, or — when the multi-speed Pareto search did not
    converge within its expansion budget — the analytical uniform slow-steam
    on the weather-aware route, awareSpeedOptFuelKg). Apples-to-apples with
    combined_benefit: same baseline (calmPathRealFuelKg at the service
    speed); the only change is variable speed under the ETA-slack deadline.
    The analytical fallback is a LOWER BOUND on the true Pareto joint
    saving (Pareto can additionally shape speed per leg), so this metric is
    conservative when Pareto times out. The marginal speed-opt contribution
    is (combined_speedopt_benefit - combined_benefit)."""
    cb = to_float(row.get("calmPathRealFuelKg"))
    so   = to_float(row.get("speedOptFuelKg"))
    meso = to_float(row.get("meshSpeedOptFuelKg"))
    aware = to_float(row.get("awareSpeedOptFuelKg"))
    if cb is None or cb <= 0.0:
        return None
    cands = [x for x in (so, meso, aware) if x is not None]
    if not cands:
        return None
    return 100.0 * (cb - min(cands)) / cb


def slow_steaming_benefit(row):
    """Pure slow-steaming benefit: the weather-blind FIXED-speed baseline vs
    the calm-optimal route sailed with variable speed under the same ETA-
    slack deadline. Isolates the cube-law fuel saving from the env-driven
    route deviation; the marginal env-routing-with-speed contribution is
    (combined_speedopt_benefit - slow_steaming_benefit)."""
    cb  = to_float(row.get("calmPathRealFuelKg"))
    cso = to_float(row.get("calmSpeedOptFuelKg"))
    if cb is None or cb <= 0.0 or cso is None:
        return None
    return 100.0 * (cb - cso) / cb


def value_for(row, metric):
    """Metric value for a row: the derived combined benefit for the special
    metric name 'combined', joint speed+route saving for 'combined_speedopt',
    slow-steaming-only for 'slow_steaming', else the named CSV column."""
    if metric == "combined":
        return combined_benefit(row)
    if metric == "combined_speedopt":
        return combined_speedopt_benefit(row)
    if metric == "slow_steaming":
        return slow_steaming_benefit(row)
    return to_float(row.get(metric))


def percentile(xs, p):
    """Linear-interpolation percentile, p in [0, 100]; xs already finite."""
    if not xs:
        return None
    s = sorted(xs)
    if len(s) == 1:
        return s[0]
    rank = (p / 100.0) * (len(s) - 1)
    lo, hi = math.floor(rank), math.ceil(rank)
    if lo == hi:
        return s[int(rank)]
    return s[lo] + (s[hi] - s[lo]) * (rank - lo)


def stats(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return dict(n=0, mean=None, median=None, p90=None, mn=None, mx=None)
    return dict(n=len(xs), mean=statistics.fmean(xs),
                median=statistics.median(xs), p90=percentile(xs, 90),
                mn=min(xs), mx=max(xs))


def _f(v):
    return "   n/a" if v is None else f"{v:6.2f}"


def print_table(title, groups):
    print(f"\n## {title}")
    print(f"{'group':<16} {'n':>3} {'mean':>6} {'med':>6} {'p90':>6} "
          f"{'max':>6} {'min':>6}")
    print("-" * 58)
    for label, st in groups:
        print(f"{label:<16} {st['n']:>3} {_f(st['mean'])} {_f(st['median'])} "
              f"{_f(st['p90'])} {_f(st['mx'])} {_f(st['mn'])}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default="campaign_results.csv",
                    help="campaign results CSV (default: campaign_results.csv)")
    ap.add_argument("--metric", default="benefitPct",
                    help="column to summarize (default: benefitPct)")
    ap.add_argument("--fig", default=None,
                    help="optional PNG path for the histogram + CDF figure")
    args = ap.parse_args()

    try:
        with open(args.csv, newline="") as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr)
        return 1
    if not rows:
        print("ERROR: CSV has no data rows", file=sys.stderr)
        return 1

    status_counts = defaultdict(int)
    for r in rows:
        status_counts[(r.get("status") or "?").strip()] += 1
    ok = [r for r in rows if (r.get("status") or "").strip() == "ok"]

    print(f"# Campaign summary: {args.csv}")
    print(f"instances: {len(rows)} total; {len(ok)} ok; statuses: "
          + ", ".join(f"{k}={v}" for k, v in sorted(status_counts.items())))

    m = args.metric
    # Derived metrics are computed by value_for() from several columns and are
    # not themselves CSV columns; only validate genuine column metrics.
    DERIVED = {"combined", "combined_speedopt", "slow_steaming"}
    if ok and m not in DERIVED and m not in ok[0]:
        print(f"ERROR: metric column '{m}' not in CSV header", file=sys.stderr)
        return 1

    vals = [value_for(r, m) for r in ok]
    pooled = stats(vals)
    print(f"\nMetric: {m}  (weather-routing benefit, % — higher is better)")
    print_table(f"POOLED ({m})", [("all", pooled)])

    for dim in ("basin", "season", "lengthClass"):
        grp = defaultdict(list)
        for r in ok:
            grp[(r.get(dim) or "?")].append(value_for(r, m))
        print_table(f"by {dim} ({m})",
                    [(k, stats(v)) for k, v in sorted(grp.items())])

    mesh_vals = [to_float(r.get("meshGainPct")) for r in ok]
    if any(x is not None for x in mesh_vals):
        print_table("meshGainPct (mesh-enabled routes)",
                    [("mesh", stats(mesh_vals))])

    # Operational HEADLINE (always): the combined mesh-aware-vs-weather-blind
    # benefit. The bare `benefitPct` column is no-mesh only and reads ~0
    # wherever the base corridor has no lateral freedom; this is the benefit of
    # the route the system actually produces.
    if m != "combined":
        cv = [combined_benefit(r) for r in ok]
        print_table("COMBINED benefit (mesh-aware vs weather-blind)",
                    [("all", stats(cv))])

    # Speed-opt headlines (Phase 3B). Print only when the speed-opt columns
    # are present in the CSV — older fixed-speed-only runs simply skip these.
    if ok and "speedOptFuelKg" in ok[0]:
        if m != "slow_steaming":
            ss = [slow_steaming_benefit(r) for r in ok]
            if any(x is not None for x in ss):
                print_table(
                    "SLOW-STEAMING-only benefit (calm route + variable speed)",
                    [("all", stats(ss))])
        if m != "combined_speedopt":
            csv2 = [combined_speedopt_benefit(r) for r in ok]
            if any(x is not None for x in csv2):
                print_table(
                    "JOINT route+speed-opt benefit (vs weather-blind)",
                    [("all", stats(csv2))])
        # Marginal speed-opt = joint - max(route-only, slow-steaming-only).
        # Positive marginal = env-aware speed choice beats both pure components
        # individually (the cross-term that closed-form decomposition misses).
        marg = []
        for r in ok:
            j = combined_speedopt_benefit(r)
            c = combined_benefit(r)
            s = slow_steaming_benefit(r)
            base = max([x for x in (c, s) if x is not None], default=None)
            if j is not None and base is not None:
                marg.append(j - base)
        if marg:
            print_table("MARGINAL speed-opt over max(route-only,slow-steaming)",
                        [("all", stats(marg))])

    if pooled["n"]:
        print(f"\nHEADLINE: {m} over {pooled['n']} instances — "
              f"mean {pooled['mean']:.2f}%, median {pooled['median']:.2f}%, "
              f"p90 {pooled['p90']:.2f}%, max {pooled['mx']:.2f}%.")
    else:
        print("\n(no ok instances with a numeric metric to summarize)")

    if args.fig:
        clean = [x for x in vals if x is not None]
        if not clean:
            print("(no numeric values to plot)", file=sys.stderr)
            return 0
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("(matplotlib not available — skipping figure; install via "
                  "uv: uv pip install matplotlib)", file=sys.stderr)
            return 0
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.hist(clean, bins=max(5, int(math.sqrt(len(clean))) * 2),
                 color="#3b78c3", edgecolor="black")
        ax1.set_xlabel(f"{m} (%)")
        ax1.set_ylabel("instances")
        ax1.set_title("Weather-routing savings distribution")
        s = sorted(clean)
        cdf = [(i + 1) / len(s) for i in range(len(s))]
        ax2.plot(s, cdf, marker="o", ms=3, color="#c3573b")
        ax2.set_xlabel(f"{m} (%)")
        ax2.set_ylabel("cumulative fraction")
        ax2.set_title("CDF")
        ax2.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(args.fig, dpi=130)
        print(f"figure -> {args.fig}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
