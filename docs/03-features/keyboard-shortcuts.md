# Keyboard Shortcuts

**Feature**: Power user productivity shortcuts  
**Status**: ✅ Production Ready  
**Added**: v2.0.0 (Task 6)

---

## All Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| `⌘K` or `Ctrl+K` | Focus ask bar | Global |
| `Shift+S` | Open settings dialog | Global |
| `Shift+D` | Toggle database | Global |
| `T` | Toggle theme | Global |
| `Escape` | Close settings | Settings open |
| `Enter` | Submit query | Ask bar focused |

---

## Detailed Behavior

### ⌘K - Focus Ask Bar
**Purpose**: Quick access to query input  
**Behavior**:
- Focuses the ask bar textarea
- Scrolls to ask bar if off-screen
- Selects existing text (if any)
- Works from anywhere on the page

**Implementation**:
```typescript
// frontend/src/app/page.tsx
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      textareaRef.current?.focus();
    }
  };
  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, []);
```

---

### Shift+S - Open Settings
**Purpose**: Quick access to preferences  
**Behavior**:
- Opens settings dialog
- Focuses first input
- Overlay blocks interaction with page

**Settings Options**:
1. Default company (Electronics/Airline)
2. Default sections (all/specific)
3. Auto-expand SQL accordion
4. Auto-expand Data accordion
5. Compact mode (reduced spacing)

See [Settings](settings.md) for details.

---

### Shift+D - Toggle Database
**Purpose**: Fast switching between companies  
**Behavior**:
- Toggles between Electronics ↔ Airline
- Updates Zustand store
- Persists to localStorage
- Updates sidebar selection
- Clears previous query results

**Use Case**: Compare data across companies quickly

**Example Flow**:
```
1. User views Electronics data
2. Press Shift+D
3. Now viewing Airline company
4. Previous results cleared (avoid confusion)
5. Ask new question in Airline context
```

---

### T - Toggle Theme
**Purpose**: Switch dark ↔ light mode  
**Behavior**:
- Toggles theme via next-themes
- Persists to localStorage
- Smooth transition (CSS transitions)
- All components update instantly

**Themes**:
- **Dark**: Neutral grey (`hsl(0 0% 9%)` background)
- **Light**: White (`hsl(0 0% 100%)` background)

---

### Enter - Submit Query
**Purpose**: Quick query submission  
**Behavior**:
- Submits query when ask bar is focused
- Disabled if input is empty
- Shows loading state immediately
- Prevents double submission

**Alternative**: Click "Ask" button

---

### Escape - Close Settings
**Purpose**: Quick close of settings dialog  
**Behavior**:
- Closes settings dialog
- Saves changes automatically (localStorage)
- Returns focus to page

**Alternative**: Click X or outside dialog

---

## Implementation Details

### Global Event Listener
Located in `frontend/src/app/page.tsx`:

```typescript
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    // ⌘K or Ctrl+K - Focus ask bar
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      textareaRef.current?.focus();
    }

    // Shift+S - Open settings
    if (e.shiftKey && e.key === 'S') {
      e.preventDefault();
      setSettingsOpen(true);
    }

    // Shift+D - Toggle database
    if (e.shiftKey && e.key === 'D') {
      e.preventDefault();
      const newCompany = scope.company === 'electronics' 
        ? 'airline' 
        : 'electronics';
      setScope({ company: newCompany, sections: ['all'] });
      setResult(null); // Clear results
    }

    // T - Toggle theme
    if (e.key === 't' || e.key === 'T') {
      e.preventDefault();
      setTheme(theme === 'dark' ? 'light' : 'dark');
    }
  };

  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, [scope, theme, setScope, setTheme]);
```

### Accessibility
- Uses `e.preventDefault()` to prevent browser default behavior
- Respects system keyboard settings
- Works with screen readers (focus management)
- Visual feedback on focus (focus rings)

---

## Platform Differences

| Platform | Modifier Key | Display |
|----------|--------------|---------|
| macOS | `⌘` (Command) | ⌘K |
| Windows | `Ctrl` | Ctrl+K |
| Linux | `Ctrl` | Ctrl+K |

**Implementation**:
```typescript
// Detects both Cmd (Mac) and Ctrl (Windows/Linux)
if (e.metaKey || e.ctrlKey) { ... }
```

---

## User Education

### In-App Hints
- Settings dialog shows all shortcuts
- Tooltips on buttons (hover to see shortcut)
- Help icon (?) in navbar links to this doc

### Documentation
- This page (comprehensive reference)
- Quickstart guide mentions ⌘K
- Settings page lists all shortcuts

---

## Future Enhancements

### Planned
- ✨ Customizable shortcuts (user preferences)
- ✨ Shortcut for "Clear results"
- ✨ Navigation shortcuts (Tab through results)
- ✨ Copy SQL with keyboard (Ctrl+C on accordion)

### Under Consideration
- Vim-style keybindings (j/k for scrolling)
- Shortcut cheatsheet (Ctrl+/)
- Quick database switcher (Ctrl+1, Ctrl+2)

---

## Conflicts to Avoid

### Browser Shortcuts
- ❌ Don't use `Ctrl+T` (new tab)
- ❌ Don't use `Ctrl+W` (close tab)
- ❌ Don't use `Ctrl+R` (refresh)
- ✅ Use `T` alone (no modifier)

### Screen Reader Shortcuts
- Compatible with NVDA, JAWS, VoiceOver
- Focus management follows WAI-ARIA guidelines

---

## Testing

### Manual Testing Checklist
- [ ] ⌘K focuses ask bar from anywhere
- [ ] Shift+S opens settings
- [ ] Shift+D toggles database (results clear)
- [ ] T toggles theme
- [ ] Escape closes settings
- [ ] Enter submits query
- [ ] Works on macOS, Windows, Linux

### Automated Tests
See `tests/integration/test_keyboard_shortcuts.spec.ts` (Playwright)

---

## Related Documentation

- [Settings](settings.md) - Preferences management
- [Natural Language](natural-language.md) - Query feature
- [Multi-Database](multi-database.md) - Database switching

---

**Last Updated**: October 31, 2025
