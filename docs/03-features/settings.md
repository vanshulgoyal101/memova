# User Settings

**Feature**: Persistent user preferences  
**Status**: ✅ Production Ready  
**Added**: v2.0.0 (Task 7)

---

## Overview

Users can configure 5 preferences that persist across sessions using browser localStorage. Settings are applied on page load and after each query.

---

## Available Settings

### 1. Default Company
**Options**: Electronics Company | Airline Company  
**Purpose**: Sets which database loads on app start  
**Storage Key**: `memova_default_company`  
**Default**: Electronics Company

**Behavior**:
- Applies immediately on change
- Updates sidebar selection
- Clears previous query results
- Persists to localStorage

---

### 2. Default Sections
**Options**: All Sections | Inventory | Sales | HR | Customers | etc.  
**Purpose**: Filter queries to specific table groups  
**Storage Key**: `memova_default_sections`  
**Default**: All Sections

**Behavior**:
- Changes available tables for AI context
- Applies to all future queries
- Can select multiple sections
- Cleared on company switch

---

### 3. Auto-Expand SQL Accordion
**Options**: On | Off  
**Purpose**: Automatically expand SQL accordion in results  
**Storage Key**: `memova_auto_expand_sql`  
**Default**: Off

**Behavior**:
- Applies after each query
- Shows SQL immediately without clicking
- Useful for developers/power users

---

### 4. Auto-Expand Data Accordion
**Options**: On | Off  
**Purpose**: Automatically expand data table accordion  
**Storage Key**: `memova_auto_expand_data`  
**Default**: Off

**Behavior**:
- Applies after each query
- Shows raw data immediately
- Useful for data analysts

---

### 5. Compact Mode
**Options**: On | Off  
**Purpose**: Reduce spacing for more content on screen  
**Storage Key**: `memova_compact_mode`  
**Default**: Off

**Behavior**:
- Reduces padding on answer panel
- Smaller card spacing
- More vertical space for data
- Applies immediately

**Visual Changes**:
- Normal: `p-6` padding
- Compact: `p-4` padding
- Card gap: `8` → `4`

---

## Settings Dialog

### Opening
- **Keyboard**: `Shift+S`
- **Click**: Settings icon in navbar
- **Button**: Settings button in sidebar

### Interface
```
┌─────────────────────────────────────┐
│  Settings                        ×  │
├─────────────────────────────────────┤
│                                     │
│  Default Company                    │
│  ┌─────────────────────────────┐   │
│  │  Electronics Company     ▼  │   │
│  └─────────────────────────────┘   │
│                                     │
│  Default Sections                   │
│  ┌─────────────────────────────┐   │
│  │  All Sections            ▼  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ☑ Auto-expand SQL accordion       │
│  ☑ Auto-expand data table          │
│  ☐ Compact mode                    │
│                                     │
│          [ Save Settings ]          │
└─────────────────────────────────────┘
```

### Closing
- Click "Save Settings" button
- Click X in top-right
- Press `Escape`
- Click outside dialog (backdrop)

All methods save changes automatically.

---

## Implementation Details

### localStorage Keys
```typescript
const STORAGE_KEYS = {
  defaultCompany: 'memova_default_company',
  defaultSections: 'memova_default_sections',
  autoExpandSql: 'memova_auto_expand_sql',
  autoExpandData: 'memova_auto_expand_data',
  compactMode: 'memova_compact_mode'
};
```

### Settings Object
```typescript
interface UserSettings {
  defaultCompany: 'electronics' | 'airline';
  defaultSections: string[];
  autoExpandSql: boolean;
  autoExpandData: boolean;
  compactMode: boolean;
}
```

### Storage Functions
Located in `frontend/src/lib/settings.ts`:

