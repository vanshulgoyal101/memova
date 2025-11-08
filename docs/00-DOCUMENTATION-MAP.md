# Documentation Map

**Purpose**: Master reference for understanding Memova's documentation structure  
**Audience**: AI assistants, developers, contributors  
**Last Updated**: November 6, 2025  
**Methodology**: Context Engineering

---

## 📋 Quick Reference: When to Update What

| I Changed... | Update These Docs |
|--------------|-------------------|
| **Code architecture** | `02-architecture/system-overview.md` + `.github/copilot-instructions.md` |
| **API endpoints** | `05-api/endpoints.md` |
| **Database schema** | `06-database/electronics_schema.md` or `airline_schema.md` |
| **Setup process** | `01-getting-started/quickstart.md` + `04-development/setup.md` |
| **New feature** | Create new doc in `03-features/` + update `INDEX.md` |
| **AI features** | `03-features/natural-language.md` + `02-architecture/system-overview.md` |
| **Charts/Insights** | `03-features/charts-insights.md` + `05-api/endpoints.md` |
| **Intelligent Problem-Solving** | `03-features/intelligent-problem-solving.md` (NEW v3.2.0) + `05-api/endpoints.md` |
| **Bug fix** | `07-maintenance/CHANGELOG.md` (if exists) |
| **Major refactoring** | Create `07-maintenance/REFACTORING_YYYY-MM-DD.md` + update architecture docs |
| **Tests** | `04-development/setup.md#testing` + `.github/copilot-instructions.md` |
| **Dependencies** | `04-development/setup.md` + `README.md` |
| **Build process** | `04-development/setup.md` + `.github/copilot-instructions.md` (Makefile section) |

---

## 📚 Complete Documentation Structure

### **Root Level**

#### `README.md` - Master Entry Point
- **Purpose**: First document users/developers see
- **Contains**: 
  - Project overview & philosophy
  - Quick links to all sections
  - Tech stack summary
  - "What is Memova?" explanation
- **Update When**: 
  - Major architecture changes
  - Tech stack changes
  - New major features added
  - Project philosophy evolves

#### `INDEX.md` - Navigation Hub
- **Purpose**: Comprehensive table of contents
- **Contains**: 
  - Links to all documentation
  - "Quick Lookup" by task
  - Section descriptions
- **Update When**: 
  - New documentation created
  - Documentation reorganized
  - New sections added

#### `.github/copilot-instructions.md` - AI Assistant Guide
- **Purpose**: Context Engineering instructions for AI
- **Contains**: 
  - Project structure (file tree)
  - Coding standards
  - Development workflow
  - Recent enhancements (version history)
  - Quick reference (ports, paths, env vars)
- **Update When**: 
  - **ANY** code structure changes
  - New modules/files created
  - Build process changes
  - Testing strategy changes
  - After EVERY refactoring

---

### **01-getting-started/** - User Onboarding

#### `quickstart.md` - 5-Minute Setup
- **Purpose**: Get project running ASAP
- **Audience**: New users, evaluators
- **Contains**: 
  - Prerequisites check
  - Installation steps
  - First run instructions
  - Troubleshooting basics
- **Update When**: 
  - Setup steps change
  - New prerequisites added
  - Installation process simplified
  - Common setup issues discovered

#### `installation.md` *(planned)*
- **Purpose**: Detailed installation for all platforms
- **Would Contain**: Platform-specific instructions, environment setup

#### `first-query.md` *(planned)*
- **Purpose**: Interactive tutorial for first-time users
- **Would Contain**: Step-by-step query walkthrough

---

### **02-architecture/** - System Design

#### `system-overview.md` - High-Level Architecture ⭐
- **Purpose**: Complete system architecture documentation
- **Contains**: 
  - Architecture diagrams (ASCII art)
  - Tech stack details
  - Component structure (frontend + backend file trees)
  - Data flow diagrams
  - Key design decisions
  - Security considerations
  - Performance metrics
  - Scalability considerations
  - **Modular architecture section** (NEW - QueryEngine refactoring)
