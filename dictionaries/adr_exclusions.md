# Architecture Decision Record Exclusions

This file lists topics that must **NOT** be generated as ADRs. These topics often appear to be decisions but are actually mandatory configurations, unsupported paths, or deprecated features.

| Topic / Keywords                 | Reason for Exclusion                                                                                                                  |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| **Network Teaming (vs Bonding)** | **Planned Deprecation.** Network Teaming is deprecated in RHEL 9 and future OCP versions. It is not a valid forward-looking strategy. |
