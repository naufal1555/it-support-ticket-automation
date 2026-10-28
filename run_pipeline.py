"""Master pipeline orchestrator for IT Support Ticket Automation.
Author: Ahmad Fathin Naufal (UGM) - System Developer
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from simulation.generate_tickets_dataset import (
    ITSMTicketSimulator,
    USERS_28,
    SPECIALISTS,
)


def run():
    print("=" * 75)
    print("IT SUPPORT TICKET LIFECYCLE AUTOMATION PIPELINE")
    print("Author: Ahmad Fathin Naufal | Candidate: System Developer (UGM)")
    print("=" * 75)

    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("outputs/figures", exist_ok=True)

    simulator = ITSMTicketSimulator(seed=42)
    df_tickets, df_logs = simulator.generate_tickets()

    # Save CSVs
    df_tickets.to_csv("data/processed/it_tickets_200.csv", index=False)
    df_logs.to_csv("data/processed/ticket_activity_log.csv", index=False)

    df_users = pd.DataFrame(
        USERS_28, columns=["UserID", "Name", "Email", "Department"]
    )
    df_users.to_csv("data/processed/user_directory.csv", index=False)

    df_specs = pd.DataFrame(
        SPECIALISTS, columns=["SpecialistID", "Name", "Email", "Domain"]
    )
    df_specs.to_csv("data/processed/it_specialists.csv", index=False)

    total_tickets = len(df_tickets)
    sla_adherence = (1.0 - df_tickets["SLABreached"].mean()) * 100.0
    mttr = df_tickets["ResolutionTimeHours"].mean()
    avg_csat = df_tickets["CSATScore"].mean()

    print("\n" + "=" * 60)
    print("ITSM OPERATIONAL BENCHMARK VERIFICATION")
    print("=" * 60)
    print(f"Total Users Deployed           : {len(df_users)} (Target >= 25)")
    print(f"Total Tickets Processed        : {total_tickets} (Target >= 200)")
    print(f"SLA Adherence Compliance Rate  : {sla_adherence:.1f}%")
    print(f"Mean Time To Resolution (MTTR) : {mttr:.1f} hours")
    print(f"Customer Satisfaction (CSAT)   : {avg_csat:.2f} / 5.00")
    print("=" * 60 + "\n")

    plot_itsm_kpis(df_tickets)


def plot_itsm_kpis(df: pd.DataFrame):
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Volume by Category
    cat_counts = df["Category"].value_counts()
    axes[0, 0].barh(cat_counts.index, cat_counts.values, color="#00ADB5")
    axes[0, 0].set_title(
        "Ticket Volume by ITSM Domain", fontweight="bold", fontsize=11
    )
    axes[0, 0].set_xlabel("Ticket Count")

    # 2. Priority Breakdown
    pri_counts = df["Priority"].value_counts()
    axes[0, 1].pie(
        pri_counts.values,
        labels=pri_counts.index,
        autopct="%1.1f%%",
        colors=["#393E46", "#00ADB5", "#222831", "#EEEEEE"],
    )
    axes[0, 1].set_title(
        "Priority Tier Distribution", fontweight="bold", fontsize=11
    )

    # 3. MTTR by Priority
    mttr_by_pri = df.groupby("Priority")["ResolutionTimeHours"].mean()
    axes[1, 0].bar(mttr_by_pri.index, mttr_by_pri.values, color="#393E46")
    axes[1, 0].set_title(
        "Mean Time To Resolution (MTTR) by Priority",
        fontweight="bold",
        fontsize=11,
    )
    axes[1, 0].set_ylabel("Hours")
    axes[1, 0].tick_params(axis="x", rotation=15)

    # 4. CSAT Distribution
    csat_counts = df["CSATScore"].value_counts().sort_index()
    axes[1, 1].bar(
        [str(x) for x in csat_counts.index],
        csat_counts.values,
        color="#4ECCA3",
    )
    axes[1, 1].set_title(
        "CSAT Rating Distribution (1-5)", fontweight="bold", fontsize=11
    )
    axes[1, 1].set_xlabel("CSAT Stars")
    axes[1, 1].set_ylabel("Count")

    plt.tight_layout()
    plt.savefig(
        "outputs/figures/itsm_performance_dashboard.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


if __name__ == "__main__":
    run()
