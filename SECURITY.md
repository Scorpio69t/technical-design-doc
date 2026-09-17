# Security Policy

## Supported versions

Security fixes are applied to the latest release. Users should upgrade to the newest version before reporting a problem that may already be fixed.

## Reporting a vulnerability

Do not open a public issue for a vulnerability. Use the repository's [private vulnerability reporting form](https://github.com/Scorpio69t/technical-design-doc/security/advisories/new).

Include:

- the affected version or commit;
- the file and instruction involved;
- a minimal reproduction or example prompt;
- the likely impact;
- any suggested mitigation.

Relevant reports include unsafe script behavior, archive path issues, instruction or prompt-injection paths that can cause unintended tool use, and examples that expose sensitive data.

The maintainer will acknowledge a report as soon as practical, assess affected versions, and coordinate disclosure after a fix is available. Please do not publish details before that coordination is complete.

## Trust boundary

This repository contains instructions, templates, examples, and local Python utilities. It does not require network access or third-party Python packages. Diagram renderers are separate tools and have their own security policies. Review all skill changes before installing an untrusted fork.
