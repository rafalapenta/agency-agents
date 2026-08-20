---
name: goal-planner
description: Refines user inputs into executable step-by-step plans
version: 1.0.0
author: Agentic OS
tags: [planning, goals, execution]
---

# Goal Planner

## Description
Takes a high-level goal or objective and breaks it down into a concrete, executable step-by-step plan with dependencies, milestones, and estimated effort.

## When to Use
- When user says "I want to..." with a complex goal
- Project kickoff
- Quarterly planning
- Learning roadmap creation

## Process
1. Clarify the goal with targeted questions
2. Identify constraints and dependencies
3. Break goal into milestones
4. Break milestones into tasks
5. Estimate effort per task
6. Identify critical path
7. Save plan to context/

## Output
Structured plan with: goal, milestones, tasks, dependencies, estimates

## Agent Assignment
- Primary: opencode
- Fallback: agy
