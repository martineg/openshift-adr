# Changelog

All notable changes to the ADR Template Repository and Customer ADR Workflow.

## [1.2.0] - 2026-03-16

### Added - Document Outline Navigation

#### Navigation Solution
- **Document Outline Navigation** - Uses native Google Docs outline sidebar
  - Removed Table of Contents (HTML anchor links don't work in Google Docs)
  - Added navigation banner with clear instructions
  - Desktop: View → Show document outline (Ctrl+Alt+A Ctrl+Alt+H)
  - Mobile: Kebab menu (⋮) → Document outline
  - Hierarchical structure: Products (H2) contain ADRs (H4)
  - Always-visible sidebar shows current position
  - Instant navigation to any ADR with single click

#### User Experience Improvements
- **Navigation Banner** - Blue info box at document top
  - Shows total ADR count
  - Platform-specific instructions (desktop vs mobile)
  - Professional styling (background: #e3f2fd, border: #2196f3)
- **Heading Structure** - Each ADR gets H4 heading with ID and title
  - Auto-generates document outline tree structure
  - Collapsible product sections in outline
  - Current position highlighted in sidebar

#### Performance
- **Faster generation** - Removed TOC processing overhead
  - 15 ADRs: ~4 seconds (same as before)
  - 128 ADRs: ~19 seconds (was 23.6s with TOC)
  - 4.6 seconds faster for large documents

#### Technical Details
- Removed TOC generation code (`toc_data` collection)
- Added H4 headings before each ADR table
- Navigation banner uses inline CSS for Google Docs compatibility
- Product headings (H2) and ADR headings (H4) create outline hierarchy

#### Documentation Updates
- Updated CLAUDE.md with navigation solution details
- Updated README.md with accurate timing (19s for 128 ADRs)
- Added "Native Document Outline Navigation" to feature list
- Documented navigation banner implementation

## [1.1.0] - 2026-03-12

### Changed - Performance Optimization (800x Faster)

#### HTML Conversion Approach
- **BREAKING CHANGE**: Replaced Google Docs API approach with HTML→Drive API conversion
  - Old approach: 27 API calls per ADR with rate limiting → 2h 24min for 128 ADRs
  - New approach: Generate HTML + 1 Drive API call → 11 seconds for 128 ADRs
  - **800x performance improvement**

#### New Features
- **Nested Agreeing Parties Table** - Person/Role columns in clean table format
- **Red Cleanup Instructions** - Guidance to remove non-selected alternatives
  - "Alternatives" field: Instructions to delete non-chosen options
  - "Justification" field: Instructions to delete non-chosen justifications
  - "Implications" field: Instructions to delete non-chosen implications
- **Simplified #TODO# markers** - Just `#TODO#` instead of `#TODO# (Customer Name)`

#### Technical Details
- Uses `googleapiclient.http.MediaIoBaseUpload` for HTML upload
- Drive API `files().create()` with `mimeType='application/vnd.google-apps.document'`
- Single API call eliminates rate limiting issues completely
- Inline CSS styling for tables and formatting
- Yellow background: `<span style="background-color: #FFFF00;">`
- Red instructions: `<p style="color: red; font-weight: bold;">`

#### Documentation Updates
- Updated CLAUDE.md with HTML generation workflow
- Updated README.md with performance metrics
- Updated docs/usage/ARCHITECT_WORKFLOW.md with current implementation
- Added performance benchmarks to documentation

## [1.0.0] - 2026-03-10

### Added - Customer ADR Workflow (Complete)

#### Core Features
- **Google Docs Integration** - Real-time collaborative ADR editing
  - OAuth 2.0 authentication with Google Cloud
  - 2-column table formatting with gray label backgrounds
  - 10pt font sizing for professional appearance
  - Bold markdown processing (`**text**` → bold without asterisks)
  - Yellow background highlighting for `#TODO#` markers
  - Red "[REMOVE IF NOT APPLICABLE]" hints on Justification/Implications
  - Bullet symbols (•) instead of dashes
  - Product full names in headings

- **Offline Mode** - Fallback for disconnected environments
  - Local markdown file generation
  - Customer data protection (never committed to git)
  - Complete workflow without internet connection

- **Automated Validation** - Check ADR completion
  - Detects `#TODO#` markers
  - Validates Decision and Agreeing Parties fields
  - Role validation against dictionary
  - Multiple output formats: text, JSON, HTML
  - Exit codes for CI/CD integration

- **Export Capabilities**
  - Markdown export with table of contents
  - HTML export with Red Hat styling
  - Group by product, category, or none
  - Exclude non-discussed ADRs option

- **Rate Limit Handling**
  - Automatic retry with exponential backoff (30s, 60s)
  - 3 retry attempts before falling back to offline
  - Clear user messaging about quota status

#### Documentation
- **SETUP.md** - Quick installation and prerequisites guide (for architects)
- **USER_MANUAL.md** - Complete workflow guide (for architects)
- **MAINTENANCE.md** - Repository maintenance guide (for maintainers)
- **docs/README.md** - Documentation index and navigation
- **docs/setup/GOOGLE_API_SETUP.md** - Google API OAuth configuration
- **docs/usage/ARCHITECT_WORKFLOW.md** - 4-phase engagement workflow
- **docs/development/** - Technical specifications and test workflows

#### Quality Assurance
- **Automated Test Suite** - Non-regression tests
  - test_slugify - Customer name conversion
  - test_extract_adr_title - ADR parsing
  - test_parse_adr_template_file - Template file parsing
  - test_extract_doc_id_from_url - Google Docs URL parsing
  - test_bold_markdown_processing - Markdown regex patterns
  - test_adr_validation_patterns - Validation logic
  - test_product_name_mapping - Product dictionary completeness
  - test_field_order - ADR field structure

### Changed

- **Repository Structure** - Reorganized for clarity
  - Created `/docs/` with setup, usage, development subdirectories
  - Created `/tests/` for automated testing
  - Moved documentation from root to organized folders
  - Updated `.gitignore` to allow docs/*.md but exclude docs/*.pdf

- **Main README** - Streamlined and modernized
  - Quick start section with clear setup steps
  - Feature highlights
  - Product coverage table
  - References to BUILD.md and RUN.md

### Removed

- Temporary documentation files:
  - GITHUB_READY.md
  - COMPLETED_FEATURES.md
  - IMPLEMENTATION_PROGRESS.md
  - UPDATE_GUIDE.md
  - INTERACTIVE_DEMO.md

- Test directories:
  - All customer-*-test-ADRs/ directories
  - Debug and development test outputs

- Python cache:
  - scripts/__pycache__/

### Fixed

- **Google Docs Spacing** - Removed extra blank lines between product headings and tables
- **Bold Markdown Pattern** - Fixed regex to correctly match `**text**` patterns
- **Pattern Overlap** - Prevented conflicts between `#TODO#` and `**bold**` patterns
- **Index Calculation** - Proper tracking of text insertion shifts in Google Docs
- **Retry Logic** - Proper exception handling for rate limits (429 errors)

## Statistics

### Code Coverage
- **Scripts:** 5 Python automation scripts
- **Tests:** 8 automated test functions
- **ADR Templates:** 291 across 19 products
- **Documentation:** 10+ comprehensive guides

### Time Savings
- **Setup:** ~5 minutes (with Google API)
- **Generate ADR Pack:** ~2 minutes
- **Workshop:** 2-4 hours (collaborative in Google Docs)
- **Validation:** ~2 minutes
- **Export:** ~1 minute
- **Total time savings vs manual:** ~5 hours per engagement

## Product Coverage

291 ADR templates across 19 products:
- OCP-NET (41), OCP-BM (28), RHOAI-SM (24), VIRT (23)
- OCP-STOR (22), ODF (18), OCP-SEC (17), OCP-MGT (16)
- OCP-OSP (16), OCP-BASE (15), OCP-MON (13), LOG (12)
- OCP-HCP (10), PIPELINES (8), NVIDIA-GPU (7), TRACING (7)
- GITOPS (6), NETOBSERV (4), POWERMON (4)

## Technical Achievements

- **Google Docs API** - Full integration with retry logic
- **OAuth 2.0** - Secure credential management
- **2-Column Tables** - Advanced formatting with fixed column widths
- **Text Styling** - Bold, colors (red, yellow), backgrounds
- **Pattern Matching** - Regex for `#TODO#` and `**bold**` processing
- **Rate Limiting** - Graceful handling with automatic retries
- **Data Protection** - Customer data never committed to git
- **Dual Mode** - Seamless online/offline operation

---

**Contributors:** Laurent TOURREAU, Claude AI (Anthropic)
**License:** Red Hat Consulting Deliverables
