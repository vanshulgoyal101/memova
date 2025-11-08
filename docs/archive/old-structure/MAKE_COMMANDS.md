# Make Commands Reference

Quick reference for all available Make commands in the Multi-Company Database System.

## 🌐 Web Server Commands

### Start Server
```bash
make start
```
Starts both the FastAPI backend and opens the frontend in your browser.
- Backend runs on http://localhost:8000
- Frontend opens automatically in your default browser
- Checks for databases and generates them if missing

### Stop Server
```bash
make stop
```
Stops the running web server by killing all uvicorn processes.

### Restart Server
```bash
make restart
```
**Most useful command!** Does a complete restart:
1. ✅ Stops the web server
2. 🧹 Clears ALL Python cache:
   - `__pycache__` directories
   - `.pyc` files
   - `.pytest_cache`
3. 🚀 Restarts both frontend and backend

**Use this when:**
- Code changes aren't reflecting
- Getting import errors
- After pulling new code
- When you want a fresh start

## 📦 Setup Commands

### Install Dependencies
```bash
make install
```
Installs all Python packages from `requirements.txt`

### Setup Virtual Environment
```bash
make setup
```
Creates a new `.venv` virtual environment (doesn't install packages)

### Full Setup
```bash
make all
```
Runs `install` + `generate` - complete initial setup

## 🎲 Data Commands

### Generate Data
```bash
make generate
```
Generates all data:
- Excel files for both companies
- SQLite databases
- Schema documentation

## 🧪 Testing Commands

### Run Tests
```bash
make test
```
Runs the full test suite with pytest

### Run Tests with Coverage
```bash
make test-cov
```
Runs tests and generates HTML coverage report

## 🧹 Cleanup Commands

### Clean Generated Files
```bash
make clean
```
Removes:
- Excel files (`data/excel/*.xlsx`)
- Database files (`data/database/*.db`)
- Log files (`logs/*.log`)

### Clean Everything
```bash
make clean-all
```
Does `clean` plus removes all cache files

## 🔍 Other Commands

### Start Interactive Query
```bash
make query
```
Starts the CLI query interface

### View Schema
```bash
make docs
```
Displays the database schema documentation

### Show Help
```bash
make help
# or just
make
```
Shows all available commands

## 💡 Common Workflows

### Fresh Start After Code Changes
```bash
make restart
```

### Complete Reset
```bash
make clean-all
make generate
make start
```

### Development Workflow
```bash
# Initial setup
make all

# Start working
make start

# After making changes
make restart

# Before committing
make test
```

### Production Deployment
```bash
make setup
source .venv/bin/activate
make all
make test
make start
```

## 🐛 Troubleshooting

### "Module not found" errors
```bash
make restart
```

### "Database not found"
```bash
make generate
```

### "Port already in use"
```bash
make stop
make start
```

### Cache issues
```bash
make restart  # or make clean-all
```

### Tests failing
```bash
make clean-all
make install
make generate
make test
```

## 📊 Quick Command Reference

| Command | Purpose | Use When |
|---------|---------|----------|
| `make start` | Start web server | Want to use the UI |
| `make stop` | Stop web server | Done working |
| `make restart` | Restart + clear cache | **Most common!** Code changes not showing |
| `make install` | Install packages | First time setup |
| `make generate` | Generate data | Need fresh data |
| `make test` | Run tests | Before committing |
| `make clean` | Remove data | Want to regenerate |
| `make all` | Full setup | Initial installation |

## 🎯 One-Line Solutions

**Can't see my code changes?**
```bash
make restart
```

**Fresh installation?**
```bash
make all && make start
```

**Something broken?**
```bash
make stop && make clean-all && make all && make start
```

**Just want to test?**
```bash
make test
```

---

**Tip**: Run `make` or `make help` anytime to see all commands!
