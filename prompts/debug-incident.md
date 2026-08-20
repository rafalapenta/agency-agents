# Debug Incident Prompt

Walk through the 4-phase debugging process:

## Phase 1: Reproduce
- What are the exact steps to reproduce?
- What environment (OS, versions, config)?
- What is the exact error message/output?

## Phase 2: Investigate
- What does the stack trace tell us?
- What changed recently that could have caused this?
- What logs are relevant?
- Can we isolate the failing component?

## Phase 3: Fix
- What is the root cause? (not the symptom)
- What is the minimal fix?
- Does this fix address the root cause permanently?
- Could this fix introduce regressions?

## Phase 4: Verify
- Does the fix resolve the original issue?
- Do existing tests still pass?
- Should we add a regression test?

If 3 fix attempts fail, trigger architectural review.
