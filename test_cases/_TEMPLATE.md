<!-- HOW TO USE THIS TEMPLATE
1. Copy to test_cases/<feature>.md (lowercase, hyphens).
2. Fill every field. If you don't know something, write "To confirm" — never guess.
3. Set Status to "Ready" only when every expected result and data set is confirmed.
   Only "Ready" cases are automated.
4. Never write credentials or real personal data — use data set names only.
5. Formatting convention (helps people and Claude read the steps precisely):
     **Bold**    = name of a UI element as labelled on screen   e.g. Click **Login**, **Reset** button is visible
     `Backticks` = exact text / value that must match exactly   e.g. shows `-- Select --`, URL matches `**/dashboard/index`, `VALID_USERNAME`
     Plain text  = normal description                           e.g. is visible, Observe the form
-->

# Test Cases — <Feature Name>

| Field | Value |
|---|---|
| Feature | <feature> |
| Application URL | <full URL of the page under test> |
| Status | <Draft / Ready> |
| Source | <Manual / Jira key (later)> |
| Author | <name> |
| Last updated | <YYYY-MM-DD> |

## Acceptance criteria

- **AC-1:** <what must be true — written as stated by the requirement / product owner>
- **AC-2:** <…>

---

## TC-1: <one-line title, specific enough to tell it apart>

| Field | Value |
|---|---|
| Covers | AC-<n> |
| Type | <Positive / Negative / Boundary> |
| Priority | <P0 / P1 / P2> |
| Tags | <module>, <suite>, <priority> — e.g. `login, smoke, p0` (lowercase, underscores) |
| Test data | `<data set name>` |

**Preconditions**
- <what must be true before step 1>

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | <action> | <expected — or "Expected result to confirm — not specified"> |
| 2 | <action> | <expected> |

**Postconditions / cleanup**
- <state or data left behind — or "None">
- Browser is closed automatically by the framework — don't add a "close browser" step.

**Notes**
- <inferences labelled as "Inferred: …", open questions>

---

<!-- Copy the TC block above for TC-2, TC-3 … IDs must be unique within this file. -->

## Coverage

| AC | Positive | Negative | Boundary |
|---|---|---|---|
| AC-1 | TC-<n> | TC-<n> / not covered — <reason> | TC-<n> / not covered — <reason> |

## To confirm

| # | Item | Affects | Answer |
|---|---|---|---|
| 1 | <open question> | TC-<n> step <n> | <filled in by reviewer> |
