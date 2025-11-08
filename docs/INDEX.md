# Documentation Index

**Memova Documentation v3.2.0**  
**Last Updated**: November 6, 2025  
**Methodology**: Context Engineering

---

## �️ **NEW: Documentation Map**

**Lost? Not sure which doc to update?**  
→ Read [Documentation Map](00-DOCUMENTATION-MAP.md) first!

This map explains:
- Purpose of each documentation file
- When to update which doc
- Complete documentation workflow
- Critical update checklist

---

## �📖 Start Here

**New to Memova?** → [Quickstart Guide](01-getting-started/quickstart.md)  
**Want to understand the system?** → [Architecture Overview](02-architecture/system-overview.md)  
**Need API docs?** → [API Reference](05-api/endpoints.md)  
**Want to contribute?** → [Development Setup](04-development/setup.md)

---

## 📂 Documentation Structure

### 01. Getting Started
For users and first-time setup
- [Quickstart Guide](01-getting-started/quickstart.md) - 5-minute setup
- Installation Guide *(coming soon)*
- First Query Tutorial *(coming soon)*

### 02. Architecture
System design and technical decisions
- [System Overview](02-architecture/system-overview.md) - High-level architecture
- Data Flow Diagram *(coming soon)*
- Tech Stack Details *(coming soon)*
- Design Decisions *(coming soon)*

### 03. Features
Feature-by-feature documentation
- [Natural Language Querying](03-features/natural-language.md) - AI-powered queries
	- Sidebar Quick Query Shortcuts (Easy/Medium/Hard)
- [Intelligent Problem-Solving](03-features/intelligent-problem-solving.md) - Business analyst for vague problems 🆕 v3.2.0
- [Charts & AI Insights](03-features/charts-insights.md) - Auto-charting + trend detection 🆕
- [Keyboard Shortcuts](03-features/keyboard-shortcuts.md) - Power user shortcuts
- [Settings](03-features/settings.md) - User preferences
- Multi-Database Support *(coming soon)*

### 04. Development
For contributors and developers
- [Development Setup](04-development/setup.md) - Complete dev environment
- Coding Standards *(coming soon)*
- Testing Guide *(coming soon)*
- Contributing Guide *(coming soon)*

### 05. API
REST API reference
- [Endpoints](05-api/endpoints.md) - All API endpoints
- Request/Response Schemas *(coming soon)*
- Error Handling *(coming soon)*

### 06. Database
Database schemas and data
- [Electronics Schema](06-database/electronics_schema.md) - 12 tables
- [Airline Schema](06-database/airline_schema.md) - 16 tables
- [EdTech India Schema](06-database/edtech_schema.md) - 15 tables
- [EdNite Schema](06-database/ednite_schema.md) - Student test results (NEW v3.2.0)
- [Liqo Retail Schema](06-database/liqo_schema.md) - 5 tables, 37,857 transactions (NEW v3.3.0) 🆕
- Data Generation *(coming soon)*

### 07. Maintenance
Operations and deployment
- [Intelligent Analyst (2025-11-06)](07-maintenance/INTELLIGENT_ANALYST_2025-11-06.md) - Schema awareness fix ⭐ NEW
- [Prompt Caching Implementation](07-maintenance/CACHING_IMPLEMENTATION.md) - 98% token reduction 🆕
- [SQL Error Recovery](07-maintenance/SQL_ERROR_RECOVERY.md) - AI fixes SQL errors automatically 🆕
- [Changelog v3.3.0](07-maintenance/CHANGELOG.md) - Liqo database + domain validation 🆕
- Deployment Guide *(coming soon)*
- Troubleshooting *(coming soon)*

---

## 🔍 Quick Lookup

### By Task

