# Audit Template Examples

> Three diverse examples showing how to adapt the template across different domains.

## Purpose

When generating audit files for the ~2,200 audits in AUDIT-MENU.md, Claude Code should reference these examples to understand how the template adapts to different audit types. **The OAuth2 example in the full template is just ONE pattern** — not all audits look like that.

---

## The Three Examples

| Example | Domain | Key Differences from OAuth2 |
|---------|--------|---------------------------|
| **01-bus-factor-audit.yaml** | Organizational/Qualitative | Interviews instead of grep; manual verification; qualitative findings |
| **02-container-resource-limits-audit.yaml** | Infrastructure/Metrics | kubectl commands; quantitative thresholds; highly automatable |
| **03-runbook-completeness-audit.yaml** | Process/Documentation | Document analysis; mixed automation; quality assessment |

---

## When to Use Each Pattern

### Pattern 1: Organizational/Qualitative (Bus Factor Example)

**Use for categories:**
- Human & Organizational (20)
- Ethical & Societal (21)
- Gamification & Behavioral Design (22)
- Emotional Design & Trust (23)
- Parts of Requirements & Specification Quality (28)
- Parts of Risk Management (29)

**Key adaptations:**
```yaml
execution:
  automatable: "manual"  # Cannot be automated
  scope: "organizational"

discovery:
  interviews:            # Instead of code_patterns
    - role: "..."
      questions: [...]
      
closeout_checklist:
  - verification: "manual"  # Human review, not bash commands
    verification_notes: "What reviewer should confirm"
```

**Signals use `evidence_indicators` (observable behaviors) instead of `evidence_pattern` (grep patterns):**
```yaml
signals:
  critical:
    - evidence_indicators:
        - "Only one person has ever resolved incidents for this system"
        - "Team members say 'only X understands that'"
```

---

### Pattern 2: Infrastructure/Metrics (Container Resource Limits Example)

**Use for categories:**
- Compute & Orchestration (13)
- Network Infrastructure (14)
- Storage Infrastructure (15)
- Infrastructure as Code (16)
- Performance & Efficiency (2) - metrics portions
- Scalability & Capacity (4)
- Cost & Economics (31)

**Key adaptations:**
```yaml
execution:
  automatable: "yes"  # Fully automatable
  scope: "infrastructure"

discovery:
  kubernetes_resources:  # Or cloud resources
    - kind: "Deployment"
      fields_of_interest: [...]
      
  metrics_queries:
    - system: "Prometheus"
      query: "..."
      threshold: "< 0.8"  # Quantitative!
```

**Signals use `evidence_threshold` with quantitative criteria:**
```yaml
signals:
  critical:
    - evidence_threshold: "Any pod without memory limits"
      verification_command: "kubectl get pods -o json | jq '...'"
      verification_expected: "0"
```

---

### Pattern 3: Process/Documentation (Runbook Completeness Example)

**Use for categories:**
- Documentation & Knowledge (27)
- Testing & Quality Assurance (26)
- Operational Excellence (25)
- Compliance & Governance (24)
- Configuration Management (30)
- Developer Experience (35) - tooling portions

**Key adaptations:**
```yaml
execution:
  automatable: "partial"  # File existence = auto, quality = manual
  scope: "documentation"

discovery:
  file_patterns:         # Find documents
    - glob: "**/runbooks/*.md"
    
  documents_to_review:   # What to analyze
    - type: "runbooks"
      analysis_checklist:
        - "Has clear title"
        - "Includes troubleshooting"
```

**Mixed closeout — some bash, some manual:**
```yaml
closeout_checklist:
  - id: "auto-check"
    verification: "find runbooks/ -name '*.md' | wc -l"
    expected: "> 0"
    
  - id: "manual-check"
    verification: "manual"
    verification_notes: "Reviewer confirms quality assessment completed"
```

---

## DO NOT Do This

❌ **Don't force-fit grep patterns where they don't apply:**
```yaml
# BAD - Bus factor can't be grepped
signals:
  critical:
    - evidence_pattern: "grep -r 'bus factor' src/"  # This is nonsense
```

❌ **Don't claim everything is automatable:**
```yaml
# BAD - Interviews can't be automated
execution:
  automatable: "yes"  # Wrong for organizational audits
```

❌ **Don't use bash verification for qualitative findings:**
```yaml
# BAD - Can't verify team health with bash
closeout_checklist:
  - verification: "test -f team-health.txt && echo PASS"  # Meaningless
```

---

## Choosing the Right Pattern

```
Is this about CODE or CONFIG?
├─ YES → Is it security-focused? 
│        ├─ YES → Use OAuth2 pattern (security signals, CWE references)
│        └─ NO → Use Infrastructure pattern (quantitative thresholds)
└─ NO → Is this about PEOPLE or PROCESS?
         ├─ PEOPLE → Use Organizational pattern (interviews, qualitative)
         └─ PROCESS → Use Documentation pattern (mixed automation)
```

---

## Category-to-Pattern Quick Reference

| Categories | Primary Pattern | Notes |
|------------|-----------------|-------|
| 1. Security & Trust | OAuth2 (security code) | CWE mappings, security tooling |
| 2. Performance & Efficiency | Infrastructure/Metrics | Quantitative thresholds |
| 3. Reliability & Resilience | Mixed | Some code, some config |
| 4. Scalability & Capacity | Infrastructure/Metrics | Capacity metrics |
| 5. Observability | Infrastructure/Metrics | Monitoring queries |
| 6. Code Quality | OAuth2 (code analysis) | Static analysis, linters |
| 7. Architecture & Design | Mixed | Some automated, much judgment |
| 8. Data & State | Mixed | Schema checks + design review |
| 9. API & Integration | OAuth2 (code/config) | Contract testing |
| 10. Messaging & Events | Infrastructure + Code | Mixed |
| 11. Time & Scheduling | Code/Config | Time handling patterns |
| 12. Versioning & Lifecycle | Documentation | Process-focused |
| 13-16. Infrastructure | Infrastructure/Metrics | kubectl, cloud CLIs |
| 17. Usability | Organizational | User research, heuristics |
| 18. Accessibility | Mixed | Automated scans + manual review |
| 19. SEO | Infrastructure/Metrics | Crawl data, scores |
| 20-23. Human/Experience | Organizational | Interviews, qualitative |
| 24-30. Process/Governance | Documentation | Mixed automation |
| 31. Cost & Economics | Infrastructure/Metrics | Cost queries |
| 32. Dependency & Supply Chain | Code/Config | SBOM, scanning |
| 33. Legacy & Migration | Mixed | Assessment + code analysis |
| 34. Business Logic | Code | Domain rule verification |
| 35. Developer Experience | Mixed | Tooling + surveys |
| 36. Internationalization | Code | i18n pattern checks |
| 37. Machine Learning & AI | Mixed | Metrics + qualitative |
| 38-40. Sensors/RT/Signal | Infrastructure | Embedded/hardware focus |
| 41. Blockchain | Code (security) | Smart contract analysis |
| 42. Quantum | Mixed | Novel domain |
| 43. Metaverse/XR | Mixed | Performance + UX |

---

## Files in This Directory

```
examples/
├── 01-bus-factor-audit.yaml           # Organizational/Qualitative
├── 02-container-resource-limits-audit.yaml  # Infrastructure/Metrics
├── 03-runbook-completeness-audit.yaml      # Process/Documentation
└── README.md                          # This file
```

---

*Last Updated: January 2025*
