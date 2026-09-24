
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.io_data import read_grid_load, read_model_inputs
from src.drivers import build_calendar
from src.pv_model import synthetic_pv
from src.simulation import simulate_consumers
from src.assumptions import PV_ANNUAL_KWH, GRID_CONNECTION_LIMIT_KW


BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)


def main() -> None:
    grid = read_grid_load(DATA / "netzbezug_2025.xlsx")
    cfg = read_model_inputs(DATA / "energiesystem_input.xlsx")

    # The measured file defines the authoritative 15-minute timeline.
    calendar = build_calendar(pd.DatetimeIndex(grid["timestamp_local"]), cfg["daily"])
    calendar.index = grid.index

    pv = synthetic_pv(pd.DatetimeIndex(grid["timestamp_local"]))
    pv.index = grid.index
    consumer_df, group_df = simulate_consumers(
        calendar=calendar,
        groups=cfg["groups"],
        consumers=cfg["consumers"],
        schedules=cfg["schedules"],
    )

    result = group_df.copy()
    result["p_pv_model_kw"] = pv
    result["p_grid_model_kw"] = np.clip(
        result["p_consumption_model_kw"] - result["p_pv_model_kw"], 0.0, None
    )
    result["p_grid_measured_kw"] = grid["p_grid_kw"]
    result["timestamp_local"] = grid["timestamp_local"].to_numpy()

    result.to_csv(RESULTS / "timeseries_15min.csv", sep=";", decimal=",", index_label="timestamp")

    dt_h = 0.25
    kpis = pd.DataFrame(
        {
            "value": {
                "measured_grid_energy_kwh": float(result["p_grid_measured_kw"].sum() * dt_h),
                "measured_grid_peak_kw": float(result["p_grid_measured_kw"].max()),
                "measured_grid_mean_kw": float(result["p_grid_measured_kw"].mean()),
                "pv_assumption_energy_kwh": float(result["p_pv_model_kw"].sum() * dt_h),
                "pv_assumption_target_kwh": float(PV_ANNUAL_KWH),
                "model_consumption_energy_kwh": float(result["p_consumption_model_kw"].sum() * dt_h),
                "model_grid_energy_kwh": float(result["p_grid_model_kw"].sum() * dt_h),
                "model_grid_peak_kw": float(result["p_grid_model_kw"].max()),
                "grid_limit_kw": float(GRID_CONNECTION_LIMIT_KW),
                "measured_quarters_over_75kw": int((result["p_grid_measured_kw"] > GRID_CONNECTION_LIMIT_KW).sum()),
            }
        }
    )
    kpis.to_csv(RESULTS / "kpis.csv", sep=";", decimal=",")

    # Group annual energy table
    group_cols = [c for c in group_df.columns if c.startswith("VG_")]
    group_energy = (group_df[group_cols].sum() * dt_h).sort_values(ascending=False)
    group_energy.rename("energy_kwh").to_csv(RESULTS / "group_energy_kwh.csv", sep=";", decimal=",")

    # Plot 1: measured grid vs first-pass model, one representative week.
    start = pd.Timestamp("2025-01-06")
    end = start + pd.Timedelta(days=7)
    sl = result.loc[start:end]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(sl.index, sl["p_grid_measured_kw"], label="Netzbezug gemessen", linewidth=1.4)
    ax.plot(sl.index, sl["p_grid_model_kw"], label="Netzbezug Modell v1", linewidth=1.2)
    ax.set_ylabel("Leistung [kW]")
    ax.set_title("Erster Modelllauf – Beispielwoche Januar")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS / "01_beispielwoche_januar.png", dpi=160)
    plt.close(fig)

    # Plot 2: group stack for one day.
    day = pd.Timestamp("2025-01-08")
    day_df = group_df.loc[day:day + pd.Timedelta(hours=23, minutes=45), group_cols]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.stackplot(day_df.index, [day_df[c].values for c in group_cols], labels=group_cols)
    ax.set_ylabel("Leistung [kW]")
    ax.set_title("Modellierte Verbrauchergruppen – Beispieltagesgang")
    ax.legend(loc="upper left", ncol=3, fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTS / "02_gruppen_beispieltag.png", dpi=160)
    plt.close(fig)

    # Plot 3: annual load duration curves.
    fig, ax = plt.subplots(figsize=(9, 5))
    measured = np.sort(result["p_grid_measured_kw"].to_numpy())[::-1]
    modeled = np.sort(result["p_grid_model_kw"].to_numpy())[::-1]
    x = np.arange(len(measured)) / len(measured) * 100
    ax.plot(x, measured, label="Netzbezug gemessen")
    ax.plot(x, modeled, label="Netzbezug Modell v1")
    ax.axhline(GRID_CONNECTION_LIMIT_KW, linestyle="--", linewidth=1, label="Netzgrenze 75 kW")
    ax.set_xlabel("Anteil der Jahresviertelstunden [%]")
    ax.set_ylabel("Leistung [kW]")
    ax.set_title("Jahresdauerlinie")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS / "03_jahresdauerlinie.png", dpi=160)
    plt.close(fig)

    print("MVP erfolgreich berechnet.")
    print(kpis.round(2).to_string())
    print("\nJahresenergie nach Verbrauchergruppe [kWh]:")
    print(group_energy.round(0).to_string())


if __name__ == "__main__":
    main()
