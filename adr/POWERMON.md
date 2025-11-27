# ARCHITECTURE DECISION RECORDS FOR: OpenShift Power Monitoring (Kepler)

## POWERMON-01

**Title**
Power Monitoring Enablement

**Architectural Question**
Will OpenShift Power Monitoring (Kepler) be deployed to track energy consumption at the node and container level?

**Issue or Problem**
Sustainability goals and cost optimization often require visibility into the energy footprint of workloads. However, collecting these metrics requires running a privileged eBPF agent on every node.

**Assumption**
Cluster is running on Bare Metal infrastructure (required for RAPL access).

**Alternatives**

- **Enable Power Monitoring:** Deploy the Power Monitoring Operator and Kepler agents.
- **Disable Power Monitoring:** Do not track energy metrics.

**Decision**
#TODO: Document the decision for the cluster.#

**Justification**

- **Enable Power Monitoring:** Provides granular visibility into energy usage (Joules/Watts) per Pod and Namespace. Essential for Green IT initiatives or chargeback based on energy.
- **Disable Power Monitoring:** Conserves CPU resources on nodes. Avoids running privileged eBPF agents if energy metrics are not a business requirement.

**Implications**

- **Enable:** Installs the `kepler` daemonset. Requires Bare Metal nodes with supported CPU architectures (Intel RAPL/AMD). Currently a **Technology Preview (TP)** feature.
- **Disable:** No visibility into power consumption.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## POWERMON-02

**Title**
Power Monitoring Security Mode

**Architectural Question**
How will access to the Kepler metrics endpoint be secured?

**Issue or Problem**
Power metrics can reveal sensitive information about workload patterns. The endpoint must be protected to prevent unauthorized scraping.

**Assumption**
Power Monitoring is enabled.

**Alternatives**

- **RBAC/TLS Mode (Recommended):** Metrics endpoint is protected by OpenShift RBAC (kube-rbac-proxy) and TLS.
- **Open/Unsecured Mode:** Metrics endpoint is exposed via HTTP without authentication.

**Decision**
#TODO: Document the decision.#

**Justification**

- **RBAC/TLS Mode:** Ensures only authorized monitoring stacks (like OpenShift User Workload Monitoring) can scrape data. Encrypts traffic.
- **Open/Unsecured Mode:** Simplifies integration with external, non-Kubernetes monitoring tools that cannot handle mTLS/Bearer tokens. High security risk.

**Implications**

- **RBAC/TLS Mode:** Requires configuring the `PowerMonitor` CR with `spec.security.mode: rbac`. Scrapers must use a ServiceAccount token.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## POWERMON-03

**Title**
Dashboard Integration Strategy

**Architectural Question**
Will Power Monitoring dashboards be integrated into the OpenShift Console or hosted externally?

**Issue or Problem**
Metrics are useless without visualization. OpenShift can embed power dashboards natively.

**Assumption**
Power Monitoring is enabled.

**Alternatives**

- **Console Integration:** Enable the `Plugin` to show power data in the OCP Console "Observe" tab.
- **External Dashboards:** Visualize data in an external Grafana instance.

**Decision**
#TODO: Document the decision.#

**Justification**

- **Console Integration:** Seamless experience for developers and admins. No context switching.
- **External Dashboards:** More flexible customization. Useful if aggregating power data across a fleet of clusters into a central view.

**Implications**

- **Console Integration:** Requires enabling the Console Plugin in the `PowerMonitor` CR.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
