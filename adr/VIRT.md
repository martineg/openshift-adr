# ARCHITECTURE DECISION RECORDS FOR: OpenShift Virtualization

## VIRT-01

**Title**
Live Migration Strategy for OpenShift Virtualization

**Architectural Question**
If using OpenShift Virtualization should the OpenShift cluster be configured to support Live Migration for virtual machines?

**Issue or Problem**
The capability to live-migrate VMs depends on the cluster-level High Availability (HA) status, which is determined **at installation time** based on the initial worker node count. This setting is immutable. Failing to identify this requirement early can lead to deploying a topology (like SNO) that permanently blocks VM mobility and maintenance without downtime.

**Assumption**
OpenShift Virtualization will be used.

**Alternatives**

- Live Migration Enabled (Recommended for Production)
- Live Migration Disabled

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Live Migration Enabled:** This ensures business continuity for virtualized workloads. It allows VMs to seamlessly move to another node during maintenance, upgrades, or node failures without service interruption. This capability requires that the cluster is installed with **two or more worker nodes**.
- **Live Migration Disabled:** This simplifies the infrastructure requirements for environments where VM downtime during maintenance is acceptable (e.g., ephemeral labs, edge sites, or cost-constrained environments).

**Implications**

- **Live Migration Enabled:** **Mandates a multi-node topology.** The cluster must be installed with at least **two worker nodes** to set the internal HA flag to `true`. Single Node OpenShift (SNO) is **not supported** for this use case.
- **Live Migration Disabled:** Allows the use of **Single Node OpenShift (SNO)** or minimalist topologies with fewer than two workers. VMs must be shut down or restarted to move between nodes (if multiple exist) or during any node-level maintenance.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---
