---
name: code-review
description: Automated code review with checklist and quality gates
version: 1.0.0
author: Agentic OS
tags: [code, review, quality, pr]
---

# Code Review

## Description
Reviews code changes against project standards, naming conventions, error handling patterns, and security best practices. Generates structured review report.

## When to Use
- Before creating a PR
- When reviewing someone else's PR
- After implementing a feature
- During CI/CD pipeline

## Process
1. Read standards/ for project conventions
2. Diff the changes
3. Check against checklist:
   - Naming conventions
   - Error handling
   - Security concerns
   - Test coverage
   - Documentation
4. Report issues by severity (critical/major/minor)
5. Critical issues block progress

## Output
Structured review report with severity levels

## Agent Assignment
- Primary: opencode
- Fallback: agy
