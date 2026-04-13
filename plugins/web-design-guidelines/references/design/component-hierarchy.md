# Component Hierarchy

## Row and Card Patterns

- Limit each row to three levels of hierarchy: primary content, supporting metadata, and status/action.
- Primary content (title, name, subject) should be immediately scannable without reading metadata.
- Supporting metadata (IDs, types, dates) should recede visually but remain accessible.
- Status or urgency text belongs at the edge, not competing with the title.

## The Three-Level Pattern

A well-structured list row reads like this:

```
Level 1: Primary identifier (what is this?)
Level 2: Metadata line (type, reference, date)
Level 3: Status or action (what state is it in?)
```

Example transformation:

**Before (flat, competing elements):**
```
[BADGE] Big Title Text ............... 92 days overdue
```

**After (clear hierarchy):**
```
Waldinteressenten Elben
BM-25-00491 · Inspection · 12.01.2026
92 days overdue
```

## Metadata Grouping

- Combine related metadata into a single line with subtle separators (middot, pipe, comma).
- Do not scatter metadata across multiple disconnected positions in the row.
- Dates, IDs, and type labels that belong together should appear together.

## Badge and Pill Placement

- Categorical badges (type, category) belong in the metadata line, not before the title.
- Status badges that duplicate status text are redundant; choose one.
- When a badge is necessary, make it small and muted unless it is the primary signal.

## Section Headers

- Section headers should organize, not alarm; use muted text and small sizing.
- Include counts inline with headers when useful (e.g., "OVERDUE · 5").
- Bright or large section headers steal attention from the content they introduce.
- The rows carry the information; headers just provide structure.

## Card Containers

- Card shells should be subtle: light borders, soft shadows or none, generous radius.
- The container frames the content; it should not compete with it.
- Header rows within cards (title + count/filter) should feel balanced and understated.
