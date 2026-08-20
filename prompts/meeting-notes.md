# Meeting Notes Prompt

Process the following raw meeting notes into structured minutes:

## Template
```markdown
# Meeting: {title}
- Date: {date}
- Attendees: {names}
- Duration: {duration}

## Decisions
- {decision 1} (by whom, by when)
- {decision 2}

## Action Items
- [ ] {task} — Owner: {name} — Due: {date}
- [ ] {task} — Owner: {name} — Due: {date}

## Open Questions
- {question 1} — needs input from {name}
- {question 2}

## Next Meeting
- {date} at {time}
- Agenda items: {items}
```

Extract every decision and action item. If ownership is unclear, flag it.
