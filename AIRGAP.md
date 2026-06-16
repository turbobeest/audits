# Airgap & Offline Consumption

> How to consume the audit catalog when you cannot fetch it at runtime — air-gapped deployments, isolated networks, regulated environments, or any situation where the consuming project must vendor a known-good snapshot.

This document is for **consumers** of the catalog. Producers (maintainers cutting releases) follow the same artifact format; the maintainer-facing release procedure lives at the bottom of this document.

---

## What's distributed offline

Every tagged release publishes signed tarball artifacts to the corresponding GitHub Release. A release contains:

| Artifact | Purpose |
|---|---|
| `audits-vX.Y.Z.tar.gz` | The catalog tarball. Deterministic content, sorted file order, zeroed timestamps. |
| `audits-vX.Y.Z.tar.gz.sha256` | SHA256 checksum for content integrity. |
| `audits-vX.Y.Z.tar.gz.sig` | Detached cosign signature (sigstore keyless). |
| `audits-vX.Y.Z.tar.gz.pem` | Cosign signing certificate. Identity-bound to this repo via OIDC. |

The tarball extracts to a versioned directory (`audits-vX.Y.Z/`) and contains:

```
audits-vX.Y.Z/
├── audits/                 # 2,186 audit YAML files across 43 categories
├── schema/                 # JSON schemas and templates
├── categories/             # Per-category markdown indexes (43 files)
├── meta-audit/             # Meta-audit definitions (audit-the-auditor patterns)
├── docs/                   # Reference documentation, whitepaper
├── scripts/                # Inventory generation and utility scripts
├── AUDIT-INVENTORY.csv     # Machine-readable audit index for AI agents
├── AUDIT-MENU.md           # Human-readable audit menu
├── AGENT-ASSIGNMENT-PROTOCOL.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── VERSION                 # Plain-text release tag (e.g., "v1.0.0")
```

The `audit-browser/` SvelteKit application is **not** included. It deploys separately (see "Browser deployment for offline networks" below).

---

## Acquisition

### From a workstation with internet access

```bash
VERSION=v1.0.0
gh release download "$VERSION" \
  --repo turbobeest/audits \
  --pattern 'audits-*.tar.gz*'
```

Or with curl, no GitHub CLI required:

```bash
VERSION=v1.0.0
BASE="https://github.com/turbobeest/audits/releases/download/${VERSION}"
for f in audits-${VERSION}.tar.gz audits-${VERSION}.tar.gz.sha256 \
         audits-${VERSION}.tar.gz.sig audits-${VERSION}.tar.gz.pem; do
  curl -L -O "${BASE}/${f}"
done
```

The tarball is typically a few MB — easy to side-channel transfer (USB, internal artifact registry, etc.) into an isolated network.

### Inside an isolated network

Place all four artifacts in the same directory. Verification and extraction are fully offline; see below.

---

## Verification

**Always verify before extracting.** Both checks below are recommended; the cosign verification is stronger.

### SHA256 integrity check

```bash
sha256sum -c audits-v1.0.0.tar.gz.sha256
# audits-v1.0.0.tar.gz: OK
```

### Cosign signature verification

The release is signed with sigstore keyless signing — no key management on the producer side, identity bound to the GitHub repo via OIDC.

**Online verification** (when the verifier can reach the sigstore transparency log):

```bash
cosign verify-blob \
  --certificate audits-v1.0.0.tar.gz.pem \
  --signature audits-v1.0.0.tar.gz.sig \
  --certificate-identity-regexp 'https://github.com/turbobeest/audits/.+' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  audits-v1.0.0.tar.gz
```

A successful verification confirms the artifact was signed by a GitHub Actions workflow running in the `turbobeest/audits` repo.

**Offline verification** (verifier has no network at all):

```bash
cosign verify-blob \
  --insecure-ignore-tlog \
  --certificate audits-v1.0.0.tar.gz.pem \
  --signature audits-v1.0.0.tar.gz.sig \
  --certificate-identity-regexp 'https://github.com/turbobeest/audits/.+' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  audits-v1.0.0.tar.gz
```

The `--insecure-ignore-tlog` flag skips the Rekor transparency-log check. The cryptographic identity binding still holds; what's lost is the public, append-only proof that this specific signature was logged at signing time. For most airgap consumers this is acceptable; for higher-assurance environments, fetch the Rekor entry alongside the artifacts at acquisition time and verify it offline.

### Cosign installation

If `cosign` is not already in your environment:

