# ARCHITECTURE DECISION RECORDS FOR: OpenShift Data Foundation (ODF)

## ODF-01

**Title**
ODF Deployment Mode

**Architectural Question**
Will OpenShift Data Foundation (ODF) be deployed internally on the OpenShift cluster (Converged Mode) or connected to an external Red Hat Ceph Storage cluster?

**Issue or Problem**
The deployment mode dictates resource sharing, scalability, and operational management boundaries. Internal mode simplifies operations but consumes cluster resources; external mode offers independent scaling but requires separate infrastructure management.

**Assumption**
OpenShift Data Foundation (ODF) has been selected as the Storage provider.

**Alternatives**

- **Internal Mode (Converged):** ODF components (Ceph, NooBaa) run containerized directly on the OpenShift worker nodes.
- **External Mode:** ODF operators manage services exposed by an **external, dedicated Red Hat Ceph Storage cluster**.

**Decision**
#TODO: Document the decision for the cluster.#

**Justification**

- **Internal Mode (Converged):** Simplifies deployment and management by consolidating resources. The storage platform lifecycle is managed by the OpenShift operators. Recommended for most standard deployments, edge sites, and where a separate Ceph team does not exist.
- **External Mode:** Offloads storage resource contention from the OpenShift cluster. This is used when integrating OCP with a pre-existing, large-scale Ceph environment or when storage scaling requirements significantly outpace compute requirements.

**Implications**

- **Internal Mode (Converged):** Requires OCP worker nodes to dedicate resources (CPU, RAM, disk I/O) to the storage platform. Requires ODF subscription and careful capacity planning on the OCP nodes.
- **External Mode:** Requires independent management and lifecycle control of the external Ceph cluster. The OCP cluster only runs the CSI consumers.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## ODF-02

**Title**
Infrastructure Node Strategy for ODF

**Architectural Question**
Will ODF workloads run on shared worker nodes (converged with applications) or on dedicated infrastructure nodes?

**Issue or Problem**
ODF is resource-intensive. Co-locating it with application workloads can lead to resource contention ("noisy neighbor" effect) and complicates licensing (e.g., paying for OCP cores vs ODF cores).

**Assumption**
ODF Deployment Mode is set to **Internal Mode**.

**Alternatives**

- **Shared Worker Nodes (Converged):** ODF runs alongside user applications on standard workers.
- **Dedicated Storage Nodes:** ODF runs on a dedicated `MachineSet` or node pool (tainted) reserved solely for storage.

**Decision**
#TODO: Document the decision.#

**Justification**

- **Shared Worker Nodes (Converged):** Minimizes hardware footprint. Suitable for smaller clusters or where hardware count is constrained (e.g., compact clusters).
- **Dedicated Storage Nodes:** Strongly recommended for production. Ensures predictable performance for both storage and applications. Simplifies subscription management (ODF cores vs OCP cores). Allows selecting hardware optimized for storage (high disk density) for these specific nodes.

**Implications**

- **Shared Worker Nodes (Converged):** High risk of CPU/RAM contention. Requires strict resource limits.
- **Dedicated Storage Nodes:** Increases the total node count of the cluster (requires at least 3 dedicated nodes).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## ODF-03

**Title**
ODF Network Isolation Strategy

**Architectural Question**
Will ODF replication and client traffic share the primary OpenShift network (SDN) or utilize dedicated secondary network interfaces via Multus?

**Issue or Problem**
Ceph replication (backend traffic) and client I/O (frontend traffic) can saturate the primary cluster network interface, affecting application and control plane stability. Isolating this traffic improves performance and security.

**Assumption**
Cluster networking supports Multus (Secondary Networks).

**Alternatives**

- **Shared Primary Network (Default):** All storage traffic flows over the standard OCP pod network (OVN-Kubernetes).
- **Dedicated Storage Network (Multus):** Storage replication and/or client traffic is segregated onto dedicated physical interfaces.

**Decision**
#TODO: Document the decision.#

**Justification**

