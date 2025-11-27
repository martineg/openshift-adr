# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Cluster general administration and Day2 operations management

## OCP-MGT-01

**Title**
Namespace/Project Allocation Strategy

**Architectural Question**
What is the strategy for grouping and allocating namespaces (projects) to users, teams, and applications?

**Issue or Problem**
The project allocation model determines the level of isolation, complexity of resource quota management, and delegation of administrative tasks.

**Assumption**
N/A

**Alternatives**

- Shared Project per Environment
- Project per Team per Environment
- Project per Application per Environment
- Project per Team per Application per Environment

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Shared Project per Environment:** Minimizes overhead (fewest total projects). Requires strict enforcement of ResourceQuota and NetworkPolicy to isolate workloads within the shared project boundary.
- **Project per Team per Environment:** Balances overhead and isolation. Projects naturally delineate resource boundaries (quotas) and RBAC delegation based on team ownership (tenant).
- **Project per Application per Environment:** Provides the highest logical isolation, allowing granular resource allocation and specific security controls (e.g., SCC/PSA policies) for each application instance.
- **Project per Team per Application per Environment:** Granular control combining team ownership and per-application isolation.

**Implications**

- **Shared Project per Environment:** High risk of resource contention and "noisy neighbor" problems if quotas are not managed precisely.
- **Project per Team per Environment:** Limits the blast radius of a single misconfigured application to the owning team's project, preventing cluster-wide impact.
- **Project per Application per Environment:** Management overhead scales linearly with the number of deployed applications.
- **Project per Team per Application per Environment:** Highest complexity and management overhead.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-MGT-02

**Title**
RBAC Model (Delegation Strategy)

**Architectural Question**
What is the strategy for delegating project-level administration and resource management permissions?

**Issue or Problem**
Defining the RBAC strategy balances centralized platform governance (security) with development team autonomy and velocity.

**Assumption**
Project Allocation Strategy is defined. Identity Provider and Groups are configured.

**Alternatives**

- Centralized Platform Team Control (e.g., `cluster-admin` for platform, `edit` for devs)
- Delegated Project Administration (e.g., `admin` role for team leads in their projects)
- Custom Role-Based Access Control (RBAC) (Tailored roles/bindings)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Centralized Control:** Maintains strict central control, platform team manages most project-level admin tasks. Minimizes security surface area delegated to tenants.
- **Delegated Admin:** Empowers project team leads (`admin` role) over their own projects, fostering autonomy and reducing burden on central platform team.
- **Custom RBAC:** Implements tailored permissions for specific complex organizational needs not met by standard roles.

**Implications**

- **Centralized:** Creates bottleneck, developers rely on platform team for admin tasks (project roles, quotas). Slower velocity for tenants.
- **Delegated:** Increases surface area for potential misconfigurations by tenants but reduces central operational load, improves developer velocity.
- **Custom:** Requires significant effort to develop, test, maintain custom roles/bindings. Increases complexity.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Security Expert

---

## OCP-MGT-03

**Title**
Image Registry Strategy (Application Images)

**Architectural Question**
Which image registry will be used for storing internally built application images (including custom RHOAI notebook images)?

**Issue or Problem**
An image registry is needed to store, scan, and distribute container images for CI/CD and deployments. This is separate from the disconnected mirror registry which primarily holds Red Hat content.

**Assumption**
Internal applications or custom container images will be built and deployed on the platform.

**Alternatives**

- OpenShift Internal Registry (Image Registry Operator)
- Existing HA Corporate Image Registry (e.g., Quay, Artifactory, Nexus)
- New Dedicated HA Corporate Image Registry (e.g., Deploying Quay)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OpenShift Internal Registry:** Uses the built-in registry. Simplest option integrated with OCP. Managed by Cluster Image Registry Operator.
- **Existing Corporate Registry:** Leverages existing, hardened, managed registry infrastructure. Maintains single source of truth for all artifacts.
- **New Dedicated Registry (Quay):** Deploys a new, fully-featured registry optimized as HA source for internal images. Offers advanced features (security, team isolation).

