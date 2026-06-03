# Audit Repository Refactoring: DoD Embedded Systems Focus

**Date:** 2026-06-03  
**Rationale:** Downselect the broad 43-category software audit taxonomy to focus
exclusively on DoD embedded software infrastructure domains.

## What Was Removed

### Phase 1: Category-Level Removal (15 categories, ~659 audits)

**Web/Consumer Categories:**
- 16-seo-discoverability (50 audits)
- 22-gamification-behavioral (35 audits)
- 23-emotional-design-trust (27 audits)
- 43-metaverse-immersive (43 audits)
- 15-accessibility-inclusion (56 audits)
- 14-usability-interaction (58 audits)
- 36-internationalization-localization (51 audits)

**Organizational/Business Categories:**
- 17-human-organizational (45 audits)
- 20-vendor-third-party (48 audits)
- 33-legacy-migration (52 audits)

**Emerging Technologies:**
- 41-blockchain-distributed-ledger (38 audits)
- 42-quantum-computing (27 audits)

**Economics/Ethics:**
- 31-cost-economics (48 audits)
- 18-ethical-societal (45 audits)
- 21-responsible-design (40 audits)

### Phase 2: Surgical Audit Removal (within remaining 28 categories)

Individual audits were removed from the following categories where they focused
on web/cloud-native patterns not applicable to DoD embedded systems:

- **09-api-integration:** Removed REST/GraphQL/webhook audits; kept CAN/Modbus/MIL-STD-1553
- **11-devops-ci-cd:** Removed container orchestration; kept embedded toolchain/HIL automation
- **12-cloud-infrastructure:** Removed AWS/Azure specifics; kept edge computing/connectivity
- **37-machine-learning-ai:** Removed cloud ML pipelines; kept embedded inference/quantization

*(Detailed surgical removal log available in git history: see commits tagged `phase-2-surgical-*`)*

## What Was Kept (28 categories, ~1,000-1,200 audits)

**Core Technical (01-13):**
- Security & Trust, Performance, Reliability, Scalability, Observability, Code Quality,
  Architecture, Data Management, API Integration, Testing, DevOps, Cloud, IaC

**Process & Governance (19, 24-30):**
- Compliance Legal, Compliance Governance, Operational Excellence, Documentation,
  Requirements, Risk Management, Configuration Management

**Dependencies (32):**
- Dependency Supply Chain

**Specialized Domains (34-35, 37-40):**
- Business Logic, Developer Experience, ML/AI, Sensors Physical Systems,
  Real-Time Embedded, Signal Processing

## Model Neutrality Clarification

As part of this refactoring, we clarified that the `tier` and `cognitive_mode`
fields in audit YAML files describe **human auditor expertise requirements**,
NOT AI model capabilities or LLM tier recommendations.

No audit YAML files were modified for this clarification; only schema and
documentation were updated.

## Recovery Instructions

### Option 1: Git History
All removed content is preserved in git history. To recover a deleted category:

```bash
# List commits that deleted categories
git log --all --oneline --grep="Phase 1"

# Restore a specific category
git checkout <commit-before-deletion> -- audits/16-seo-discoverability
```

### Option 2: External Backup
The complete original taxonomy (43 categories, 2,204 audits) is backed up
externally. Contact the repository maintainer for access.

## Future Expansion

If additional audit categories become relevant to DoD embedded systems
(e.g., automotive-specific ISO 26262 audits, edge ML/AI for autonomous systems),
they can be reintroduced from git history or external backup.
