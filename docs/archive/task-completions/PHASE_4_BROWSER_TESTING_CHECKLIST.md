# Multi-Query UI - Browser Testing Checklist ✅

**Date**: 2025-11-06  
**URL**: http://localhost:3000  
**Feature**: Multi-Query System Frontend

---

## 🧪 Test Cases

### Test 1: Simple Question (No Multi-Query)
**Question**: "How many employees are there?"

**Expected Behavior**:
- [ ] Answer appears in <1 second
- [ ] NO "Multi-Query" badge in header
- [ ] NO query count in description
- [ ] NO QueryPlanPanel visible
- [ ] Clean, familiar UI (unchanged from before)
- [ ] Answer text: "There are X employees..."
- [ ] Data table shows results
- [ ] SQL accordion works

---

### Test 2: Comparison Question (Multi-Query)
**Question**: "Compare IT vs Sales departments"

**Expected Behavior**:
- [ ] "Multi-Query" badge visible in answer header
- [ ] Query count shown in card description (e.g., "Multi-query execution (5 queries)")
- [ ] QueryPlanPanel rendered below answer card
- [ ] Response time ~12 seconds (AI generation + execution)

**Query Plan Panel Checks**:
- [ ] Summary header shows:
  - [ ] Question text
  - [ ] Total query count
  - [ ] Completed count (green)
  - [ ] Total execution time (ms)
- [ ] Status badges:
  - [ ] "Complete" badge (green/default variant)
  - [ ] NO "Has Errors" badge
- [ ] Query steps (3-5 cards):
  - [ ] Each card shows query ID (q1, q2, etc.)
  - [ ] Description text visible
  - [ ] Status badge (green ✓ Completed)
  - [ ] SQL query in code block
  - [ ] Row count displayed
  - [ ] Execution time in milliseconds
  - [ ] Dependencies shown if present (arrow icon + IDs)
- [ ] Final query:
  - [ ] Blue border around card
  - [ ] "Final" badge in top-right corner
  - [ ] Depends on previous queries

---

### Test 3: Visual Polish
**Checks**:
- [ ] Animations smooth (fade in, slide up)
- [ ] Card shadows visible on hover
- [ ] Status badges color-coded:
  - [ ] Green = Completed (CheckCircle icon)
  - [ ] Red = Failed (XCircle icon)
  - [ ] Blue = Executing (Clock icon)
  - [ ] Gray = Pending (Clock icon)
- [ ] Code blocks formatted (monospace font)
- [ ] Icons aligned properly
- [ ] Responsive on window resize
- [ ] No layout shift when query plan loads

---

### Test 4: Accessibility
**Keyboard Navigation**:
- [ ] Tab through elements
- [ ] Focus indicators visible (ring on focus)
- [ ] Enter expands accordions
- [ ] Escape closes dialogs

**Screen Reader** (if available):
- [ ] Badges announced with status
- [ ] Card structure clear
- [ ] SQL labeled as code

---

### Test 5: Error Handling
**Question**: "Compare extremely complex invalid query"

**Expected Behavior** (if AI generates bad SQL):
- [ ] 500 error OR multi-query with failed steps
- [ ] Failed queries show red status badge
- [ ] Error message displayed in red alert box
- [ ] Other queries still show as completed
- [ ] "Has Errors" badge visible in summary

---

### Test 6: Different Comparisons
**Try These Questions**:
1. "Compare IT vs Sales vs Finance" (3-way comparison)
2. "Show difference between highest and lowest salaries"
3. "Compare departments by average salary"
4. "IT versus Sales employee count"

**For Each**:
- [ ] Multi-Query badge appears
- [ ] Query plan shows appropriate number of steps
- [ ] Dependencies make sense (merge query depends on individual queries)
- [ ] Final results accurate

---

### Test 7: Backward Compatibility
**Non-Comparison Questions**:
1. "What is the average salary?"
2. "List all departments"
3. "Show top 5 employees by salary"
4. "Count orders by status"

**For Each**:
- [ ] NO multi-query indicators
- [ ] Response time fast (<1s)
- [ ] Charts still detected (if applicable)
- [ ] Trends still detected (if applicable)
- [ ] UI identical to before

---

## 🎨 Visual Design Checks

### Colors
- [ ] Primary blue for accents
- [ ] Green for success/completed
- [ ] Red for errors/failed
- [ ] Gray for pending/muted
- [ ] Muted foreground for metadata

### Typography
- [ ] Headers: semibold, larger size
- [ ] Body text: regular weight
- [ ] SQL: monospace font
- [ ] IDs: monospace font
- [ ] Metrics: small, muted

### Spacing
- [ ] Cards have proper padding
- [ ] Gap between sections consistent
- [ ] No elements touching edges
- [ ] White space balanced

### Components
- [ ] Badges: pill-shaped, small text
- [ ] Cards: rounded corners, shadows
- [ ] Code blocks: syntax highlighting
- [ ] Icons: proper size, aligned

---

## 📊 Performance Checks

### Timing
- [ ] Simple queries: <1 second
- [ ] Multi-queries: ~10-15 seconds
- [ ] Animation duration: 300-400ms
- [ ] No lag when scrolling plan

### Network
- [ ] Only 1 API call per question
- [ ] Response size reasonable (<100KB)
- [ ] No unnecessary re-fetches

---

## ✅ Sign-Off

**Tester**: _____________  
**Date**: _____________  
**Browser**: _____________  
**Screen Size**: _____________

**Overall Status**: [ ] PASS  [ ] FAIL  [ ] NEEDS FIX

**Notes**:
```
(Add any observations, bugs, or suggestions here)
```

---

## 🐛 Known Issues

(Document any bugs found during testing)

1. Issue: _______________
   - Steps to reproduce: _______________
   - Expected: _______________
   - Actual: _______________
   - Severity: [ ] Critical  [ ] Major  [ ] Minor

---

## 🎯 Success Criteria

- ✅ All simple questions work without multi-query UI
- ✅ Comparison questions show multi-query plan
- ✅ Query plan is readable and informative
- ✅ No regressions in existing features
- ✅ UI is responsive and accessible
- ✅ Performance is acceptable

**If all criteria met → Phase 4 APPROVED ✅**