**Implications**

- **Internal Registry:** Lifecycle tied to cluster. Requires persistent storage config (ODF RWO/RWX or other PVs). Storage must be sized appropriately. May need extra security hardening if exposed externally. Lacks advanced features of dedicated registries.
- **Existing Registry:** Requires network connectivity and pull secrets in app namespaces. Build pipelines need push credentials. May need `ImageContentSourcePolicy`. Relies on external system availability/management and registry team support.
- **New Dedicated Registry:** Provides most features but adds another critical HA component to deploy/manage. Requires dedicated infrastructure or significant OCP resources if run internally. May require separate subscription/license (e.g., Quay).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MGT-04

**Title**
Project Resource Quotas Strategy

**Architectural Question**
What strategy will enforce resource consumption limits (CPU, memory, storage, GPUs) at the project (tenant) level?

**Issue or Problem**
Without quotas, a single project could monopolize cluster resources, impacting stability and availability for all tenants.

**Assumption**
Multi-tenancy or resource contention is expected. Project Allocation is defined.

**Alternatives**

- No Quotas
- Standardized Tier-Based Quotas (e.g., Small, Medium, Large)
- Custom Per-Project Quotas

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Quotas:** Simplifies administration in non-prod or trusted environments with low contention risk. Not recommended for production/multi-tenant.
- **Standardized Tiers:** Scalable, manageable approach. Defines standard project sizes with preset resource budgets (including specialized resources like `requests.nvidia.com/gpu`). Simplifies onboarding.
- **Custom Per-Project:** Maximum flexibility, tailoring budgets to specific project needs.

**Implications**

- **No Quotas:** High risk of resource starvation, "noisy neighbors" destabilizing the cluster.
- **Standardized Tiers:** Simplifies onboarding/capacity planning. May not perfectly fit every project's needs but provides reasonable bounds. Easier to automate.
- **Custom Per-Project:** Most accurate allocation but significant administrative overhead to define, approve, manage each custom quota. Harder to automate.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MGT-05

**Title**
Cluster Update Channel Strategy

**Architectural Question**
Which OpenShift update channel will be selected to govern the cadence and stability of platform upgrades?

**Issue or Problem**
The update channel determines how quickly the cluster receives new versions and the level of validation those versions have undergone. This impacts stability, feature availability, and support windows.

**Assumption**
N/A

**Alternatives**

- **Stable Channel:** Releases are promoted only after passing testing in the Fast channel and proving stability in the field.
- **Fast Channel:** Releases are promoted as soon as Red Hat QA approves them. Access to new features sooner, but potentially higher risk of bugs.
- **Candidate Channel:** Pre-release builds. Not for production.
- **EUS (Extended Update Support) Channel:** Allows staying on specific even-numbered minor versions (e.g., 4.14) for longer periods (18+ months) with a simplified upgrade path to the next EUS version.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Stable Channel:** Recommended default for production. Balances novelty with reliability.
- **Fast Channel:** Suitable for non-production or "canary" clusters to test upcoming features before they hit Stable.
- **EUS Channel:** Critical for mission-critical clusters where upgrade frequency must be minimized (e.g., Telco, Edge, Banking).

**Implications**

- **Stable:** Slower access to fixes/features than Fast.
- **Fast:** Higher risk of regression.
- **EUS:** Upgrade paths are stricter (e.g., 4.12 -> 4.13 -> 4.14 required, even if "skipping" via EUS logic). Only available on specific versions.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MGT-06

**Title**
Platform Backup and Restore Strategy

**Architectural Question**
What is the strategy for backing up and restoring OpenShift cluster state (etcd) and application persistent data (PVs)?

**Issue or Problem**
A comprehensive, tested backup/restore strategy is critical for disaster recovery and protecting against data loss/corruption. Must cover control plane (etcd), stateful app data (PVs), and potentially stateless app resources.

**Assumption**
Disaster recovery and data protection are required.

**Alternatives**

