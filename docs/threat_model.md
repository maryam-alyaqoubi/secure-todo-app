# Threat Model (STRIDE) — Secure TODO App

## Summary
This document lists key threats using the STRIDE framework and proposed mitigations.

| STRIDE | Threat | Impact | Likelihood | Mitigation |
|---|---|---:|---:|---|
| Spoofing | Credential theft or brute-force login to impersonate users | High | Medium | Hash passwords, rate limit login, account lockout |
| Tampering | SQL Injection to modify tasks or users | High | Medium | Parameterized queries/ORM, input validation |
| Repudiation | User denies performing action | Medium | Low | Server-side logging with timestamps |
| Information Disclosure | Leakage of sensitive data (passwords, emails) | High | Medium | Hashing, HTTPS, least privilege |
| Denial of Service | Flooding registration or login endpoints | Medium | Low | Rate limiting, resource limits |
| Elevation of Privilege | User manipulates role to become admin | High | Medium | Server-side RBAC checks, not trusting client input |

## Notes
- Threats will be demonstrated (vulnerable commit) and remediated (fixed commit). Evidence (screenshots/logs) included in report.