- **Update When**: 
  - ✅ **CRITICAL**: File structure changes (add/remove modules)
  - ✅ **CRITICAL**: Architecture refactoring (split/merge components)
  - New components added
  - Tech stack changes
  - Design patterns change
  - Performance characteristics change
  - Security model changes

#### `data-flow.md` *(planned)*
- **Purpose**: Detailed sequence diagrams for request/response flows

#### `tech-stack.md` *(planned)*
- **Purpose**: Deep dive into each technology choice

#### `design-decisions.md` *(planned)*
- **Purpose**: ADRs (Architecture Decision Records)

---

### **03-features/** - Feature Documentation

#### `natural-language.md` - AI Query Feature
- **Purpose**: How AI-powered querying works
- **Contains**: 
  - Feature description
  - How it works (Gemini integration)
  - Example queries
  - Limitations
- **Update When**: 
  - AI model changes (e.g., Gemini -> GPT)
  - Query processing logic changes
  - New capabilities added

#### `keyboard-shortcuts.md` - Productivity Shortcuts
- **Purpose**: Power user keyboard shortcuts
- **Contains**: 
  - Complete shortcut list
  - Usage examples
  - Implementation details
- **Update When**: 
  - New shortcuts added
  - Shortcuts changed
  - Conflicts resolved

#### `settings.md` - User Preferences
- **Purpose**: Configurable user settings
- **Contains**: 
  - Available settings
  - Default values
  - Storage mechanism (localStorage)
- **Update When**: 
  - New settings added
  - Settings behavior changes
  - Storage mechanism changes

#### `multi-database.md` *(planned)*
- **Purpose**: How multi-database switching works

---

### **04-development/** - Developer Guides

#### `setup.md` - Dev Environment Setup ⭐
- **Purpose**: Complete development setup instructions
- **Contains**: 
  - System requirements
  - Installation steps
  - Project structure overview
  - Build commands (`make` targets)
  - Testing instructions
  - Code structure details
  - **File line counts and sizes**
- **Update When**: 
  - ✅ **CRITICAL**: New dependencies added
  - ✅ **CRITICAL**: Build process changes
  - ✅ **CRITICAL**: Project structure changes
  - Testing strategy changes
  - Development workflow changes
  - New make targets added

#### `coding-standards.md` *(planned)*
- **Purpose**: Code style guide, naming conventions, best practices

#### `testing.md` *(planned)*
- **Purpose**: Testing philosophy, how to write tests, coverage requirements

#### `contributing.md` *(planned)*
- **Purpose**: How to contribute, PR process, code review guidelines

---

### **05-api/** - API Reference

#### `endpoints.md` - REST API Reference ⭐
- **Purpose**: Complete API documentation
- **Contains**: 
  - All endpoints with request/response schemas
  - Error codes
  - Example requests/responses
  - Authentication (if any)
- **Update When**: 
  - ✅ **CRITICAL**: New endpoints added
  - ✅ **CRITICAL**: Endpoint signatures change
  - Request/response format changes
  - New error codes added
  - Authentication changes

#### `request-response.md` *(planned)*
- **Purpose**: Detailed request/response schemas

#### `error-handling.md` *(planned)*
- **Purpose**: Error codes, handling strategies

---

### **06-database/** - Database Schemas

#### `electronics_schema.md` - Electronics Company Schema
- **Purpose**: Complete schema documentation for electronics database
- **Contains**: 
  - All tables with columns, types, constraints
  - Relationships (foreign keys)
  - Sample data counts
  - Auto-generated from database
- **Update When**: 
  - Schema changes (new tables, columns)
  - Data generation logic changes
  - Relationships change

#### `airline_schema.md` - Airline Company Schema
- **Purpose**: Complete schema documentation for airline database
- **Contains**: Same as electronics_schema.md
- **Update When**: Same as electronics_schema.md

#### `data-generation.md` *(planned)*
- **Purpose**: How synthetic data is generated

---

### **07-maintenance/** - Operations & History