- **Shared Primary Network (Default):** Simplest configuration. No requirement for extra NICs or complex network plumbing. Suitable for 10Gbps+ networks with moderate load.
- **Dedicated Storage Network (Multus):** Recommended for high-performance production environments. Physically isolates heavy write replication traffic from the API/App traffic. prevents storage bursts from causing API latency or heartbeat timeouts.

**Implications**

- **Dedicated Storage Network (Multus):** Requires nodes to have multiple physical interfaces. Requires configuring `NetworkAttachmentDefinition`s and selecting the correct interface during ODF installation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Storage Expert

---

## ODF-04

**Title**
Backing Storage Mechanism

**Architectural Question**
How will the underlying storage devices be consumed by ODF for the creation of Object Storage Daemons (OSDs)?

**Issue or Problem**
ODF requires raw storage capacity. The method of consuming this capacity depends heavily on the underlying infrastructure (Cloud vs Bare Metal vs Virtualization) and impacts performance and flexibility.

**Assumption**
ODF Deployment Mode is set to **Internal Mode**.

**Alternatives**

- **Dynamic Cloud Provisioning:** Use cloud provider PVs (e.g., AWS gp3, vSphere VMDK) via StorageClasses.
- **Local Devices via LVMS (Recommended for Bare Metal):** Use the Logical Volume Manager Storage (LVMS) operator to manage local disks.
- **Local Devices via LSO (Legacy/Specific):** Use the Local Storage Operator (LSO) for direct disk mapping.

**Decision**
#TODO: Document the decision for the platform.#

**Justification**

- **Dynamic Cloud Provisioning:** Standard for Cloud and Virtualized environments (AWS, VMware, OpenStack). ODF consumes PVs dynamically provisioned by the infrastructure provider.
- **Local Devices via LVMS:** **Recommended for Bare Metal** (and edge). Provides flexibility (snapshots, resizing) and efficient disk usage by placing LVM thin provisioning between the raw disk and Ceph.
- **Local Devices via LSO:** Legacy method or for specific use cases requiring direct disk-to-OSD mapping. Less flexible than LVMS.

**Implications**

- **Dynamic Cloud Provisioning:** Performance is bound by the underlying cloud volume limits.
- **Local Devices via LVMS:** Requires the LVMS Operator. Offers better flexibility for managing underlying devices and aligns with modern OCP storage practices.
- **Local Devices via LSO:** Rigid configuration; 1:1 disk mapping.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## ODF-05

**Title**
Failure Domain / Availability Zone Strategy

**Architectural Question**
How will ODF be configured to distribute data replicas across physical failure domains (Racks, Zones, Regions)?

**Issue or Problem**
To ensure data survivability, ODF must be aware of the underlying physical topology. Placing all replicas in the same rack or zone creates a Single Point of Failure (SPoF).

**Assumption**
The underlying platform (Bare Metal, OpenStack, Cloud) exposes topology information (e.g., node labels).

**Alternatives**

- **No Failure Domain Awareness (Single Zone):** Replicas distributed by node only.
- **Topology-Aware Distribution (Multi-AZ / Rack-Aware):** Replicas distributed across explicit fault domains.

**Decision**
#TODO: Document the decision.#

**Justification**

- **No Failure Domain Awareness (Single Zone):** Simpler deployment for environments that truly lack physical redundancy (e.g., a single server room). No protection against rack/zone failure.
- **Topology-Aware Distribution (Multi-AZ / Rack-Aware):** **Mandatory for Production HA.** Ensures that 3 replicas of data land in 3 distinct physical locations (e.g., 3 AWS AZs, 3 OpenStack AZs, or 3 Bare Metal Racks).

**Implications**

- **Topology-Aware Distribution:** Requires at least 3 distinct failure domains (3 Racks, 3 Zones). Requires nodes to be correctly labeled (`topology.kubernetes.io/zone`).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## ODF-06

**Title**
Cluster-Wide Encryption Strategy

**Architectural Question**
Will cluster-wide encryption (encryption-at-rest) be enabled for all ODF-managed drives?

**Issue or Problem**
Security compliance often requires data at rest to be encrypted. ODF can enforce this at the OSD level, ensuring that even if a physical disk is removed (or a cloud volume detached), the data is unreadable.

