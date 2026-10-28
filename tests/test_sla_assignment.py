"""Unit tests for SLA Priority Mapping and Breach Detection.
Author: Ahmad Fathin Naufal (UGM)
"""

import pytest
from simulation.generate_tickets_dataset import ITSMTicketSimulator


def test_sla_hours_per_priority():
    sim = ITSMTicketSimulator(seed=42)
    df_tickets, _ = sim.generate_tickets()

    p1 = df_tickets[df_tickets["Priority"].str.startswith("P1")]
    p2 = df_tickets[df_tickets["Priority"].str.startswith("P2")]
    p3 = df_tickets[df_tickets["Priority"].str.startswith("P3")]
    p4 = df_tickets[df_tickets["Priority"].str.startswith("P4")]

    assert (p1["SLAHours"] == 2).all()
    assert (p2["SLAHours"] == 8).all()
    assert (p3["SLAHours"] == 24).all()
    assert (p4["SLAHours"] == 72).all()


def test_sla_adherence_threshold():
    sim = ITSMTicketSimulator(seed=42)
    df_tickets, _ = sim.generate_tickets()

    adherence = (1.0 - df_tickets["SLABreached"].mean()) * 100.0
    # Expected enterprise adherence >= 90%
    assert (
        adherence >= 90.0
    ), f"Expected >= 90% SLA adherence rate, got {adherence:.1f}%"