- Etcd Snapshot Only
- OpenShift Data Protection (OADP/Velero) for PVs and Resources
- Comprehensive Layered Backup

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Etcd Snapshot Only:** Backs up the critical control plane state (Kubernetes resources, cluster configuration) via etcd snapshots, which is sufficient for cluster recovery if underlying application data (PVs) is handled separately or is ephemeral.
- **OpenShift Data Protection (OADP/Velero) for PVs and Resources:** Uses the OADP Operator (based on Velero) to back up cluster resources and application persistent data volumes (PVs/PVCs). OADP supports incremental backups of block and Filesystem volumes.
- **Comprehensive Layered Backup:** Combines Etcd snapshots for cluster state with OADP for application data and additional measures for immutable objects (e.g., MachineConfigs, custom resources).

**Implications**

- **Etcd Snapshot Only:** Does not protect application data (PVs), leading to data loss unless application storage is managed by an external highly available/DR solution.
- **OpenShift Data Protection (OADP/Velero) for PVs and Resources:** Requires deploying the OADP Operator and defining backup storage locations (e.g., S3, ODF Object Storage). Requires enabling OpenShift User Workload Monitoring to observe OADP metrics.
- **Comprehensive Layered Backup:** Highest complexity and resource usage. Requires meticulous planning to ensure consistency between etcd snapshots and volume backups during restore operations.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-MGT-07

**Title**
Remote Health Reporting (Telemetry) Configuration

**Architectural Question**
Should the cluster enable the Remote Health Reporting (Telemetry) service to send cluster diagnostics and usage data to Red Hat?

**Issue or Problem**
Telemetry is enabled by default for connected OpenShift clusters. A decision is required on whether to maintain this default or disable it to meet strict security and compliance requirements related to exporting cluster diagnostic data or to conserve outbound network bandwidth.

**Assumption**
Cluster is in a connected environment.

**Alternatives**

- Enable Remote Health Reporting (Telemetry) (Default)
- Disable Remote Health Reporting (Telemetry)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Enable Remote Health Reporting (Telemetry) (Default):** This leverages the default cluster configuration. The service automatically entitles the cluster if it has internet access. This configuration provides valuable built-in remote health monitoring and diagnostics to Red Hat.
- **Disable Remote Health Reporting (Telemetry):** This is necessary to satisfy strict security policies or compliance mandates that prohibit sending diagnostic or usage data outside the internal network.

**Implications**

- **Enable Remote Health Reporting (Telemetry) (Default):** Requires open firewall egress rules to external Red Hat endpoints for the Telemetry service to function.
- **Disable Remote Health Reporting (Telemetry):** Removes a built-in diagnostic safety net, potentially complicating troubleshooting and relying solely on external tools or manual inspection.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MGT-08

**Title**
Cluster Autoscaling Strategy

**Architectural Question**
Will the cluster utilize the Cluster Autoscaler to dynamically adjust the size of MachineSets based on workload demand?

**Issue or Problem**
Static clusters may be over-provisioned (wasting money) or under-provisioned (causing pending pods). Autoscaling adapts infrastructure to demand but adds complexity and cost unpredictability.

**Assumption**
Platform supports Machine API (IPI/Cloud).

**Alternatives**

- **Static Sizing:** Fixed number of nodes per MachineSet. Manual scaling only.
- **Cluster Autoscaler Enabled:** Dynamic scaling within defined min/max bounds.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Static Sizing:** Predictable costs and topology. Simple to manage. Recommended for Bare Metal UPI or fixed-budget environments.
- **Cluster Autoscaler Enabled:** Optimizes cloud costs by creating nodes only when pods are pending and deleting them when empty. Recommended for cloud IPI or dynamic virtualization environments.

**Implications**

- **Static Sizing:** Operations team must monitor capacity and manually scale out/in.
- **Autoscaler:** Risk of "runaway" costs if max limits are too high or workloads lack requests/limits. Pods must tolerate disruption (node scale-down).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MGT-09

**Title**
General Node Remediation Strategy (MachineHealthCheck)

