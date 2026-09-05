# Changelog

All notable changes to the Audit Taxonomy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Restored 775 removed audit definitions from `5fbaa0750d`, bringing the collection
  back to 2,186 definitions across 43 categories while keeping the root layout.
- Initial repository structure with 43 categories
- Schema templates and 3 example audit patterns
- Master audit menu (AUDIT-MENU.md) with ~2,200 audit definitions
- Documentation framework

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- Inventory generation scans numbered root categories, preserves per-file SDLC
  selections, and refuses to overwrite the catalog after an empty or invalid scan.
- Catalog paths and GitHub Pages category triggers match the flattened layout.

### Security
- N/A
