# -stra ecosystem demo

[![CI](https://github.com/sadpig70/stra-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/sadpig70/stra-demo/actions/workflows/ci.yml)

> **route → clear → certify → attest, end to end.** The four HELIX-derived `-stra`
> platforms run one datacenter siting decision together and produce a single unified
> verdict + attestation.

The `-stra` family are four independent deterministic platforms, each a kernel + N
domain packs condensed from a different HELIX corpus cluster:

| Platform | verb | does |
|---|---|---|
| [Routestra](https://github.com/sadpig70/Routestra) | route | routes a resource to the best constraint-satisfying site |
| [Clearstra](https://github.com/sadpig70/Clearstra) | clear | clears capacity/rights allocation (conflict-free, priority) |
| [Certstra](https://github.com/sadpig70/Certstra) | certify | certifies a robot/OS release against a baseline |
| [Attestra](https://github.com/sadpig70/Attestra) | attest | attests a delegated action and issues a warrant |

They were built independently but **share one severity algebra**:

```
valid   ==  compliant   ==  certifiable    ==  sovereign     (ok)
thin    ==  restricted  ==  needs_review   ==  conditional   (caution)
breach  ==  violation   ==  blocked                          (fail)
```

That shared algebra is what makes them **compose**.

## The scenario

One decision — siting an AI datacenter — flows through all four:

1. **route (Routestra)** — is the candidate site within grid + thermal/ecological bounds?
   → `compliant`
2. **clear (Clearstra → Attestra)** — clear the site's capacity among tenants; the
   allocation is emitted as an Attestra clearing packet and **verified by Attestra's
   `reserve-flow` pack** (conservation / no-conflict / priority). → `valid`
   *(This is a proven cross-platform composition: `Clearstra.clear()` output attests as valid.)*
3. **certify (Certstra)** — certify the robot OS release running at the site against its
   certified baseline. → `certifiable`
4. **attest (Attestra)** — attest the delegated siting action (authority/custody/route/
   rollback/trace) and issue a warrant. → `valid`

Each stage's verdict is mapped to the shared severity; the **ecosystem verdict** is the
worst severity across the four, and a single combined **attestation** is issued.

## Run

```bash
# place the four platform repos as siblings of this one:
#   ../Routestra  ../Clearstra  ../Certstra  ../Attestra
python demo.py
```

```
=== -stra ecosystem: datacenter siting decision ===
  [compliant   ] route (Routestra thermal-cascade)
  [valid       ] clear (Clearstra -> Attestra reserve-flow)
  [certifiable ] certify (Certstra cert-mesh)
  [valid       ] attest (Attestra handback)
  ECOSYSTEM VERDICT: valid  (severity-aligned across route/clear/certify/attest)
  ATTESTATION: ATT-... (grade=full)

=== Compatibility Mesh: one named cluster -> three machines -> three platforms ===
  [Attestra ] pqc-mesh (gate)    valid
  [Routestra] flow-mesh (bound)  compliant
  [Clearstra] agent-ops (price)  $10.00 -> tool-operator
```

## Compatibility Mesh — one name, three machines, three platforms

The second block demonstrates HELIX's **machine-aware routing**. The corpus contained a
five-project cluster that all called themselves a "Compatibility Mesh" (SovMesh, PqcMesh,
SignalMesh, FlowMesh, AgentMesh). A naive read would condense them into *one* new
platform. But reading each project's real code shows they share a **name, not a machine**:

| sibling | machine | landed on | as |
|---|---|---|---|
| SovMesh · PqcMesh · SignalMesh | assessment → severity **verdict** | Attestra | predicate-gate packs |
| FlowMesh | utilization **threshold-bound** | Routestra | a `bound` pack |
| AgentMesh | cost **pricing** + rollup (no verdict) | Clearstra | a `price` market |

So routing sent the five to **three existing platforms — zero new kernels**. The demo runs
the three that landed on distinct platforms against one datacenter and shows the
heterogeneity directly: a gate and a bound return a **verdict**; a price returns a **cost**.
Each absorbed pack ships a parity test against its source (`test_*_mesh_parity.py`).

## The full sweep — one corpus, sorted by machine

The Compatibility Mesh was one cluster. HELIX then ran the same machine-aware routing
across the *whole* corpus candidate pool and resolved every project into one of three
classes — decided by reading real code, never the name:

| class | what it is | outcome | count |
|---|---|---|---|
| **absorb** | a self-contained gate/primitive (check-ladder → verdict, or a price/bound/certify) | becomes a pack **with a source-parity test** | 14 |
| **defer** | a multi-output simulation/scoring machine (pathfinding, physics sim, weighted score + ledger) | left standalone — a faithful pack would need the whole engine | 6 |
| **design-only** | no real code yet | marked, skipped | 8 |

The 14 absorptions grew all four platforms from the corpus, and routing corrected two by
machine: **AgentMesh** (pricing) went Attestra→Clearstra; **SettleMesh** (a compliance
gate, despite the name) went Clearstra→Attestra.

| platform | verb | packs (from corpus) |
|---|---|---|
| [Attestra](https://github.com/sadpig70/Attestra) | attest | **23** predicate gates |
| [Clearstra](https://github.com/sadpig70/Clearstra) | clear | **12** markets (price/clear/settle/rehearse) |
| [Routestra](https://github.com/sadpig70/Routestra) | route | **11** routing/bound packs |
| [Certstra](https://github.com/sadpig70/Certstra) | certify | **4** certify packs |

After the sweep, HELIX's `build_on_platform_candidate()` returns None — the pool is fully
routed. The remaining growth path is **CONDENSE** (emit a *new* platform) for a cluster
with a genuinely novel machine, not another pack.

## Notes

- Thin orchestration only: the demo imports each platform's **public kernel/packs** and
  wires them. Each platform stays standalone (no cross-dependency); this repo depends on
  all four being present as siblings.
- Deterministic: `now` is injected; no clock/network/AI.
- Lineage: the four platforms were condensed from the HELIX corpus (see
  [HELIX `docs/CONDENSE.md`](https://github.com/sadpig70/HELIX)).

## License

MIT License © 2026 sadpig70 (Jung Wook Yang)
