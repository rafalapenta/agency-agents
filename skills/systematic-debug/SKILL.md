---
name: systematic-debug
description: 4-phase root cause analysis and debugging
version: 1.0.0
author: Agentic OS
tags: [debugging, bug, fix, root-cause]
---

# Systematic Debugging

## Description
Four-phase debugging methodology: reproduce, investigate, fix, verify. Prevents guesswork and ensures root cause is found before any fix is applied.

## When to Use
- Encountering a bug or error
- System failure or crash
- Unexplained behavior
- Performance regression

## Process
1. **Reproduce**: Capture exact steps, environment, and error output
2. **Investigate**: Trace root cause through logs, stack traces, and code analysis
3. **Fix**: Apply minimal fix addressing root cause (not symptoms)
4. **Verify**: Confirm fix resolves the issue and doesn't introduce regressions
5. Update learnings.md with debugging insights

## Safety
- If 3 fix attempts fail, trigger architectural review
- Never apply workaround without understanding root cause

## Output
Debug report: symptoms, root cause, fix applied, verification results

## Agent Assignment
- Primary: opencode
