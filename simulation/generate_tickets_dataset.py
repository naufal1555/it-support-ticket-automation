"""Enterprise IT Support Ticket Simulation Engine.
Generates 25+ Users, 8 IT Specialists, and 200+ Valid Lifecycle ITSM Tickets.
Author: Ahmad Fathin Naufal (UGM) - System Developer
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
import logging
import os

logger = logging.getLogger("itsm.simulation")

DOMAINS = [
    "Hardware Issue",
    "Software Application",
    "Network & VPN",
    "Security & Account Access",
]

PRIORITIES = [
    ("P1 - Critical (2h SLA)", 2),
    ("P2 - High (8h SLA)", 8),
    ("P3 - Medium (24h SLA)", 24),
    ("P4 - Low (72h SLA)", 72),
]

SPECIALISTS = [
    (
        "IT-ENG-01",
        "Ahmad Fathin Naufal",
        "ahmad.fathin@enterprise.com",
        "Security & Account Access",
    ),
    (
        "IT-ENG-02",
        "Bayu Wicaksono",
        "bayu.wicaksono@enterprise.com",
        "Network & VPN",
    ),
    (
        "IT-ENG-03",
        "Chandra Kirana",
        "chandra.kirana@enterprise.com",
        "Hardware Issue",
    ),
    (
        "IT-ENG-04",
        "Dian Sastrowardoyo",
        "dian.sastro@enterprise.com",
        "Software Application",
    ),
    (
        "IT-ENG-05",
        "Erwin Prasetya",
        "erwin.prasetya@enterprise.com",
        "Network & VPN",
    ),
    (
        "IT-ENG-06",
        "Fitria Ramadhani",
        "fitria.ramadhani@enterprise.com",
        "Software Application",
    ),
    (
        "IT-ENG-07",
        "Gilang Ramadhan",
        "gilang.ramadhan@enterprise.com",
        "Hardware Issue",
    ),
    (
        "IT-ENG-08",
        "Hafiz Syahrin",
        "hafiz.syahrin@enterprise.com",
        "Security & Account Access",
    ),
]

# 28 Users to strictly exceed the 25+ CV metric
USERS_28 = [
    (
        f"USR-{str(i+1).zfill(3)}",
        name,
        email,
        dept,
    )
    for i, (name, email, dept) in enumerate(
        [
            (
                "Aditya Pratama",
                "aditya.pratama@enterprise.com",
                "Engineering",
            ),
            (
                "Bella Safira",
                "bella.safira@enterprise.com",
                "Human Resources",
            ),
            ("Cahyo Utomo", "cahyo.utomo@enterprise.com", "Operations"),
            ("Desi Ratnasari", "desi.ratnasari@enterprise.com", "Finance"),
            (
                "Erlangga Satria",
                "erlangga.satria@enterprise.com",
                "Marketing",
            ),
            ("Farida Nurhan", "farida.nurhan@enterprise.com", "Operations"),
            ("Guntur Triyoga", "guntur.triyoga@enterprise.com", "Engineering"),
            ("Hani Purnamasari", "hani.purnamasari@enterprise.com", "Finance"),
            ("Indra Bekti", "indra.bekti@enterprise.com", "Marketing"),
            (
                "Jovita Karen",
                "jovita.karen@enterprise.com",
                "Human Resources",
            ),
            ("Krisna Mukti", "krisna.mukti@enterprise.com", "Engineering"),
            ("Lidya Pratiwi", "lidya.pratiwi@enterprise.com", "Operations"),
            ("Mochtar Kusuma", "mochtar.kusuma@enterprise.com", "Finance"),
            ("Nadya Hutagalung", "nadya.huta@enterprise.com", "Marketing"),
            (
                "Oscar Lawalata",
                "oscar.lawalata@enterprise.com",
                "Engineering",
            ),
            (
                "Paramitha Rusady",
                "paramitha.rusady@enterprise.com",
                "Human Resources",
            ),
            ("Qori Sandioriva", "qori.sandio@enterprise.com", "Operations"),
            ("Raffi Ahmad", "raffi.ahmad@enterprise.com", "Marketing"),
            ("Syahrini Zaskia", "syahrini.zaskia@enterprise.com", "Finance"),
            (
                "Taufik Hidayat",
                "taufik.hidayat@enterprise.com",
                "Engineering",
            ),
            ("Uut Permatasari", "uut.permata@enterprise.com", "Operations"),
            (
                "Vicky Prasetyo",
                "vicky.prasetyo@enterprise.com",
                "Marketing",
            ),
            ("Wulan Guritno", "wulan.guritno@enterprise.com", "Finance"),
            (
                "Xavier Marks",
                "xavier.marks@enterprise.com",
                "Human Resources",
            ),
            ("Yayan Ruhian", "yayan.ruhian@enterprise.com", "Operations"),
            ("Zaskia Sungkar", "zaskia.sungkar@enterprise.com", "Finance"),
            ("Bambang Soesatyo", "bambang.soe@enterprise.com", "Engineering"),
            ("Citra Kirana", "citra.kirana@enterprise.com", "Marketing"),
        ]
    )
]


class ITSMTicketSimulator:

    def __init__(self, seed: int = 42):
        np.random.seed(seed)

    def generate_tickets(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        tickets = []
        activity_logs = []

        total_tickets = 225  # Strictly exceeds 200+ CV metric
        base_time = datetime(2025, 8, 1, 8, 30, 0)

        for i in range(total_tickets):
            ticket_id = f"INC-2025-{str(i+1).zfill(5)}"
            user = USERS_28[i % len(USERS_28)]
            domain = DOMAINS[i % len(DOMAINS)]

            # Priority assignment
            rand_p = np.random.rand()
            if rand_p < 0.10:
                p_tuple = PRIORITIES[0]  # P1 - 2h SLA
            elif rand_p < 0.35:
                p_tuple = PRIORITIES[1]  # P2 - 8h SLA
            elif rand_p < 0.85:
                p_tuple = PRIORITIES[2]  # P3 - 24h SLA
            else:
                p_tuple = PRIORITIES[3]  # P4 - 72h SLA

            priority_name, sla_hours = p_tuple

            # Assigned Specialist based on domain
            matching_specs = [s for s in SPECIALISTS if s[3] == domain]
            spec = matching_specs[i % len(matching_specs)]

            created_time = base_time + timedelta(
                hours=i * 5.2 + np.random.uniform(0, 2)
            )
            due_time = created_time + timedelta(hours=sla_hours)

            # SLA Breach Rate modeled at ~7.5% (Adherence ~92.5%)
            is_breached = bool((i % 13 == 0) and (i > 0))

            if is_breached:
                turnaround = float(
                    sla_hours + np.random.uniform(1.5, sla_hours * 0.8)
                )
                csat = int(np.random.choice([2, 3, 4], p=[0.4, 0.4, 0.2]))
            else:
                turnaround = float(
                    np.random.uniform(0.4 * sla_hours, 0.88 * sla_hours)
                )
                csat = int(np.random.choice([4, 5], p=[0.25, 0.75]))

            resolved_time = created_time + timedelta(hours=turnaround)

            ticket = {
                "TicketID": ticket_id,
                "Title": f"Issue with {domain.split()[0]} on workstation {user[0]}",
                "Category": domain,
                "Priority": priority_name,
                "SLAHours": sla_hours,
                "RequesterID": user[0],
                "RequesterName": user[1],
                "RequesterEmail": user[2],
                "Department": user[3],
                "AssignedSpecialist": spec[1],
                "SpecialistEmail": spec[2],
                "Status": "Resolved",
                "CreatedDate": created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "DueDate": due_time.strftime("%Y-%m-%d %H:%M:%S"),
                "ResolvedDate": resolved_time.strftime("%Y-%m-%d %H:%M:%S"),
                "ResolutionTimeHours": round(turnaround, 2),
                "SLABreached": is_breached,
                "CSATScore": csat,
            }
            tickets.append(ticket)

            # Work activity logs
            activity_logs.append(
                {
                    "ActivityID": f"ACT-{str(i*2 + 1).zfill(6)}",
                    "TicketID": ticket_id,
                    "Author": "System Auto-Triage",
                    "NoteType": "System Auto-Triage",
                    "Notes": f"Ticket triaged into domain '{domain}' with {sla_hours}h SLA. Assigned to {spec[1]}.",
                    "Timestamp": ticket["CreatedDate"],
                }
            )
            activity_logs.append(
                {
                    "ActivityID": f"ACT-{str(i*2 + 2).zfill(6)}",
                    "TicketID": ticket_id,
                    "Author": spec[1],
                    "NoteType": "Resolution Summary",
                    "Notes": f"Issue resolved within {turnaround:.1f} hours. Requester confirmed functionality.",
                    "Timestamp": ticket["ResolvedDate"],
                }
            )

        df_tix = pd.DataFrame(tickets)
        df_act = pd.DataFrame(activity_logs)
        return df_tix, df_act
