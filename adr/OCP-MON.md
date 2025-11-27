# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Monitoring stacks (Metrics)

## OCP-MON-01

**Title**
Monitoring Strategy

**Architectural Question**
What is the strategy for monitoring cluster and application metrics?

**Issue or Problem**
A monitoring solution is required to collect and store metrics for observing cluster health, managing capacity, and troubleshooting performance issues. Decisions are needed on the scope of monitoring and long-term data retention.

**Assumption**
N/A

**Alternatives**

- Default Platform Monitoring
- Enable User Workload Monitoring
- Customized Monitoring Stack via COO

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Platform Monitoring:** Provides built-in, preconfigured monitoring for all core OpenShift components (e.g., etcd, Kubernetes API server, nodes, Operators) using Prometheus, Alertmanager, and Thanos Query. This is enabled by default.
- **Enable User Workload Monitoring:** Extends the Prometheus stack to collect metrics and expose alerts specifically for workloads running in user-defined projects (namespaces). This is optional.
- **Customized Monitoring Stack via COO:** Leverages the Cluster Observability Operator (COO) to create and manage highly customizable monitoring stacks, offering a more tailored and detailed view of specific namespaces or components beyond the default configuration.

**Implications**

- **Default Platform Monitoring:** Configuration is locked down and supported only via the Cluster Monitoring Operator (CMO) ConfigMap. Data storage capacity for Thanos is pre-allocated.
- **Enable User Workload Monitoring:** Increases resource consumption (CPU/RAM/storage) due to additional Prometheus and Thanos Ruler instances running in the `openshift-user-workload-monitoring` project.
- **Customized Monitoring Stack via COO:** Provides maximum flexibility for metric collection and routing, but introduces management overhead for the custom stacks and requires advanced knowledge of monitoring configuration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: DevOps Engineer
- Person: #TODO#, Role: Operations Engineer

---

## OCP-MON-02

**Title**
Metrics Collection Profile

**Architectural Question**
Which metrics collection profile will be applied to the cluster to balance observability depth against resource consumption?

**Issue or Problem**
The default monitoring stack scrapes a vast number of metrics. On resource-constrained clusters (e.g., SNO, Edge), this overhead (CPU/RAM) can be prohibitive.

**Assumption**
N/A

**Alternatives**

- **Default Profile:** Collects all standard platform metrics.
- **Minimal Profile:** Collects only essential metrics for alerts and core health.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Profile:** Maximize observability. Support teams have full data for debugging.
- **Minimal Profile:** Reduces CPU/Memory usage significantly. Recommended for SNO/Edge.

**Implications**

- **Minimal Profile:** Some dashboards in the console may be empty. Troubleshooting complex issues may require temporarily enabling full metrics.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MON-03

**Title**
Persistent Storage Strategy for Monitoring

**Architectural Question**
Will Persistent Volume Claims (PVCs) be configured for Prometheus and Alertmanager to ensure metric durability?

**Issue or Problem**
By default, OpenShift Monitoring uses ephemeral storage. If a Prometheus pod restarts, recent metrics are lost. This impacts alerting continuity and historical trending.

**Assumption**
Storage Provider is defined.

**Alternatives**

- **Ephemeral Storage (Default):** Metrics lost on pod restart.
- **Persistent Storage (PVC):** Metrics retained across restarts.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Ephemeral:** Simple. No storage management overhead. Acceptable if long-term metrics are offloaded via Remote Write.
- **Persistent (PVC):** Essential for standalone clusters where local history matters. Prevents data gaps during upgrades.

**Implications**

- **Persistent:** Requires a block storage class. Resizing PVCs later can be complex (Prometheus statefulsets).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-MON-04

**Title**
Data Retention Policy

**Architectural Question**
How long should high-resolution metrics be retained within the cluster's local Prometheus instance?

**Issue or Problem**
Default retention is 15 days. Extending this increases disk space requirements linearly.

**Assumption**
Persistent Storage is enabled (if retention > restart).

**Alternatives**

- **Default Retention (15 Days):** Balanced for operational health checks.
- **Custom Retention (Extended):** For compliance or local trending.
- **Minimal Retention:** If offloading to central system immediately.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default (15 Days):** Sufficient for most "Is it healthy now?" questions.
- **Custom:** Required if no central metrics store exists.

**Implications**

- **Extended Retention:** drastically increases PVC size requirements. Prometheus query performance may degrade over long time ranges.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert

---

## OCP-MON-05

**Title**
Remote Write / Federation Strategy

**Architectural Question**
Will cluster metrics be forwarded (Remote Write) to a centralized long-term storage system (e.g., Thanos, Cortex, Splunk)?

**Issue or Problem**
Local Prometheus is not a long-term archive. To analyze trends across months/years or aggregate multiple clusters, data must be exported.

**Assumption**
Multi-cluster fleet or Long-term retention requirement exists.

**Alternatives**

- **Local Only:** No export. Data dies with retention policy.
- **Remote Write Enabled:** Metrics pushed to central store.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Local Only:** Simple for standalone/dev clusters.
- **Remote Write:** Mandatory for Fleet Observability (ACM Observability uses this). Enables global querying.

**Implications**

- **Remote Write:** Increases network egress bandwidth. Requires authentication configuration to the remote endpoint.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-MON-06

**Title**
Alertmanager Integration Strategy

**Architectural Question**
How will alerts be routed to operational teams?

**Issue or Problem**
Alerts inside the cluster are useless if no one sees them.

**Assumption**
N/A

**Alternatives**

- **Cluster-Local Alertmanager:** Configure receivers (Slack, PagerDuty, Email) directly in the cluster.
- **External Alert Routing:** Forward all alerts to a central event bus or external Alertmanager (e.g., via Remote Write or Webhook).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Cluster-Local:** Good for team autonomy (tenants manage their own alerts).
- **External Routing:** Centralizes noise reduction, inhibition, and aggregation in a NOC/SOC.

**Implications**

- **Cluster-Local:** Operational overhead to manage secrets (API keys) in every cluster.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert

---