#### `INTELLIGENT_ANALYST_2025-11-06.md` - Schema Awareness Fix & UX Improvements ⭐ NEW
- **Purpose**: Document critical fix for AI query hallucination
- **Contains**: 
  - Problem analysis (0-20% query success rate)
  - Solution (schema embedding in prompts)
  - Before/after test results (80-100% success)
  - Token impact analysis (trade-offs)
  - UX improvements (fallback messages)
- **Update When**: Never (historical record)

#### `REFACTORING_2025-10-31.md` - QueryEngine Refactoring Log
- **Purpose**: Document major refactoring (query_engine.py split)
- **Contains**: 
  - Motivation, strategy, execution
  - Before/after comparison
  - Test results
  - Migration guide
  - Lessons learned
- **Update When**: Never (historical record)

#### `TESTING_STRATEGY.md` - Test Strategy Document
- **Purpose**: How to handle API rate limits in tests
- **Contains**: 
  - Problem description
  - Solution strategy
  - Implementation guide
- **Update When**: Testing strategy evolves

#### `TEST_FIX_2025-10-31.md` - Test Fix Log
- **Purpose**: Document test suite fixes
- **Contains**: 
  - Current test status
  - Issues discovered
  - Fixes applied
- **Update When**: Never (historical record)

#### `deployment.md` *(planned)*
- **Purpose**: Production deployment instructions

#### `troubleshooting.md` *(planned)*
- **Purpose**: Common issues and solutions

#### `changelog.md` *(planned)*
- **Purpose**: Version history, release notes

---

### **archive/** - Historical Documentation

#### Purpose
- Preserve old documentation for reference
- Never delete (Context Engineering principle)
- Useful for understanding evolution

#### Key Files
- `old-structure/ARCHITECTURE.md` - Pre-reorganization architecture
- `task-completions/TASK_*.md` - Historical task completion logs
- `REORGANIZATION_2025-10-31.md` - Documentation reorganization record

#### Update When
- Never modify archived docs
- Only add new docs when major changes occur

---

## 🔄 Documentation Update Workflow

### Step 1: Before Coding
1. **Read** `README.md` to understand project
2. **Read** `INDEX.md` to find relevant docs
3. **Read** specific docs (e.g., `system-overview.md`)
4. **Check** `.github/copilot-instructions.md` for latest structure

### Step 2: During Coding
5. Make changes incrementally
6. Note which docs need updating

### Step 3: After Coding (CRITICAL!)
7. **Update documentation IMMEDIATELY**:
   - If changed **architecture**: Update `system-overview.md` + `copilot-instructions.md`
   - If changed **API**: Update `endpoints.md`
   - If changed **setup**: Update `setup.md` + `quickstart.md`
   - If changed **database**: Regenerate schema docs
   - If **major refactoring**: Create `07-maintenance/REFACTORING_YYYY-MM-DD.md`
8. **Update** `INDEX.md` if new docs created
9. **Update** `README.md` if major features/tech stack changed
10. **Commit** code + docs together

---

## 🎯 Critical Documentation Principles

### 1. Documentation = Single Source of Truth
- **Never** rely on memory or conversation history
- **Always** read docs before coding
- **Always** update docs after coding

### 2. Nested Structure for Scalability
- Group related docs in folders
- Use clear naming conventions (01-, 02-, etc.)
- Cross-reference between docs

### 3. Rich Metadata
- Include version numbers, dates
- Mark status (✅ complete, ⏳ planned, ❌ deprecated)
- Use emojis for visual scanning

### 4. Keep Archives Forever
- Never delete old docs
- Move to `archive/` when superseded
- Helps understand evolution

---

## 📊 Documentation Health Checklist

After ANY code change, ask:

- [ ] Did I update `02-architecture/system-overview.md` if structure changed?
- [ ] Did I update `.github/copilot-instructions.md` if files added/removed?
- [ ] Did I update `05-api/endpoints.md` if API changed?
- [ ] Did I update `04-development/setup.md` if build/test process changed?
- [ ] Did I create maintenance log for major refactoring?
- [ ] Did I update `INDEX.md` if new docs created?
- [ ] Did I commit docs with code changes?

---

**This map is the meta-documentation.** Read this first when you're unsure which doc to update!
