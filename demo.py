#!/usr/bin/env python3
"""-stra ecosystem demo — route -> clear -> certify -> attest, end to end.

The four HELIX-derived platforms are independent repos that share one severity algebra
(valid/thin/breach == compliant/restricted/violation == certifiable/needs_review/blocked).
This thin orchestration runs a single datacenter siting decision through all four and
produces one unified ecosystem verdict + attestation.

Requires the four sibling repos next to this one:
    ../Routestra  ../Clearstra  ../Certstra  ../Attestra
Each stays standalone; the demo only wires their public kernels/packs.
Deterministic: `now` is injected; no clock/network/AI.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for repo in ("Routestra", "Clearstra", "Certstra", "Attestra"):
    path = os.path.join(HERE, "..", repo)
    if path not in sys.path:
        sys.path.insert(0, path)

NOW = "2026-07-06"


def _sev(verdict):
    """Map any -stra verdict to the shared severity {0 ok, 1 caution, 2 fail}."""
    table = {
        "valid": 0, "thin": 1, "breach": 2,
        "compliant": 0, "restricted": 1, "violation": 2,
        "certifiable": 0, "needs_review": 1, "blocked": 2,
        "sovereign": 0, "conditional": 1,
    }
    return table[verdict]


def run_demo():
    steps = []

    # 1) ROUTE (Routestra) — is the candidate datacenter site within grid/thermal bounds?
    from routestra_packs.loader import load_packs as r_load, run_stage as r_run
    r_pack = r_load()["packs"]["thermal-cascade"]
    route_bound = r_run(r_pack, "bound", r_pack["samples"]["bound"], now=NOW)
    steps.append(("route (Routestra thermal-cascade)", route_bound["verdict"],
                  "site power/thermal within grid + ecological thresholds"))

    # 2) CLEAR (Clearstra) — clear the site's capacity among tenants; emit an Attestra packet.
    from clearstra_markets.loader import load_markets, run_stage as c_run
    from clearstra_core.attestra_bridge import to_attestra_packet
    c_pack = load_markets()["markets"]["reserve-flow"]
    clearing = c_run(c_pack, "clear", c_pack["samples"]["clear"], now=NOW)
    packet = to_attestra_packet(clearing, "SITE-CAPACITY-1")

    # 2b) ATTEST the clearing (Attestra reserve-flow pack verifies the allocation).
    from attestra_packs.loader import load_packs as a_load
    from attestra_core.gate_runtime import run_gates
    a_reg = a_load()
    rf = a_reg["packs"]["reserve-flow"]
    clear_verdict = run_gates(packet, rf["predicate_fns"], now=NOW,
                              id_field=rf.get("id_field", "packet_id"), schema=rf.get("schema"))
    steps.append(("clear (Clearstra -> Attestra reserve-flow)", clear_verdict["verdict"],
                  "capacity allocation attests as conservation/no-conflict/priority sound"))

    # 3) CERTIFY (Certstra) — certify the robot OS release running at the site.
    from certstra_packs.loader import load_packs as ce_load, run_stage as ce_run
    ce_pack = ce_load()["packs"]["cert-mesh"]
    cert = ce_run(ce_pack, "certify", ce_pack["samples"]["certify"], now=NOW)
    steps.append(("certify (Certstra cert-mesh)", cert["verdict"],
                  "learned robot policy stays within the certified baseline"))

    # 4) ATTEST (Attestra) — attest the delegated siting action and issue a warrant.
    from attestra_packs import handback
    from attestra_core.attestation import issue_attestation
    hb = run_gates(handback.SAMPLES["valid"], handback.PREDICATES, now=NOW, id_field="handback_id")
    steps.append(("attest (Attestra handback)", hb["verdict"],
                  "the delegated siting action was handed back with full evidence"))

    # 5) UNIFIED — one ecosystem verdict (worst severity) + a combined attestation.
    worst = max(steps, key=lambda s: _sev(s[1]))
    inv = {0: "valid", 1: "thin", 2: "breach"}
    ecosystem_verdict = inv[_sev(worst[1])]
    warrant = issue_attestation({
        "verdict": ecosystem_verdict, "subject": "datacenter-siting-decision-1",
        "pack": "stra-ecosystem",
        "checks": [{"gate": s[0], "verdict": inv[_sev(s[1])]} for s in steps],
    }, now=NOW)

    return {"steps": steps, "worst_stage": worst[0], "ecosystem_verdict": ecosystem_verdict,
            "attestation": warrant}


def run_compat_mesh():
    """The 'Compatibility Mesh' cluster: one name, three machines, three platforms.

    SovMesh/PqcMesh/SignalMesh/FlowMesh/AgentMesh share a name (an interconnection-mesh
    transplant) but NOT one machine. HELIX's machine-aware routing verified each against
    real code and sent it to the platform whose kernel matches its machine. Here the same
    datacenter is audited by the three that landed on DISTINCT platforms — a predicate
    gate (Attestra), a threshold-bound (Routestra), and a price (Clearstra) — so the
    heterogeneity is visible: a gate and a bound return a verdict; a price returns a cost.
    """
    rows = []

    # PqcMesh -> Attestra pqc-mesh (predicate gate): is the site's crypto PQC-ready?
    from attestra_packs.loader import load_packs as a_load
    from attestra_core.gate_runtime import run_gates
    pqc = a_load()["packs"]["pqc-mesh"]
    pqc_packet = {"packet_id": "SITE-CRYPTO-1", "subject": "SITE-CRYPTO-1", "assets": [
        {"asset_id": "kms", "algorithm": "ml_kem_768", "purpose": "key_exchange"},
        {"asset_id": "bulk", "algorithm": "aes256", "purpose": "confidentiality"},
        {"asset_id": "logs", "algorithm": "sha384", "purpose": "integrity"}]}
    pqc_v = run_gates(pqc_packet, pqc["predicate_fns"], now=NOW,
                      id_field=pqc.get("id_field", "packet_id"), schema=pqc.get("schema"))
    rows.append(("Attestra", "pqc-mesh (gate)", pqc_v["verdict"],
                 "site crypto is quantum-safe / PQC-ready"))

    # FlowMesh -> Routestra flow-mesh (threshold-bound): pipeline throughput headroom?
    from routestra_packs.loader import load_packs as r_load, run_stage as r_run
    flow = r_load()["packs"]["flow-mesh"]
    flow_b = r_run(flow, "bound", {"telemetry": {"input_rate": 80, "stages": [
        {"stage_id": "ingest", "constraint_type": "io", "capacity": 200},
        {"stage_id": "gpu", "constraint_type": "compute", "capacity": 100}]}}, now=NOW)
    rows.append(("Routestra", "flow-mesh (bound)", flow_b["verdict"],
                 "inference pipeline runs within capacity (no critical bottleneck)"))

    # AgentMesh -> Clearstra agent-ops (pricing, NOT a verdict): what do agent ops cost?
    from clearstra_markets.loader import load_markets, run_stage as c_run
    ao = load_markets()["markets"]["agent-ops"]
    priced = c_run(ao, "price", {"order": {"op_type": "tool", "units": 5000,
                                           "operator": "site-agents"}})
    rows.append(("Clearstra", "agent-ops (price)",
                 f"${priced['cost']:.2f} -> {priced['accountable_role']}",
                 "5000 agent tool calls priced + assigned an accountable role (a cost, not pass/fail)"))

    return rows


def main():
    r = run_demo()
    print("=== -stra ecosystem: datacenter siting decision ===\n")
    for name, verdict, why in r["steps"]:
        print(f"  [{verdict:12s}] {name}")
        print(f"               -> {why}")
    print(f"\n  worst stage: {r['worst_stage']}")
    print(f"  ECOSYSTEM VERDICT: {r['ecosystem_verdict']}  "
          f"(severity-aligned across route/clear/certify/attest)")
    att = r["attestation"]
    if att:
        print(f"  ATTESTATION: {att['attestation_id']} (grade={att['grade']})")

    print("\n=== Compatibility Mesh: one named cluster -> three machines -> three platforms ===\n")
    for platform, name, result, why in run_compat_mesh():
        print(f"  [{platform:9s}] {name:18s} {result}")
        print(f"               -> {why}")
    print("\n  same-named siblings, machine-aware routing sent each to a different kernel:")
    print("  Attestra=gate (verdict) | Routestra=bound (verdict) | Clearstra=price (cost)")

    return 0 if r["ecosystem_verdict"] != "breach" else 1


if __name__ == "__main__":
    raise SystemExit(main())
