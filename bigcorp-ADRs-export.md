# Architecture Decisions - BigCorp

**Generated:** 2026-03-23
**Total ADRs:** 91

## Table of Contents

### OCP-MGT (12 ADRs)

- [OCP-MGT-01: Namespace/Project Allocation Strategy](#ocp-mgt-01)
- [OCP-MGT-02: RBAC Model (Delegation Strategy)](#ocp-mgt-02)
- [OCP-MGT-03: Image Registry Strategy (Application Images)](#ocp-mgt-03)
- [OCP-MGT-04: Project Resource Quotas Strategy](#ocp-mgt-04)
- [OCP-MGT-05: Cluster Update Channel Strategy](#ocp-mgt-05)
- [OCP-MGT-06: Platform Backup and Restore Strategy](#ocp-mgt-06)
- [OCP-MGT-07: Remote Health Reporting (Telemetry) Configuration](#ocp-mgt-07)
- [OCP-MGT-08: Cluster Autoscaling Strategy](#ocp-mgt-08)
- [OCP-MGT-09: General Node Remediation Strategy (MachineHealthCheck)](#ocp-mgt-09)
- [OCP-MGT-10: Pod Descheduling Strategy](#ocp-mgt-10)
- [OCP-MGT-11: Web Console Customization Strategy](#ocp-mgt-11)
- [OCP-MGT-12: Cluster Capabilities Selection Strategy](#ocp-mgt-12)

### OCP-BM (58 ADRs)

- [OCP-BM-01: OCP installation method on baremetal infrastructure](#ocp-bm-01)
- [OCP-BM-02: UPI Worker Node Operating System Selection (RHCOS vs RHEL)](#ocp-bm-02)
- [OCP-BM-03: Bare Metal Provisioning Workflow](#ocp-bm-03)
- [OCP-BM-04: Bare Metal Fleet Cluster Upgrade Strategy](#ocp-bm-04)
- [OCP-BM-05: Bare Metal Operator (BMO) for UPI](#ocp-bm-05)
- [OCP-BM-06: Bare Metal Operator Enrollment Policy for Existing UPI Hosts](#ocp-bm-06)
- [OCP-BM-07: Bare Metal Operator Namespace Scope](#ocp-bm-07)
- [OCP-BM-08: Host Role Assignment Strategy (ABI/Assisted)](#ocp-bm-08)
- [OCP-BM-09: BMC protocol](#ocp-bm-09)
- [OCP-BM-10: BMC Credential Security and Storage Strategy](#ocp-bm-10)
- [OCP-BM-11: Network Controller Sideband Interface (NC-SI) Support Enforcement](#ocp-bm-11)
- [OCP-BM-12: Provisioning Network Strategy for Installer-Provisioned Bare Metal](#ocp-bm-12)
- [OCP-BM-13: IPI Provisioning Network DHCP Management Mode](#ocp-bm-13)
- [OCP-BM-14: IPI/Assisted Provisioning Boot Mechanism](#ocp-bm-14)
- [OCP-BM-15: Ironic RHCOS Image Transfer Protocol (Virtual Media)](#ocp-bm-15)
- [OCP-BM-16: UPI Provisioning Boot Mechanism](#ocp-bm-16)
- [OCP-BM-17: Ignition Configuration Integrity Validation Strategy](#ocp-bm-17)
- [OCP-BM-18: RHCOS Live Installer Custom CA Trust Strategy](#ocp-bm-18)
- [OCP-BM-19: RHCOS Image Signature Verification Policy for UPI Installation](#ocp-bm-19)
- [OCP-BM-20: RHCOS Artifact Sourcing Strategy](#ocp-bm-20)
- [OCP-BM-21: RHCOS Day-1 Customization and Network Configuration Strategy](#ocp-bm-21)
- [OCP-BM-22: RHCOS Customization Timing Strategy (Live vs Permanent Ignition)](#ocp-bm-22)
- [OCP-BM-23: RHCOS Live Network Configuration Persistence Strategy (UPI)](#ocp-bm-23)
- [OCP-BM-24: Node IP Address Management](#ocp-bm-24)
- [OCP-BM-25: RHCOS Node Day-1 DNS Resolver Redundancy Strategy](#ocp-bm-25)
- [OCP-BM-26: Multi-NIC Strategy for RHCOS Core Network (UPI)](#ocp-bm-26)
- [OCP-BM-27: Bare Metal Network Bridge Configuration Tooling Strategy](#ocp-bm-27)
- [OCP-BM-28: NMState Configuration Scope for Provisioning](#ocp-bm-28)
- [OCP-BM-29: Cluster Node Hostname Assignment Strategy (User-Provisioned Infrastructure)](#ocp-bm-29)
- [OCP-BM-30: Host Network Bonding Mode for High Availability (OVS)](#ocp-bm-30)
- [OCP-BM-31: Bare Metal Node Secure Boot Strategy](#ocp-bm-31)
- [OCP-BM-32: Boot disks encryption](#ocp-bm-32)
- [OCP-BM-33: Bare Metal Host Firmware Configuration Management](#ocp-bm-33)
- [OCP-BM-34: RHCOS Node Console Access Strategy](#ocp-bm-34)
- [OCP-BM-35: RHCOS Installation Boot Device Selection](#ocp-bm-35)
- [OCP-BM-36: iSCSI Boot Configuration Method for RHCOS](#ocp-bm-36)
- [OCP-BM-37: RHCOS Multipathing Enablement Strategy (Boot and Secondary Disks)](#ocp-bm-37)
- [OCP-BM-38: RHCOS Multipath Installation Target Naming](#ocp-bm-38)
- [OCP-BM-39: RHCOS Installation Drive Identification Strategy](#ocp-bm-39)
- [OCP-BM-40: Hardware RAID Configuration for Bare Metal Installation Drive](#ocp-bm-40)
- [OCP-BM-41: Control Plane Storage Performance Validation Strategy](#ocp-bm-41)
- [OCP-BM-42: Bare Metal Minimum Boot Disk Capacity Strategy](#ocp-bm-42)
- [OCP-BM-43: RHCOS /var Partitioning Strategy (General Data Isolation)](#ocp-bm-43)
- [OCP-BM-44: Bare Metal Node OS Disk Partitioning for Container Storage](#ocp-bm-44)
- [OCP-BM-45: Control Plane Etcd Storage Partitioning Strategy](#ocp-bm-45)
- [OCP-BM-46: RHCOS Partition Retention Strategy during Reinstallation (UPI)](#ocp-bm-46)
- [OCP-BM-47: Bare Metal Node Image Pre-caching Strategy for Disconnected/Edge Deployments](#ocp-bm-47)
- [OCP-BM-48: Internal Image Registry Management State on Bare Metal UPI](#ocp-bm-48)
- [OCP-BM-49: Storage Architecture for the Internal Image Registry](#ocp-bm-49)
- [OCP-BM-50: Bare Metal Kernel Selection: Real-Time Kernel Implementation](#ocp-bm-50)
- [OCP-BM-51: Simultaneous Multithreading (SMT) Configuration Strategy](#ocp-bm-51)
- [OCP-BM-52: Workload Partitioning (CPU Isolation)](#ocp-bm-52)
- [OCP-BM-53: Container Runtime Selection for Bare Metal Performance Workloads](#ocp-bm-53)
- [OCP-BM-54: Precision Time Protocol (PTP) Configuration Strategy for Low-Latency Workloads](#ocp-bm-54)
- [OCP-BM-55: Kernel Module and Device Plugin Management on Bare Metal using KMM](#ocp-bm-55)
- [OCP-BM-56: Bare Metal Node Firmware Management](#ocp-bm-56)
- [OCP-BM-57: Bare Metal Firmware Update Application Timing Policy](#ocp-bm-57)
- [OCP-BM-58: Bare Metal Node Remediation](#ocp-bm-58)

### OCP-MON (6 ADRs)

- [OCP-MON-01: Monitoring Strategy](#ocp-mon-01)
- [OCP-MON-02: Metrics Collection Profile](#ocp-mon-02)
- [OCP-MON-03: Persistent Storage Strategy for Monitoring](#ocp-mon-03)
- [OCP-MON-04: Data Retention Policy](#ocp-mon-04)
- [OCP-MON-05: Remote Write / Federation Strategy](#ocp-mon-05)
- [OCP-MON-06: Alertmanager Integration Strategy](#ocp-mon-06)

### OCP-BASE (15 ADRs)

- [OCP-BASE-01: Environment Isolation Strategy](#ocp-base-01)
- [OCP-BASE-02: Cloud model](#ocp-base-02)
- [OCP-BASE-03: Internet Connectivity Model](#ocp-base-03)
- [OCP-BASE-04: Mirrored images registry (Disconnected Environments)](#ocp-base-04)
- [OCP-BASE-05: Fleet Management](#ocp-base-05)
- [OCP-BASE-06: Platform Configuration & Deployment Engine Selection](#ocp-base-06)
- [OCP-BASE-07: Multiple site deployment mode.](#ocp-base-07)
- [OCP-BASE-08: Intra-Site Availability Zone / Failure Domain Strategy](#ocp-base-08)
- [OCP-BASE-09: Platform infrastructure](#ocp-base-09)
- [OCP-BASE-10: Cluster Topology](#ocp-base-10)
- [OCP-BASE-11: Control Plane Schedulability Configuration](#ocp-base-11)
- [OCP-BASE-12: Infrastructure nodes](#ocp-base-12)
- [OCP-BASE-13: Dedicated Infrastructure Node Count for HA](#ocp-base-13)
- [OCP-BASE-14: Hardware Acceleration Strategy](#ocp-base-14)
- [OCP-BASE-15: Virtualization Strategy](#ocp-base-15)

---

# OCP-MGT

---

**Title**
Namespace/Project Allocation Strategy

Title: Namespace/Project Allocation Strategy
Architectural Question: What is the strategy for grouping and allocating namespaces (projects) to users, teams, and applications?
Issue or Problem: The project allocation model determines the level of isolation, complexity of resource quota management, and delegation of administrative tasks.
Assumption: N/A
Alternatives: Shared Project per Environment
Project per Team per Environment
Project per Application per Environment
Project per Team per Application per Environment
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Shared Project per Environment: Minimizes overhead (fewest total projects). Requires strict enforcement of ResourceQuota and NetworkPolicy to isolate workloads within the shared project boundary.
Project per Team per Environment: Balances overhead and isolation. Projects naturally delineate resource boundaries (quotas) and RBAC delegation based on team ownership (tenant).
Project per Application per Environment: Provides the highest logical isolation, allowing granular resource allocation and specific security controls (e.g., SCC/PSA policies) for each application instance.
Project per Team per Application per Environment: Granular control combining team ownership and per-application isolation.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Shared Project per Environment: High risk of resource contention and "noisy neighbor" problems if quotas are not managed precisely.
Project per Team per Environment: Limits the blast radius of a single misconfigured application to the owning team's project, preventing cluster-wide impact.
Project per Application per Environment: Management overhead scales linearly with the number of deployed applications.
Project per Team per Application per Environment: Highest complexity and management overhead.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: AI/ML Platform Owner

☐ OCP-MGT-02: RBAC Model (Delegation Strategy)

---

**Title**
RBAC Model (Delegation Strategy)

Title: RBAC Model (Delegation Strategy)
Architectural Question: What is the strategy for delegating project-level administration and resource management permissions?
Issue or Problem: Defining the RBAC strategy balances centralized platform governance (security) with development team autonomy and velocity.
Assumption: Project Allocation Strategy is defined. Identity Provider and Groups are configured.
Alternatives: Centralized Platform Team Control (e.g., `cluster-admin` for platform, `edit` for devs)
Delegated Project Administration (e.g., `admin` role for team leads in their projects)
Custom Role-Based Access Control (RBAC) (Tailored roles/bindings)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Centralized Control: Maintains strict central control, platform team manages most project-level admin tasks. Minimizes security surface area delegated to tenants.
Delegated Admin: Empowers project team leads (`admin` role) over their own projects, fostering autonomy and reducing burden on central platform team.
Custom RBAC: Implements tailored permissions for specific complex organizational needs not met by standard roles.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Centralized: Creates bottleneck, developers rely on platform team for admin tasks (project roles, quotas). Slower velocity for tenants.
Delegated: Increases surface area for potential misconfigurations by tenants but reduces central operational load, improves developer velocity.
Custom: Requires significant effort to develop, test, maintain custom roles/bindings. Increases complexity.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: AI/ML Platform Owner
#TODO#: Security Expert

☐ OCP-MGT-03: Image Registry Strategy (Application Images)

---

**Title**
Image Registry Strategy (Application Images)

Title: Image Registry Strategy (Application Images)
Architectural Question: Which image registry will be used for storing internally built application images (including custom RHOAI notebook images)?
Issue or Problem: An image registry is needed to store, scan, and distribute container images for CI/CD and deployments. This is separate from the disconnected mirror registry which primarily holds Red Hat content.
Assumption: Internal applications or custom container images will be built and deployed on the platform.
Alternatives: OpenShift Internal Registry (Image Registry Operator)
Existing HA Corporate Image Registry (e.g., Quay, Artifactory, Nexus)
New Dedicated HA Corporate Image Registry (e.g., Deploying Quay)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: OpenShift Internal Registry: Uses the built-in registry. Simplest option integrated with OCP. Managed by Cluster Image Registry Operator.
Existing Corporate Registry: Leverages existing, hardened, managed registry infrastructure. Maintains single source of truth for all artifacts.
New Dedicated Registry (Quay): Deploys a new, fully-featured registry optimized as HA source for internal images. Offers advanced features (security, team isolation).
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Internal Registry: Lifecycle tied to cluster. Requires persistent storage config (ODF RWO/RWX or other PVs). Storage must be sized appropriately. May need extra security hardening if exposed externally. Lacks advanced features of dedicated registries.
Existing Registry: Requires network connectivity and pull secrets in app namespaces. Build pipelines need push credentials. May need `ImageContentSourcePolicy`. Relies on external system availability/management and registry team support.
New Dedicated Registry: Provides most features but adds another critical HA component to deploy/manage. Requires dedicated infrastructure or significant OCP resources if run internally. May require separate subscription/license (e.g., Quay).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Security Expert
#TODO#: AI/ML Platform Owner
#TODO#: Operations Expert

☐ OCP-MGT-04: Project Resource Quotas Strategy

---

**Title**
Project Resource Quotas Strategy

Title: Project Resource Quotas Strategy
Architectural Question: What strategy will enforce resource consumption limits (CPU, memory, storage, GPUs) at the project (tenant) level?
Issue or Problem: Without quotas, a single project could monopolize cluster resources, impacting stability and availability for all tenants.
Assumption: Multi-tenancy or resource contention is expected. Project Allocation is defined.
Alternatives: No Quotas
Standardized Tier-Based Quotas (e.g., Small, Medium, Large)
Custom Per-Project Quotas
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: No Quotas: Simplifies administration in non-prod or trusted environments with low contention risk. Not recommended for production/multi-tenant.
Standardized Tiers: Scalable, manageable approach. Defines standard project sizes with preset resource budgets (including specialized resources like `requests.nvidia.com/gpu`). Simplifies onboarding.
Custom Per-Project: Maximum flexibility, tailoring budgets to specific project needs.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: No Quotas: High risk of resource starvation, "noisy neighbors" destabilizing the cluster.
Standardized Tiers: Simplifies onboarding/capacity planning. May not perfectly fit every project's needs but provides reasonable bounds. Easier to automate.
Custom Per-Project: Most accurate allocation but significant administrative overhead to define, approve, manage each custom quota. Harder to automate.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: AI/ML Platform Owner
#TODO#: Operations Expert

☐ OCP-MGT-05: Cluster Update Channel Strategy

---

**Title**
Cluster Update Channel Strategy

Title: Cluster Update Channel Strategy
Architectural Question: Which OpenShift update channel will be selected to govern the cadence and stability of platform upgrades?
Issue or Problem: The update channel determines how quickly the cluster receives new versions and the level of validation those versions have undergone. This impacts stability, feature availability, and support windows.
Assumption: N/A
Alternatives: Stable Channel: Releases are promoted only after passing testing in the Fast channel and proving stability in the field.
Fast Channel: Releases are promoted as soon as Red Hat QA approves them. Access to new features sooner, but potentially higher risk of bugs.
Candidate Channel: Pre-release builds. Not for production.
EUS (Extended Update Support) Channel: Allows staying on specific even-numbered minor versions (e.g., 4.14) for longer periods (18+ months) with a simplified upgrade path to the next EUS version.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Stable Channel: Recommended default for production. Balances novelty with reliability.
Fast Channel: Suitable for non-production or "canary" clusters to test upcoming features before they hit Stable.
EUS Channel: Critical for mission-critical clusters where upgrade frequency must be minimized (e.g., Telco, Edge, Banking).
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Stable: Slower access to fixes/features than Fast.
Fast: Higher risk of regression.
EUS: Upgrade paths are stricter (e.g., 4.12 -> 4.13 -> 4.14 required, even if "skipping" via EUS logic). Only available on specific versions.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-MGT-06: Platform Backup and Restore Strategy

---

**Title**
Platform Backup and Restore Strategy

Title: Platform Backup and Restore Strategy
Architectural Question: What is the strategy for backing up and restoring OpenShift cluster state (etcd) and application persistent data (PVs)?
Issue or Problem: A comprehensive, tested backup/restore strategy is critical for disaster recovery and protecting against data loss/corruption. Must cover control plane (etcd), stateful app data (PVs), and potentially stateless app resources.
Assumption: Disaster recovery and data protection are required.
Alternatives: Etcd Snapshot Only
OpenShift Data Protection (OADP/Velero) for PVs and Resources
Comprehensive Layered Backup
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Etcd Snapshot Only: Backs up the critical control plane state (Kubernetes resources, cluster configuration) via etcd snapshots, which is sufficient for cluster recovery if underlying application data (PVs) is handled separately or is ephemeral.
OpenShift Data Protection (OADP/Velero) for PVs and Resources: Uses the OADP Operator (based on Velero) to back up cluster resources and application persistent data volumes (PVs/PVCs). OADP supports incremental backups of block and Filesystem volumes.
Comprehensive Layered Backup: Combines Etcd snapshots for cluster state with OADP for application data and additional measures for immutable objects (e.g., MachineConfigs, custom resources).
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Etcd Snapshot Only: Does not protect application data (PVs), leading to data loss unless application storage is managed by an external highly available/DR solution.
OpenShift Data Protection (OADP/Velero) for PVs and Resources: Requires deploying the OADP Operator and defining backup storage locations (e.g., S3, ODF Object Storage). Requires enabling OpenShift User Workload Monitoring to observe OADP metrics.
Comprehensive Layered Backup: Highest complexity and resource usage. Requires meticulous planning to ensure consistency between etcd snapshots and volume backups during restore operations.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert
#TODO#: Storage Expert
#TODO#: OCP Platform Owner

☐ OCP-MGT-07: Remote Health Reporting (Telemetry) Configuration

---

**Title**
Remote Health Reporting (Telemetry) Configuration

Title: Remote Health Reporting (Telemetry) Configuration
Architectural Question: Should the cluster enable the Remote Health Reporting (Telemetry) service to send cluster diagnostics and usage data to Red Hat?
Issue or Problem: Telemetry is enabled by default for connected OpenShift clusters. A decision is required on whether to maintain this default or disable it to meet strict security and compliance requirements related to exporting cluster diagnostic data or to conserve outbound network bandwidth.
Assumption: Cluster is in a connected environment.
Alternatives: Enable Remote Health Reporting (Telemetry) (Default)
Disable Remote Health Reporting (Telemetry)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Enable Remote Health Reporting (Telemetry) (Default): This leverages the default cluster configuration. The service automatically entitles the cluster if it has internet access. This configuration provides valuable built-in remote health monitoring and diagnostics to Red Hat.
Disable Remote Health Reporting (Telemetry): This is necessary to satisfy strict security policies or compliance mandates that prohibit sending diagnostic or usage data outside the internal network.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Enable Remote Health Reporting (Telemetry) (Default): Requires open firewall egress rules to external Red Hat endpoints for the Telemetry service to function.
Disable Remote Health Reporting (Telemetry): Removes a built-in diagnostic safety net, potentially complicating troubleshooting and relying solely on external tools or manual inspection.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-MGT-08: Cluster Autoscaling Strategy

---

**Title**
Cluster Autoscaling Strategy

Title: Cluster Autoscaling Strategy
Architectural Question: Will the cluster utilize the Cluster Autoscaler to dynamically adjust the size of MachineSets based on workload demand?
Issue or Problem: Static clusters may be over-provisioned (wasting money) or under-provisioned (causing pending pods). Autoscaling adapts infrastructure to demand but adds complexity and cost unpredictability.
Assumption: Platform supports Machine API (IPI/Cloud).
Alternatives: Static Sizing: Fixed number of nodes per MachineSet. Manual scaling only.
Cluster Autoscaler Enabled: Dynamic scaling within defined min/max bounds.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Static Sizing: Predictable costs and topology. Simple to manage. Recommended for Bare Metal UPI or fixed-budget environments.
Cluster Autoscaler Enabled: Optimizes cloud costs by creating nodes only when pods are pending and deleting them when empty. Recommended for cloud IPI or dynamic virtualization environments.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Static Sizing: Operations team must monitor capacity and manually scale out/in.
Autoscaler: Risk of "runaway" costs if max limits are too high or workloads lack requests/limits. Pods must tolerate disruption (node scale-down).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-MGT-09: General Node Remediation Strategy (MachineHealthCheck)

---

**Title**
General Node Remediation Strategy (MachineHealthCheck)

Title: General Node Remediation Strategy (MachineHealthCheck)
Architectural Question: How will unhealthy nodes (e.g., NotReady state) be automatically remediated in Cloud/Virtualization environments?
Issue or Problem: Nodes can freeze or disconnect. Manual recovery is slow. Automated remediation improves uptime but risks data loss if configured incorrectly (e.g., fencing).
Assumption: Platform supports Machine API (IPI).
Alternatives: Manual Remediation: Alerts fire; humans investigate.
MachineHealthCheck (MHC) Enabled: Controller detects unhealthy nodes and recreates them (Cloud/Virt) or reboots them (Bare Metal).
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Manual: Safe. Prevents accidental data loss or "reboot loops" in unstable clusters.
MHC Enabled: Self-healing infrastructure. Essential for high availability in cloud environments where instances are ephemeral.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: MHC Enabled: Must configure `maxUnhealthy` to prevent cascading failures. Warning: On platforms without shared storage (like vSphere without RWX), recreating a node might detach RWO volumes safely, but requires careful testing.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-MGT-10: Pod Descheduling Strategy

---

**Title**
Pod Descheduling Strategy

Title: Pod Descheduling Strategy
Architectural Question: Will the Descheduler be deployed to proactively move running pods to optimize cluster balance?
Issue or Problem: The default scheduler only places _new_ pods. Over time, clusters become fragmented or imbalanced (e.g., all high-cpu pods on one node).
Assumption: N/A
Alternatives: No Descheduler: Pods stay where they land until deleted or evicted.
Descheduler Enabled: Automated eviction of pods based on policies (e.g., `RemoveDuplicates`, `LowNodeUtilization`).
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: No Descheduler: Stability. Pods are not restarted unless necessary.
Descheduler Enabled: Optimization. Actively corrects placement to enforce anti-affinity, improve bin-packing, or clear nodes with high utilization.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Descheduler: Pods will be killed and rescheduled. Workloads must utilize PodDisruptionBudgets (PDBs) and handle restarts gracefully.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Application team leadership

☐ OCP-MGT-11: Web Console Customization Strategy

---

**Title**
Web Console Customization Strategy

Title: Web Console Customization Strategy
Architectural Question: Will the OpenShift Web Console be customized with organization-specific branding, links, or plugins?
Issue or Problem: The default console implies a generic Red Hat experience. Enterprises often need to add "Help" links to internal ticketing systems, display classification banners (e.g., "TOP SECRET"), or integrate custom UI plugins (e.g., for internal tools).
Assumption: N/A
Alternatives: Standard Console: Default look and feel.
Customized Console: Custom logo, login text, help links, notification banners, or dynamic plugins enabled.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Standard: Zero maintenance.
Customized: Improves user experience and compliance (e.g., mandatory warning banners). Directs users to correct support channels.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Customized: Requires managing `Console` resource configuration and potentially hosting assets (logos) or plugin containers.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner

☐ OCP-MGT-12: Cluster Capabilities Selection Strategy

---

**Title**
Cluster Capabilities Selection Strategy

Title: Cluster Capabilities Selection Strategy
Architectural Question: Will optional cluster capabilities (e.g., Marketplace, Insights, Console) be disabled to optimize resource consumption?
Issue or Problem: By default, OpenShift installs a comprehensive set of operators. For resource-constrained environments like Single Node OpenShift (SNO) or Edge, these idle operators consume valuable CPU/RAM.
Assumption: Cluster topology is SNO or Edge.
Alternatives: Full Capabilities (Default): Installs all standard operators.
Optimized/Reduced Capabilities: Explicitly disables optional components via `install-config.yaml` (`capabilities.baselineCapabilitySet` or `additionalEnabledCapabilities`).
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Full Capabilities: Ensures feature parity with standard clusters. Simpler updates (no missing dependencies).
Optimized/Reduced: Critical for SNO. Can save significant memory (e.g., disabling `Marketplace`, `Console`, `Insights`).
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Full: Higher overhead.
Optimized: "Day 2" enablement of features (like adding the Console back later) can be complex.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

OpenShift Container Platform - Monitoring (Metrics)
☐ OCP-MON-01: Monitoring Strategy

---

# OCP-BM

---

**Title**
OCP installation method on baremetal infrastructure

Title: OCP installation method on baremetal infrastructure
Architectural Question: Which OCP installation method will be used to deploy a cluster on baremetal infrastructure?
Issue or Problem: The choice of installation method for Bare Metal impacts the level of automation, network prerequisites (like PXE), and how the cluster interacts with the physical hardware. This choice also dictates which disk encryption methods are technically feasible.
Assumption: N/A
Alternatives: User-Provisioned Infrastructure (UPI)
Installer-Provisioned Infrastructure (IPI)
Agent-based Installer (ABI)
Assisted Installer
Image-based Installer (IBI)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: User-Provisioned Infrastructure (UPI): Leverages existing data center tools, provides maximum control and customizability over the cluster infrastructure and installation prerequisites.
Installer-Provisioned Infrastructure (IPI): Delegates the infrastructure bootstrapping and provisioning to the installation program, automating provisioning using the Bare Metal Operator (BMO) features.
Agent-based Installer (ABI): Provides the convenience of the Assisted Installer but enables installation locally for disconnected environments or restricted networks.
Assisted Installer: A web-based SaaS service designed for connected networks that simplifies deployment via a user-friendly interface, smart defaults, and pre-flight validations.
Image-based Installer (IBI): Significantly reduces the deployment time of Single Node OpenShift clusters by enabling the preinstallation of configured and validated instances on target hosts.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: User-Provisioned Infrastructure (UPI): Implies the highest operational overhead because the user must manage and maintain all infrastructure resources. UPI is the only method that supports Tang Server Only and the TPM v2 and Tang Server Combination for disk encryption.
Installer-Provisioned Infrastructure (IPI): Requires integration with the BMO and related provisioning infrastructure. Supports only TPM for disk encryption, excluding Tang Server Only and the combined TPM/Tang method.
Agent-based Installer (ABI): Ideal for disconnected environments. Supports only TPM for disk encryption, excluding Tang Server Only and the combined TPM/Tang method.
Assisted Installer: Requires a working internet connection during the preparation phase. Supports only TPM for disk encryption, excluding Tang Server Only and the combined TPM/Tang method.
Image-based Installer (IBI): Primarily intended for Single-Node OpenShift (SNO) cluster deployments. Does not support disk encryption.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader

☐ OCP-BM-02: UPI Worker Node Operating System Selection (RHCOS vs RHEL)

---

**Title**
UPI Worker Node Operating System Selection (RHCOS vs RHEL)

Title: UPI Worker Node Operating System Selection (RHCOS vs RHEL)
Architectural Question: Which operating system (RHCOS or RHEL) will be standardized for compute (worker) nodes in user-provisioned infrastructure (UPI) bare metal clusters?
Issue or Problem: The choice between RHCOS and RHEL for compute machines in UPI environments dictates the Day 2 operational model: RHEL provides flexibility but shifts OS lifecycle management entirely to the user, while RHCOS ensures consistency and uses the Machine Config Operator (MCO) for updates, supporting the standard immutable infrastructure model.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: Standardize on Red Hat Enterprise Linux CoreOS (RHCOS) workers
Standardize on Red Hat Enterprise Linux (RHEL) workers
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Standardize on Red Hat Enterprise Linux CoreOS (RHCOS) workers: This ensures the standard immutable OS image is used and allows the Machine Config Operator to manage the OS lifecycle via cluster upgrades, simplifying ongoing maintenance and consistency.
Standardize on Red Hat Enterprise Linux (RHEL) workers: This allows the use of a traditional Linux OS, providing maximum customizability for specialized applications or legacy configurations, and leveraging existing enterprise RHEL operational toolchains.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Standardize on Red Hat Enterprise Linux CoreOS (RHCOS) workers: Supports the default cluster operational model. All cluster changes are applied by Operators. SSH access is not recommended for routine use.
Standardize on Red Hat Enterprise Linux (RHEL) workers: The organization takes full responsibility for all operating system life cycle management and maintenance of the compute nodes, including updates, patching, and required tasks. The cluster upgrade process will not automatically update the OS on these nodes.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: Security Expert

☐ OCP-BM-03: Bare Metal Provisioning Workflow

---

**Title**
Bare Metal Provisioning Workflow

Title: Bare Metal Provisioning Workflow
Architectural Question: How will the provisioning of bare metal clusters be orchestrated and automated to ensure reproducibility and scale?
Issue or Problem: Bare metal provisioning involves complex steps (BMC interaction, ISO booting, host discovery). Performing these manually or via ad-hoc scripts is error-prone and inconsistent. A workflow is needed that leverages the Centralized Fleet Management strategy (RHACM).
Assumption: Cluster is managed by RHACM.
Cluster installation method is Agent-based Installer (ABI), Assisted Installer, or Image-based Installer (IBI)
Alternatives: Manual / Imperative Provisioning (Console/API): Operators manually define clusters and hosts using the RHACM web console or trigger provisioning via imperative scripts/API calls to the Assisted Service.
GitOps Zero Touch Provisioning (ZTP): A declarative, pipeline-based approach where cluster definitions (`ClusterInstance`, `PolicyGenerator`) are managed in Git and applied by OpenShift GitOps (Argo CD) to the RHACM Hub.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision#
Justification: Manual / Imperative Provisioning (Console/API): Simplifies the user experience for Day 0 ("ClickOps") or allows for custom integration via API scripts. However, it lacks a native audit trail, makes disaster recovery harder (no "state" in Git), and is difficult to scale consistently across hundreds of sites.
GitOps Zero Touch Provisioning (ZTP): Treats infrastructure-as-code. The entire cluster definition (hardware, network, configuration) is versioned in Git. This is the standard Red Hat solution for mass-scale edge deployments, enabling "factory-precaching" and ensuring the actual state always matches the desired state in Git.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Manual / Imperative Provisioning: Deployment intent is not stored in Git, increasing the risk of configuration drift over time.
GitOps Zero Touch Provisioning (ZTP): Requires setting up an Argo CD pipeline on the Hub. Establishes strict requirements for downstream decisions, such as the need for `watchAllNamespaces` on the BMO and specific firmware management via `ClusterInstance`.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-BM-04: Bare Metal Fleet Cluster Upgrade Strategy

---

**Title**
Bare Metal Fleet Cluster Upgrade Strategy

Title: Bare Metal Fleet Cluster Upgrade Strategy
Architectural Question: How will large-scale, distributed bare metal cluster updates (OCP version upgrades) be managed and orchestrated from the central hub cluster?
Issue or Problem: Managing simultaneous upgrades across a large fleet of bare metal clusters, particularly Single Node OpenShift (SNO) clusters at the edge, requires a robust orchestration mechanism that can handle sequencing, image consistency, and minimal disruption. A choice must be made between the currently supported policy-driven approach and the image-based method designed for rapid edge updates.
Assumption: Cluster topology is Single-Node (SNO).
Provisioning workflow is GitOps ZTP.
Alternatives: Policy-Driven Rollout using TALM and PolicyGenerator CRs
Image-Based Group Upgrade (IBGU) (TP)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Policy-Driven Rollout using TALM and PolicyGenerator CRs: This is the standard, generally available approach for managing configurations and upgrades via policies, enabling granular control over rollout sequencing, customization, and remediation actions.
Image-Based Group Upgrade (IBGU) (TP): This methodology is designed to reduce deployment time significantly, especially for SNO clusters. It leverages the Lifecycle Agent (LCA) to deploy new operating system images (stateroots), making it suitable for rapid, consistent rollouts in edge environments.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Policy-Driven Rollout using TALM and PolicyGenerator CRs: Upgrades rely on ensuring policy compliance across the fleet, which may involve individual cluster reboots initiated by configuration changes (e.g., Node Tuning Operator). This approach requires meticulous policy management but is fully supported.
Image-Based Group Upgrade (IBGU) (TP): Is a Technology Preview feature only and is not supported with Red Hat production SLAs. While offering faster, image-based upgrades, reliance on this method for production clusters introduces support risk.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BM-05: Bare Metal Operator (BMO) for UPI

---

**Title**
Bare Metal Operator (BMO) for UPI

Title: Bare Metal Operator (BMO) for UPI
Architectural Question: Will the Bare Metal Operator (BMO) be enabled for a User-Provisioned Infrastructure (UPI) deployment?
Issue or Problem: A standard UPI installation does not include the Bare Metal Operator, meaning all Day 2 operations (like node remediation, scaling, or hardware management) are fully manual. Enabling BMO on UPI adds this automation but requires additional configuration.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: BMO will not be enabled
BMO will be enabled
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: BMO will not be enabled: This maintains a pure UPI model where the platform has no control over the physical hardware, relying on manual intervention or external automation for all node lifecycle management.
BMO will be enabled: This creates a "hybrid" model that combines the Day 1 control of UPI with the Day 2 automation benefits of IPI, such as automated node remediation and hardware inspection.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: BMO will not be enabled: The organization is fully responsible for all Day 2 bare metal operations, and ADRs related to BMCs (remediation, protocol, NC-SI) are not applicable.
BMO will be enabled: Subsequent ADRs for BMC protocols, NC-SI, and automated remediation must be addressed, and the operator must be manually installed and configured post-installation.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Operations Expert

☐ OCP-BM-06: Bare Metal Operator Enrollment Policy for Existing UPI Hosts

---

**Title**
Bare Metal Operator Enrollment Policy for Existing UPI Hosts

Title: Bare Metal Operator Enrollment Policy for Existing UPI Hosts
Architectural Question: When enabling the Bare Metal Operator (BMO) on a User-Provisioned Infrastructure (UPI) cluster for Day 2 automation, should existing, already-installed nodes (e.g., control plane) be enrolled only for inventory and status purposes, or prepared for full BMO lifecycle management (remediation, re-provisioning)?
Issue or Problem: Integrating existing UPI nodes into the BMO system for inventory and management visibility risks accidental re-provisioning or state corruption if the BMO attempts to manage the node's lifecycle without the correct configuration flag.
Assumption: The Bare Metal Operator (BMO) is enabled on a UPI cluster.
Alternatives: Enroll as Fully Managed Hosts
Enroll as Externally Provisioned Hosts (Inventory Only)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Enroll as Fully Managed Hosts: This allows the BMO to perform full node lifecycle management (remediation, scaling), treating the UPI node similarly to an IPI node, provided it conforms to Ironic standards.
Enroll as Externally Provisioned Hosts (Inventory Only): This strategy allows the cluster administrator to use the BMO to manage existing hosts solely for inventory purposes and to observe status, ensuring the host is recognized without attempting to re-provision the underlying operating system.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Enroll as Fully Managed Hosts: Increased risk of unintended node re-provisioning if the original UPI installation deviated from the BMO/Ironic expectations or if the `externallyProvisioned` flag is mistakenly omitted.
Enroll as Externally Provisioned Hosts (Inventory Only): Requires explicitly setting the `spec.externallyProvisioned: true` specification in the `BareMetalHost` Custom Resource to prevent the BMO from re-provisioning the host.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Operations Expert

☐ OCP-BM-07: Bare Metal Operator Namespace Scope

---

**Title**
Bare Metal Operator Namespace Scope

Title: Bare Metal Operator Namespace Scope
Architectural Question: Should the Bare Metal Operator (BMO) be configured to manage BareMetalHost resources across all namespaces in the cluster?
Issue or Problem: To enable features like Bare Metal as a Service (BMaaS) or GitOps ZTP, the BMO must be configured to find and manage BareMetalHost resources created outside its default namespace. Deciding this scope is a fundamental configuration for the BMO.
Assumption: The Bare Metal Operator (BMO) is enabled on the cluster.
The cluster fulfills a management role: It is either an ACM Hub Cluster managing a ZTP fleet OR a centralized BMaaS provider allocating physical nodes to various namespaces.
Alternatives: BMO Watches All Namespaces (Watch-All)
BMO Watches Specific/Limited Namespaces (Default)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: BMO Watches All Namespaces (Watch-All): This is required for BMaaS and GitOps ZTP. It allows the BMO on the Hub Cluster to discover `BareMetalHost` CRs created in any namespace (e.g., a spoke cluster namespace) and provision them.
BMO Watches Specific/Limited Namespaces (Default): This is the default behavior. BMO will only discover and provision hosts defined in its own `openshift-machine-api` namespace. All other `BareMetalHost` CRs in the cluster are ignored.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: BMO Watches All Namespaces (Watch-All): The BMO `Provisioning` CR must be patched to set `watchAllNamespaces: true`, enabling advanced, cluster-wide provisioning workflows.
BMO Watches Specific/Limited Namespaces (Default): The cluster is isolated, and advanced, multi-namespace provisioning workflows like BMaaS and GitOps ZTP are not possible.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader

☐ OCP-BM-08: Host Role Assignment Strategy (ABI/Assisted)

---

**Title**
Host Role Assignment Strategy (ABI/Assisted)

Title: Host Role Assignment Strategy (ABI/Assisted)
Architectural Question: How will physical hosts be assigned to OpenShift node roles (Control Plane vs. Worker) during Agent-based or Assisted installation?
Issue or Problem: The installer needs to know which physical server becomes a Master and which becomes a Worker. This can be done dynamically based on resource availability or explicitly defined to ensure deterministic placement.
Assumption: Cluster installation method is Agent-based Installer (ABI) or Assisted Installer.
Alternatives: Automatic Assignment (Resource-Based): The installer automatically assigns roles based on discovered hardware specs (e.g., largest nodes become Masters).
Explicit Assignment (MAC/Hostname Binding): Administrators explicitly map specific physical hosts (identified by MAC address or hostname) to specific roles in the `agent-config.yaml` or API.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Automatic Assignment: Simplifies zero-touch provisioning for homogeneous hardware pools. Reduces configuration toil.
Explicit Assignment: Mandatory for heterogeneous hardware or when specific rack/power placement is required for the control plane (e.g., ensuring masters are in different racks). Guarantees deterministic cluster layout.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Automatic Assignment: Risk of non-deterministic placement (e.g., Master 1 lands on a rack you wanted to be Worker-only).
Explicit Assignment: Requires gathering MAC addresses or BMC hostnames beforehand and maintaining a strict inventory mapping in the installation manifests.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Infra Leader
#TODO#: OCP Platform Owner

☐ OCP-BM-09: BMC protocol

---

**Title**
BMC protocol

Title: BMC protocol
Architectural Question: Which Baseboard Management Controller (BMC) protocol (Redfish, IPMI, or proprietary) should be standardized for automated provisioning, hardware inspection, and ongoing bare metal host lifecycle management using the Bare Metal Operator (BMO)?
Issue or Problem: The Bare Metal Operator (BMO) requires reliable, consistent, and secure connectivity to the BMC for key operations such as power management, image deployment, and hardware inspection. Different protocols offer varying levels of security, support for modern features (like firmware management), and compatibility across diverse hardware vendors, necessitating a standardized choice for cluster management.
Assumption: Bare Metal Operator is enabled.
Alternatives: Redfish
IPMI
Other proprietary protocol
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Redfish: This is the industry-standard, modern API recommended for hardware management. It enables advanced Bare Metal Operator features such as inspecting and configuring BIOS/Firmware settings (`HostFirmwareSettings`) and updating network interface controller (NIC) firmware (`HostFirmwareComponents`), which rely on Redfish support. Furthermore, Redfish BMC addressing is required for managed Secure Boot deployments, and for using Bare Metal as a Service (BMaaS) (TP).
IPMI: IPMI is an older, widely supported protocol. It is required in specific environments, such as IBM Cloud Bare Metal (Classic) deployments, where Redfish may not be tested or supported. It is supported if hardware does not support Redfish network boot.
Other proprietary protocol: This covers vendor-specific protocols (e.g., Fujitsu iRMC, Cisco CIMC) that are explicitly supported by Ironic/BMO. It is necessary when the fleet uses hardware that primarily relies on these interfaces for BMC connectivity.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Redfish: Requires ensuring hardware and BMC firmware meet the necessary compatibility versions validated for Redfish virtual media installation. If self-signed certificates are used, `disableCertificateVerification: True` must be configured in the `install-config.yaml` or `BareMetalHost` object. Enables the most robust lifecycle management features via BMO/Ironic.
IPMI: IPMI does not encrypt communications and requires use over a secured or dedicated management network. It cannot be used for managed Secure Boot deployments. If PXE booting is used with IPMI, a provisioning network is mandatory.
Other proprietary protocol: Management capabilities (especially advanced features like firmware configuration) may be limited to specific BMO drivers (like Fujitsu iRMC or HP iLO) and might not support the full range of vendor-independent Redfish capabilities.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Infra Leader
#TODO#: Security Expert
#TODO#: Operations Expert

☐ OCP-BM-10: BMC Credential Security and Storage Strategy

---

**Title**
BMC Credential Security and Storage Strategy

Title: BMC Credential Security and Storage Strategy
Architectural Question: How will the highly sensitive Baseboard Management Controller (BMC) credentials, necessary for Bare Metal Operator (BMO) operation, Agent-based Installation (ABI), and GitOps Zero Touch Provisioning (ZTP), be securely stored and accessed by the OpenShift control plane?
Issue or Problem: The automated bare metal workflow requires storing BMC login credentials (username/password) as Kubernetes Secrets (referenced by bmcCredentialsName). These secrets grant full out-of-band control over physical hosts (e.g., power cycle, firmware updates, OS installation). Protecting these secrets is critical for platform security.
Assumption: Bare Metal Operator is enabled.
Alternatives: Standard Kubernetes Secrets with OCP/etcd Encryption
External Secret Management System Integration
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Standard Kubernetes Secrets with OCP/etcd Encryption: This is the native pattern used by the Agent Installer and GitOps ZTP (via `bmcCredentialsName`). Protection relies on Role-Based Access Control (RBAC) and application-layer encryption in etcd (if enabled). This simplifies deployment as no external dependencies are introduced during installation.
External Secret Management System Integration: Credentials are stored exclusively outside of the Kubernetes cluster (e.g., in HashiCorp Vault or CyberArk). OCP components/operators would retrieve the secrets just-in-time via an integration service (e.g., external Secrets Operator). This approach offers stronger separation of duties and auditing for access to critical infrastructure credentials.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Standard Kubernetes Secrets with OCP/etcd Encryption: If an attacker gains sufficient privilege to read Kubernetes Secrets, the BMC credentials for all managed hosts are exposed. Requires stringent RBAC enforcement on the namespace containing the secrets.
External Secret Management System Integration: Increases Day 1 complexity by requiring deployment and highly available integration with the external secret system. Adds an external dependency that must be reachable and operational for BMO functions (like host remediation and provisioning) to succeed.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: OCP Platform Owner
#TODO#: Infra Leader

☐ OCP-BM-11: Network Controller Sideband Interface (NC-SI) Support Enforcement

---

**Title**
Network Controller Sideband Interface (NC-SI) Support Enforcement

Title: Network Controller Sideband Interface (NC-SI) Support Enforcement
Architectural Question: For OpenShift Container Platform bare metal deployments utilizing hardware where the Baseboard Management Controller (BMC) shares a system Network Interface Card (NIC) via NC-SI, how must the cluster ensure continuous BMC connectivity during power events?
Issue or Problem: OpenShift Container Platform require NC-SI compliant hardware when the BMC shares a system NIC. Without the correct configuration, powering down the host can cause the loss of BMC connectivity (NC-SI connection loss), interrupting bare metal provisioning or management operations.
Assumption: Bare Metal Operator is enabled.
Alternatives: BMC uses Network Controller Sideband Interface (NC-SI) for management traffic
BMC uses a dedicated network interface for management traffic
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: BMC uses Network Controller Sideband Interface (NC-SI) for management traffic: This approach reduces the overall physical network port requirement per server by allowing the BMC to share a system NIC with the host for management traffic. This method is supported on OpenShift Container Platform if the hardware is NC-SI compliant. However, this configuration mandates the use of the `DisablePowerOff` feature to ensure soft reboots do not result in the loss of BMC connectivity.
BMC uses a dedicated network interface for management traffic: This method enhances performance and improves security by isolating the BMC traffic onto a separate physical NIC and network, avoiding the complications and dependencies inherent in NC-SI deployments. This avoids the specific requirement to utilize the `DisablePowerOff` feature.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: BMC uses Network Controller Sideband Interface (NC-SI) for management traffic: Requires verification that BMCs and NICs support NC-SI. The `BareMetalHost` resource must be explicitly configured with `disablePowerOff: true` to prevent loss of BMC connectivity during soft reboots or OS shutdown events.
BMC uses a dedicated network interface for management traffic: This requires additional physical NIC hardware dedicated solely to out-of-band management. If a separate management network is implemented, the provisioner node must have routing access to this network for a successful installer-provisioned installation.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Infra Leader
#TODO#: Network Expert

☐ OCP-BM-12: Provisioning Network Strategy for Installer-Provisioned Bare Metal

---

**Title**
Provisioning Network Strategy for Installer-Provisioned Bare Metal

Title: Provisioning Network Strategy for Installer-Provisioned Bare Metal
Architectural Question: Will a dedicated provisioning network be used during IPI cluster deployment?
Issue or Problem: The Installer-Provisioned Infrastructure (IPI) deployment model, especially on bare metal, defaults to leveraging an optional, segregated provisioning network to manage tasks like DHCP, TFTP, and operating system deployment via Ironic. Deciding whether to utilize this network or provision entirely over the routable bare metal network dictates hardware requirements (NIC count) and the mandatory use of certain Baseboard Management Controller (BMC) protocols (virtual media).
Assumption: Cluster installation method is Installer-Provisioned Infrastructure (IPI).
Alternatives: A dedicated provisioning network is used for deploying the cluster
The provisioning will be performed on the routable bare metal network
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: A dedicated provisioning network is used for deploying the cluster: This method is the default Managed provisioning network setting. It automatically enables the Ironic-dnsmasq DHCP server on the provisioner node and is required for deployments using PXE booting. Using this network isolates the operating system provisioning traffic onto a non-routable network segment.
The provisioning will be performed on the routable bare metal network: This approach is configured by setting `provisioningNetwork: "Disabled"` in the `install-config.yaml` file. This simplifies networking requirements by eliminating the need for a dedicated physical NIC for provisioning. This option enables the use of the Assisted Installer.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: A dedicated provisioning network is used for deploying the cluster: Requires a dedicated physical network interface (NIC1) on all nodes, distinct from the routable baremetal network (NIC2). This network must be isolated and cannot have an external DHCP server if configured as Managed.
The provisioning will be performed on the routable bare metal network: This approach mandates the use of virtual media BMC addressing options (such as `redfish-virtualmedia` or `idrac-virtualmedia`). The BMCs must be accessible from the routable bare metal network. If disabled, the installation program requires two IP addresses on the bare metal network for provisioning services.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Infra Leader
#TODO#: Network Expert

☐ OCP-BM-13: IPI Provisioning Network DHCP Management Mode

---

**Title**
IPI Provisioning Network DHCP Management Mode

Title: IPI Provisioning Network DHCP Management Mode
Architectural Question: When utilizing a dedicated provisioning network during Installer-Provisioned Infrastructure (IPI) deployment, should the cluster allow Ironic to manage DHCP services, or should it rely on an existing external DHCP server?
Issue or Problem: The default IPI installation attempts to run an Ironic-managed DHCP service (`ironic-dnsmasq`) on the provisioning network. If another DHCP server is already present on this non-routable network, this causes conflicts and installation failure unless the provisioning network mode is explicitly changed to unmanaged.
Assumption: A dedicated provisioning network is configured for IPI deployment.
Alternatives: Managed Provisioning Network (Ironic DHCP)
Unmanaged Provisioning Network (External DHCP)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Managed Provisioning Network (Ironic DHCP): This is the default `Managed` provisioning network setting. It automatically enables the `ironic-dnsmasq` DHCP server on the provisioner node, isolating the operating system provisioning traffic onto a non-routable network segment.
Unmanaged Provisioning Network (External DHCP): This is configured by setting `provisioningNetwork` to a setting other than `Managed`. This is required if a DHCP server is already running on the provisioning network, as relying on an existing external server avoids conflicts with Ironic's integrated DHCP service.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Managed Provisioning Network (Ironic DHCP): This network must be isolated and cannot have an external DHCP server if configured as `Managed`.
Unmanaged Provisioning Network (External DHCP): The administrator is fully responsible for deploying and managing the highly available external DHCP service on the provisioning network to assign IP addresses to the bare metal nodes.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Network Expert
#TODO#: Infra Leader

☐ OCP-BM-14: IPI/Assisted Provisioning Boot Mechanism

---

**Title**
IPI/Assisted Provisioning Boot Mechanism

Title: IPI/Assisted Provisioning Boot Mechanism
Architectural Question: Which boot mechanism (iPXE or Redfish Virtual Media) should be standardized for provisioning bare metal hosts managed by the Bare Metal Operator (BMO)?
Issue or Problem: Automated bare metal provisioning (as used by IPI, ABI, and AI) requires a reliable method for the BMO/Ironic service to boot the discovery ISO on the physical host. The choice of method is constrained by network infrastructure and BMC capabilities.
Assumption: Cluster installation method is IPI, Agent-based Installer (ABI), or Assisted Installer (AI).
Alternatives: iPXE Booting (Network Boot)
Redfish Virtual Media Booting
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: iPXE Booting (Network Boot): Provides fast, zero-touch provisioning typically favored in centralized data centers. It relies on robust PXE/DHCP/TFTP infrastructure.
Redfish Virtual Media Booting: Leverages the BMC's ability to mount a remote ISO image, ensuring reliability even if the host's primary network configuration is complex. This is a common requirement for edge or disconnected deployments using ABI/AI.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: iPXE Booting (Network Boot): Requires a provisioning network and adherence to network prerequisites like DHCP, TFTP, and Web servers.
Redfish Virtual Media Booting: This is the mandatory choice if Provisioning Network is not used. It requires that the BMC supports the Virtual Media feature via the chosen Redfish/IPMI protocol.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Network Expert

☐ OCP-BM-15: Ironic RHCOS Image Transfer Protocol (Virtual Media)

---

**Title**
Ironic RHCOS Image Transfer Protocol (Virtual Media)

Title: Ironic RHCOS Image Transfer Protocol (Virtual Media)
Architectural Question: When deploying OpenShift Container Platform using virtual media for RHCOS image transfer via the Baseboard Management Controller (BMC), should the transfer rely on unencrypted HTTP or TLS-encrypted HTTPS?
Issue or Problem: When omitting the provisioning network, virtual media transfer is required. Using unencrypted HTTP for image transfer introduces a data security risk during the provisioning phase. However, enabling TLS/HTTPS adds operational complexity related to certificate trust management.
Assumption: Installation utilizes Virtual Media BMC addressing (e.g., `redfish-virtualmedia` or `idrac-virtualmedia`).
Alternatives: HTTP Image Transfer (Port 6180)
HTTPS/TLS Image Transfer (Port 6183)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: HTTP Image Transfer (Port 6180): This is the default HTTP port for image access. It simplifies the setup as it avoids the requirement for provisioning and managing TLS certificates for the provisioning service.
HTTPS/TLS Image Transfer (Port 6183): This enhances security by encrypting the RHCOS image transfer. Port 6183 is the required TLS port for virtual media installation.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: HTTP Image Transfer (Port 6180): The RHCOS image is transferred unencrypted, which may not meet security or compliance mandates.
HTTPS/TLS Image Transfer (Port 6183): Requires that the provisioner node and control plane nodes have port 6183 open on the baremetal network interface. Requires careful management of the certificate authority chain to ensure the BMC trusts the server.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: Network Expert
#TODO#: Infra Leader

☐ OCP-BM-16: UPI Provisioning Boot Mechanism

---

**Title**
UPI Provisioning Boot Mechanism

Title: UPI Provisioning Boot Mechanism
Architectural Question: How will Red Hat Enterprise Linux CoreOS (RHCOS) be provisioned onto the bare metal nodes when using UPI method deployment?
Issue or Problem: The method chosen to boot and install RHCOS on physical hardware dictates the required network infrastructure (e.g., PXE services) and the level of manual effort (e.g., ISO mounting). This decision is a prerequisite for User-Provisioned method.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: Install RHCOS using ISO (Customized Virtual Media or USB)
Install RHCOS using PXE (Network Boot)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Install RHCOS using ISO (Customized Virtual Media or USB): This method is viable for deployments of any size. When customized via `coreos-installer iso customize`, it allows the embedding of the Ignition config and installation device, enabling an automated, zero-touch boot-to-install cycle without relying on complex external PXE/TFTP infrastructure.
Install RHCOS using PXE (Network Boot): This method is highly desirable for full, scalable automation in large data centers where a dedicated network boot infrastructure (DHCP, TFTP) is already robustly managed.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Install RHCOS using ISO (Customized Virtual Media or USB): Requires a pre-processing step to create the customized media (ISO/USB). It relies on BMC/KVM access to mount the image, but significantly reduces Day 1 network prerequisites compared to PXE.
Install RHCOS using PXE (Network Boot): Enables full, scalable, "zero-touch" provisioning, which is ideal for large-scale UPI deployments. Requires significant prerequisite infrastructure (DHCP, TFTP, Web servers) and detailed network configuration.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Network Expert
#TODO#: Infra Leader

☐ OCP-BM-17: Ignition Configuration Integrity Validation Strategy

---

**Title**
Ignition Configuration Integrity Validation Strategy

Title: Ignition Configuration Integrity Validation Strategy
Architectural Question: How will the authenticity and integrity of the fetched Ignition Configuration files be validated during Red Hat Enterprise Linux CoreOS (RHCOS) node installation?
Issue or Problem: During manual RHCOS installation (ISO/PXE), the Ignition config files are downloaded from an HTTP/S server. Without verification, the system is vulnerable to fetching tampered configurations. If relying on HTTP, a hash is required for integrity validation.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: Validate using SHA512 Hash over HTTP/S
Validate using HTTPS TLS/CA Trust (without explicit hash)
Disable Integrity Validation (Insecure)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Validate using SHA512 Hash over HTTP/S: This approach provides a strong integrity check regardless of the network protocol (HTTP or HTTPS). Using the `--ignition-hash` is required when the Ignition config file is obtained through an HTTP URL to validate its authenticity.
Validate using HTTPS TLS/CA Trust (without explicit hash): If the Ignition configuration files are provided through an HTTPS server that uses TLS, the certificate authority (CA) can be added to the system trust store before running `coreos-installer`, ensuring integrity and confidentiality during transfer.
Disable Integrity Validation (Insecure): This simplifies installation and debugging by removing the dependency on HTTPS certificate authorities or manually verifying the SHA512 digest. Supported via the `--insecure-ignition` option.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Validate using SHA512 Hash over HTTP/S: Requires the administrator to obtain the SHA512 digest for each Ignition config file and pass it using the `--ignition-hash` option to `coreos-installer`.
Validate using HTTPS TLS/CA Trust (without explicit hash): If using a custom CA, requires adding the internal certificate authority (CA) to the system trust store via `coreos-installer` before installation to ensure the live installer can securely fetch the configuration.
Disable Integrity Validation (Insecure): Not recommended for production. This leaves the node vulnerable to accepting a compromised Ignition configuration file if the network or download URL is manipulated (Man-in-the-Middle).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: OCP Platform Owner

☐ OCP-BM-18: RHCOS Live Installer Custom CA Trust Strategy

---

**Title**
RHCOS Live Installer Custom CA Trust Strategy

Title: RHCOS Live Installer Custom CA Trust Strategy
Architectural Question: How will a custom Certificate Authority (CA) required to access secure installation artifacts (like the Ignition Config over HTTPS) be trusted by the Red Hat Enterprise Linux CoreOS (RHCOS) live installer environment during User-Provisioned Infrastructure (UPI) boot?
Issue or Problem: If the Ignition configuration files are served over HTTPS secured by a non-standard or corporate Certificate Authority (CA), the minimal live RHCOS installer environment (booted from ISO/PXE) will fail to download the configurations unless the custom CA is explicitly trusted. The standard mechanism for augmenting the cluster's trust bundle applies only after the node installs and boots.
Assumption: The cluster installation method is User-Provisioned Infrastructure (UPI) or PXE/ISO installation. The Ignition Configuration file URL uses HTTPS secured by a custom CA.
Alternatives: Customize Live Media with Embedded CA (--ignition-ca)
Rely on Default RHCOS Trust Bundle (Use HTTP or Public CA)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Customize Live Media with Embedded CA (--ignition-ca): This method provides the required trust for network-based installations that rely on a custom Certificate Authority (CA) during the minimal boot phase. It is achieved by using the `coreos-installer iso customize` or `coreos-installer pxe customize` subcommands with the `--ignition-ca cert.pem` flag.
Rely on Default RHCOS Trust Bundle (Use HTTP or Public CA): This approach simplifies the installation process by avoiding the media customization step. If relying on the default RHCOS trust bundle, the Ignition config must either be obtained over plain HTTP, requiring the SHA512 hash validation (via `--ignition-hash`), or accessed via HTTPS signed by a CA already present in the RHCOS trust bundle.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Customize Live Media with Embedded CA (--ignition-ca): Requires a pre-processing step to customize ("stamp") the ISO or initramfs file with the CA certificate before booting the media. This process ensures that the live environment can securely fetch the Ignition configuration files over HTTPS.
Rely on Default RHCOS Trust Bundle (Use HTTP or Public CA): If HTTPS with a custom CA is required for the Ignition URL, this option will result in the live installer failing to establish a secure connection, leading to installation failure. If the Ignition configuration is obtained via HTTP, the administrator must supply the SHA512 digest to `coreos-installer` using the `--ignition-hash` option to validate the content's integrity.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: Network Expert
#TODO#: OCP Platform Owner

☐ OCP-BM-19: RHCOS Image Signature Verification Policy for UPI Installation

---

**Title**
RHCOS Image Signature Verification Policy for UPI Installation

Title: RHCOS Image Signature Verification Policy for UPI Installation
Architectural Question: Should Red Hat Enterprise Linux CoreOS (RHCOS) installer images (used for UPI installation) require cryptographic signature verification, or should verification be explicitly disabled?
Issue or Problem: Supply chain integrity requires ensuring the OS image used for provisioning nodes has not been tampered with. The `coreos-installer` defaults to enforcing signatures, but specific bare metal installation paths or troubleshooting steps may require using the `--insecure` flag or `coreos.inst.insecure` kernel argument, which bypasses validation of the OS image.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: Enforce Image Signature Verification (Secure Default)
Disable Image Signature Verification (Insecure Mode)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Enforce Image Signature Verification (Secure Default): This option ensures the cluster only installs RHCOS images that have been cryptographically signed and verified, maintaining supply chain integrity. This is the recommended secure posture.
Disable Image Signature Verification (Insecure Mode): This is intended for debugging or installing a version of RHCOS that does not match the live media, especially since bare-metal media for OCP are not GPG-signed. Choosing this provides installation flexibility but removes a critical security barrier.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Enforce Image Signature Verification (Secure Default): Requires the use of supported installation media and methods that allow verification. Unauthorized or modified images will fail to install, enhancing security.
Disable Image Signature Verification (Insecure Mode): Leaves the cluster vulnerable to compromise if the installation media or the RHCOS image itself is tampered with prior to node installation.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: OCP Platform Owner

☐ OCP-BM-20: RHCOS Artifact Sourcing Strategy

---

**Title**
RHCOS Artifact Sourcing Strategy

Title: RHCOS Artifact Sourcing Strategy
Architectural Question: How will the necessary Red Hat Enterprise Linux CoreOS (RHCOS) installation artifacts (kernel, initramfs, rootfs, or ISO image) be reliably sourced for the cluster deployment process?
Issue or Problem: Sourcing RHCOS installation files directly from the public image mirror might lead to version misalignment or compatibility issues, especially if the artifacts have changed since the last installer release. A robust method is required to guarantee the correct, compatible artifacts are used for installation.
Assumption: N/A
Alternatives: Source artifacts via openshift-install coreos print-stream-json utility (Recommended)
Source artifacts directly from the RHCOS image mirror page
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Source artifacts via openshift-install coreos print-stream-json utility (Recommended): The recommended way to obtain the correct version of RHCOS images is from the output of the `openshift-install` command. This ensures the necessary compatibility is maintained.
Source artifacts directly from the RHCOS image mirror page: While possible, this method requires manually verifying that the downloaded images are the highest version less than or equal to the OpenShift Container Platform version being installed.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Source artifacts via openshift-install coreos print-stream-json utility (Recommended): Requires access to the `openshift-install` executable during the preparation phase.
Source artifacts directly from the RHCOS image mirror page: Increases the operational risk of using incompatible kernel/rootfs/initramfs files, potentially leading to installation failure.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BM-21: RHCOS Day-1 Customization and Network Configuration Strategy

---

**Title**
RHCOS Day-1 Customization and Network Configuration Strategy

Title: RHCOS Day-1 Customization and Network Configuration Strategy
Architectural Question: Which mechanism will be used to apply Day-1 configurations—specifically complex network settings (bonding, VLANs) and disk partitions—to RHCOS nodes during UPI installation?
Issue or Problem: Standard kernel arguments (`ip=`, `bond=`) are often insufficient or error-prone for enterprise bare metal deployments requiring complex network topologies (LACP bonds, multiple VLANs) or static IPs. A standardized method is required to inject these configurations reliably into the installation media to ensure successful bootstrapping and fetching of the ignition configuration.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: Kernel Arguments (Standard/Simple)
ISO/PXE Customization with Embedded Keyfiles (Advanced/Complex)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Kernel Arguments (Standard/Simple): Uses standard boot parameters (e.g., `ip=dhcp`, `coreos.inst.ignition_url=`) passed via the bootloader. This is sufficient for simple, single-interface DHCP environments but becomes unmanageable for complex bonding or static IP configurations due to character string complexity and lack of persistence features.
ISO/PXE Customization with Embedded Keyfiles (Advanced/Complex): Uses `coreos-installer iso/pxe customize` to embed NetworkManager Keyfiles (`.nmconnection`) and `MachineConfig` manifests directly into the initramfs of the installation media. This is the preferred and most robust method for enterprise deployments, as it supports complex LACP bonding, VLAN tagging, and static IPs natively without relying on fragile kernel argument strings.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Kernel Arguments (Standard/Simple): Works identically for ISO and PXE. High risk of syntax errors for complex networking. Changes require editing boot menus or PXE config files. Cannot apply configurations that exceed the kernel command line length limit.
ISO/PXE Customization with Embedded Keyfiles (Advanced/Complex): Requires a pre-processing step to "stamp" the ISO or initramfs with the configuration before booting. Enables "Infrastructure as Code" for the network config but adds a build step to the provisioning workflow.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Network Expert
#TODO#: Operations Expert

☐ OCP-BM-22: RHCOS Customization Timing Strategy (Live vs Permanent Ignition)

---

**Title**
RHCOS Customization Timing Strategy (Live vs Permanent Ignition)

Title: RHCOS Customization Timing Strategy (Live vs Permanent Ignition)
Architectural Question: Should Day-0 configuration tasks (e.g., advanced disk partitioning) be performed using a temporary Live Install Ignition config, or incorporated into the standard, persistent Permanent Install Ignition config via wrapped manifests?
Issue or Problem: The Live Install Ignition config runs immediately on boot and is required for complex, one-time setup (like advanced disk partitioning) that cannot be managed by the Machine Config Operator (MCO). However, using this mechanism adds a pre-processing step to the provisioning workflow.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Custom Day-0 tasks requiring non-MCO methods are needed (e.g., advanced partitioning).
Alternatives: Utilize Permanent Install Ignition Config (Embedded Manifests)
Utilize Live Install Ignition Config (ignition.config.url)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Utilize Permanent Install Ignition Config (Embedded Manifests): This method is preferred for standard cluster components and configurations that are consistently managed by the Machine Config Operator (MCO) throughout the cluster lifecycle.
Utilize Live Install Ignition Config (ignition.config.url): This is intended specifically for performing configuration tasks that must occur once and cannot be applied again later, such as complex disk partitioning.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Utilize Permanent Install Ignition Config (Embedded Manifests): This method cannot be used for highly specialized, one-time changes like complex custom disk partitioning.
Utilize Live Install Ignition Config (ignition.config.url): This requires appending specific kernel arguments (e.g., `ignition.config.url=`, `ignition.firstboot`, `ignition.platform.id=metal`) to the installation media, increasing setup complexity.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BM-23: RHCOS Live Network Configuration Persistence Strategy (UPI)

---

**Title**
RHCOS Live Network Configuration Persistence Strategy (UPI)

Title: RHCOS Live Network Configuration Persistence Strategy (UPI)
Architectural Question: When performing a manual User-Provisioned Infrastructure (UPI) installation of RHCOS from a live environment, how will the network configuration detected or used by the live installer be persisted to the installed system?
Issue or Problem: During manual RHCOS installation (ISO/PXE), the temporary live environment successfully obtains network settings (IP, DNS). This configuration must be transferred robustly to the permanent OS installation for successful first boot and Ignition fetch, and this persistence can be handled either implicitly by copying the live environment's state or explicitly via declarative mechanisms.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: Explicit Configuration (NetworkManager Keyfiles/Kernel Arguments)
Implicit Configuration (Copy Network Flag)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Explicit Configuration (NetworkManager Keyfiles/Kernel Arguments): This approach utilizes declarative configuration (NetworkManager Keyfiles embedded via `coreos-installer customize` or kernel arguments) to ensure the target OS configuration is strictly deterministic. It maintains consistency and is independent of how the live system initially derived its network settings.
Implicit Configuration (Copy Network Flag): This method simplifies the installation process by transferring the existing, validated network configuration used by the running live system directly to the installed operating system using the `--copy-network` flag with `coreos-installer install`.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Explicit Configuration (NetworkManager Keyfiles/Kernel Arguments): This requires a pre-processing step (like customizing the ISO/PXE image with `--network-keyfile`) or configuring kernel argument strings, adding complexity to the provisioning build step.
Implicit Configuration (Copy Network Flag): Achieved via the `--copy-network` option. This approach relies on the live environment successfully detecting or configuring the network correctly, making the persistence based on an implicit state transfer rather than a declared manifest.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Network Expert
#TODO#: Operations Expert
#TODO#: OCP Platform Owner

☐ OCP-BM-24: Node IP Address Management

---

**Title**
Node IP Address Management

Title: Node IP Address Management
Architectural Question: How will the cluster nodes (Control Plane and Compute) obtain their IP addresses from the Machine IP Range?
Issue or Problem: IP Address Management (IPAM) affects node address predictability, critical for setup, security policies, and installation method compatibility.
Assumption: N/A
Alternatives: DHCP
Static IP Configuration
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: DHCP: Simplifies node provisioning by automatically assigning IPs. Reduces manual configuration.
Static IP Configuration: Ensures persistent, predictable node IPs. For Agent-based Installer, this is achieved by embedding NMState configurations directly into the agent-config.yaml, allowing the ISO to boot with static networking without external DHCP.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: DHCP: Requires a highly available DHCP server, ideally with reservations. It is recommended that the DHCP server be configured to provide persistent IP addresses, DNS server information, and hostnames to all cluster machines for long-term management. Simplifies node scaling/replacement.
Static IP Configuration: Increases manual configuration effort during install and scaling. Requires a robust external IPAM process to avoid conflicts.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Network Expert

☐ OCP-BM-25: RHCOS Node Day-1 DNS Resolver Redundancy Strategy

---

**Title**
RHCOS Node Day-1 DNS Resolver Redundancy Strategy

Title: RHCOS Node Day-1 DNS Resolver Redundancy Strategy
Architectural Question: When statically configuring RHCOS nodes during UPI deployment, should multiple DNS server addresses be provided to the installer to enhance Day-1 connectivity and resilience?
Issue or Problem: During manual installation (UPI) with static IP addresses, RHCOS relies on kernel arguments to define networking. If only a single DNS server is configured and that server is unreachable, the bootstrapping process will fail as the node cannot resolve endpoints like the Ignition configuration server URL.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
The cluster machines are configured with static IP addresses during RHCOS installation.
Alternatives: Configure Multiple Redundant DNS Servers
Configure Only a Single Primary DNS Server
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Configure Multiple Redundant DNS Servers: This method provides stronger resilience for the RHCOS nodes during the critical bootstrapping phase by listing multiple upstream DNS resolvers using multiple `nameserver=` kernel arguments. This is achieved by adding a `nameserver=` entry for each server.
Configure Only a Single Primary DNS Server: This simplifies the configuration required in the kernel argument string. It is only sufficient if the specified DNS server is guaranteed to be highly available during the installation phase.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Configure Multiple Redundant DNS Servers: Requires meticulous coordination with the network team to identify and correctly configure all redundant enterprise DNS servers within the boot parameters.
Configure Only a Single Primary DNS Server: Introduces a Single Point of Failure (SPoF) for initial host-level name resolution, increasing the risk of installation failure.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Network Expert
#TODO#: Operations Expert
#TODO#: Security Expert

☐ OCP-BM-26: Multi-NIC Strategy for RHCOS Core Network (UPI)

---

**Title**
Multi-NIC Strategy for RHCOS Core Network (UPI)

Title: Multi-NIC Strategy for RHCOS Core Network (UPI)
Architectural Question: Should the core cluster network connectivity for RHCOS nodes leverage a single interface/bond, or multiple distinct, non-aggregated physical network interfaces (NICs)?
Issue or Problem: Utilizing multiple discrete physical network interfaces allows for traffic segmentation at the physical layer, but increases the complexity of network bootstrapping compared to a single aggregated interface.
Assumption: Cluster uses User-Provisioned Infrastructure (UPI).
Alternatives: Single Interface or Aggregated Interface (Bonding)
Multiple Discrete Network Interfaces (Configured Separately)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Single Interface or Aggregated Interface (Bonding): This approach simplifies initial configuration and reduces the number of kernel arguments required during installation. It provides redundancy at the link layer while presenting a single logical interface to the OS.
Multiple Discrete Network Interfaces (Configured Separately): This allows for strict physical isolation of traffic types (e.g., separating management traffic from data traffic on different physical hardware) without relying on VLAN tagging over a shared bond.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Single Interface or Aggregated Interface (Bonding): May limit flexibility if strict physical air-gapping between network segments is required.
Multiple Discrete Network Interfaces (Configured Separately): Requires careful planning and configuration of multiple kernel arguments (e.g., multiple `ip=` entries) during the RHCOS installation process. Increases the complexity of the Day 1 configuration.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Network Expert
#TODO#: Infra Leader

☐ OCP-BM-27: Bare Metal Network Bridge Configuration Tooling Strategy

---

**Title**
Bare Metal Network Bridge Configuration Tooling Strategy

Title: Bare Metal Network Bridge Configuration Tooling Strategy
Architectural Question: Which method will be standardized for configuring the Open vSwitch (OVS) br-ex bridge network on bare metal nodes, balancing simplicity for single-NIC setups against flexibility for advanced and multi-NIC post-installation changes?
Issue or Problem: The choice of tooling (shell script vs. MachineConfig/NMState) determines whether post-installation network changes are supported and limits the ability to define advanced network configurations (e.g., specific interfaces or complex topologies) for the br-ex bridge.
Assumption: N/A
Alternatives: Configure br-ex using the configure-ovs.sh Shell Script (Single NIC/Simple Default)
Configure br-ex using NMState Configuration embedded in a MachineConfig
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Configure br-ex using the configure-ovs.sh Shell Script (Single NIC/Simple Default): This approach is simpler and should be used if the environment requires a single Network Interface Controller (NIC) and default network settings. It minimizes initial complexity.
Configure br-ex using NMState Configuration embedded in a MachineConfig: This method is recommended when advanced configurations are required, such as deploying the bridge on a different interface, supporting post-installation changes to the bridge network, or implementing configurations not possible with the shell script (e.g., complex multi-interface setups).
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Configure br-ex using the configure-ovs.sh Shell Script (Single NIC/Simple Default): This script does not support making post-installation changes to the bridge. Using the script for advanced configurations may result in the bridge failing to connect multiple network interfaces.
Configure br-ex using NMState Configuration embedded in a MachineConfig: Requires defining and managing an NMState configuration file and corresponding MachineConfig object. This process involves base64 encoding the configuration and embedding it in the manifest. The NMState configuration must include `auto-route-metric: 48` to ensure the `br-ex` default route has the highest precedence, preventing routing conflicts.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Network Expert
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BM-28: NMState Configuration Scope for Provisioning

---

**Title**
NMState Configuration Scope for Provisioning

Title: NMState Configuration Scope for Provisioning
Architectural Question: Should NMState configuration, embedded via MachineConfig during bare metal provisioning, be applied using a single cluster-wide file or separated into node-specific files?
Issue or Problem: When defining customized network configurations via NMState embedded in MachineConfig, a standard methodology is required to manage configuration scope, balancing the simplicity of a global file against the need for node-specific overrides.
Assumption: Network configuration requires NMState and is delivered via MachineConfig.
Alternatives: Cluster-wide Global Configuration
Node-specific Configuration Files
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Cluster-wide Global Configuration: Minimizes complexity by applying the same configuration (e.g., `/etc/nmstate/openshift/cluster.yml`) to all nodes. This approach simplifies configuration management when the hardware profile is homogeneous.
Node-specific Configuration Files: Allows for configuration overrides and specific tailoring for individual nodes by defining separate files keyed by the short hostname (e.g., `/etc/nmstate/openshift/worker-0.yml`).
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Cluster-wide Global Configuration: Less suitable if nodes have heterogeneous network interfaces or need per-host variations.
Node-specific Configuration Files: Increases the manifest complexity by requiring explicit configuration entries for each node in the cluster.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Network Expert
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BM-29: Cluster Node Hostname Assignment Strategy (User-Provisioned Infrastructure)

---

**Title**
Cluster Node Hostname Assignment Strategy (User-Provisioned Infrastructure)

Title: Cluster Node Hostname Assignment Strategy (User-Provisioned Infrastructure)
Architectural Question: How will the hostnames for OpenShift cluster nodes (RHCOS) in a User-Provisioned Infrastructure (UPI) deployment be determined and maintained?
Issue or Problem: In UPI deployments, RHCOS nodes must obtain a hostname during boot. If this is not explicitly provided by DHCP, the system defaults to using reverse DNS lookup, which can be slow and result in critical system services detecting the hostname as "localhost". A stable and quickly resolved hostname is required for node readiness and CSR generation.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: DHCP-Provided Hostnames (Recommended)
Reverse DNS Lookup (Default Fallback)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: DHCP-Provided Hostnames (Recommended): This approach minimizes operational risk by ensuring the hostname is obtained quickly and reliably during network initialization. It simplifies Day 1 setup and bypasses manual DNS record configuration errors in environments that use DNS split-horizon implementations.
Reverse DNS Lookup (Default Fallback): This requires minimal specific configuration on the DHCP server side, relying solely on the presence of accurate PTR records in the DNS infrastructure.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: DHCP-Provided Hostnames (Recommended): Requires ensuring the DHCP server is configured to provide persistent IP addresses, DNS server information, and hostnames to all cluster machines for long-term management.
Reverse DNS Lookup (Default Fallback): Node initialization can be delayed while the reverse DNS lookup occurs, potentially causing system services to incorrectly start with "localhost" as the hostname.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Network Expert
#TODO#: Infra Leader

☐ OCP-BM-30: Host Network Bonding Mode for High Availability (OVS)

---

**Title**
Host Network Bonding Mode for High Availability (OVS)

Title: Host Network Bonding Mode for High Availability (OVS)
Architectural Question: When configuring high availability for bare metal node network interfaces, should the solution rely on standard kernel bonding methods or utilize the specialized OVS balance-slb mode?
Issue or Problem: When provisioning bare metal nodes for high-performance workloads (like OpenShift Virtualization), standard bonding modes (like active-backup or LACP) may not effectively distribute traffic for OVN-Kubernetes pods or VMs that share the same physical link characteristics (MAC/VLAN). A mode is needed to ensure true load balancing for this traffic.
Assumption: The cluster hosts performance-sensitive workloads (e.g., virtualization) that rely on OVS-based networking for High Availability.
Alternatives: Standard NetworkManager/Kernel Bonding
Open vSwitch (OVS) balance-slb Mode
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Standard NetworkManager/Kernel Bonding: Relies on the host OS/NetworkManager for bonding implementation (e.g., active-backup). While simpler to configure, it does not guarantee load distribution for OVN-Kubernetes traffic which uses consistent MAC/VLAN combinations.
Open vSwitch (OVS) balance-slb Mode: This mode is specifically designed and supported for virtualization workloads on bare metal. It natively supports source load balancing for OVN-Kubernetes CNI plugin traffic, ensuring that traffic from different VM ports is balanced over the physical interface links.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Standard NetworkManager/Kernel Bonding: May lead to sub-optimal performance or lack of true load balancing for OVN-Kubernetes/VM traffic, impacting HA and resource utilization.
Open vSwitch (OVS) balance-slb Mode: Requires complex network configuration, potentially involving OVS bonding modes like `balance-slb`, managed via MachineConfig/NMState configuration during installation.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Network Expert
#TODO#: Infra Leader

☐ OCP-BM-31: Bare Metal Node Secure Boot Strategy

---

**Title**
Bare Metal Node Secure Boot Strategy

Title: Bare Metal Node Secure Boot Strategy
Architectural Question: Will Secure Boot be enabled on bare metal cluster nodes?
Issue or Problem: Secure Boot is often required for security compliance to ensure nodes only boot with trusted software. The implementation method chosen (disabled, manual, or managed) has different operational overheads, specific setup requirements (e.g., reliance on Redfish virtual media), and stringent hardware compatibility restrictions.
Assumption: The bare metal hardware supports UEFI boot mode and Secure Boot functionality.
Alternatives: Secure Boot will not be enabled
Secure Boot will be enabled manually
Secure Boot will be enabled through Managed Secure Boot (TP)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Secure Boot will not be enabled: This simplifies installation and avoids the complex hardware compatibility constraints associated with enabling Secure Boot.
Secure Boot will be enabled manually: This approach utilizes the node's native Secure Boot feature, which is supported during IPI deployments when using Redfish virtual media. This is also the only supported method for UPI deployment. This method provides flexibility across more diverse hardware platforms compared to the Managed option and avoids reliance on a Technology Preview feature.
Secure Boot will be enabled through Managed Secure Boot (TP): This option automates Secure Boot provisioning by setting `bootMode: "UEFISecureBoot"` in the `install-config.yaml` file. It streamlines node configuration and management, and crucially, does not require using Redfish virtual media for the installation.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Secure Boot will not be enabled: This approach might fail to meet security or regulatory compliance standards that require verifying the integrity of the boot chain.
Secure Boot will be enabled manually: Requires manual configuration of UEFI boot mode and Secure Boot settings on each control plane and worker node. This is the only supported method when using UPI deployment. Furthermore, Red Hat explicitly supports this manual configuration for IPI only when the installation uses Redfish virtual media.
Secure Boot will be enabled through Managed Secure Boot (TP): This capability is currently designated as a Technology Preview (TP) feature and is only supported on specific, verified hardware models.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: Infra Leader

☐ OCP-BM-32: Boot disks encryption

---

**Title**
Boot disks encryption

Title: Boot disks encryption
Architectural Question: Will the RHCOS boot disks be encrypted, and which key management mechanism will be used for automated unlocking upon node boot?
Issue or Problem: Servers often require full disk encryption (LUKS) for security compliance. A decision must be made on whether to encrypt, and if so, how to manage the decryption keys to allow for automated, unattended reboots. The feasibility of using network-bound keys (Tang) versus hardware-bound keys (TPM) is constrained by the choice of OpenShift installer.
Assumption: Platform infrastructure is vSphere or baremetal. The cluster installation method has been determined.
Alternatives: No disk encryption (Default)
TPM v2 Only Unlock
Tang Server Only Unlock (UPI)
TPM v2 and Tang Server Combination (UPI)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: No disk encryption (Default): This is the default behavior. It simplifies installation and node provisioning, as no additional key management infrastructure (TPM, Tang) or configuration is required. It relies solely on physical data center security for data-at-rest protection.
TPM v2 Only Unlock: This method uses the on-board TPM v2 chip to seal the decryption key. The key is only released if the boot measurements (PCRs) are correct, ensuring the system's boot chain has not been tampered with. This is a high-security, self-contained solution.
Tang Server Only Unlock (UPI): This method uses a network-bound key release. The node fetches its decryption key from a highly available Tang server on the network during boot. This decouples the key from the hardware state, simplifying operational events like firmware updates.
TPM v2 and Tang Server Combination (UPI): This is the most resilient automated method. The node can be configured to unlock if either the TPM measurements are correct or it can successfully contact the Tang server. This provides the security of TPM binding while adding the operational flexibility of Tang.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: No disk encryption (Default): Simplest and fastest provisioning. No external dependencies for boot. Fails to meet many security and compliance standards for data-at-rest encryption.
TPM v2 Only Unlock: High security, as the key is bound to the hardware state. No external infrastructure (like Tang) is needed. Node recovery after expected changes (like a BIOS or firmware update) can be complex. This is the only disk encryption method supported by Installer-Provisioned Infrastructure (IPI), Agent-based Installer (ABI), and Assisted Installer methods. The Image-based Installer (IBI) does not support disk encryption.
Tang Server Only Unlock (UPI): Decouples the key from the hardware state (TPM PCRs), making firmware updates non-disruptive. Creates a hard dependency on the network and the Tang servers. This option is supported only by User-Provisioned Infrastructure (UPI) deployments. The Image-based Installer (IBI) does not support disk encryption.
TPM v2 and Tang Server Combination (UPI): Provides the "best of both worlds": high security (TPM) and operational flexibility (Tang). This option is supported only by User-Provisioned Infrastructure (UPI) deployments. The Image-based Installer (IBI) does not support disk encryption.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: Storage Expert

☐ OCP-BM-33: Bare Metal Host Firmware Configuration Management

---

**Title**
Bare Metal Host Firmware Configuration Management

Title: Bare Metal Host Firmware Configuration Management
Architectural Question: How will host firmware settings (BIOS/UEFI) be applied, validated, and maintained to ensure consistency and compliance across the bare metal fleet?
Issue or Problem: Managing firmware settings manually across a fleet of physical servers leads to configuration drift, inconsistent node behavior, and increased troubleshooting time. A standardized method is required to ensure that every host is provisioned with the exact same BIOS/UEFI configuration defined by the platform standards.
Assumption: Provisioning workflow is GitOps ZTP.
Alternatives: Manual/Out-of-Band Configuration
Automated Configuration via GitOps ZTP/ClusterInstance
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Manual/Out-of-Band Configuration: Relies on server administrators manually configuring BIOS settings via vendor consoles (e.g., iDRAC, iLO) or ad-hoc scripts. This is prone to human error and makes auditing the actual state of the fleet difficult.
Automated Configuration via GitOps ZTP/ClusterInstance: Uses the Infrastructure-as-Code model. Firmware settings are defined in a `HardwareProfile` file stored in Git and referenced by the `ClusterInstance` (`biosConfigRef`). The underlying automation (BMO) applies these settings during provisioning, ensuring every node matches the definition in Git.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Manual/Out-of-Band Configuration: High operational overhead. No automated way to detect or remediate if a server's settings drift from the standard.
Automated Configuration via GitOps ZTP/ClusterInstance: Requires creating and maintaining hardware profile files (e.g., `.profile`) in the Git repository. Provides a single source of truth for hardware configuration, simplifying audits and disaster recovery.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Operations Expert

☐ OCP-BM-34: RHCOS Node Console Access Strategy

---

**Title**
RHCOS Node Console Access Strategy

Title: RHCOS Node Console Access Strategy
Architectural Question: Which console mechanism (Graphical, Serial, or both) will be configured as the primary interface for OpenShift Container Platform nodes installed on bare metal to facilitate troubleshooting and out-of-band access?
Issue or Problem: Bare metal RHCOS nodes installed from a boot image use default kernel settings, which typically results in the graphical console being primary and the serial console being disabled. This may conflict with operational requirements, such as accessing the emergency shell for debugging or if the underlying infrastructure only provides serial console access.
Assumption: N/A
Alternatives: Default Console Configuration (Graphical Primary, Serial Disabled)
Serial Console Configuration (Serial Primary, Graphical Secondary)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Default Console Configuration (Graphical Primary, Serial Disabled): This setting is inherited from the boot image. It uses kernel default settings, which is standard but may prevent remote interactive access if the platform does not easily expose the graphical console.
Serial Console Configuration (Serial Primary, Graphical Secondary): Explicitly configures the serial console (e.g., `console=ttyS0,`). This is necessary for environments where console access is crucial for management or when the cloud platform does not provide interactive access to the graphical console.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Default Console Configuration (Graphical Primary, Serial Disabled): Requires careful evaluation to ensure troubleshooting capabilities meet disaster recovery requirements if the graphical console is not easily accessible.
Serial Console Configuration (Serial Primary, Graphical Secondary): Requires adding one or more `console=` arguments (e.g., `console=tty0 console=ttyS0`) to the APPEND line during PXE installation, or using the `--console` option with `coreos-installer` during manual ISO installation to set the serial port as the primary console. Note: For automated ISO/PXE artifact customization, this setting can be persisted by using the `coreos-installer iso customize` command with the `--dest-console` flag (e.g., `--dest-console ttyS0,115200n8`).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BM-35: RHCOS Installation Boot Device Selection

---

**Title**
RHCOS Installation Boot Device Selection

Title: RHCOS Installation Boot Device Selection
Architectural Question: Will Red Hat Enterprise Linux CoreOS (RHCOS) be installed and booted from local internal storage (e.g., NVMe, SATA SSD) or from network-attached SAN storage (iSCSI/Fibre Channel)?
Issue or Problem: The choice of boot device impacts storage management, failure domains, and the complexity of the installation process. Integrating with existing Storage Area Networks (SANs) requires specific installation steps (Zoning, LUN masking, WWN/IQN configuration) not needed for local disk deployment.
Assumption: N/A
Alternatives: Local Disk Installation (Internal NVMe/SSD/HDD)
SAN Storage (iSCSI/Fibre Channel)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Local Disk Installation (Internal NVMe/SSD/HDD): This is the default, simpler installation path, requiring less complex networking and kernel configuration during the RHCOS installation boot process.
SAN Storage (iSCSI/Fibre Channel): This is required to leverage centralized, highly available, and potentially multi-pathed SAN infrastructure for the OS root disk. It supports fully diskless machines (Boot from SAN) and allows the OS disk to survive physical server chassis replacement.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Local Disk Installation (Internal NVMe/SSD/HDD): Resilience relies entirely on the local disk health (e.g., RAID, if configured). Storage capacity and performance are confined to the internal server limits.
SAN Storage (iSCSI/Fibre Channel): Significantly increases installation complexity. For iSCSI: Requires configuration of the target portal, IQN, and LUN, either manually or via iBFT. For Fibre Channel: Requires HBAs, correct fabric zoning, and LUN masking to the HBA's WWN. Both require the multipath configuration to be enabled during installation to prevent I/O errors.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Storage Expert
#TODO#: Infra Leader

☐ OCP-BM-36: iSCSI Boot Configuration Method for RHCOS

---

**Title**
iSCSI Boot Configuration Method for RHCOS

Title: iSCSI Boot Configuration Method for RHCOS
Architectural Question: When using an iSCSI boot device for RHCOS, should the configuration be handled manually via the live installer shell/scripts and kernel arguments, or automatically via iBFT (iSCSI Boot Firmware Table)?
Issue or Problem: Installing RHCOS onto iSCSI requires the initiator and target information (IQN, LUN, etc.) to be passed to the kernel and the `coreos-installer`. A choice must be made between highly automated firmware integration (iBFT) and explicit manual configuration/scripting.
Assumption: iSCSI boot device is used
Alternatives: Manual/Scripted iSCSI Configuration
iBFT/Firmware-Based iSCSI Configuration
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Manual/Scripted iSCSI Configuration: Allows explicit control over the entire iSCSI mounting and unmounting process utilizing coreos-installer scripting hooks (`--pre-install` / `--post-install`) to run `iscsiadm` commands manually. This is the standard method for implementing complex Day 1 storage logic that cannot be handled by firmware.
iBFT/Firmware-Based iSCSI Configuration: Enables a more automated, cleaner configuration path for diskless machines by allowing the RHCOS installer to read the iSCSI parameters directly from the BIOS firmware during boot. This simplifies the kernel argument configuration during PXE/ISO boot.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Manual/Scripted iSCSI Configuration: Higher setup complexity requiring maintenance of external scripts and detailed kernel parameter passing during boot, but offers maximum flexibility, especially if the firmware is older or iBFT support is unreliable.
iBFT/Firmware-Based iSCSI Configuration: Requires ensuring BIOS/UEFI firmware is correctly configured to expose the iSCSI parameters. If not properly configured, installation will fail without manual overrides.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert
#TODO#: Storage Expert
#TODO#: Infra Leader

☐ OCP-BM-37: RHCOS Multipathing Enablement Strategy (Boot and Secondary Disks)

---

**Title**
RHCOS Multipathing Enablement Strategy (Boot and Secondary Disks)

Title: RHCOS Multipathing Enablement Strategy (Boot and Secondary Disks)
Architectural Question: Will multipathing be explicitly enabled for Red Hat Enterprise Linux CoreOS (RHCOS) disks (primary boot or secondary data disks) during installation to enhance resilience against hardware failure?
Issue or Problem: Multipathing is essential for highly available storage backends (especially iSCSI/Fibre Channel), providing redundant data paths. Failure to enable it at installation time prevents its use for the boot disk. Furthermore, secondary disks (like `/var/lib/containers`) require a different configuration mechanism (Ignition/Systemd) than the boot disk (Kernel Arguments).
Assumption: Installation Boot Device or Secondary Storage is a SAN device.
Alternatives: Enable Multipathing at Installation Time
Rely on Default Single-Path Configuration
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Enable Multipathing at Installation Time: This is the recommended approach for providing stronger resilience.
For Primary Boot Disks: Configured via kernel arguments (`rd.multipath=default`) passed to the installer.
For Secondary Data Disks: Configured using Ignition/Butane manifests to define the necessary `multipathd` systemd units and filesystem mounts, ensuring consistency from Day 1.
Rely on Default Single-Path Configuration: This avoids the complexity of installing Multipathd and configuring the device mapper during the Day 1 installation process. Suitable only if the underlying storage provides a single path or redundancy is handled at the array level.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Enable Multipathing at Installation Time: Mandatory in setups where non-optimized paths result in I/O system errors.
Boot Disk: Requires explicit kernel arguments.
Secondary Disk: Requires maintaining custom Butane/Ignition manifests. Failure to configure the systemd units correctly via Ignition will result in secondary disks mounting as single paths, creating a hidden Single Point of Failure.
Rely on Default Single-Path Configuration: Increases the vulnerability of the node to a Single Point of Failure (SPoF) if a network path, cable, or HBA connected to the storage array fails. Not recommended for production environments requiring high availability.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert
#TODO#: Storage Expert
#TODO#: Infra Leader

☐ OCP-BM-38: RHCOS Multipath Installation Target Naming

---

**Title**
RHCOS Multipath Installation Target Naming

Title: RHCOS Multipath Installation Target Naming
Architectural Question: When installing RHCOS onto a primary multipathed SAN storage device, should the `coreos-installer` target the generic device mapper path or the unique World Wide Name (WWN) symlink?
Issue or Problem: When multiple multipath devices are connected or device enumeration changes, using non-explicit device names can reduce installation reliability. A clear, persistent naming convention for the installation target device is required to maintain automation robustness.
Assumption: Installation Boot Device is SAN device.
Multipathing to be enabled.
Alternatives: Use World Wide Name (WWN) Symlink
Use Generic Device Mapper Path
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Use World Wide Name (WWN) Symlink: This approach is explicitly recommended when multiple multipath devices are connected to the machine, or when greater explicitness is required, because the symlink provides persistence in device identification. The WWN symlink is available in `/dev/disk/by-id` and represents the target multipathed device.
Use Generic Device Mapper Path: This method simplifies the command line argument (e.g., `/dev/mapper/mpatha`).
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Use World Wide Name (WWN) Symlink: Requires an explicit step to identify the WWN ID of the target multipathed device, and the installation command must reference the persistent path (e.g., `/dev/disk/by-id/wwn-`).
Use Generic Device Mapper Path: If multiple multipath devices exist or if device mapping changes unpredictably, this path may be less reliable for automated provisioning compared to the explicit WWN symlink.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Infra Leader
#TODO#: Storage Expert
#TODO#: Operations Expert

☐ OCP-BM-39: RHCOS Installation Drive Identification Strategy

---

**Title**
RHCOS Installation Drive Identification Strategy

Title: RHCOS Installation Drive Identification Strategy
Architectural Question: How should the installation target disk device (e.g., local disk, non-multipath SAN LUN) be specified to the `coreos-installer` during Red Hat Enterprise Linux CoreOS (RHCOS) installation to ensure persistence and reliability?
Issue or Problem: Using ephemeral device paths (e.g., `/dev/sda`) can lead to installation failure or inconsistent behavior if the kernel enumerates devices differently across reboots or installations, disrupting automation scripts. A persistent naming convention is required for robust deployment automation.
Assumption: Installation target is a local disk or single-path SAN LUN.
Alternatives: Volatile Device Path Naming
Persistent Device Path Naming
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Volatile Device Path Naming: This approach simplifies command usage (e.g., using `/dev/sda`) and is explicitly allowed for the `coreos.inst.install_dev` kernel argument.
Persistent Device Path Naming: This is the recommended practice. It prevents errors related to device enumeration changes upon reboot, which is critical for reliable automation and large-scale deployments. For Agent-based/Assisted Installer, this utilizes the rootDeviceHints API (matching by Model, Serial, or WWN) to deterministically select the boot drive regardless of kernel enumeration order. For multipath devices, using the World Wide Name (WWN) symlink available in `/dev/disk/by-id` is explicitly recommended over simpler paths.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Volatile Device Path Naming: This carries a high risk of installation failure if the device naming changes (e.g., `/dev/sda` becomes `/dev/sdb`), which is common in environments where device enumeration is not strictly controlled.
Persistent Device Path Naming: Requires an additional step in the automation workflow to identify the persistent device path (e.g., `by-id`, `by-path`, or `by-wwn`) of the target installation disk before executing `coreos-installer`.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Infra Leader
#TODO#: Operations Expert

☐ OCP-BM-40: Hardware RAID Configuration for Bare Metal Installation Drive

---

**Title**
Hardware RAID Configuration for Bare Metal Installation Drive

Title: Hardware RAID Configuration for Bare Metal Installation Drive
Architectural Question: On bare metal nodes, how should hardware RAID be configured for the installation drive, ensuring compatibility with supported BMCs and adhering to Red Hat requirements?
Issue or Problem: The choice of hardware RAID must align with Red Hat requirements: only specific Hardware RAID volumes (e.g., Dell iDRAC, Fujitsu iRMC) are supported on the installation drive, and software RAID is not supported. This decision determines whether to utilize supported hardware RAID features or configure nodes without RAID for the installation drive.
Assumption: Installation Boot Device is Local Device.
Alternatives: Configure and use supported Hardware RAID volumes for the installation drive.
Configure the installation drive without using Hardware RAID.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Configure and use supported Hardware RAID volumes for the installation drive: Leveraging hardware RAID provides disk redundancy and potential performance improvements managed entirely by the hardware controller/BMC interface, which is supported for specific configurations.
Configure the installation drive without using Hardware RAID: This simplifies the underlying storage configuration and avoids potential compatibility issues, focusing solely on single disk volumes. This relies on internal cluster components like etcd managing their own redundancy.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Configure and use supported Hardware RAID volumes for the installation drive: Requires ensuring the hardware, BMC firmware, and RAID levels match the specific configurations officially supported for use as the installation drive.
Configure the installation drive without using Hardware RAID: Simplifies the underlying storage configuration, avoiding configuration complexities, but software RAID is not supported for the installation drive. This relies solely on redundancy provided by software volumes (e.g., etcd).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Security Expert
#TODO#: Storage Expert

☐ OCP-BM-41: Control Plane Storage Performance Validation Strategy

---

**Title**
Control Plane Storage Performance Validation Strategy

Title: Control Plane Storage Performance Validation Strategy
Architectural Question: What is the strategy for automatically configuring and validating the storage performance for etcd (on control plane nodes) to ensure cluster stability?
Issue or Problem: Etcd is extremely sensitive to disk write latency. If the storage cannot sustain a specific performance metric (fsync duration < 10ms at the 99th percentile), the cluster will experience instability, leader elections, and potential outages.
Assumption: N/A
Alternatives: Pre-flight Benchmark Validation (Strict)
Specification-Based Provisioning (Standard)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Pre-flight Benchmark Validation (Strict): This treats performance as a hard prerequisite. It creates a "Go/No-Go" gate based on real-world metrics, such as running the standard Red Hat etcd test: `fio --rw=write --ioengine=sync --fdatasync=1 --directory=/var/lib/etcd`. If the 99th percentile result is > 10ms, the hardware is rejected. This guarantees stability but adds time to the provisioning process.
Specification-Based Provisioning (Standard): This approach trusts the infrastructure provider's SLA. It significantly speeds up deployment by skipping manual testing. It is appropriate when using standardized, known-good SKUs (e.g., Enterprise NVMe or a specific Tier 1 SSD model) where performance variance is known to be low.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Pre-flight Benchmark Validation (Strict): Requires a pre-install automation step to run a bare metal benchmarking tool (e.g., fio). This catches "bad drives" or "noisy neighbor" issues early but increases deployment complexity.
Specification-Based Provisioning (Standard): Removes the validation overhead. However, it introduces the risk of "silent" performance degradation where a disk meets the throughput spec but fails the latency requirement (fsync), which may only be discovered during a production outage.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Storage Expert

☐ OCP-BM-42: Bare Metal Minimum Boot Disk Capacity Strategy

---

**Title**
Bare Metal Minimum Boot Disk Capacity Strategy

Title: Bare Metal Minimum Boot Disk Capacity Strategy
Architectural Question: What is the standardized minimum capacity for the primary boot drive across the bare metal fleet to support lifecycle operations, logging, and partitioning requirements?
Issue or Problem: While OpenShift supports small boot drives (e.g., 120GB for SNO), advanced configurations such as separate `/var` partitioning, image pre-caching for edge upgrades (IBU), or retention of verbose failure logs require significantly more space. Failing to standardize on a sufficient minimum capacity prevents the adoption of these resiliency patterns later in the cluster lifecycle.
Assumption: RHCOS Installation Boot Device Selection has been defined.
Alternatives: Minimal Capacity (e.g., 120GB)
Expanded Capacity (e.g., 500GB or greater)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Minimal Capacity (e.g., 120GB): Meets the absolute minimum requirements for a Single Node OpenShift (SNO) or standard node deployment. It reduces hardware costs but leaves very little headroom for Day 2 operations, log retention, or custom partitioning.
Expanded Capacity (e.g., 500GB or greater): Recommended for production environments. This provides the necessary storage buffer to safely implement General /var Partitioning, store pre-cached update images (saving bandwidth at the edge), and retain system logs during failure triage without triggering disk pressure evictions.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Minimal Capacity (e.g., 120GB): Severely restricts the ability to use custom disk partitioning. The separate `/var` partitioning strategy is not recommended and likely impossible on this size due to the overhead of the immutable OS partitions.
Expanded Capacity (e.g., 500GB or greater): Increases the per-node hardware cost. Enables robust "Image-Based Upgrade" workflows by allowing multiple OS versions (stateroots) to coexist on the disk. Supports isolating volatile data (`/var`) to protect the root filesystem.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Infra Leader
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-BM-43: RHCOS /var Partitioning Strategy (General Data Isolation)

---

**Title**
RHCOS /var Partitioning Strategy (General Data Isolation)

Title: RHCOS /var Partitioning Strategy (General Data Isolation)
Architectural Question: Should the core RHCOS boot disk be partitioned to include a separate, dedicated partition for the entire `/var` directory to manage system log/data growth and simplify subsequent node reinstallation?
Issue or Problem: Allowing the potentially volatile contents of the `/var` directory (which holds data like logs and container images) to remain solely on the root partition risks system instability due to aggressive application logging or large data growth consuming the root filesystem space. Implementing a dedicated partition isolates this volatile data.
Assumption: The cluster will utilize large disk sizes (e.g., > 100GB) and may host applications requiring logging or large caches that reside in `/var`.
Alternatives: Dedicated Partition for /var
Co-locate /var on the Root Partition (Default)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Dedicated Partition for /var: This approach prevents data growth within `/var` (such as audit data or logs) from filling up the root file system. It is recommended for disk sizes larger than 100GB, and especially larger than 1TB. This method also supports reinstalling OpenShift Container Platform while keeping the `/var` data intact, accelerating recovery by preventing the need for massive container pulls post-reinstall.
Co-locate /var on the Root Partition (Default): This option relies on the default disk partitioning created during the RHCOS installation, which simplifies the initial configuration process.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Dedicated Partition for /var: This configuration increases complexity during the installation process, as it requires setting up a custom MachineConfig manifest (e.g., using a Butane config).
CONSTRAINT NOTE: When adding a data partition to the boot disk, a minimum offset value of 25000 mebibytes is recommended; if the offset is smaller than this minimum, the resulting root file system will be too small, risking future reinstalls of RHCOS overwriting the data partition.
Additionally, mixing different instance types for compute nodes is not supported if those instance types do not have the same storage device name.
Co-locate /var on the Root Partition (Default): This configuration carries a high risk of disk exhaustion affecting system stability if container usage, logs, or other system data within `/var` is heavy or unpredictable.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Storage Expert
#TODO#: Operations Expert

☐ OCP-BM-44: Bare Metal Node OS Disk Partitioning for Container Storage

---

**Title**
Bare Metal Node OS Disk Partitioning for Container Storage

Title: Bare Metal Node OS Disk Partitioning for Container Storage
Architectural Question: How should the root disk be partitioned on bare metal nodes to accommodate container runtime storage (`/var/lib/containers`), specifically concerning separation from the operating system partition, and what filesystem options should be used?
Issue or Problem: If the container storage (`/var/lib/containers`) directory resides on the same partition as its parent filesystem (Root or `/var`), aggressive application logging or large image pull caches can lead to the node running out of disk space. This potentially causes instability by starving the OS or critical logging services.
Assumption: General /var Partitioning Strategy is defined.
Alternatives: Dedicated partition for `/var/lib/containers`
Co-locate `/var/lib/containers` on the parent partition (Root or `/var`)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Dedicated partition for `/var/lib/containers`: This is the recommended approach for workload partitioning and robustness, explicitly setting up a separate partition, formatted with `xfs` and mounted using `prjquota` for appropriate resource handling. This practice isolates volatile container data storage from the core OS filesystems.
Co-locate `/var/lib/containers` on the parent partition (Root or `/var`): Simplifies the initial installation process by relying on the default partitioning scheme. However, this risks system instability if container images or ephemeral volumes consume excessive disk space, impacting the underlying filesystem.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Dedicated partition for `/var/lib/containers`: Requires custom Ignition configuration overrides within the installation manifest (e.g., `ClusterInstance` or `BareMetalHost` definition). This adds complexity to the installation process.
Co-locate `/var/lib/containers` on the parent partition (Root or `/var`): Higher risk of disk exhaustion affecting system stability if container usage is heavy or unpredictable. Management of disk quotas becomes less granular.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Storage Expert
#TODO#: Operations Expert

☐ OCP-BM-45: Control Plane Etcd Storage Partitioning Strategy

---

**Title**
Control Plane Etcd Storage Partitioning Strategy

Title: Control Plane Etcd Storage Partitioning Strategy
Architectural Question: Should etcd data storage (`/var/lib/etcd`) on control plane nodes be isolated onto a dedicated partition separate from the root (or `/var`) filesystem to ensure performance and prevent resource conflicts?
Issue or Problem: Etcd is extremely sensitive to disk performance, requiring a 10 ms p99 fsync duration. If etcd data is co-located with other volatile system data (logs, container images), aggressive writing or system maintenance operations may introduce contention and jitter, risking cluster instability and leader elections.
Assumption: General /var Partitioning Strategy is defined.
Alternatives: Dedicated partition for `/var/lib/etcd`
Co-locate `/var/lib/etcd` on the parent partition
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Dedicated partition for `/var/lib/etcd`: This separates the critical etcd workload from the operating system and other volatile system data (like logs in `/var/log`), mitigating the risk of data growth or I/O contention affecting etcd performance.
Co-locate `/var/lib/etcd` on the parent partition: This is the default RHCOS partitioning scheme, simplifying the initial installation process by avoiding custom Ignition configurations.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Dedicated partition for `/var/lib/etcd`: Requires custom MachineConfig or Butane manifest configurations during the installation phase to define and mount the separate partition.
Co-locate `/var/lib/etcd` on the parent partition: Increases the risk of disk exhaustion or I/O contention affecting etcd, potentially leading to performance instability or cluster outages if the underlying storage does not meet the strict latency requirements.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Storage Expert
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-BM-46: RHCOS Partition Retention Strategy during Reinstallation (UPI)

---

**Title**
RHCOS Partition Retention Strategy during Reinstallation (UPI)

Title: RHCOS Partition Retention Strategy during Reinstallation (UPI)
Architectural Question: When reinstalling Red Hat Enterprise Linux CoreOS (RHCOS) on User-Provisioned Infrastructure (UPI) nodes, should existing data partitions be automatically preserved or overwritten, and which mechanism should be used?
Issue or Problem: When performing an RHCOS reinstallation, particularly to recover a node or perform an OS upgrade, existing data partitions (e.g., separate `/var` partitions created during Day 1 configuration) must either be explicitly preserved or risk being overwritten by the `coreos-installer`. A strategy is needed to ensure continuity of data or configuration residing on these preserved partitions.
Assumption: N/A
Alternatives: Retain Existing Partitions (By Label or Index)
Overwrite All Partitions (Clean Slate Installation)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Retain Existing Partitions (By Label or Index): This allows for preservation of non-OS data (e.g., application logs, `/var/lib/containers` contents) during a reinstall or upgrade, accelerating recovery by preventing the need for massive container pulls post-reinstall. This is achieved using `coreos-installer` arguments like `--save-partlabel` or `--save-partindex`.
Overwrite All Partitions (Clean Slate Installation): This is the default or simplified approach where all existing data is wiped clean, ensuring no remnants of old partitions interfere with the new installation. This is simpler operationally but results in data loss if external backups are not used.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Retain Existing Partitions (By Label or Index): Requires meticulous use of specific kernel arguments (e.g., `coreos.inst.save_partlabel=data*` or `coreos.inst.save_partindex=5-`) during the PXE/ISO boot process. Increases complexity during the OS installation phase.
Overwrite All Partitions (Clean Slate Installation): Requires applications and storage layers to handle the recreation and re-synchronization of all data post-installation.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert
#TODO#: Storage Expert

☐ OCP-BM-47: Bare Metal Node Image Pre-caching Strategy for Disconnected/Edge Deployments

---

**Title**
Bare Metal Node Image Pre-caching Strategy for Disconnected/Edge Deployments

Title: Bare Metal Node Image Pre-caching Strategy for Disconnected/Edge Deployments
Architectural Question: How will required container images (OCP release, operators, application base images) be transferred and prepared on bare metal edge nodes prior to or during installation/upgrade to minimize network latency and bandwidth dependency?
Issue or Problem: In disconnected environments or at the far edge, pulling large container images during installation or upgrade (JIT pull) can be slow or unreliable. A structured method is needed to pre-position images on the node's container storage partition, supporting efficient Zero Touch Provisioning (ZTP) and Image-Based Upgrades (IBU).
Assumption: Provisioning workflow is GitOps ZTP.
Cluster is on the edge.
Nodes utilize disk partitioning to include a shared container partition (`/var/lib/containers`).
Alternatives: Client-side Image Pre-caching via Ignition/IBU
Just-In-Time (JIT) Pull during Installation and Runtime
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Client-side Image Pre-caching via Ignition/IBU: This method significantly reduces installation time and network load, which is critical for far edge or constrained environments. It integrates seamlessly with ZTP using `ignitionConfigOverride` (configured via `ClusterInstance`) to configure mount points and launch services to extract pre-cached images before the cluster installation fully proceeds..
Just-In-Time (JIT) Pull during Installation and Runtime: This simplifies the pre-install setup since no manual image pre-packaging or partition management is required. It relies on the network being stable and high-bandwidth enough to pull all necessary images when needed.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Client-side Image Pre-caching via Ignition/IBU: Requires careful configuration of OS disk partitioning (e.g., separating `/var/lib/containers`) and precise Ignition/systemd units to manage mounting and extraction of compressed image artifacts (tarballs) before core services start. This adds complexity to the Day 1 manifests.
Just-In-Time (JIT) Pull during Installation and Runtime: Risk of installation/upgrade failure or significant delays due to network instability or slow download speeds, common challenges at the far edge.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: Network Expert

☐ OCP-BM-48: Internal Image Registry Management State on Bare Metal UPI

---

**Title**
Internal Image Registry Management State on Bare Metal UPI

Title: Internal Image Registry Management State on Bare Metal UPI
Architectural Question: Should the built-in Image Registry Operator's default `Removed` state on bare metal User-Provisioned Infrastructure (UPI) clusters be explicitly switched to `Managed` post-installation, or should the platform rely exclusively on an external image registry?
Issue or Problem: On bare metal UPI environments that do not provide default shared storage, the OpenShift Image Registry Operator bootstraps itself in a `Removed` management state to allow installation to complete. If the registry remains `Removed`, image building and pushing of application images are disabled. A decision is required to determine the long-term image hosting strategy (internal or external) and mandate the necessary post-installation operational steps.
Assumption: Cluster installation method is User-Provisioned Infrastructure (UPI).
Alternatives: Switch Internal Registry to Managed State Post-Install
Maintain Removed State (Rely Exclusively on External Registry)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Switch Internal Registry to Managed State Post-Install: This enables the use of the built-in, cluster-managed image registry. This simplifies integration with OpenShift builds and standard platform services once appropriate persistent storage is provisioned.
Maintain Removed State (Rely Exclusively on External Registry): This approach minimizes the cluster footprint and ensures that all core OCP components and applications rely on an existing external corporate image registry (e.g., Quay, Artifactory, Nexus), leveraging existing security and management infrastructure.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Switch Internal Registry to Managed State Post-Install: Requires manual intervention by the cluster administrator to edit the `configs.imageregistry/cluster` resource to change `managementState: Removed` to `Managed` after installation. Subsequently, persistent storage must be configured. For highly available (HA) deployments, ReadWriteMany (RWX) access is required. For supported single-replica deployments using block storage (RWO), the administrator must also set the `rolloutStrategy` to `Recreate` and set `replicas` to 1.
Maintain Removed State (Rely Exclusively on External Registry): Disables the ability to use the cluster’s internal image building capabilities, requiring all image dependencies (including custom RHOAI notebook images) to be pulled from the external registry. The cluster network must allow external pull access for all nodes and application namespaces must be configured with pull secrets.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: Storage Expert

☐ OCP-BM-49: Storage Architecture for the Internal Image Registry

---

**Title**
Storage Architecture for the Internal Image Registry

Title: Storage Architecture for the Internal Image Registry
Architectural Question: How should storage be architected for the OpenShift Internal Image Registry, balancing bare metal infrastructure limitations (RWO/RWX availability) with performance, enterprise object storage requirements, and non-production simplicity?
Issue or Problem: OpenShift Container Platform's internal image registry requires high-availability storage (supporting multiple replicas) for production clusters. On bare metal, achieving native ReadWriteMany (RWX) access is challenging. A decision must be made between deploying complex RWX solutions, utilizing dedicated Object Storage (S3 API), settling for low-resilience ReadWriteOnce (RWO) storage, or utilizing ephemeral storage for non-critical environments.
Assumption: Internal Image Registry Management State is set to "Managed".
Alternatives: Dedicated Object Storage (S3 API Compatible)
ReadWriteMany (RWX) Access Mode (PVC)
ReadWriteOnce (RWO) Access Mode (PVC)
Ephemeral Storage (EmptyDir) (Non-Production)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Dedicated Object Storage (S3 API Compatible): This approach leverages object storage (such as Red Hat OpenShift Data Foundation's Multicloud Gateway or an external S3 provider) for the image repository. Object storage is highly scalable and natively supports high availability (HA) required for image registries. ODF is the preferred option when Object (MCG) storage capabilities are necessary.
ReadWriteMany (RWX) Access Mode (PVC): This access mode is required to deploy an image registry that supports high availability with two or more replicas. It is typically implemented using shared file system storage.
ReadWriteOnce (RWO) Access Mode (PVC): This access mode is supported only when the image registry has one replica and explicitly requires the `Recreate` rollout strategy during upgrades.
Ephemeral Storage (EmptyDir) (Non-Production): This simplifies configuration and is available only for non-production clusters. It minimizes setup complexity as no underlying persistent storage solution is required.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Dedicated Object Storage (S3 API Compatible): Requires the installation and maintenance of an Object Storage solution (e.g., ODF/MCG). This decouples image storage scalability from local block or file storage limitations.
ReadWriteMany (RWX) Access Mode (PVC): Requires coordination to provision storage that supports RWX access mode, which is necessary for HA scaled registries.
ReadWriteOnce (RWO) Access Mode (PVC): The cluster must accept reduced resiliency, as the registry cannot have more than one replica. Block storage volumes, which typically use RWO, are supported but explicitly not recommended for use with the image registry on production clusters.
Ephemeral Storage (EmptyDir) (Non-Production): All container images are lost if the registry pod restarts or the node fails. This configuration must be used for only non-production clusters (e.g., Lab/Sandbox) where image rebuilds are acceptable.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Storage Expert
#TODO#: OCP Platform Owner
#TODO#: Security Expert
#TODO#: Operations Expert

☐ OCP-BM-50: Bare Metal Kernel Selection: Real-Time Kernel Implementation

---

**Title**
Bare Metal Kernel Selection: Real-Time Kernel Implementation

Title: Bare Metal Kernel Selection: Real-Time Kernel Implementation
Architectural Question: Should the OpenShift Container Platform nodes leverage the Real-Time Kernel for low-latency performance, and how will this requirement be enforced and configured across the cluster nodes?
Issue or Problem: Bare metal deployments for demanding workloads, such as virtual Distributed Unit (vDU) applications in Telco environments, require guaranteed low latency and high performance. The standard RHCOS kernel may introduce unacceptable jitter or delay, necessitating the use of the Real-Time (RT) kernel.
Assumption: Low-latency workloads are required, consistent with the Hardware Acceleration Strategy.
Alternatives: Enable Real-Time Kernel via Performance Profile
Use Default Standard Kernel
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Enable Real-Time Kernel via Performance Profile: This is the recommended approach for running low-latency applications on OpenShift Container Platform. Enabling the RT kernel through the `PerformanceProfile` custom resource is crucial for isolating CPU resources and achieving performance guarantees required by vDU applications.
Use Default Standard Kernel: This simplifies cluster management and updates, as the standard kernel is fully supported and requires fewer specialized tunings. It avoids the overhead associated with the RT kernel but cannot guarantee the low latency required for critical applications.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Enable Real-Time Kernel via Performance Profile: Requires the use of the Node Tuning Operator and specific configurations in the `PerformanceProfile` (e.g., setting `realTimeKernel: enabled: true`). Changes to this kernel may require node reboots for application. This configuration is mandated for VDU workloads.
Use Default Standard Kernel: May lead to performance instability, resource jitter, or failure to meet Service Level Objectives (SLOs) for latency-sensitive applications.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Network Expert

☐ OCP-BM-51: Simultaneous Multithreading (SMT) Configuration Strategy

---

**Title**
Simultaneous Multithreading (SMT) Configuration Strategy

Title: Simultaneous Multithreading (SMT) Configuration Strategy
Architectural Question: Should Simultaneous Multithreading (SMT), often referred to as hyperthreading, be globally enabled or disabled on cluster nodes via the installation configuration?
Issue or Problem: SMT is enabled by default to increase core performance and maximize resource efficiency. However, disabling SMT is sometimes required for strict security profiles (to mitigate side-channel attacks) or specific performance-critical workloads (like vDU or high-frequency trading) that require dedicated physical cores to eliminate "noisy neighbor" interference on the pipeline.
Assumption: N/A
Alternatives: SMT Enabled (Default)
SMT Disabled (Security/Performance Optimized)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: SMT Enabled (Default): This maximizes the total thread count and overall throughput of the machine. It is the standard setting for general-purpose container workloads.
SMT Disabled (Security/Performance Optimized): Disabling SMT provides stronger CPU isolation. This is often mandatory for Real-Time/vDU workloads to guarantee deterministic latency, or for environments requiring mitigation of specific processor side-channel vulnerabilities (e.g., L1TF/Foreshadow) where software mitigation is insufficient.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: SMT Enabled (Default): May leave the cluster vulnerable to specific side-channel security threats inherent to hyperthreading architectures. Latency-sensitive applications may experience jitter due to thread contention on the same physical core.
SMT Disabled (Security/Performance Optimized): Dramatically decreases the total vCPU capacity of the cluster (typically by 50%). This requires careful capacity planning and potentially increases the hardware footprint/subscriptions required. This setting is applied via the `install-config.yaml` (compute/controlPlane hyperthreading) or Day 2 MachineConfigs.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Security Expert
#TODO#: Infra Leader

☐ OCP-BM-52: Workload Partitioning (CPU Isolation)

---

**Title**
Workload Partitioning (CPU Isolation)

Title: Workload Partitioning (CPU Isolation)
Architectural Question: What strategy will be implemented for dedicating CPU resources (workload partitioning) to isolate performance-sensitive tenant workloads from host and OpenShift platform processes?
Issue or Problem: For bare metal deployments hosting performance-critical or low-latency workloads (like RAN Distributed Units, or vDU applications), unpartitioned CPU usage leads to performance jitter due to contention between application pods and platform/kernel components. Defining isolated and reserved CPU sets is critical to meet required performance constraints.
Assumption: Low-latency workloads are required.
Alternatives: No Partitioning (Default)
Enable Workload Partitioning
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: No Partitioning (Default): This is the simplest operational model. All platform and application pods are scheduled across all available CPU cores, which is sufficient for workloads without real-time or low-latency requirements.
Enable Workload Partitioning: This is the required method for isolating performance-sensitive workloads. It involves creating a `PerformanceProfile` to divide the node's CPUs into a `reserved` set (for platform/OS processes) and an `isolated` set (exclusively for tenant workloads).
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: No Partitioning (Default): This configuration will not support real-time workloads like vDUs, as platform and application CPU contention will cause unacceptable performance jitter and potential service failure.
Enable Workload Partitioning: This adds configuration complexity, requiring a `PerformanceProfile` and `Tuned` CRs. It also "costs" CPU cores, as the `reserved` cores are permanently removed from the schedulable capacity for general pods, but this is necessary to guarantee performance for isolated workloads.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Network Expert

☐ OCP-BM-53: Container Runtime Selection for Bare Metal Performance Workloads

---

**Title**
Container Runtime Selection for Bare Metal Performance Workloads

Title: Container Runtime Selection for Bare Metal Performance Workloads
Architectural Question: Should the default CRI-O container runtime be replaced or augmented with CRUN to optimize performance for latency-sensitive workloads on bare metal nodes?
Issue or Problem: To support stringent latency and high-performance requirements typical of applications like virtual Distributed Units (vDU), relying solely on the default container runtime may not be sufficient. Utilizing an optimized runtime like CRUN is often recommended for these performance-sensitive environments.
Assumption: Performance-sensitive workloads (e.g., vDU) will be deployed on the bare metal cluster.
Alternatives: Default Container Runtime (CRI-O)
Optimized Container Runtime (CRUN)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Default Container Runtime (CRI-O): Simplifies installation and operational maintenance by relying on the standard, supported container engine bundled with Red Hat Enterprise Linux CoreOS (RHCOS).
Optimized Container Runtime (CRUN): This option is strongly recommended for performance workloads, such as vDU, to achieve specific low-latency optimization.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Default Container Runtime (CRI-O): May lead to sub-optimal latency performance for critical telecommunication or AI/ML workloads.
Optimized Container Runtime (CRUN): It is strongly recommended to include `crun` manifests as part of the additional install-time manifests. This requires defining `ContainerRuntimeConfig` manifests (e.g., `enable-crun-master.yaml`, `enable-crun-worker.yaml`) via the GitOps ZTP pipeline or equivalent mechanism.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Operations Expert

☐ OCP-BM-54: Precision Time Protocol (PTP) Configuration Strategy for Low-Latency Workloads

---

**Title**
Precision Time Protocol (PTP) Configuration Strategy for Low-Latency Workloads

Title: Precision Time Protocol (PTP) Configuration Strategy for Low-Latency Workloads
Architectural Question: How will highly accurate time synchronization be achieved and managed on bare metal nodes to meet the strict timing requirements of low-latency applications (e.g., vDU)?
Issue or Problem: Standard Network Time Protocol (NTP) often lacks the precision required by workloads such as vDU (Virtual Distributed Unit) applications, which require Precision Time Protocol (PTP) synchronization to function correctly. A standardized mechanism is needed to deploy and manage PTP services across the cluster nodes.
Assumption: Performance-sensitive workloads (e.g., vDU) will be deployed on the bare metal cluster.
Alternatives: Rely Solely on Standard NTP
Managed PTP using the PTP Operator
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Rely Solely on Standard NTP: Minimizes cluster complexity but fails to meet the time synchronization requirements for stringent low-latency workloads like vDU.
Managed PTP using the PTP Operator: This approach ensures the cluster can support low latency applications by managing time synchronization through the PTP Operator. It allows for configuration of specific roles like `boundary` or `slave` using `PtpConfig` CRs.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Rely Solely on Standard NTP: Critical applications (like vDU) will likely fail due to insufficient time synchronization precision.
Managed PTP using the PTP Operator: Requires installing the PTP Operator and configuring appropriate `PtpConfig` resources for roles, interfaces, and options (e.g., `ptp4lOpts`, `phc2sysOpts`). Managing PTP requires ensuring interfaces are correctly configured for PTP, potentially using specific network interface cards (NICs), and integrating with kernel tuning profiles.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Network Expert
#TODO#: Infra Leader
#TODO#: Operations Expert

☐ OCP-BM-55: Kernel Module and Device Plugin Management on Bare Metal using KMM

---

**Title**
Kernel Module and Device Plugin Management on Bare Metal using KMM

Title: Kernel Module and Device Plugin Management on Bare Metal using KMM
Architectural Question: What standard mechanism will be used to build, deploy, and manage out-of-tree kernel modules (like specialized GPU or NIC drivers) and their corresponding device plugins across bare metal cluster nodes?
Issue or Problem: Specialized hardware acceleration or networking components often require kernel modules and device plugins not included in the default Red Hat Enterprise Linux CoreOS (RHCOS) images. Deploying these manually leads to version misalignment and complex lifecycle management whenever kernel updates occur.
Assumption: The bare metal cluster will utilize specialized hardware requiring out-of-tree kernel drivers (e.g., GPUs or high-performance network adapters).
Alternatives: Kernel Module Management (KMM) Operator
Manual build and DaemonSet deployment (Driver Toolkit approach)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Kernel Module Management (KMM) Operator: KMM is designed to simplify the lifecycle management of kernel modules by automating the build process, tracking kernel versions, and optionally signing the resulting kernel objects.
Manual build and DaemonSet deployment (Driver Toolkit approach): This method requires manually fetching the Driver Toolkit image, building the module outside the cluster, and creating DaemonSets for deployment and pre/post-start hooks. This is highly complex and error-prone during RHCOS updates.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Kernel Module Management (KMM) Operator: Requires installing and maintaining the KMM Operator and associated secrets/config maps. Provides high operational stability by ensuring modules match the current running kernel version automatically.
Manual build and DaemonSet deployment (Driver Toolkit approach): High maintenance burden, as module compatibility must be manually verified and re-deployed on every kernel update or cluster upgrade.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: AI/ML Platform Owner

☐ OCP-BM-56: Bare Metal Node Firmware Management

---

**Title**
Bare Metal Node Firmware Management

Title: Bare Metal Node Firmware Management
Architectural Question: How will ongoing firmware updates (BIOS, BMC, NIC) for bare metal nodes be managed and automated post-installation?
Issue or Problem: Managing firmware updates manually (BIOS, BMC, NICs) across a bare metal fleet is complex, time-consuming, and prone to error, posing maintenance and compliance risks. A standardized, automatable process is required, especially when leveraging the Bare Metal Operator (BMO) for node lifecycle management, utilizing resources like `HostFirmwareComponents` and `HostUpdatePolicy`.
Assumption: Cluster installation method is IPI / Assisted Installer / Agent-based installer / IBI or UPI with Bare Metal Operator enabled.
Alternatives: Automated Management via HostFirmware/HostUpdate CRs
External/Vendor Management Tools
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Automated Management via HostFirmware/HostUpdate CRs: Leverages native BMO capabilities (`HostFirmwareComponents`, `HostUpdatePolicy`) to apply, track, and manage firmware versions for components like BIOS, BMC, and NICs directly through Kubernetes Custom Resources, supporting automated updates and inspection.
External/Vendor Management Tools: Relies on existing organizational tools (e.g., vendor-specific console or infrastructure automation) to perform firmware updates. This allows separation of concerns if the platform team is not responsible for hardware maintenance.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Automated Management via HostFirmware/HostUpdate CRs: Requires defining, testing, and maintaining `HostFirmwareComponents` and `HostUpdatePolicy` CRs. The process may cause node disruption and require coordination (e.g., node draining).
External/Vendor Management Tools: Updates are decoupled from the OpenShift workflow, potentially simplifying BMO configuration, but resulting in a manual process that requires coordinating external maintenance windows with cluster availability (e.g., node draining, cluster remediation).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-BM-57: Bare Metal Firmware Update Application Timing Policy

---

**Title**
Bare Metal Firmware Update Application Timing Policy

Title: Bare Metal Firmware Update Application Timing Policy
Architectural Question: When leveraging the Bare Metal Operator (BMO) for node firmware management (BIOS, BMC, NICs) via `HostFirmwareComponents` or `HostFirmwareSettings`, should updates be applied immediately (live update) or deferred until a scheduled node reboot?
Issue or Problem: This decision defines whether disruptive firmware updates are applied immediately (requiring coordination) or aligned with planned OS reboots, balancing rapid deployment against maximum control and reliability.
Assumption: The Bare Metal Operator (BMO) is enabled and managing node firmware configurations.
Alternatives: Immediate Application (Live Update) (TP)
Deferred Application (Update on Next Reboot)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Immediate Application (Live Update) (TP): This option allows for rapid deployment of firmware updates, as the firmware change is performed while the host is provisioned or active. This can be achieved by utilizing BMO's advanced features, such as `HostFirmwareSettings` live updates.
Deferred Application (Update on Next Reboot): This method provides maximum control and reliability, ensuring that disruptive firmware updates are performed during a planned maintenance window or scheduled operating system reboot. This approach requires setting the `HostUpdatePolicy` resource to `onReboot`.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Immediate Application (Live Update) (TP): Live updates to the BMC are generally not recommended for testing, especially on earlier generation hardware. This process may cause node disruption and require coordination (e.g., node draining). Some advanced features supporting this may also be Technology Preview (TP).
Deferred Application (Update on Next Reboot): This simplifies maintenance coordination by aligning the disruptive firmware update process with the operating system update schedule. This requires defining, testing, and maintaining the `HostUpdatePolicy` Custom Resource.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BM-58: Bare Metal Node Remediation

---

**Title**
Bare Metal Node Remediation

Title: Bare Metal Node Remediation
Architectural Question: What is the strategy for automatically remediating unhealthy Bare Metal nodes?
Issue or Problem: A strategy is needed to automatically detect and recover failed physical nodes. This is critical for maintaining cluster health and HA for workloads, especially for stateful services that run directly on the nodes.
Assumption: N/A.
Alternatives: No Automated Remediation
Node Health Check (NHC) with Self Node Remediation
Node Health Check (NHC) with BareMetal Operator (BMO) Remediation (TP)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: No Automated Remediation: To rely on manual detection (via monitoring) and manual intervention by an operator to troubleshoot and reboot physical nodes.
Node Health Check (NHC) with Self Node Remediation: To deploy the Node Health Check operator, which monitors node health. When a node fails, the `SelfNodeRemediation` agent on other nodes will fence the unhealthy node and restart its workloads elsewhere.
Node Health Check (NHC) with BareMetal Operator (BMO) Remediation (TP): This is the most robust, fully automated solution. It attempts to recover the node by "turning it off and on again" via its BMC.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: No Automated Remediation: High operational burden and slow recovery times. Not recommended for a production cluster.
Node Health Check (NHC) with Self Node Remediation: Provides software-level remediation. It ensures workloads are moved but does not fix the underlying node, which will remain unavailable until manually repaired.
Node Health Check (NHC) with BareMetal Operator (BMO) Remediation (TP): This requires a reliable IPI installation and stable Redfish/IPMI connectivity. The BMO facilitates the Cluster API management of compute nodes (TP) for dynamic lifecycle management. It also enables access to advanced operational features, such as firmware management via HostFirmwareSettings/HostFirmwareComponents, including live updates (TP).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

OpenShift Container Platform - Cluster Management & Day2 Ops
☐ OCP-MGT-01: Namespace/Project Allocation Strategy

---

# OCP-MON

---

**Title**
Monitoring Strategy

Title: Monitoring Strategy
Architectural Question: What is the strategy for monitoring cluster and application metrics?
Issue or Problem: A monitoring solution is required to collect and store metrics for observing cluster health, managing capacity, and troubleshooting performance issues. Decisions are needed on the scope of monitoring and long-term data retention.
Assumption: N/A
Alternatives: Default Platform Monitoring
Enable User Workload Monitoring
Customized Monitoring Stack via COO
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Default Platform Monitoring: Provides built-in, preconfigured monitoring for all core OpenShift components (e.g., etcd, Kubernetes API server, nodes, Operators) using Prometheus, Alertmanager, and Thanos Query. This is enabled by default.
Enable User Workload Monitoring: Extends the Prometheus stack to collect metrics and expose alerts specifically for workloads running in user-defined projects (namespaces). This is optional.
Customized Monitoring Stack via COO: Leverages the Cluster Observability Operator (COO) to create and manage highly customizable monitoring stacks, offering a more tailored and detailed view of specific namespaces or components beyond the default configuration.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Default Platform Monitoring: Configuration is locked down and supported only via the Cluster Monitoring Operator (CMO) ConfigMap. Data storage capacity for Thanos is pre-allocated.
Enable User Workload Monitoring: Increases resource consumption (CPU/RAM/storage) due to additional Prometheus and Thanos Ruler instances running in the `openshift-user-workload-monitoring` project.
Customized Monitoring Stack via COO: Provides maximum flexibility for metric collection and routing, but introduces management overhead for the custom stacks and requires advanced knowledge of monitoring configuration.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: DevOps Engineer
#TODO#: Operations Engineer

☐ OCP-MON-02: Metrics Collection Profile

---

**Title**
Metrics Collection Profile

Title: Metrics Collection Profile
Architectural Question: Which metrics collection profile will be applied to the cluster to balance observability depth against resource consumption?
Issue or Problem: The default monitoring stack scrapes a vast number of metrics. On resource-constrained clusters (e.g., SNO, Edge), this overhead (CPU/RAM) can be prohibitive.
Assumption: N/A
Alternatives: Default Profile: Collects all standard platform metrics.
Minimal Profile: Collects only essential metrics for alerts and core health.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Default Profile: Maximize observability. Support teams have full data for debugging.
Minimal Profile: Reduces CPU/Memory usage significantly. Recommended for SNO/Edge.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Minimal Profile: Some dashboards in the console may be empty. Troubleshooting complex issues may require temporarily enabling full metrics.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert

☐ OCP-MON-03: Persistent Storage Strategy for Monitoring

---

**Title**
Persistent Storage Strategy for Monitoring

Title: Persistent Storage Strategy for Monitoring
Architectural Question: Will Persistent Volume Claims (PVCs) be configured for Prometheus and Alertmanager to ensure metric durability?
Issue or Problem: By default, OpenShift Monitoring uses ephemeral storage. If a Prometheus pod restarts, recent metrics are lost. This impacts alerting continuity and historical trending.
Assumption: Storage Provider is defined.
Alternatives: Ephemeral Storage (Default): Metrics lost on pod restart.
Persistent Storage (PVC): Metrics retained across restarts.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Ephemeral: Simple. No storage management overhead. Acceptable if long-term metrics are offloaded via Remote Write.
Persistent (PVC): Essential for standalone clusters where local history matters. Prevents data gaps during upgrades.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Persistent: Requires a block storage class. Resizing PVCs later can be complex (Prometheus statefulsets).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Storage Expert
#TODO#: Operations Expert

☐ OCP-MON-04: Data Retention Policy

---

**Title**
Data Retention Policy

Title: Data Retention Policy
Architectural Question: How long should high-resolution metrics be retained within the cluster's local Prometheus instance?
Issue or Problem: Default retention is 15 days. Extending this increases disk space requirements linearly.
Assumption: Persistent Storage is enabled (if retention > restart).
Alternatives: Default Retention (15 Days): Balanced for operational health checks.
Custom Retention (Extended): For compliance or local trending.
Minimal Retention: If offloading to central system immediately.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Default (15 Days): Sufficient for most "Is it healthy now?" questions.
Custom: Required if no central metrics store exists.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Extended Retention: drastically increases PVC size requirements. Prometheus query performance may degrade over long time ranges.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert

☐ OCP-MON-05: Remote Write / Federation Strategy

---

**Title**
Remote Write / Federation Strategy

Title: Remote Write / Federation Strategy
Architectural Question: Will cluster metrics be forwarded (Remote Write) to a centralized long-term storage system (e.g., Thanos, Cortex, Splunk)?
Issue or Problem: Local Prometheus is not a long-term archive. To analyze trends across months/years or aggregate multiple clusters, data must be exported.
Assumption: Multi-cluster fleet or Long-term retention requirement exists.
Alternatives: Local Only: No export. Data dies with retention policy.
Remote Write Enabled: Metrics pushed to central store.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Local Only: Simple for standalone/dev clusters.
Remote Write: Mandatory for Fleet Observability (ACM Observability uses this). Enables global querying.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Remote Write: Increases network egress bandwidth. Requires authentication configuration to the remote endpoint.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Network Expert
#TODO#: OCP Platform Owner

☐ OCP-MON-06: Alertmanager Integration Strategy

---

**Title**
Alertmanager Integration Strategy

Title: Alertmanager Integration Strategy
Architectural Question: How will alerts be routed to operational teams?
Issue or Problem: Alerts inside the cluster are useless if no one sees them.
Assumption: N/A
Alternatives: Cluster-Local Alertmanager: Configure receivers (Slack, PagerDuty, Email) directly in the cluster.
External Alert Routing: Forward all alerts to a central event bus or external Alertmanager (e.g., via Remote Write or Webhook).
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Cluster-Local: Good for team autonomy (tenants manage their own alerts).
External Routing: Centralizes noise reduction, inhibition, and aggregation in a NOC/SOC.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Cluster-Local: Operational overhead to manage secrets (API keys) in every cluster.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: Operations Expert

---

# OCP-BASE

---

**Title**
Environment Isolation Strategy

Title: Environment Isolation Strategy
Architectural Question: How will workloads for different lifecycle stages (e.g., Dev, Test, Prod) be separated and hosted across OpenShift clusters?
Issue or Problem: Isolation is required for security, stability, and adherence to change control policies, balanced against the management overhead of multiple clusters.
Assumption: N/A
Alternatives: Consolidated Cluster Model
Prod/Non-Prod Split Model
Per-Environment Model
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision.#
Justification: Consolidated Cluster Model: Minimizes the infrastructure footprint and simplifies cluster management by consolidating all environments (Dev, Test, Prod) into a single operational cluster. This minimizes cost but requires reliance on OpenShift Namespaces/Projects, ResourceQuotas, NetworkPolicy, RBAC, Security Context Constraints (SCCs), and Pod Security Admission (PSA) for isolation. The inclusion of User Namespaces (TP) can further enhance workload isolation within this model.
Prod/Non-Prod Split Model: Provides strong isolation between production and non-production workloads, preventing development or testing activities from impacting the production environment. This is often a minimum compliance requirement.
Per-Environment Model: Offers maximum isolation between all environments (e.g., dev, test, UAT, prod), which is ideal for organizations with strict compliance, security, or change-control requirements for each stage, incurring maximum management overhead.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Consolidated Cluster Model: Increased risk of resource contention ("noisy neighbors") and Single Point of Failure (SPoF) impacting all environments if a critical component or underlying infrastructure service fails.
Prod/Non-Prod Split Model: Requires managing at least two separate clusters, increasing infrastructure and operational costs.
Per-Environment Model: Highest operational overhead due to managing multiple, smaller clusters, but offers the clearest path to strict regulatory compliance and failure domain separation.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Storage Expert
#TODO#: Network Expert

☐ OCP-BASE-02: Cloud model

---

**Title**
Cloud model

Title: Cloud model
Architectural Question: Which cloud operating model will be adopted for the OpenShift platform?
Issue or Problem: A cloud model must be selected that aligns with the organization's strategy for infrastructure ownership, operational expenditure (OpEx) versus capital expenditure (CapEx), scalability, and data governance.
Assumption: N/A
Alternatives: Private Cloud Model
Public Cloud Model
Hybrid Cloud Model
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision.#
Justification: Private Cloud Model: Leverages existing data center investments, provides maximum control over the hardware and network stack, and can help meet strict data sovereignty or residency requirements.
Public Cloud Model: Offers rapid provisioning, on-demand scalability, a pay-as-you-go pricing model (OpEx), and offloads the management of physical infrastructure.
Hybrid Cloud Model: Provides the flexibility to run workloads in the most suitable environment, balancing cost, performance, security, and features between private and public clouds.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Private Cloud Model: The organization is fully responsible for infrastructure capacity planning, maintenance, power, cooling, and networking. Lead times for new hardware can be long. This is a CapEx-intensive model.
Public Cloud Model: Incurs ongoing operational expenses tied to usage. It requires expertise in the specific cloud provider's services, security models, and cost management.
Hybrid Cloud Model: Introduces complexity in network connectivity (e.g., VPN, Direct Connect) and management across different environments. Multi-cluster management tools are essential for a unified operational view.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Storage Expert
#TODO#: Network Expert

☐ OCP-BASE-03: Internet Connectivity Model

---

**Title**
Internet Connectivity Model

Title: Internet Connectivity Model
Architectural Question: Will the OpenShift cluster be deployed in an environment with direct internet access or a highly restricted (air-gapped) network?
Issue or Problem: The connectivity model dictates how installation files, container images, and cluster updates are sourced, impacting initial complexity and ongoing operational tooling. This decision must be made early, as it significantly constrains the choice of cluster topology and installation platform, as not all options fully support disconnected environments.
Assumption: N/A
Alternatives: Connected (Direct Internet Access)
Disconnected (Restricted/Air-Gapped Network)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Connected (Direct Internet Access): Enables simplified installation and uses the OpenShift Update Service (OSUS) to provide over-the-air updates and update recommendations directly from Red Hat.
Disconnected (Restricted/Air-Gapped Network): Required for environments with high security constraints or lack of external network access. Requires establishing a mirroring process to synchronize content from the public Red Hat repositories to a local registry.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Connected (Direct Internet Access): Requires stable internet access for all nodes and adherence to firewall egress rules for Red Hat endpoints.
Disconnected (Restricted/Air-Gapped Network): Significantly increases installation complexity and requires dedicated mirroring infrastructure. For hosted control planes, the ImageContentSourcePolicy (ICSP) for the data plane is managed via the ImageContentSources API.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Security Expert
#TODO#: Network Expert
#TODO#: Operations Expert

☐ OCP-BASE-04: Mirrored images registry (Disconnected Environments)

---

**Title**
Mirrored images registry (Disconnected Environments)

Title: Mirrored images registry (Disconnected Environments)
Architectural Question: In a disconnected environment, which mirrored images registry solution will be used to provide required container images to the cluster?
Issue or Problem: In a disconnected environment, the cluster needs access to Red Hat software (release images, operators) via a local mirror registry for installation and updates.
Assumption: Environment is disconnected.
Alternatives: Filesystem-based Mirror (using `oc mirror` or `oc adm release mirror`)
Dedicated Mirror Registry Server (e.g., Quay, Nexus, Artifactory)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Filesystem-based Mirror: Uses oc mirror (preferred) to create a simple mirror (filesystem or basic registry push). Minimum requirement for mirroring essential OCP software.
Dedicated Mirror Registry Server: Leverages a full-featured registry (existing or new) as the single source for both mirrored Red Hat content and internal application images. This is the preferred enterprise approach.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Filesystem-based Mirror: Primarily for Red Hat content, not a full registry (no UI, advanced RBAC, scanning unless paired). Simpler setup for core content, less suitable for applications. Requires manual sync.
Dedicated Mirror Registry Server: Preferred enterprise approach. Requires ensuring the registry supports OCP content formats (Operator catalogs) and the mirroring process. Leverages existing HA, security, and management features.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Security Expert
#TODO#: Network Expert
#TODO#: Operations Expert

☐ OCP-BASE-05: Fleet Management

---

**Title**
Fleet Management

Title: Fleet Management
Architectural Question: What strategic model will be used to manage the lifecycle (provisioning, upgrades, governance, and observability) of the OpenShift cluster fleet?
Issue or Problem: Managing clusters individually ("pets") leads to configuration drift, inconsistent security postures, and operational bottlenecks as the fleet grows. A strategy is needed to determine if clusters will be managed autonomously or via a unified, centralized control plane.
Assumption: N/A
Alternatives: Decentralized Management: Each cluster is provisioned, upgraded, and configured independently using disparate tools (CLI, Jenkins, Ansible) and individual consoles.
Centralized Fleet Management (RHACM): A hub-and-spoke architecture is used where a central "Hub" cluster (running Red Hat Advanced Cluster Management) orchestrates the lifecycle and governance of all "Spoke" clusters.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision#
Justification: Decentralized Management: Suitable only for very small, static environments where the overhead of a management hub is not justified.
Centralized Fleet Management (RHACM): The strategic requirement for enterprise scale. It provides a single pane of glass for observability, a unified engine for policy-based governance (GRC), and enables advanced provisioning workflows (like GitOps ZTP) across all infrastructure providers.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Decentralized Management: High operational overhead per cluster; auditing compliance across the fleet is manual and error-prone.
Centralized Fleet Management (RHACM): Requires deploying and maintaining a dedicated Hub cluster. Establishes the dependency required for advanced automation patterns like GitOps Zero Touch Provisioning (ZTP) and Hosted Control Planes.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BASE-06: Platform Configuration & Deployment Engine Selection

---

**Title**
Platform Configuration & Deployment Engine Selection

Title: Platform Configuration & Deployment Engine Selection
Architectural Question: Which technology will be designated as the standardized, strategic engine for declarative configuration management (GitOps) and continuous delivery for the OpenShift platform?
Issue or Problem: A single, authoritative operational model must be chosen to manage cluster configuration drift, ensure consistency, and provide a verifiable audit trail for infrastructure changes. Relying on fragmented tooling (manual scripts, unmanaged YAMLs) leads to operational bottlenecks and inconsistency, regardless of whether managing a single cluster or a large fleet.
Assumption: Declarative infrastructure-as-code is the desired operating model.
Alternatives: OpenShift GitOps (Argo CD) - Declarative Model
Red Hat Ansible Automation Platform (AAP) / Imperative Model
Manual / Scripting Tooling - Decentralized Control
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: OpenShift GitOps (Argo CD) - Declarative Model: Standardizes on a declarative, reconciliation-based model where Git is the single source of truth. It provides continuous drift detection and scales seamlessly from single-cluster management to full fleet automation (ZTP) when paired with a management hub.
Red Hat Ansible Automation Platform (AAP) / Imperative Model: Best suited for imperative, "fire-and-forget" Day 2 operations or orchestrating dependencies external to the Kubernetes platform (e.g., hardware firewalls, legacy IT systems) that cannot be managed natively by Kubernetes Operators.
Manual / Scripting Tooling - Decentralized Control: Low-overhead approach suitable only for transient PoCs where audit trails, consistency, and automated drift remediation are not required.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: OpenShift GitOps (Argo CD) - Declarative Model: Mandates strict "Infrastructure-as-Code" discipline; all configurations must be committed to Git. It serves as the prerequisite engine for advanced fleet patterns (like PolicyGenerator and ZTP) while remaining fully functional for standalone cluster management.
Red Hat Ansible Automation Platform (AAP) / Imperative Model: Configuration state is maintained in playbook execution history rather than the cluster, potentially leading to undetected drift. It is an excellent complementary tool for orchestration spanning non-Kubernetes systems.
Manual / Scripting Tooling - Decentralized Control: Lacks scalability and native audit capabilities, creating significant technical debt and high operational overhead as the environment grows.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: DevOps Engineer

☐ OCP-BASE-07: Multiple site deployment mode.

---

**Title**
Multiple site deployment mode.

Title: Multiple site deployment mode.
Architectural Question: How will the OpenShift platform be deployed across multiple physical sites (data centers, regions) to meet high availability, disaster recovery, or geo-locality requirements?
Issue or Problem: Deploying a platform across multiple sites introduces significant complexity related to network latency, failure domains, and data replication. A clear strategy is required to balance the operational overhead against the business requirements for resilience and service availability, while adhering to Red Hat supportability guidelines.
Assumption: N/A
Alternatives: Stretched Cluster Across Sites
Multi-Cluster (Independent Cluster per Site)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Stretched Cluster Across Sites: Deploys a single OpenShift cluster with control plane nodes distributed across multiple logical or physical locations. This typically involves exactly three control plane nodes, with the Red Hat recommendation being one node in each of three sites. This allows the cluster to maintain quorum and remain operational if one site fails. However, Red Hat warns this configuration extends the cluster as a single failure domain and should not be considered a replacement for a disaster recovery plan.
Multi-Cluster (Independent Cluster per Site): Deploys a separate, independent OpenShift cluster in each site (e.g., one cluster per region/site). This is Red Hat's strongly recommended alternative to a stretched deployment. This model provides clear failure domain isolation. Tools like Red Hat Advanced Cluster Management (ACM) are then used to manage the clusters, application deployments, and disaster recovery policies from a single point of control.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Stretched Cluster Across Sites:
Strict Network Requirements: The deployment is bound by etcd network performance. The combined disk and network latency and jitter must maintain an etcd peer round trip time of less than 100ms. Note that the etcd peer RTT is an end-to-end test metric distinct from network RTT. For the default 100ms heartbeat interval, the suggested RTT between control plane nodes is less than 33ms, with a maximum of less than 66ms.
Layered Product Constraints: Critically, layered products like storage (e.g., OpenShift Data Foundation) have _much_ lower latency requirements (e.g., < 10ms RTT) that will dictate the feasibility of the stretched model.
Amplified Failure Scenarios: This model has "additional inherent complexities" and "a higher number of points of failure". The organization must extensively test and document cluster behavior during network partitions, latency spikes, and jitter before production use.
Multi-Cluster (Independent Cluster per Site):
Recommended Practice: This approach aligns with Red Hat's recommended practice and avoids the strict low-latency network requirements for the control plane.
Failure Isolation: Each cluster is an independent failure domain, preventing a network issue or outage in one site from impacting another site's cluster.
Management Overhead: Requires managing multiple independent clusters, though this is the intended use case for tools like Advanced Cluster Management (ACM).
Application-Level DR: Failover is not automatic at the cluster level. It must be managed at the application level (e.g., via ACM policies) and data level (e.g., using OpenShift API for Data Protection (OADP) and replication technologies like ODF Regional-DR).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: Network Expert
#TODO#: Storage Expert
#TODO#: Infra Leader

☐ OCP-BASE-08: Intra-Site Availability Zone / Failure Domain Strategy

---

**Title**
Intra-Site Availability Zone / Failure Domain Strategy

Title: Intra-Site Availability Zone / Failure Domain Strategy
Architectural Question: Within a single site or region, how will OpenShift cluster nodes (Control Plane, Compute) be distributed across available Availability Zones (AZs) or Failure Domains (FDs) for high availability?
Issue or Problem: Lack of distribution across failure domains can lead to a Single Point of Failure (SPoF) if a physical location, rack, or infrastructure zone experiences an outage, impacting the control plane (etcd) quorum and worker node availability.
Assumption: N/A
Alternatives: Single AZ/FD Deployment (No HA)
Three or More AZ/FD Deployment (Recommended HA for Standard/Compact)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Single AZ/FD Deployment (No HA): Simplifies network planning and latency management since all nodes reside in one logical or physical area. However, this subjects the entire cluster to a site-wide or rack-level outage event.
Three or More AZ/FD Deployment (Recommended HA for Standard/Compact): Provides maximum resilience by ensuring the control plane's etcd quorum members and worker nodes are distributed across physically isolated domains. This is the preferred approach for production clusters. The core mechanism relies on maintaining strict network latency requirements for etcd; specifically, the suggested Round-Trip Time (RTT) between control plane nodes is less than 33 ms (with a maximum under 66 ms) to ensure stability and avoid missed heartbeats.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Single AZ/FD Deployment (No HA): Significantly increases the risk of a Single Point of Failure (SPoF) for OpenShift infrastructure services and the cluster state (etcd).
Three or More AZ/FD Deployment (Recommended HA for Standard/Compact): Requires careful network design to manage inter-AZ latency. Requires that the underlying platform supports multiple availability zones/failure domains (FDs). This approach is necessary to ensure that High Availability workloads can be correctly distributed using node labels (e.g., `topology.kubernetes.io/zone`) as mandated by default TopologySpreadConstraint policies applied to replicated pods in OpenShift.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Network Expert
#TODO#: Storage Expert

☐ OCP-BASE-09: Platform infrastructure

---

**Title**
Platform infrastructure

Title: Platform infrastructure
Architectural Question: On which specific infrastructure platform(s) will OpenShift Container Platform be installed?
Issue or Problem: The choice of underlying infrastructure platform directly impacts the available installation methods, supported features, operational complexity, performance characteristics, and required team skill sets. More than one platform can be selected.
Assumption: Cloud model has been selected.
Alternatives: Self-Managed Public Cloud (AWS, Azure, GCP, OCI, IBM Cloud, Azure Stack Hub, ALIBABA Cloud)
Bare Metal / On-Premise Virtualized (vSphere, RHOSP, Bare Metal, Nutanix, IBM Power, IBM Z/LinuxONE, External/None)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Self-Managed Public Cloud: Supports Installer-Provisioned Infrastructure (IPI) on platforms including AWS, Azure, GCP, Azure Stack Hub, and IBM Cloud Classic/VPC. User-Provisioned Infrastructure (UPI) maximizes flexibility and is supported on AWS, Azure, GCP, OCI, Azure Stack Hub, and ALIBABA Cloud.
Bare Metal / On-Premise Virtualized: Provides full hardware control. Supported IPI options include vSphere, RHOSP, Bare Metal, and Nutanix. UPI is supported on platforms including vSphere, RHOSP, Bare Metal, IBM Power®, IBM Z®/IBM® LinuxONE, and External/None.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Self-Managed Public Cloud: IPI mode abstracts infrastructure management via the Machine API, simplifying cluster scaling and node lifecycle. Requires cloud credentials and IAM setup. UPI requires manual management of underlying resources.
Bare Metal / On-Premise Virtualized: For UPI deployment, administrators must manually manage all underlying infrastructure components. IPI and Assisted/Agent Installer automate provisioning of infrastructure. UPI deployments on Bare Metal can enable the Bare Metal Operator (BMO) post-installation to gain access to Day 2 automation benefits, such as node remediation and scaling capabilities provided by the Machine API.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Storage Expert
#TODO#: Network Expert
#TODO#: Infra Leader

☐ OCP-BASE-10: Cluster Topology

---

**Title**
Cluster Topology

Title: Cluster Topology
Architectural Question: What OpenShift topology should be deployed based on resource availability, HA requirements, and scale for each cluster?
Issue or Problem: Selecting the cluster topology determines the minimum node count, control plane resilience, resource usage efficiency, and suitability for specific use cases (e.g., edge). This choice impacts High Availability (HA) capabilities within a site and influences multi-site strategies.
Assumption: Platform infrastructure supports the chosen topology.
Alternatives: Standard HA Topology (3+ Control Plane, N+ Workers)
Compact HA Topology (3 Combined Control/Worker)
Two-Node OpenShift with Arbiter (TNA)
Two-Node OpenShift with Fencing (TP: Technology Preview)
Single Node OpenShift (SNO)
Hosted Control Planes (HCP)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Standard HA Topology (3+ Control Plane, N+ Workers): Provides maximum resilience, scalability, and separation of control plane functions from application workloads onto dedicated worker nodes. Recommended for large or general-purpose production clusters.
Compact HA Topology (3 Combined Control/Worker): Reduces the hardware footprint and provides a smaller, more resource-efficient cluster. It is suitable for smaller production environments that require high availability, as the three control plane nodes are configured to be schedulable (running workloads).
Two-Node OpenShift with Arbiter (TNA): A compact, cost-effective OpenShift Container Platform topology that provides high availability (HA). The topology uses two control plane nodes and a lightweight arbiter node to maintain etcd quorum and prevent split brain.
Two-Node OpenShift with Fencing (TP): Designed for distributed or edge environments where deploying a full three-node cluster is impractical, providing HA with a reduced hardware footprint. Fencing, managed by Pacemaker, isolates unresponsive nodes so the remaining node can safely continue operation.
Single Node OpenShift (SNO): Ideal for edge computing workloads, portable clouds, and environments with intermittent connectivity or severe resource constraints, such as 5G radio access networks (RAN).
Hosted Control Planes (HCP): A feature that enables hosting the control plane as pods on a management cluster, optimizing infrastructure costs required for the control planes and improving cluster creation time. This model decouples the control plane from the data plane, providing resiliency.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Standard HA Topology: Requires a minimum of three control plane machines and at least two compute machines. Requires maintaining separate physical hosts for the cluster machines to ensure high availability.
Compact HA Topology: Infrastructure components (monitoring, registry, ingress) often share resources with the control plane, requiring careful sizing. If resource constraints exist, workload partitioning is strongly recommended.
Two-Node OpenShift with Arbiter (TNA): Requires 2 control plane nodes and 1 arbiter node. The arbiter node must meet minimum system requirements.
Two-Node OpenShift with Fencing (TP): Implies reliance on a Technology Preview (TP) feature, which is not recommended for production environments requiring full Red Hat support and Service Level Agreements (SLAs).
Single Node OpenShift (SNO): The major tradeoff is the lack of high availability, as failure of the single node stops the cluster. Requires a minimum of 8 vCPUs and 120GB of storage.
Hosted Control Planes (HCP): The control plane runs in a single namespace on a management cluster. A Single-Node OpenShift cluster is explicitly not supported as a management cluster.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Storage Expert
#TODO#: Network Expert
#TODO#: Infra Leader

☐ OCP-BASE-11: Control Plane Schedulability Configuration

---

**Title**
Control Plane Schedulability Configuration

Title: Control Plane Schedulability Configuration
Architectural Question: Should control plane nodes be configured to accept application workloads (be schedulable) by setting the `mastersSchedulable` parameter to true?
Issue or Problem: Configuring control plane nodes to accept application workloads increases resource utilization and efficiency for smaller clusters but requires explicitly overriding the default Kubernetes manifest configuration, potentially leading to additional subscription costs.
Assumption: Cluster topology is defined.
Alternatives: Configure Control Plane Nodes as Schedulable
Configure Control Plane Nodes as Unschedulable (Default)
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: Configure Control Plane Nodes as Schedulable: This configuration is required for 3-node/Compact HA clusters to efficiently run application workloads. It maximizes the resource utilization of the control plane nodes.
Configure Control Plane Nodes as Unschedulable (Default): This configuration ensures separation between critical platform components and user workloads, providing dedicated stability and resilience, which is typically recommended for large or Standard HA clusters. This relies on the default manifest setting of `mastersSchedulable: false`.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Configure Control Plane Nodes as Schedulable: Additional subscriptions are required because configuring control plane nodes as schedulable causes them to be treated as compute nodes for licensing purposes. If the cluster has zero dedicated compute nodes, the application ingress load balancer must be configured to route HTTP/HTTPS traffic to the control plane nodes.
Configure Control Plane Nodes as Unschedulable (Default): Requires the deployment of separate worker nodes for hosting application workloads (Standard HA topology).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Operations Expert
#TODO#: Infra Leader

☐ OCP-BASE-12: Infrastructure nodes

---

**Title**
Infrastructure nodes

Title: Infrastructure nodes
Architectural Question: Should platform services (e.g., Ingress routers, internal image registry, monitoring, logging, etc.) be isolated onto a dedicated pool of nodes, or co-located with application workloads?
Issue or Problem: Platform services are critical for cluster operation and consume significant resources (CPU, memory, network I/O). Co-locating them with application workloads can lead to resource contention ("noisy neighbor" effect), impacting the stability of both the platform and the applications. However, creating dedicated nodes increases infrastructure cost and management overhead.
Assumption: Cluster has a standard HA topology.
Alternatives: Co-located on General Worker Nodes: Platform services are deployed on the default worker pool alongside all other applications.
Dedicated Infrastructure Nodes: A separate pool of worker nodes is created and reserved (using taints and labels) to run only platform services.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Co-located on General Worker Nodes: This is the default behavior. It minimizes the number of required nodes and is simpler for small clusters or non-production environments where performance isolation is not a strict requirement.
Dedicated Infrastructure Nodes: This is the recommended practice for production and large-scale clusters. It provides strong resource isolation, preventing application workloads from impacting critical platform services. It also simplifies resource management, licensing (e.g., not running OpenShift platform services on nodes licensed for specific software), and chargeback for application teams.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Co-located on General Worker Nodes: Requires careful sizing of the general worker pool to account for both application and platform overhead. ResourceQuotas and LimitRanges are critical to prevent contention.
Dedicated Infrastructure Nodes: Requires creating and managing a separate MachineSet (on platforms that support it) or a manually configured node pool. Platform operators (like ingress, registry, monitoring) must be configured to tolerate the `node-role.kubernetes.io/infra` taint and use node selectors to run on this pool. This requires at least two (preferably three) additional nodes for high availability.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Operations Expert
#TODO#: Network Expert

☐ OCP-BASE-13: Dedicated Infrastructure Node Count for HA

---

**Title**
Dedicated Infrastructure Node Count for HA

Title: Dedicated Infrastructure Node Count for HA
Architectural Question: What is the minimum required size (replica count) for the dedicated infrastructure node pool to ensure high availability of critical platform services (e.g., Ingress, Registry, Monitoring)?
Issue or Problem: The decision to isolate infrastructure services onto dedicated nodes requires defining the node count necessary to meet site-level High Availability (HA) requirements, balancing operational costs against service resilience.
Assumption: Dedicated Infrastructure Nodes strategy has been selected.
Alternatives: 2 Dedicated Infrastructure Nodes
3 Dedicated Infrastructure Nodes
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document decision.#
Justification: 2 Dedicated Infrastructure Nodes: Minimizes the additional infrastructure footprint and costs while still providing basic High Availability (HA) against a single node failure. This configuration requires at least two additional nodes for high availability.
3 Dedicated Infrastructure Nodes: This is the preferred practice for production and large-scale clusters, providing maximum redundancy and aligning with the recommended count for control plane resilience, ensuring platform services can survive a single domain failure and allow maintenance with zero platform service interruption.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: 2 Dedicated Infrastructure Nodes: This configuration requires careful planning. While providing basic HA, the cluster may experience performance degradation or instability during node maintenance or failure events, as the remaining node(s) must handle the full load.
3 Dedicated Infrastructure Nodes: Highest infrastructure and operational overhead due to managing the additional machines, but offers strong resource isolation and fault tolerance.
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader
#TODO#: Operations Expert

☐ OCP-BASE-14: Hardware Acceleration Strategy

---

**Title**
Hardware Acceleration Strategy

Title: Hardware Acceleration Strategy
Architectural Question: Will the OpenShift platform be architected to support hardware acceleration (e.g., GPUs, TPUs, HPUs) for AI/ML, data science, or high-performance computing workloads?
Issue or Problem: Specialized workloads often require hardware acceleration to meet performance and latency requirements. Enabling this capability impacts hardware procurement, cluster sizing, operator management (e.g., NVIDIA GPU Operator), and scheduling strategies. A strategic decision is needed to prepare the infrastructure for these resources.
Assumption: N/A
Alternatives: General Purpose Compute Only: Rely solely on standard CPU-based compute nodes.
Hardware Acceleration Enabled: Architect the cluster to support and manage specialized accelerator hardware nodes.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: General Purpose Compute Only: Simplifies hardware standardization and reduces cost. Suitable for general microservices, web applications, and lighter data processing tasks that do not require massive parallel processing.
Hardware Acceleration Enabled: Essential for training deep learning models, large-scale inference, and heavy data processing tasks. Requires integrating specialized hardware (e.g., NVIDIA GPUs) and management operators.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: General Purpose Compute Only: Precludes running high-performance AI/ML models efficiently. May lead to extremely high CPU usage and poor performance for specific mathematical workloads.
Hardware Acceleration Enabled: Increases infrastructure cost and complexity. Requires specific node labels, taints, and tolerations to ensure correct workload placement. Introduces dependencies on hardware vendors (e.g., NVIDIA, Intel, AMD).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: AI/ML Platform Owner
#TODO#: Infra Leader

☐ OCP-BASE-15: Virtualization Strategy

---

**Title**
Virtualization Strategy

Title: Virtualization Strategy
Architectural Question: Will the OpenShift platform be configured to host Virtual Machines (VMs) alongside containerized workloads (Converged Infrastructure)?
Issue or Problem: Many organizations have legacy applications that cannot be immediately containerized but need to run in close proximity to modern cloud-native services. A decision is required on whether to manage VMs within OpenShift or rely on external hypervisors (vSphere, RHV).
Assumption: Platform Infrastructure supports virtualization (Bare Metal is preferred; Nested Virtualization is possible but performance-limited).
Alternatives: Containers Only (No Virtualization): The platform hosts only containerized workloads. VMs remain on legacy hypervisors.
Converged Containers & VMs (OpenShift Virtualization): The platform hosts both containers and VMs using KubeVirt technology.
[INSTRUCTIONS: After making your decision, delete the alternatives you did NOT choose from the list above]
Decision: #TODO: Document the decision for each cluster.#
Justification: Containers Only (No Virtualization): Keeps the platform simple and focused on cloud-native patterns. Reduces the "noisy neighbor" risk of heavy VM monoliths affecting microservices.
Converged Containers & VMs (OpenShift Virtualization): Enables infrastructure consolidation ("modernize in place"). Allows legacy VMs to share the same network/storage fabric as containers, reducing latency and operational silos. It is a prerequisite for running Windows Containers (via WMCO) or Hosted Control Planes (HCP) on Bare Metal.
[INSTRUCTIONS: Delete justification points for alternatives you did NOT choose]
Implications: Containers Only: Requires maintaining separate legacy hypervisor infrastructure/licensing.
Converged Containers & VMs (OpenShift Virtualization):
Bare Metal is strongly recommended for production performance.
Requires enabling the OpenShift Virtualization Operator.
Impacts Storage decisions (Block storage/RWX is often required for VM disks and Live Migration).
Impacts Networking (L2/Multus is often required for VMs to look like "real servers" on the network).
[INSTRUCTIONS: Delete implication points for alternatives you did NOT choose]
Agreeing Parties: Person: Role
#TODO#: Enterprise Architect
#TODO#: OCP Platform Owner
#TODO#: Infra Leader

OpenShift Container Platform - Bare Metal Installation
☐ OCP-BM-01: OCP installation method on baremetal infrastructure

---