- **Online install:** `go install github.com/sigstore/cosign/v2/cmd/cosign@v2.x.x` or `brew install cosign` on macOS.
- **Offline install:** download a release binary from <https://github.com/sigstore/cosign/releases> on a connected workstation, verify its own signature, transfer it to the airgap network. Cosign is a single static binary.

---

## Extraction and consumption

```bash
tar -xzf audits-v1.0.0.tar.gz
cd audits-v1.0.0/
```

The tree under `audits-v1.0.0/` is identical in shape to the live repo (minus `audit-browser/`). Consumers point their tools at the extracted directory:

```bash
# Find audits by category
ls audits/01-security-trust/

# Find by ID across the whole catalog
grep -r 'oauth2-implementation' audits/

# Validate a custom audit against the schema
# (using your preferred YAML schema validator, e.g. ajv-cli, check-jsonschema)
check-jsonschema --schemafile schema/audit-schema.json audits/01-security-trust/*.yaml
```

For autonomy-harness consumers, point `AUTONOMY-MANIFEST.yaml` at the extracted directory:

```yaml
audit_catalog:
  source: vendored
  path: ./vendor/audits-v1.0.0
  version: v1.0.0
```

The harness then loads audit definitions from disk rather than fetching from GitHub.

---

## Update flow

Updating a vendored catalog is a deliberate act, not an automated one. Recommended cadence: pin a version, refresh quarterly or when a release introduces audits relevant to the consuming project.

1. Track the consumed version in your project (in `AUTONOMY-MANIFEST.yaml`, in an ADR, or both).
2. When a new release ships, review its `CHANGELOG.md` entries (visible on the release page or in the new tarball).
3. Acquire the new artifacts, verify, extract.
4. Diff the new extracted tree against the old: `diff -r vendor/audits-v1.0.0 vendor/audits-v1.1.0`.
5. Run your audit pipeline against the new catalog in a non-production project state first; promote to main only after the diff is understood.
6. Record the version bump in `docs/adr/` or your equivalent.

Treat catalog updates as you would any vendored dependency update — auditable, tested, recorded.

---

## Browser deployment for offline networks

The `audit-browser/` SvelteKit application is published at <https://turbobeest.github.io/audits/>. For offline networks that want the same browse experience:

1. Clone the repo on a connected workstation, build the static site (`cd audit-browser && npm ci && npm run build`).
2. The build output is a self-contained static site (HTML + JS + JSON data). Transfer it to the offline network.
3. Serve it from any static-file server inside the network — nginx, an internal artifact registry, even a directory mounted by IIS or Apache.

The browser is a separate concern from the catalog tarball because most catalog consumers (CI pipelines, AI agents) do not need the browser; the small fraction that does (humans exploring the taxonomy) can deploy it once and reuse.

---

## What's NOT covered by this distribution

- **Live updates.** Vendored catalogs do not refresh themselves. The update is explicit.
- **Industry overlays under active development.** When an overlay (HIPAA, FedRAMP, etc.) is being iterated on, vendored consumers may pin an older version intentionally. Track that decision.
- **Custom project audits.** Project-specific audit definitions live in the consuming project's repo, not in this catalog. The vendored catalog is the *common* definitions.
- **Tool binaries** (Semgrep, gitleaks, syft, etc.). Audit definitions reference these tools; the tools themselves are sourced separately.

---

## For maintainers — release procedure

Releases are cut by pushing a semver tag matching `v*`. The `release.yml` workflow handles tarball construction, checksum, signing, and release publication:

```bash
# From a clean main branch
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

The workflow:

1. Builds the deterministic tarball.
2. Computes the SHA256.
3. Signs with cosign keyless (uses GitHub Actions OIDC; no signing keys to manage).
4. Creates a GitHub Release and attaches all four artifacts.

Manual triggering is supported via `workflow_dispatch` for testing the artifact production without cutting a real release; the manual run produces the artifacts as workflow outputs but does not create a public release.

### Pre-release checklist

- [ ] `CHANGELOG.md` has an entry describing what's in the release.
- [ ] `AUDIT-INVENTORY.csv` reflects the current `audits/` tree (the existing `update-inventory.yml` workflow handles this nightly; verify).
- [ ] No PRs in flight that would have made the release (the cut should reflect a stable point).
- [ ] Tag is created from `main`, not from a feature branch.

### Verifying a release post-publish

After the workflow completes, download the artifacts from the public release and run the consumer-side verification flow above. This confirms the signature chain works end-to-end before announcing the release.

---

## Reporting issues

Issues with offline consumption (broken signatures, tarball anomalies, missing files) should be filed at <https://github.com/turbobeest/audits/issues> with the release tag, the SHA256 of your tarball, and the cosign verification output (if relevant).
