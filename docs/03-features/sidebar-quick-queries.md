# Sidebar Quick Queries

**Feature**: One-click query shortcuts in the sidebar  
**Version**: 3.2.0  
**Last Updated**: November 7, 2025

---

## Overview

The sidebar provides **quick query shortcuts** for each database, categorized by difficulty level (Easy/Medium/Hard). These shortcuts allow users to instantly run common queries with a single click, improving productivity and helping users discover the system's capabilities.

---

## Design Philosophy

### User Experience Goals
1. **Discoverability**: New users can see example queries immediately
2. **Efficiency**: Power users can run common queries without typing
3. **Learning**: Query examples teach users what's possible
4. **Visual Hierarchy**: Color-coded difficulty badges guide users

### UI/UX Patterns
- **Pill-shaped buttons**: Left-aligned text, rounded corners
- **Difficulty badges**: Color-coded with icons (✨ Easy, ⚡ Medium, 🔥 Hard)
- **Micro-interactions**: Hover scale (1.01x), shadow transitions
- **Keyboard accessible**: Tab navigation, focus-visible ring
- **Responsive**: Touch targets ≥44px, vertical stacking on mobile

---

## Query Categories

### Electronics Company

#### Easy ✨
- "How many products are in inventory?"
- "Show all departments"
- "What are our top 5 selling products?"

#### Medium ⚡
- "What is our total revenue this month?"
- "Which products have low stock levels?"
- "Show customer satisfaction by product category"

#### Hard 🔥
- "Analyze revenue trends by product category over time"
- "Which customers generate the most revenue and what do they buy?"
- "Compare marketing campaign ROI across channels"
- "Identify products with declining sales and high inventory"
- "Show correlation between customer feedback and product returns"

---

### Airline Company

#### Easy ✨
- "How many aircraft are in the fleet?"
- "List all flight routes"
- "What flights depart today?"

#### Medium ⚡
- "Which routes have the highest passenger volume?"
- "Show average flight delay by route"
- "Compare cabin class revenue distribution"

#### Hard 🔥
- "Analyze seasonal trends in passenger bookings"
- "Which aircraft require the most maintenance and why?"
- "Compare on-time performance across different times of day"
- "Identify most profitable routes considering fuel and crew costs"
- "Show passenger satisfaction correlation with flight delays"

---

### EdTech India

#### Easy ✨
- "How many students are enrolled?"
- "List all active courses"
- "What are the most popular course categories?"

#### Medium ⚡
- "Which courses have the highest completion rates?"
- "Show revenue breakdown by course difficulty level"
- "Compare student performance across cities"

#### Hard 🔥
- "Analyze enrollment trends by demographics and location"
- "Which instructors have the best student outcomes?"
- "Compare placement rates across course categories and cities"
- "Identify factors correlating with course completion success"
- "Show revenue potential by expanding to untapped demographics"

---

### EdNite Test Results 🆕

#### Easy ✨
- "How many students took the test?"
- "Show me the top 10 students by score"
- "What is the average score across all students?"

#### Medium ⚡
- "Compare average scores between classes"
- "Which questions had the lowest correct answer rate?"
- "Show students who scored above 80%"

#### Hard 🔥
- "Give me insights on student performance across classes"
- "Analyze question difficulty patterns and identify challenging topics"
- "Find students who attempted many questions but scored low"
- "Compare Class 10 performance with Class 5 performance"
- "Identify questions where less than 30% students answered correctly"

---

## Implementation Details

### Component Location
`frontend/src/components/layout/sidebar.tsx`

### Query Shortcuts Data Structure
```typescript
const QUERY_SHORTCUTS = {
  electronics: {
    easy: [{ text: "Query text here" }, ...],
    medium: [...],
    hard: [...]
  },
  airline: { ... },
  edtech: { ... },
  ednite: { ... }
};
```

### Difficulty Badge Configuration
```typescript
const DIFFICULTY = {
  easy: { 
    label: "Easy", 
    color: "bg-green-500/15 text-green-700 dark:text-green-400", 
    icon: "✨" 
  },
  medium: { 
    label: "Medium", 
    color: "bg-yellow-500/15 text-yellow-700 dark:text-yellow-400", 
    icon: "⚡" 
  },
  hard: { 
    label: "Hard", 
    color: "bg-red-500/15 text-red-700 dark:text-red-400", 
    icon: "🔥" 
  },
};
```

### Event Dispatch Mechanism
When a query button is clicked:
```typescript
const handleQueryShortcut = (query: string) => {
  window.dispatchEvent(
    new CustomEvent('askbar-query-shortcut', { detail: query })
  );
};
```

