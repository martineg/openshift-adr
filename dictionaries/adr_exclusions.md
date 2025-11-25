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

| ADR Title / Scope                                           | Suppressed Issue                            | Instruction                                                                                            |
| :---------------------------------------------------------- | :------------------------------------------ | :----------------------------------------------------------------------------------------------------- |
| **Bare Metal Node Secure Boot Strategy**                    | **(TP) Flag on Managed Secure Boot**        | The flag is already present. Ignore requests to add it.                                                |
| **OVN-Kubernetes IP Forwarding Scope**                      | **Versioning Policy (New Install Default)** | The phrase "New Install Default" is a valid architectural state. Do not report.                        |
| **Node IP Address Management**                              | **Mixed / Hybrid IPAM**                     | This ADR correctly chooses _between_ DHCP and Static. It is NOT a "Mixed" strategy. Do not remove.     |
| **OVN-Kubernetes Internal Masquerade Subnet Configuration** | **Default Masquerade CIDR**                 | The ADR already correctly states the 169.254.0.0/17 default. Ignore comparisons to legacy /29 subnets. |
