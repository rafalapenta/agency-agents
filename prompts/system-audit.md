# System Audit Prompt

Perform a comprehensive system audit covering:
1. **Infrastructure**: GCP resources, Kubernetes clusters, Cloud SQL, CDN
2. **Security**: IAM roles, service accounts, firewall rules, SSL certs
3. **CI/CD**: Pipeline status, build times, failure rates
4. **Cost**: Current spend, projections, optimization opportunities
5. **Performance**: Latency, error rates, resource utilization

For each category, provide:
- Status: PASS / WARN / FAIL
- Evidence (specific numbers, configs, logs)
- Recommendation with priority (high/medium/low)
