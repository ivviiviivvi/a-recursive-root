<!-- AI-Handoff:START -->
**AI Handoff Context**: Cross-reference map linking major knowledge domains across the repository.
**Maintainer**: gpt-5-codex orchestration lead
**Generated**: 2025-10-28T06:20:00Z
<!-- AI-Handoff:END -->

# Repository Interconnected Knowledge Key

This key acts as the connective tissue between technical assets, documentation, and operational playbooks. Each entry highlights
primary directories, their purpose, and the recommended adjacent references for deeper context.

## Core Program Areas

- **AI Council Platform (`workspace/projects/ai-council-system`)**
  - Pair with: [`docs/architecture/system-architecture.md`](architecture/system-architecture.md),
    [`docs/overview.md`](overview.md)
  - Dependencies: `workspace/projects/ai-council-system/core/`, `web/`, `blockchain/`
  - Supporting notes: `workspace/projects/ai-council-system/docs/`, `docs/runbooks/`
- **Governance & Policy (`governance/`)**
  - Pair with: [`docs/layering.md`](layering.md) for layered accountability
  - Licensing crosswalk: `licenses/`, `governance/licenses/`
  - Operational guardrails: `governance/policies/`
- **Observability Stack (`observability/`)**
  - Pair with: `workspace/projects/ai-council-system/deployment/grafana-dashboards/`
  - Integrations: `integrations/`, `cloud/`
- **AI Agent Swarm (`ai/` and `workspace/projects/ai-council-system/swarm/`)**
  - Pair with: `docs/technical/`, `docs/user/`
  - Orchestration notes: `docs/agentic-orchestration.md`

## Documentation Fabric

- **High-Level Orientation**: `README.md`, `docs/overview.md`, `docs/user/README.md`
- **Academic + Research**: `docs/academic/`, `research/README.md`
- **Operational Excellence**: `docs/runbooks/`, `docs/maintenance.md`, `observability/README.md`
- **Compliance + Security**: `SECURITY.md`, `governance/standards/README.md`, `provenance/README.md`

## Delivery Pipelines & Tooling

- **Automation Scripts**: `scripts/`, `workspace/projects/ai-council-system/scripts/`
- **Infrastructure as Code**: `cloud/`, `environment/`
- **Developer Experience**: `tools/README.md`, `workspace/orgs/CoreSystems/`

## Knowledge Continuity Threads

1. Begin with `docs/interconnected-key.md` (this file) to orient the topology.
2. Follow directory-level `README.md` files generated via `tools/generate_directory_readmes.py`.
3. Dive into specialized modules using references listed within each README.
4. Capture learnings or updates in `workspace/_meta/README.md` for session-to-session continuity.

<!-- AI-Handoff:FOOTER-START -->
**Next Steps**: Expand each reference with owner contacts, status tags, and dependency health in subsequent passes.
<!-- AI-Handoff:FOOTER-END -->