| What do you want to do? | Go here |
|-------------------------|---------|
| Set up the project | [Quickstart](01-getting-started/quickstart.md) |
| Understand architecture | [System Overview](02-architecture/system-overview.md) |
| Use the API | [API Endpoints](05-api/endpoints.md) |
| Learn keyboard shortcuts | [Shortcuts](03-features/keyboard-shortcuts.md) |
| Configure settings | [Settings](03-features/settings.md) |
| Contribute code | [Development Setup](04-development/setup.md) |
| Check database schema | Database Docs (06-database/) |
| Run tests | [Development Setup](04-development/setup.md#testing) |
| Optimize performance | [Caching Implementation](07-maintenance/CACHING_IMPLEMENTATION.md) |

### By Role

**End User**:
1. [Quickstart Guide](01-getting-started/quickstart.md)
2. [Keyboard Shortcuts](03-features/keyboard-shortcuts.md)
3. [Settings](03-features/settings.md)

**Developer**:
1. [Development Setup](04-development/setup.md)
2. [System Overview](02-architecture/system-overview.md)
3. [API Reference](05-api/endpoints.md)

**Data Analyst**:
1. [Natural Language Queries](03-features/natural-language.md)
2. [Charts & AI Insights](03-features/charts-insights.md) 🆕
3. Database Schemas (06-database/)
4. [API Reference](05-api/endpoints.md)

**DevOps**:
1. Deployment Guide *(coming soon)*
2. Troubleshooting *(coming soon)*
3. [System Overview](02-architecture/system-overview.md)

---

## 📝 Documentation Philosophy

This documentation follows **Context Engineering** principles:

1. **Nested Structure** - Organized by topic, not chronology
2. **Single Source of Truth** - One place for each concept
3. **Concise Over Verbose** - Essential information only
4. **Cross-Referenced** - Links between related topics
5. **Always Updated** - Code changes = doc changes

**Why?** AI assistants (and humans) have limited context windows. Well-organized docs = faster development.

---

## 📚 Archive

Legacy documentation moved to `archive/` for reference:

- `archive/task-completions/` - Historical task completion logs (TASK_5, 6, 7)
- `archive/old-structure/` - Previous flat documentation structure
- `archive/` - Other legacy files

**Rule**: Never delete documentation. Archive with timestamp and reason.

---

## 🔄 Documentation Updates

### When to Update Docs

- ✅ **Before coding** - Review relevant docs for context
- ✅ **After coding** - Update docs with changes
- ✅ **Before PR** - Ensure docs reflect new code
- ✅ **After release** - Update changelog and version numbers

### What to Update

| Code Change | Update These Docs |
|-------------|-------------------|
| New API endpoint | `05-api/endpoints.md` |
| New feature | `03-features/` (new file) |
| Architecture change | `02-architecture/system-overview.md` |
| Database schema | `06-database/` |
| Dev environment | `04-development/setup.md` |
| Bug fix | Changelog *(coming soon)* |

---

## 🎯 Context Engineering Workflow

### For AI Assistants (Like Me!)

1. **Read docs FIRST** before suggesting code changes
2. **Use grep/search** to find current implementation
3. **Update docs** immediately after code changes
4. **Never rely on memory** - trust the documentation

### For Humans

1. **Check docs** before asking questions
2. **Update docs** when you fix something
3. **Add examples** to help future developers
4. **Keep it concise** - quality over quantity

---

## 📊 Documentation Metrics

- **Total Docs**: 12+ files (7 directories)
- **Average Read Time**: 3-5 minutes per doc
- **Coverage**: All core features documented
- **Last Full Audit**: October 31, 2025
- **Next Review**: When v3.0.0 is planned

---

## 🤝 Contributing to Docs

Found an error? Want to improve something?

1. Read the doc you want to improve
2. Make changes (follow existing style)
3. Update this INDEX.md if adding new files
4. Submit PR with clear description

**Style Guide**:
- Use Markdown
- Add code examples
- Include command outputs
- Link related docs
- Keep it concise

---

## 🆘 Need Help?

- **Can't find what you need?** - Check [Search](#-quick-lookup) above
- **Found a bug in docs?** - Open an issue
- **Want to contribute?** - See Contributing Guide *(coming soon)*

---

**Built with ❤️ using Context Engineering**

*Remember: Documentation is code. Treat it with the same care.*
