# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Storage

## OCP-STOR-01

**Title**
Storage provider

**Architectural Question**
Which storage provider will be deployed in each cluster for persistent application data?

**Issue or Problem**
A storage provider must be selected to meet the persistence, performance, and access mode requirements (e.g., ReadWriteMany, RWX) of stateful applications.

**Assumption**
N/A

**Alternatives**

- Platform-Native Storage
- OpenShift Data Foundation (ODF)
- Third-Party CSI Storage

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Platform-Native Storage:** Leverages integrated cloud storage (e.g., AWS EBS, Azure Disk, GCP PD) or basic on-premise PV types (e.g., Local Volume, HostPath). Reduces complexity but relies solely on the underlying platform's features.
- **OpenShift Data Foundation (ODF):** Provides a unified, software-defined storage layer backed by Red Hat Ceph Storage (Block/File) and NooBaa (Object). Provides advanced features like ReadWriteMany (RWX) access, replication, encryption, and multi-AZ resilience.
- **Third-Party CSI Storage:** Allows integration with existing enterprise storage solutions via a vendor-provided Container Storage Interface (CSI) driver. This utilizes existing hardware investments.

**Implications**

- **Platform-Native Storage:** Storage features and access modes (especially ReadWriteMany [RWX]) are dependent on the capabilities of the underlying platform's storage. Many native options only support ReadWriteOnce (RWO).
- **OpenShift Data Foundation (ODF):** **Requires a separate subscription and dedicated resources**. It is the preferred option for HA scaled registries and provides maximum resilience via Multi-AZ deployment. ODF is necessary when File (CephFS) or Object (MCG) storage capabilities are required.
- **Third-Party CSI Storage:** The organization is dependent on the vendor for the quality and support of the Container Storage Interface (CSI) driver.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert

---

## OCP-STOR-02

**Title**
Default Storage Class Strategy

**Architectural Question**
Which storage class will be designated as the default for the cluster, and will implicit dynamic provisioning be allowed?

**Issue or Problem**
Users creating PersistentVolumeClaims (PVCs) without specifying a `storageClassName` rely on the cluster default. If no default is set, provisioning fails. If the wrong default is set (e.g., expensive high-IOPS storage), costs may spiral.

**Assumption**
Storage Provider (OCP-STOR-01) has been selected.

**Alternatives**

- **Explicit Default Storage Class:** One class is marked `is-default-class: true`.
- **No Default Storage Class:** Users must explicitly specify a class in every PVC.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Explicit Default:** Simplifies developer experience. Standardizes storage consumption (e.g., "Standard-GP3").
- **No Default:** Enforces intentionality. Prevents accidental provisioning of storage. Useful for multi-tenant clusters with strict billing.

**Implications**

- **Explicit Default:** Easy to use. Risk of "silent" cost accumulation.
- **No Default:** Higher friction for developers; Helm charts/Operators assuming a default may fail.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert

---

## OCP-STOR-03

**Title**
Local Storage Management Strategy

**Architectural Question**
How will local disks on nodes be managed and provisioned for applications requiring local persistence?

**Issue or Problem**
Some workloads (databases, caches, ODF) require direct access to local disks. OpenShift offers two distinct operators for this.

**Assumption**
Cluster has nodes with available local disks.

**Alternatives**

- **Local Storage Operator (LSO):** Traditional block/file access. Static provisioning.
- **LVM Storage (LVMS):** Dynamic provisioning via LVM.
- **No Local Storage:** Only network storage is used.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **LSO:** Stable, widely used. Maps physical disks directly to PVs 1:1. Best for ODF backing store.
- **LVMS:** Flexible. Creates Logical Volumes (LVs) from a Volume Group. Allows sharing one disk across multiple PVs. Better for edge/SNO.
- **No Local Storage:** Simplifies node management (stateless nodes).

**Implications**

- **LSO:** Rigid. Expanding storage means adding physical disks.
- **LVMS:** Dynamic. Supports snapshots and resizing (within disk limits).
- **No Local Storage:** High dependency on network storage availability.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-STOR-04

**Title**
Encryption at Rest for Persistent Volumes (KMS)

