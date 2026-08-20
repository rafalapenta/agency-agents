---
name: devops-audit
description: GCP/K8s infrastructure audit and health check
version: 1.0.0
author: Agentic OS
tags: [devops, gcp, kubernetes, infrastructure]
---

# DevOps Audit

## Description
Audits GCP infrastructure, Kubernetes clusters, CI/CD pipelines, and deployment configurations. Generates a comprehensive health report with recommendations.

## When to Use
- Daily infrastructure health check
- Before/after deployments
- Monthly compliance audit

## Process
1. Check GCP resource usage (Cloud SQL, GKE, Cloud CDN)
2. Verify Kubernetes cluster health
3. Review CI/CD pipeline status
4. Check certificate expiry dates
5. Review IAM and security configurations
6. Generate audit report with pass/warn/fail per category

## Output
Structured audit report markdown in context/ folder

## Agent Assignment
- Primary: opencode
- Fallback: agy