**Assumption**
N/A

**Alternatives**

- **Encryption Enabled:** All OSDs encrypted.
- **Encryption Disabled:** No encryption at the ODF level.

**Decision**
#TODO: Document the decision.#

**Justification**

- **Encryption Enabled:** Critical for physical security (Bare Metal) and compliance (Cloud). Adds a layer of defense independent of the underlying infrastructure. Can utilize internal keys or an external KMS (HashiCorp Vault/Thales).
- **Encryption Disabled:** Removes CPU overhead of encryption. Relies entirely on the underlying storage (e.g., SAN encryption) for protection.

**Implications**

- **Encryption Enabled:** Small CPU overhead. If using external KMS, creates a dependency on the KMS availability for the storage cluster to start.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Storage Expert

---

## ODF-07

**Title**
Disaster Recovery (DR) Strategy

**Architectural Question**
What Disaster Recovery strategy will ODF implement to protect data across geographic sites?

**Issue or Problem**
Standard ODF replicates data within a cluster (usually one site/region). Surviving a total site failure requires cross-cluster replication.

**Assumption**
Multi-site requirement exists.

**Alternatives**

- **No Storage DR (Local Resilience Only):** Relies on backup/restore.
- **Regional-DR (Async Replication):** Asynchronous replication between two clusters in different regions.
- **Metro-DR (Sync Replication):** Synchronous replication between two clusters with low latency (<10ms).

**Decision**
#TODO: Document the decision.#

**Justification**

- **No Storage DR:** Sufficient if RPO/RTO targets allow for restoration from backups.
- **Regional-DR (Async):** Protects against regional disasters. Higher RPO (seconds/minutes) but tolerates high latency. Uses **Advanced Cluster Management (ACM)** to orchestrate failover.
- **Metro-DR (Sync):** Zero RPO (no data loss). Requires expensive, low-latency networking.

**Implications**

- **Regional/Metro DR:** Requires **Advanced Cluster Management (ACM)** and **Advanced Data Protection** subscription.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## ODF-08

**Title**
Object Storage Architecture (MCG)

**Architectural Question**
Will the Multicloud Object Gateway (MCG/NooBaa) be deployed, and if so, how will its backing database be architected?

**Issue or Problem**
MCG provides S3-compatible storage. It relies on a PostgreSQL database for metadata. For production scale, the default internal database may be a bottleneck.

**Assumption**
Object Storage is required.

**Alternatives**

- **No Object Storage:** ODF Block/File only.
- **MCG with Internal Database:** Default deployment.
- **MCG with External Database:** Connects to an external HA PostgreSQL.

**Decision**
#TODO: Document the decision.#

**Justification**

- **MCG with Internal Database:** Simple, self-contained. Good for standard workloads.
- **MCG with External Database:** Essential for massive object counts (billions of objects). Decouples metadata performance from the ODF cluster pods.

**Implications**

- **MCG:** Provides S3 access and federation (mirroring data to AWS S3/Azure Blob).
- **External DB:** Increases operational complexity (managing an HA Postgres cluster).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## ODF-09

**Title**
Storage Class Design

**Architectural Question**
What specific `StorageClasses` will be created to expose ODF's capabilities (File, Block, Object) to different types of workloads?

**Issue or Problem**
A clear strategy for defining `StorageClasses` is needed to provide users with self-service access to the correct type of storage. Without this, users might use inappropriate storage for their applications.

**Assumption**
ODF is deployed.

**Alternatives**

- **Default Classes Only:** Rely solely on the default `StorageClasses`.
- **Role-Based Storage Classes:** Create specific `StorageClasses` for different workload profiles (e.g., `odf-rwx-files-gold`, `odf-rwo-block-bronze`).

**Decision**
#TODO: Document the decision.#

**Justification**

- **Default Classes Only:** Simplifies administration but offers no granularity.
- **Role-Based Storage Classes:** The recommended approach. Allows the platform team to abstract complexity and offer a tiered catalog of storage services (e.g., guiding databases to Block and shared webservices to File).

**Implications**

- **Role-Based:** Requires the platform team to define and manage these classes.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert
