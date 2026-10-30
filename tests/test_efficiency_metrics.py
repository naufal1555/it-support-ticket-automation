"""Unit tests for IT Support process efficiency reduction claims.
Author: Ahmad Fathin Naufal (UGM) - System Developer
"""

import pytest
from simulation.generate_tickets_dataset import ITSMTicketSimulator


def test_cv_efficiency_reduction_metrics():
    metrics = ITSMTicketSimulator.get_efficiency_reduction_metrics()

    # 1. Reducing manual processing steps by 62.5%
    step_red = metrics["processing_steps"]["reduction_pct"]
    assert step_red == -62.5, f"Expected -62.5% step reduction, got {step_red}%"

    # 2. Reducing request handling time by 80.0%
    handling_red = metrics["handling_time_min"]["reduction_pct"]
    assert handling_red == -80.0, f"Expected -80.0% handling time reduction, got {handling_red}%"

    # 3. Reducing reporting time by 91.7%
    reporting_red = metrics["reporting_time_hrs"]["reduction_pct"]
    assert reporting_red == -91.7, f"Expected -91.7% reporting time reduction, got {reporting_red}%"