```typescript
// Save settings
export function saveSettings(settings: UserSettings): void {
  if (typeof window === 'undefined') return; // SSR safety
  
  localStorage.setItem(
    STORAGE_KEYS.defaultCompany, 
    settings.defaultCompany
  );
  localStorage.setItem(
    STORAGE_KEYS.defaultSections, 
    JSON.stringify(settings.defaultSections)
  );
  // ... etc
}

// Load settings
export function loadSettings(): UserSettings {
  if (typeof window === 'undefined') {
    return DEFAULT_SETTINGS; // SSR fallback
  }
  
  return {
    defaultCompany: localStorage.getItem(STORAGE_KEYS.defaultCompany) 
      ?? 'electronics',
    defaultSections: JSON.parse(
      localStorage.getItem(STORAGE_KEYS.defaultSections) ?? '["all"]'
    ),
    // ... etc
  };
}
```

---

## Lifecycle

### 1. Page Load
```typescript
useEffect(() => {
  const settings = loadSettings();
  
  // Apply default company
  setScope({
    company: settings.defaultCompany,
    sections: settings.defaultSections
  });
  
  // Store other settings in state
  setAutoExpandSql(settings.autoExpandSql);
  setAutoExpandData(settings.autoExpandData);
  setCompactMode(settings.compactMode);
}, []);
```

### 2. After Query
```typescript
useEffect(() => {
  if (result && settings.autoExpandSql) {
    // Expand SQL accordion programmatically
    setSqlExpanded(true);
  }
  if (result && settings.autoExpandData) {
    setDataExpanded(true);
  }
}, [result, settings]);
```

### 3. On Settings Change
```typescript
const handleSaveSettings = () => {
  const newSettings = {
    defaultCompany,
    defaultSections,
    autoExpandSql,
    autoExpandData,
    compactMode
  };
  
  saveSettings(newSettings);
  setSettingsOpen(false);
  
  // Apply immediately
  applySettings(newSettings);
};
```

---

## Data Persistence

### Storage Location
- **Browser**: localStorage (client-side only)
- **Scope**: Per domain/origin
- **Size Limit**: ~5-10 MB
- **Expiration**: Never (until cleared)

### When Data is Lost
- User clears browser data
- Private/incognito mode (cleared on close)
- Different browser/device
- Different URL (e.g., localhost vs production)

---

## Privacy & Security

### What is Stored
- ✅ UI preferences only
- ✅ No personal data
- ✅ No query history
- ✅ No authentication tokens

### Data Access
- ✅ Stays in browser (never sent to server)
- ✅ Only JavaScript on same origin can read
- ✅ Not accessible from other websites
- ✅ User can inspect/clear via browser DevTools

---

## Testing

### Manual Testing
1. Open settings (Shift+S)
2. Change all 5 preferences
3. Click "Save Settings"
4. Refresh page (Cmd+R)
5. Verify settings persist
6. Clear localStorage (DevTools)
7. Verify defaults restored

### Automated Tests
```typescript
// tests/integration/test_settings.spec.ts
test('settings persist across page reloads', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Open settings
  await page.keyboard.press('Shift+S');
  
  // Change company
  await page.selectOption('[name="company"]', 'airline');
  
  // Enable compact mode
  await page.check('[name="compactMode"]');
  
  // Save
  await page.click('button:has-text("Save Settings")');
  
  // Reload
  await page.reload();
  
  // Verify company changed
  expect(await page.textContent('.sidebar')).toContain('Airline');
});
```

---

## Troubleshooting

### Settings Not Persisting
**Cause**: localStorage disabled or in private mode  
**Solution**: Use regular browser window

### Settings Reset on Refresh
**Cause**: Different domain (e.g., localhost vs 127.0.0.1)  
**Solution**: Use same URL consistently

### Settings Not Applying
**Cause**: JavaScript error preventing load  
**Solution**: Check browser console (F12)

---

## Future Enhancements

### Planned
- ✨ Export/import settings (JSON file)
- ✨ Sync settings across devices (cloud storage)
- ✨ More preferences (font size, animations)
- ✨ Reset to defaults button

### Under Consideration
- User accounts (server-side preferences)
- Settings versioning (migration on update)
- Settings presets (Analyst, Developer, Manager)

---

## Related Documentation

- [Keyboard Shortcuts](keyboard-shortcuts.md) - `Shift+S` to open settings
- [Natural Language](natural-language.md) - Auto-expand affects query results
- [Multi-Database](multi-database.md) - Default company preference

---

**Last Updated**: October 31, 2025
