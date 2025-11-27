# Architecture Decision Record Exclusions

## 1. Forbidden Topics (REJECT / REMOVE)

These topics are **invalid** as ADRs (Misconfigurations, Deprecated, Non-Decisions).

| Topic / Keywords                           | Reason for Exclusion                                                                                                                                            |
| :----------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Network Teaming (vs Bonding)**           | **Planned Deprecation.** Network Teaming is deprecated in RHEL 9 and future OCP versions. It is not a valid forward-looking strategy.                           |
| **API LB Probe Interval Configuration**    | **Duplicate.** Health check intervals (5-10s) are already mandated in OCP-NET-10. Slower probing is a misconfiguration.                                         |
| **Mixed / Hybrid IPAM**                    | **Invented Strategy.** Do not suggest mixing DHCP and Static IPs on the same node as a standalone architectural strategy.                                       |
| **Default Catalog Sources (Disconnected)** | **Misconfiguration.** In disconnected environments, disabling default sources is a mandatory configuration step to prevent errors, not an architectural choice. |

## 2. False Positive Suppression (IGNORE UPDATES)

These topics are known to be correct. **Do NOT report updates** if the ADR matches these Titles/Topics.

| ADR Title / Scope                                        | Suppressed Issue                     | Instruction                                                                                        |
| :------------------------------------------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------- |
| **Bare Metal Node Secure Boot Strategy**                 | **(TP) Flag on Managed Secure Boot** | The flag is already present. Ignore requests to add it.                                            |
| **OVN-Kubernetes Internal Masquerade Subnet**            | **Default Masquerade CIDR**          | The CIDR is already updated. Ignore legacy comparison.                                             |
| **Node IP Address Management**                           | **Mixed / Hybrid IPAM**              | This ADR correctly chooses _between_ DHCP and Static. It is NOT a "Mixed" strategy. Do not remove. |
| **OVN-Kubernetes IP Forwarding Scope**                   | **Versioning Policy**                | The ADR correctly uses "New Install Default" without version numbers. Do not report.               |
| **Bare Metal Fleet Cluster Upgrade Strategy**            | **(TP) Flag on IBGU**                | The (TP) flag is already present or decided. Do not report.                                        |
| **Bare Metal Firmware Update Application Timing Policy** | **(TP) Flag on Live Update**         | The (TP) flag is already present or decided. Do not report.                                        |
| **Bare Metal Node Remediation**                          | **(TP) Flag on BMO Remediation**     | The (TP) flag is already present or decided. Do not report.                                        |
| **Environment Isolation Strategy**                       | **(TP) Flag on Consolidated Model**  | Do not flag the entire model as TP just because of User Namespaces.                                |
