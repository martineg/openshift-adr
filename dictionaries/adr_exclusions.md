# Architecture Decision Record Exclusions

This file lists topics that must **NOT** be generated as ADRs. These topics often appear to be decisions but are actually mandatory configurations, unsupported paths, or deprecated features.

| Topic / Keywords                           | Reason for Exclusion                                                                                                                                            |
| :----------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Network Teaming (vs Bonding)**           | **Planned Deprecation.** Network Teaming is deprecated in RHEL 9 and future OCP versions. It is not a valid forward-looking strategy.                           |
| **API Load Balancer Health Timing**        | **Duplicate.** Health check intervals (5-10s) are already mandated in OCP-NET. Slower probing is a misconfiguration.                                            |
| **Mixed / Hybrid IPAM**                    | **Invented Strategy.** Do not suggest mixing DHCP and Static IPs on the same node as a standalone architectural strategy.                                       |
| **Default Catalog Sources (Disconnected)** | **Misconfiguration.** In disconnected environments, disabling default sources is a mandatory configuration step to prevent errors, not an architectural choice. |
