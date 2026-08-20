---
name: tdd-cycle
description: Red-Green-Refactor test-driven development cycle
version: 1.0.0
author: Agentic OS
tags: [testing, tdd, quality, development]
---

# TDD Cycle

## Description
Enforces the Red-Green-Refactor TDD cycle: write a failing test, make it pass, then refactor. No code is written before a test exists.

## When to Use
- When implementing any new feature
- When fixing a bug
- When refactoring existing code

## Process
1. **RED**: Write a failing test for the desired behavior
2. Verify test fails (confirm test is valid)
3. **GREEN**: Write minimal code to make the test pass
4. Verify test passes
5. **REFACTOR**: Clean up code while keeping tests green
6. Commit with message format: `RED|GREEN|REFACTOR: description`

## Rules
- Production code is only written to make a failing test pass
- Delete any code written before tests
- Never skip the RED phase

## Agent Assignment
- Primary: opencode
