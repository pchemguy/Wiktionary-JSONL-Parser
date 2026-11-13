# Upstream provenance and adaptation

Adapted from Jesse Vincent's [Superpowers test-driven-development skill](https://github.com/obra/superpowers/tree/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/test-driven-development), including both `SKILL.md` and `writing-good-tests.md`, reviewed on 2026-09-30. The upstream revision is `8ca22dba9a94f28898bbce59f2537ff4d87c747d`. Its MIT copyright and permission notice is retained in this skill's `LICENSE`.

The adaptation preserves observed test failures, the red → green → refactor cycle, independent expected values, behavior-focused assertions, deliberate mock boundaries, test-helper ownership, and checks for test sensitivity.

SDD-specific changes assign testing strategy and test edits to **sdd-tdd**, production changes and completion to the active **sdd-implement** or **sdd-steer** workflow, boundary verification to **sdd-verify**, and documentation to **sdd-docs**. Accepted project contracts determine expectations and verification scope. Existing work is preserved when test-first evidence is absent; the adaptation replaces mandatory code deletion with an explicit evidence gap and safe characterization or isolated sensitivity checks. Exceptions follow governing project policy and existing user authorization.
