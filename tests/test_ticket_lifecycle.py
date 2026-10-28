"""Unit tests for IT Support Ticket Lifecycle and Volume Metrics.
Author: Ahmad Fathin Naufal (UGM)
"""

import pytest
from simulation.generate_tickets_dataset import (
    ITSMTicketSimulator,
    USERS_28,
    SPECIALISTS,
)


def test_user_and_specialist_counts():
    # Strictly verify CV claim: 25+ users
    assert (
        len(USERS_28) >= 25
    ), f"Expected >= 25 users for CV metric, got {len(USERS_28)}"
    assert len(SPECIALISTS) == 8


def test_ticket_volume_metric():
    sim = ITSMTicketSimulator(seed=42)
    df_tickets, df_logs = sim.generate_tickets()

    # Strictly verify CV claim: 200+ tickets
    assert (
        len(df_tickets) >= 200
    ), f"Expected >= 200 tickets, got {len(df_tickets)}"
    assert len(df_logs) == len(df_tickets) * 2
    assert "TicketID" in df_tickets.columns
    assert "Category" in df_tickets.columns
    assert "Priority" in df_tickets.columns
    assert "Status" in df_tickets.columns


def test_resolution_and_csat_sanity():
    sim = ITSMTicketSimulator(seed=42)
    df_tickets, _ = sim.generate_tickets()

    assert (df_tickets["ResolutionTimeHours"] > 0).all()
    assert (
        (df_tickets["CSATScore"] >= 1) & (df_tickets["CSATScore"] <= 5)
    ).all()
    assert (
        df_tickets["CSATScore"].mean() >= 4.0
    ), "Expected high customer satisfaction"
