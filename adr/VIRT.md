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

## VIRT-02

**Title**
VM Network Connectivity Strategy

**Architectural Question**
How will Virtual Machines connect to the network (Pod Network vs External Network)?

**Issue or Problem**
VMs have different networking needs than Pods. Some need simple outbound access (Masquerade), while others need Layer 2 access to existing physical VLANs (Bridge/SR-IOV).

**Assumption**
OpenShift Virtualization is enabled.

**Alternatives**

- **Masquerade (Default Pod Network):** VM uses the Pod IP and NAT.
- **Linux Bridge (Layer 2):** VM attaches directly to a physical/VLAN network via a node bridge.
- **SR-IOV:** VM bypasses kernel for high performance.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Masquerade:** Simplest. Good for web apps/databases that just need an IP.
- **Linux Bridge:** Essential for legacy apps requiring L2 connectivity, broadcast/multicast, or specific VLAN IPs (migration from VMware).
- **SR-IOV:** Mandatory for high-throughput/low-latency workloads (Telco/VDU).

**Implications**

- **Masquerade:** No L2 visibility. Ingress via Services/Routes.
- **Linux Bridge:** Requires configuring NNCP on nodes (`br-ex` or secondary bridges).
- **SR-IOV:** Requires hardware support and SR-IOV Operator.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## VIRT-03

**Title**
VM Storage Class Strategy

**Architectural Question**
Which StorageClass will be used for VM disks to ensure Live Migration compatibility?

**Issue or Problem**
Live Migration requires shared storage. Specifically, it requires **RWX Block** (optimal) or **RWX Filesystem** (acceptable but slower). RWO storage blocks migration.

**Assumption**
Live Migration is enabled.

**Alternatives**

- **RWX Block Storage (Recommended):** ODF Block, external SAN.
- **RWX Filesystem:** NFS, ODF CephFS.
- **RWO Block:** Local disks, standard cloud disks.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **RWX Block:** Best performance and reliability for VM disk images.
- **RWX Filesystem:** Good compatibility, slightly higher overhead (locks).
- **RWO Block:** High performance but **disables Live Migration**. Good for static/pinned VMs.

**Implications**

- **RWX:** Requires a storage provider that supports it (ODF is the standard choice).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## VIRT-04

**Title**
Workload Update Strategy (Eviction Policy)

**Architectural Question**
How will running VMs be handled when a node enters maintenance mode (e.g., OCP upgrade)?

**Issue or Problem**
When a node drains, VMs must move.

**Assumption**
Live Migration is enabled.

**Alternatives**

- **LiveMigrate (Default):** VMs are moved to another node without shutdown.
- **Evict (Shutdown):** VMs are stopped and restarted elsewhere.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **LiveMigrate:** Zero downtime. Essential for production.
- **Evict:** Necessary for VMs using non-migratable hardware (PCI Passthrough/vGPU) or RWO storage.

**Implications**

- **LiveMigrate:** Requires cluster-level HA (2+ workers).
- **Evict:** Causes service interruption.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert

---

## VIRT-05

**Title**
Resource Allocation Strategy (InstanceTypes)

**Architectural Question**
Will VM sizing be standardized using InstanceTypes or defined via custom ad-hoc templates?

**Issue or Problem**
Ad-hoc sizing leads to fragmentation and difficult capacity planning ("Snowflake VMs").

**Assumption**
N/A

**Alternatives**

- **InstanceTypes (Standardized):** Use `VirtualMachineClusterInstancetype` (e.g., `u1.medium`, `m1.large`).
- **Custom Templates:** Users define arbitrary CPU/RAM.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **InstanceTypes:** Cloud-like experience. Simplifies quota management and scheduling.
- **Custom Templates:** Flexibility for niche legacy apps with weird ratios.

**Implications**

- **InstanceTypes:** Requires managing the catalog of types.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner

---

## VIRT-06

**Title**
Performance Isolation (Dedicated CPU)

**Architectural Question**
Will performance-sensitive VMs utilize Dedicated (Pinned) CPU resources?

**Issue or Problem**
Standard VMs share CPU time. Latency-sensitive apps (DBs, Telco) need guaranteed cycles.

**Assumption**
N/A

**Alternatives**

- **Shared CPU (Default):** Burstable. High density.
- **Dedicated CPU (Pinned):** 1:1 mapping to physical cores.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Shared:** efficient. Good for web apps.
- **Dedicated:** Guarantees performance. Eliminates noisy neighbors.

**Implications**

- **Dedicated:** Reduces node density. Requires `Guaranteed` QoS class.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## VIRT-07

**Title**
Live Migration Network Isolation

**Architectural Question**
Will Live Migration traffic run on the primary pod network or a dedicated secondary network?

**Issue or Problem**
Migration involves copying RAM/Disk state. This generates massive bandwidth, potentially choking the App/API network.

**Assumption**
Cluster supports Multus.

**Alternatives**

- **Primary Network (Default):** Shared with all traffic.
- **Dedicated Secondary Network:** Isolated NIC/VLAN for migration.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Primary:** Simple. Fine for small VMs.
- **Dedicated:** Mandatory for large memory VMs (SAP HANA, DBs) or 10Gbps+ clusters.

**Implications**

- **Dedicated:** Requires extra physical NICs and Multus config (`NetworkAttachmentDefinition`).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---