**Architectural Question**
Will persistent volumes be encrypted using the cloud provider's default keys or customer-managed keys (KMS)?

**Issue or Problem**
Data sovereignty and compliance often mandate that the customer controls the encryption keys (BYOK), rather than relying on the cloud provider's managed keys.

**Assumption**
Storage Provider supports encryption (e.g., AWS EBS, Azure Disk, ODF).

**Alternatives**

- **Platform-Managed Keys (Default):** Keys managed by AWS/Azure/Google.
- **Customer-Managed Keys (KMS/BYOK):** Keys managed by the customer via KMS integration.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Platform-Managed:** Setup is transparent. Zero operational overhead. Sufficient for general data.
- **Customer-Managed:** Required for high-compliance data (PCI/HIPAA). Allows cryptographic erasure (shredding keys) and independent audit trails.

**Implications**

- **Platform-Managed:** Customer cannot independently revoke access to data if the cloud account is compromised.
- **Customer-Managed:** High complexity. Configuring StorageClass with KMS Key IDs. Risk of data loss if KMS keys are deleted or inaccessible.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-STOR-05

**Title**
Volume Snapshot Enablement

**Architectural Question**
Will the Volume Snapshot capability be enabled and exposed to users?

**Issue or Problem**
Snapshots provide point-in-time copies of data. Enabling them requires installing the Snapshot Controller and ensuring the CSI driver supports it.

**Assumption**
CSI Driver supports snapshots.

**Alternatives**

- **Snapshots Enabled:** Snapshot Controller installed; `VolumeSnapshotClass` defined.
- **Snapshots Disabled:** Feature not made available.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Enabled:** Enables backup workflows (OADP/Velero), cloning for dev/test, and quick recovery.
- **Disabled:** Reduces API surface area. Prevents users from consuming storage quota via hidden snapshots.

**Implications**

- **Enabled:** Need to manage snapshot quotas. Snapshots consume backend storage space.
- **Disabled:** Backup solutions must rely on filesystem-level copy (Restic/Kopia), which is slower and more resource-intensive.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-STOR-06

**Title**
Volume Expansion Policy

**Architectural Question**
Should `allowVolumeExpansion` be enabled on StorageClasses to permit online resizing of PVCs?

**Issue or Problem**
Applications often outgrow their initial storage requests. Resizing can be seamless (online expansion) or disruptive.

**Assumption**
CSI Driver supports expansion.

**Alternatives**

- **Expansion Enabled:** `allowVolumeExpansion: true`.
- **Expansion Disabled:** PVCs are immutable in size.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Enabled:** Allows "Day 2" growth without downtime or manual migration. Critical for databases.
- **Disabled:** Enforces strict capacity planning. Prevents runaway storage consumption.

**Implications**

- **Enabled:** Users can increase (but never decrease) volume size. Filesystem expansion happens automatically on the node.
- **Disabled:** To grow a volume, the user must create a new larger PVC, migrate data, and cut over. High operational toil.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-STOR-07

**Title**
Large Volume Permission Optimization Strategy

**Architectural Question**
Will `fsGroupChangePolicy` be set to `OnRootMismatch` to optimize pod startup times for large volumes?

**Issue or Problem**
By default, Kubernetes recursively `chown`s all files in a volume to the Pod's `fsGroup` on every startup. For large volumes (TB+ with millions of files), this causes massive delays (minutes/hours) where the pod is stuck in `ContainerCreating`.

**Assumption**
Workloads use `fsGroup` security contexts.

**Alternatives**

- **Always (Default):** Recursive permission change on every mount.
- **OnRootMismatch (Optimized):** Only change permissions if the root directory permissions do not match.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Always:** Ensures absolute consistency of file permissions. Safe but slow.
- **OnRootMismatch:** Drastically reduces startup latency for large volumes. Skips unnecessary permission updates.

**Implications**

- **Always:** Timeout risks for large databases/datasets.
- **OnRootMismatch:** If files _inside_ the volume have incorrect permissions but the root is correct, the pod may fail to read them. Requires trusting the initial state.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner

---
