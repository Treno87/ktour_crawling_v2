# Ktourstory Reservation Crawler Project

## 📋 Project Overview

Python-based web crawler that scrapes reservation data from [ktourstory guide site](https://guide.ktourstory.com/) and automatically saves to Google Sheets.

### Tech Stack

- **Runtime**: Python 3.13+
- **Browser Control**: SeleniumBase (uc=True) + Playwright (Hybrid)
- **Data Storage**: gspread (Google Sheets API)
- **Testing**: pytest
- **Environment**: python-dotenv

### Architecture

**Hybrid Browser Control**
- SeleniumBase's `uc=True` mode bypasses bot detection
- Playwright connects via CDP for stable page control
- Best combination of evasion capability and modern API

## 🎯 Core Development Principles

All code in this project follows:
- **TDD**: RED → GREEN → REFACTOR cycle (see @tdd.md)
- **Kent Beck's 4 Rules**: See @agents.md (always applied)
- **Clean Code**: See @clean-code.md (reference during refactoring)
- **Tidy First**: Separate structural and behavioral changes (see @agents.md)

## 🛠️ Custom Commands

### TDD Workflow

- `/verify`: Run tests only (no revert on failure)
  - Check current state

- `/tcr`: Test && Commit || Revert
  - Test passes → auto commit
  - Test fails → auto revert
  - Extreme TDD practice

### Refactoring Workflow

- `/beck`: Analyze code with Beck's 4 rules (suggestions only)
  - Identify improvement opportunities

- `/refactor`: Execute refactoring immediately
  - Apply `/beck` analysis results

- `/tidy`: Clean code and commit immediately
  - Structural changes only, no behavior change
  - Commit with `[Tidy]` prefix

## 📁 Project Structure

```
ktoure_crawling/
├── .claude/
│   ├── CLAUDE.md         # This file - project overview
│   ├── agents.md         # Kent Beck principles (always applied)
│   ├── clean-code.md     # Code quality reference
│   └── tdd.md            # TDD cycle reference
├── config.py              # Environment variables and settings
├── browser_controller.py  # Hybrid browser setup
├── scraper.py            # Login, date selection, data extraction
├── gsheets_client.py     # Google Sheets integration
├── main.py               # Full pipeline integration
├── test_scraper.py       # Scraping logic tests
├── test_gsheets_client.py # Google Sheets tests
├── .env                  # Environment variables (gitignored)
└── credentials.json      # Google API credentials (gitignored)
```

## 🔄 Workflows

### Adding New Features

1. **Analyze Requirements**: Clarify what to build
2. **Write Test** (RED): Start with failing test
3. **Minimal Implementation** (GREEN): Just pass the test
4. **Refactor** (REFACTOR): Improve code, separate commit
5. **Update Docs**: README.md, comments if needed

### Fixing Bugs

1. **Write Reproduction Test**: Test that reveals the bug
2. **Fix**: Make test pass
3. **Prevent Regression**: Test prevents future occurrence

### Refactoring

1. **Verify Tests Pass**: Only refactor in green state
2. **Improve Structure**: No behavior changes
3. **Re-run Tests**: Verify still passing
4. **Separate Commit**: Format as `[Tidy] Remove duplication`

## ⚠️ Critical Rules

### Never Do

- ❌ Write production code without tests
- ❌ Mix feature changes + refactoring in one commit
- ❌ Create unnecessary documentation files (unless requested)
- ❌ Commit with failing tests
- ❌ Commit credentials.json to git

### Always Do

- ✅ Explain before making changes (Korean)
- ✅ Clear commit messages ([Tidy]/[Feature]/[Fix])
- ✅ Write one test at a time
- ✅ Refactor only after tests pass
- ✅ Manage secrets via `.env` file

## 🧪 Testing Guide

### Test Priority

1. **Core Scraping Logic**: All functions in `scraper.py`
2. **Google Sheets Integration**: `save_to_sheet` function
3. **Browser Setup**: `setup_browser` function
4. **Config Loading**: `config.py`

### Running Tests

```bash
# All tests
pytest -v

# Specific file
pytest test_scraper.py -v

# With coverage
pytest --cov=. --cov-report=html
```

## 💡 Project-Specific Tips

### Selector Management

```python
# Bad: Magic strings
page.locator("button.MuiButtonBase-root.css-ab6e07").click()

# Good: Use constants
DATE_BUTTON_SELECTOR = "button.MuiButtonBase-root.css-ab6e07"
page.locator(DATE_BUTTON_SELECTOR).click()
```

### Error Handling

```python
# Clear error messages
try:
    worksheet.append_row(row)
except Exception as e:
    raise Exception(f"Failed to save to Google Sheets: {e}") from e
```

### Environment Variables First

```python
# Bad: Hardcoded
LOGIN_ID = "user@example.com"

# Good: From environment
LOGIN_ID = os.getenv("LOGIN_ID", "")
```

## 🗣️ Communication Style

**Code and Documentation**: English
**Explanations and Questions**: Korean (한국어)

When working:
- Write code comments in English
- Keep variable/function names in English
- Write commit messages in English
- **Explain changes in Korean** (한국어로 설명)
- **Ask questions in Korean** (한국어로 질문)

## 📚 Context Loading Strategy

**Progressive Disclosure**: Load additional context only when needed

- **Always loaded**: This file + @agents.md + @tdd.md + @clean-code.md
- **Module-specific**: Load `<module>/.claude/CLAUDE.md` when working on that module
- **Feature-specific**: Create temporary context files for complex features

Example:
```
scraper/.claude/CLAUDE.md  → Load when working on scraper module
gsheets/.claude/CLAUDE.md  → Load when working on Google Sheets
```