The `AskBar` component listens for this event and populates the input field.

---

## Styling Details

### Button Styles
```css
className="w-full text-left px-3 py-2 rounded-lg 
  bg-muted/30 hover:bg-muted/50 
  text-xs font-medium 
  hover:scale-[1.01] 
  focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary/30 
  transition-all flex items-center gap-2 min-h-9"
```

### Key CSS Features
- **Background**: `bg-muted/30` (transparent overlay)
- **Hover**: `hover:bg-muted/50` (darker on hover)
- **Scale**: `hover:scale-[1.01]` (subtle zoom)
- **Focus**: `focus-visible:ring-1` (accessibility)
- **Min Height**: `min-h-9` (44px touch target)
- **Text**: `text-xs font-medium` (readable but compact)

---

## Accessibility

### ARIA Labels
```tsx
aria-label={`Run query: ${q.text}`}
```

### Keyboard Navigation
- All buttons are keyboard accessible (Tab key)
- Focus-visible ring shows current focus
- Enter/Space to activate

### Screen Readers
- Difficulty badges have proper aria-labels
- Button text is fully readable

---

## Adding New Queries

### Step 1: Add to QUERY_SHORTCUTS Object
```typescript
const QUERY_SHORTCUTS = {
  // ... existing companies
  newcompany: {
    easy: [
      { text: "Your easy query here" },
      { text: "Another easy query" },
    ],
    medium: [
      { text: "Your medium query here" },
    ],
    hard: [
      { text: "Your complex query here" },
    ],
  },
};
```

### Step 2: Update Company Type Check
```typescript
{(company === 'electronics' || company === 'airline' || company === 'edtech' || company === 'ednite' || company === 'newcompany') && 
  QUERY_SHORTCUTS[company as 'electronics' | 'airline' | 'edtech' | 'ednite' | 'newcompany'][level].map((q, idx) => (
    // ... button JSX
  ))
}
```

### Step 3: Test
- Select the new company from dropdown
- Verify queries appear in sidebar
- Click queries to ensure they populate AskBar

---

## Best Practices

### Query Writing Guidelines

1. **Easy Queries** (Green ✨)
   - Simple counts or lists
   - Single table queries
   - No complex conditions
   - Example: "How many X are there?"

2. **Medium Queries** (Yellow ⚡)
   - Aggregations (SUM, AVG)
   - JOINs across 2-3 tables
   - Simple GROUP BY
   - Example: "What is the average X by Y?"

3. **Hard Queries** (Red 🔥)
   - Multiple JOINs (3+ tables)
   - Complex WHERE clauses
   - Subqueries or CTEs
   - Analytical insights
   - Example: "Analyze X trends and identify Y patterns"

### Query Characteristics

- **Specific**: Clear, actionable questions
- **Relevant**: Match common use cases for the database
- **Diverse**: Cover different data aspects (counts, trends, comparisons)
- **Realistic**: Questions users would actually ask

---

## Performance Considerations

### Query Complexity
- Easy: <50ms execution time
- Medium: <200ms execution time
- Hard: <1s execution time

### UI Performance
- No re-renders when switching companies (memoization)
- Event dispatch is lightweight (custom DOM event)
- CSS transitions use GPU acceleration

---

## Future Enhancements

### Potential Features
1. **User-defined shortcuts**: Allow users to save custom queries
2. **Query history**: Show recently run queries
3. **Categories**: Group by business function (Sales, Operations, etc.)
4. **Search**: Filter queries by keyword
5. **Copy to clipboard**: Copy query text without running
6. **Favorites**: Star frequently used queries

---

## Testing

### Manual Test Checklist
- [ ] Queries appear for all 4 companies
- [ ] Click query → AskBar populates correctly
- [ ] Difficulty badges show correct colors
- [ ] Hover effects work smoothly
- [ ] Keyboard navigation works (Tab, Enter)
- [ ] Mobile view stacks vertically
- [ ] Dark/light theme colors are readable

### Automated Tests
Currently no automated tests for sidebar queries. Consider adding:
- Component rendering tests
- Event dispatch tests
- Accessibility tests (a11y)

---

## Related Documentation

- [Keyboard Shortcuts](keyboard-shortcuts.md) - Other keyboard shortcuts in the app
- [Natural Language Queries](natural-language.md) - How queries are processed
- [Settings](settings.md) - User preferences for default company

---

**Version**: 3.2.0  
**Component**: `frontend/src/components/layout/sidebar.tsx`  
**Last Updated**: November 7, 2025  
**Status**: ✅ Production Ready