**Architectural Question**
How will unhealthy nodes (e.g., NotReady state) be automatically remediated in Cloud/Virtualization environments?

**Issue or Problem**
Nodes can freeze or disconnect. Manual recovery is slow. Automated remediation improves uptime but risks data loss if configured incorrectly (e.g., fencing).

**Assumption**
Platform supports Machine API (IPI).

**Alternatives**

- **Manual Remediation:** Alerts fire; humans investigate.
- **MachineHealthCheck (MHC) Enabled:** Controller detects unhealthy nodes and recreates them (Cloud/Virt) or reboots them (Bare Metal).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Manual:** Safe. Prevents accidental data loss or "reboot loops" in unstable clusters.
- **MHC Enabled:** Self-healing infrastructure. Essential for high availability in cloud environments where instances are ephemeral.

**Implications**

- **MHC Enabled:** Must configure `maxUnhealthy` to prevent cascading failures. **Warning:** On platforms without shared storage (like vSphere without RWX), recreating a node might detach RWO volumes safely, but requires careful testing.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MGT-10

**Title**
Pod Descheduling Strategy

**Architectural Question**
Will the Descheduler be deployed to proactively move running pods to optimize cluster balance?

**Issue or Problem**
The default scheduler only places _new_ pods. Over time, clusters become fragmented or imbalanced (e.g., all high-cpu pods on one node).

**Assumption**
N/A

**Alternatives**

- **No Descheduler:** Pods stay where they land until deleted or evicted.
- **Descheduler Enabled:** Automated eviction of pods based on policies (e.g., `RemoveDuplicates`, `LowNodeUtilization`).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Descheduler:** Stability. Pods are not restarted unless necessary.
- **Descheduler Enabled:** Optimization. Actively corrects placement to enforce anti-affinity, improve bin-packing, or clear nodes with high utilization.

**Implications**

- **Descheduler:** Pods will be killed and rescheduled. Workloads **must** utilize PodDisruptionBudgets (PDBs) and handle restarts gracefully.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Application team leadership

---

## OCP-MGT-11

**Title**
Web Console Customization Strategy

**Architectural Question**
Will the OpenShift Web Console be customized with organization-specific branding, links, or plugins?

**Issue or Problem**
The default console implies a generic Red Hat experience. Enterprises often need to add "Help" links to internal ticketing systems, display classification banners (e.g., "TOP SECRET"), or integrate custom UI plugins (e.g., for internal tools).

**Assumption**
N/A

**Alternatives**

- **Standard Console:** Default look and feel.
- **Customized Console:** Custom logo, login text, help links, notification banners, or dynamic plugins enabled.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Standard:** Zero maintenance.
- **Customized:** Improves user experience and compliance (e.g., mandatory warning banners). Directs users to correct support channels.

**Implications**

- **Customized:** Requires managing `Console` resource configuration and potentially hosting assets (logos) or plugin containers.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-MGT-12

**Title**
Cluster Capabilities Selection Strategy

**Architectural Question**
Will optional cluster capabilities (e.g., Marketplace, Insights, Console) be disabled to optimize resource consumption?

**Issue or Problem**
By default, OpenShift installs a comprehensive set of operators. For resource-constrained environments like Single Node OpenShift (SNO) or Edge, these idle operators consume valuable CPU/RAM.

**Assumption**
Cluster topology is SNO or Edge.

**Alternatives**

- **Full Capabilities (Default):** Installs all standard operators.
- **Optimized/Reduced Capabilities:** Explicitly disables optional components via `install-config.yaml` (`capabilities.baselineCapabilitySet` or `additionalEnabledCapabilities`).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Full Capabilities:** Ensures feature parity with standard clusters. Simpler updates (no missing dependencies).
- **Optimized/Reduced:** Critical for SNO. Can save significant memory (e.g., disabling `Marketplace`, `Console`, `Insights`).

**Implications**

- **Full:** Higher overhead.
- **Optimized:** "Day 2" enablement of features (like adding the Console back later) can be complex.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
