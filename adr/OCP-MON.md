# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Monitoring stacks (Metrics)

## OCP-MON-01

**Title**
Monitoring

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
