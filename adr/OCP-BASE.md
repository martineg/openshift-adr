# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - General platform high level considerations

## OCP-BASE-01

**Title**
Environment Isolation Strategy

**Architectural Question**
How will workloads for different lifecycle stages (e.g., Dev, Test, Prod) be separated and hosted across OpenShift clusters?

**Issue or Problem**
Isolation is required for security, stability, and adherence to change control policies, balanced against the management overhead of multiple clusters.

**Assumption**
N/A

**Alternatives**

- Consolidated Cluster Model
- Prod/Non-Prod Split Model
- Per-Environment Model

**Decision**
#TODO: Document the decision.#

**Justification**

- **Consolidated Cluster Model:** Minimizes the infrastructure footprint and simplifies cluster management by consolidating all environments (Dev, Test, Prod) into a single operational cluster. This minimizes cost but requires reliance on OpenShift Namespaces/Projects, ResourceQuotas, NetworkPolicy, RBAC, Security Context Constraints (SCCs), and Pod Security Admission (PSA) for isolation. The inclusion of User Namespaces (TP) can further enhance workload isolation within this model.
- **Prod/Non-Prod Split Model:** Provides strong isolation between production and non-production workloads, preventing development or testing activities from impacting the production environment. This is often a minimum compliance requirement.
- **Per-Environment Model:** Offers maximum isolation between all environments (e.g., dev, test, UAT, prod), which is ideal for organizations with strict compliance, security, or change-control requirements for each stage, incurring maximum management overhead.

**Implications**

- **Consolidated Cluster Model:** Increased risk of resource contention ("noisy neighbors") and Single Point of Failure (SPoF) impacting all environments if a critical component or underlying infrastructure service fails.
- **Prod/Non-Prod Split Model:** Requires managing at least two separate clusters, increasing infrastructure and operational costs.
- **Per-Environment Model:** Highest operational overhead due to managing multiple, smaller clusters, but offers the clearest path to strict regulatory compliance and failure domain separation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-BASE-02

**Title**
Cloud model

**Architectural Question**
Which cloud operating model will be adopted for the OpenShift platform?

**Issue or Problem**
A cloud model must be selected that aligns with the organization's strategy for infrastructure ownership, operational expenditure (OpEx) versus capital expenditure (CapEx), scalability, and data governance.

**Assumption**
N/A

**Alternatives**

- Private Cloud Model
- Public Cloud Model
- Hybrid Cloud Model

**Decision**
#TODO: Document the decision.#

**Justification**

- **Private Cloud Model:** Leverages existing data center investments, provides maximum control over the hardware and network stack, and can help meet strict data sovereignty or residency requirements.
- **Public Cloud Model:** Offers rapid provisioning, on-demand scalability, a pay-as-you-go pricing model (OpEx), and offloads the management of physical infrastructure.
- **Hybrid Cloud Model:** Provides the flexibility to run workloads in the most suitable environment, balancing cost, performance, security, and features between private and public clouds.

**Implications**

- **Private Cloud Model:** The organization is fully responsible for infrastructure capacity planning, maintenance, power, cooling, and networking. Lead times for new hardware can be long. This is a CapEx-intensive model.
- **Public Cloud Model:** Incurs ongoing operational expenses tied to usage. It requires expertise in the specific cloud provider's services, security models, and cost management.
- **Hybrid Cloud Model:** Introduces complexity in network connectivity (e.g., VPN, Direct Connect) and management across different environments. Multi-cluster management tools are essential for a unified operational view.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-BASE-03

**Title**
Internet Connectivity Model

**Architectural Question**
Will the OpenShift cluster be deployed in an environment with direct internet access or a highly restricted (air-gapped) network?

**Issue or Problem**
The connectivity model dictates how installation files, container images, and cluster updates are sourced, impacting initial complexity and ongoing operational tooling. This decision must be made early, as it significantly constrains the choice of cluster topology and installation platform, as not all options fully support disconnected environments.

**Assumption**
N/A

**Alternatives**

- Connected (Direct Internet Access)
- Disconnected (Restricted/Air-Gapped Network)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Connected (Direct Internet Access):** Enables simplified installation and uses the OpenShift Update Service (OSUS) to provide over-the-air updates and update recommendations directly from Red Hat.
- **Disconnected (Restricted/Air-Gapped Network):** Required for environments with high security constraints or lack of external network access. Requires establishing a mirroring process to synchronize content from the public Red Hat repositories to a local registry.

**Implications**

- **Connected (Direct Internet Access):** Requires stable internet access for all nodes and adherence to firewall egress rules for Red Hat endpoints.
- **Disconnected (Restricted/Air-Gapped Network):** Significantly increases installation complexity and requires dedicated mirroring infrastructure. For hosted control planes, the ImageContentSourcePolicy (ICSP) for the data plane is managed via the ImageContentSources API.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BASE-04

**Title**
Fleet Management

**Architectural Question**
What strategic model will be used to manage the lifecycle (provisioning, upgrades, governance, and observability) of the OpenShift cluster fleet?

**Issue or Problem**
Managing clusters individually ("pets") leads to configuration drift, inconsistent security postures, and operational bottlenecks as the fleet grows. A strategy is needed to determine if clusters will be managed autonomously or via a unified, centralized control plane.

**Assumption**
N/A

**Alternatives**

- **Decentralized Management:** Each cluster is provisioned, upgraded, and configured independently using disparate tools (CLI, Jenkins, Ansible) and individual consoles.
- **Centralized Fleet Management (RHACM):** A hub-and-spoke architecture is used where a central "Hub" cluster (running Red Hat Advanced Cluster Management) orchestrates the lifecycle and governance of all "Spoke" clusters.

**Decision**
#TODO: Document the decision#

**Justification**

- **Decentralized Management:** Suitable only for very small, static environments where the overhead of a management hub is not justified.
- **Centralized Fleet Management (RHACM):** The strategic requirement for enterprise scale. It provides a single pane of glass for observability, a unified engine for policy-based governance (GRC), and enables advanced provisioning workflows (like GitOps ZTP) across all infrastructure providers.

**Implications**

- **Decentralized Management:** High operational overhead per cluster; auditing compliance across the fleet is manual and error-prone.
- **Centralized Fleet Management (RHACM):** Requires deploying and maintaining a dedicated Hub cluster. Establishes the dependency required for advanced automation patterns like GitOps Zero Touch Provisioning (ZTP) and Hosted Control Planes.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-05

**Title**
Platform Configuration & Deployment Engine Selection

**Architectural Question**
Which technology will be designated as the standardized, strategic engine for declarative configuration management (GitOps) and continuous delivery for the OpenShift platform?

**Issue or Problem**
A single, authoritative operational model must be chosen to manage cluster configuration drift, ensure consistency, and provide a verifiable audit trail for infrastructure changes. Relying on fragmented tooling (manual scripts, unmanaged YAMLs) leads to operational bottlenecks and inconsistency, regardless of whether managing a single cluster or a large fleet.

**Assumption**
Declarative infrastructure-as-code is the desired operating model.

**Alternatives**

- OpenShift GitOps (Argo CD) - Declarative Model
- Red Hat Ansible Automation Platform (AAP) / Imperative Model
- Manual / Scripting Tooling - Decentralized Control

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OpenShift GitOps (Argo CD) - Declarative Model:** Standardizes on a declarative, reconciliation-based model where Git is the single source of truth. It provides continuous drift detection and scales seamlessly from single-cluster management to full fleet automation (ZTP) when paired with a management hub.
- **Red Hat Ansible Automation Platform (AAP) / Imperative Model:** Best suited for imperative, "fire-and-forget" Day 2 operations or orchestrating dependencies external to the Kubernetes platform (e.g., hardware firewalls, legacy IT systems) that cannot be managed natively by Kubernetes Operators.
- **Manual / Scripting Tooling - Decentralized Control:** Low-overhead approach suitable only for transient PoCs where audit trails, consistency, and automated drift remediation are not required.

**Implications**

- **OpenShift GitOps (Argo CD) - Declarative Model:** Mandates strict "Infrastructure-as-Code" discipline; all configurations must be committed to Git. It serves as the prerequisite engine for advanced fleet patterns (like PolicyGenerator and ZTP) while remaining fully functional for standalone cluster management.
- **Red Hat Ansible Automation Platform (AAP) / Imperative Model:** Configuration state is maintained in playbook execution history rather than the cluster, potentially leading to undetected drift. It is an excellent complementary tool for orchestration spanning non-Kubernetes systems.
- **Manual / Scripting Tooling - Decentralized Control:** Lacks scalability and native audit capabilities, creating significant technical debt and high operational overhead as the environment grows.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: DevOps Lead

---

## OCP-BASE-06

**Title**
Multiple site deployment mode.

**Architectural Question**
How will the OpenShift platform be deployed across multiple physical sites (data centers, regions) to meet high availability, disaster recovery, or geo-locality requirements?

**Issue or Problem**
Deploying a platform across multiple sites introduces significant complexity related to network latency, failure domains, and data replication. A clear strategy is required to balance the operational overhead against the business requirements for resilience and service availability, while adhering to Red Hat supportability guidelines.

**Assumption**
N/A

**Alternatives**

- Stretched Cluster Across Sites
- Multi-Cluster (Independent Cluster per Site)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Stretched Cluster Across Sites:** Deploys a **single OpenShift cluster** with control plane nodes distributed across multiple logical or physical locations. For OpenShift 4.x, this typically involves **exactly three control plane nodes**, with the Red Hat recommendation being one node in each of **three sites**. This allows the cluster to maintain quorum and remain operational if one site fails. However, Red Hat warns this configuration extends the cluster as a **single failure domain** and should **not** be considered a replacement for a disaster recovery plan.
- **Multi-Cluster (Independent Cluster per Site):** Deploys a separate, independent OpenShift cluster in each site (e.g., one cluster per region/site). This is Red Hat's **strongly recommended** alternative to a stretched deployment. This model provides clear failure domain isolation. Tools like **Red Hat Advanced Cluster Management (ACM)** are then used to manage the clusters, application deployments, and disaster recovery policies from a single point of control.

**Implications**

- **Stretched Cluster Across Sites:**
  - **Strict Network Requirements:** The deployment is bound by etcd network performance. The combined disk and network latency and jitter must maintain an etcd peer round trip time of less than 100ms. Note that the etcd peer RTT is an end-to-end test metric distinct from network RTT. For the default 100ms heartbeat interval, the suggested RTT between control plane nodes is less than 33ms, with a maximum of less than 66ms.
  - **Layered Product Constraints:** Critically, layered products like storage (e.g., OpenShift Data Foundation) have _much_ lower latency requirements (e.g., < 10ms RTT) that will dictate the feasibility of the stretched model.
  - **Amplified Failure Scenarios:** This model has "additional inherent complexities" and "a higher number of points of failure". The organization **must** extensively test and document cluster behavior during network partitions, latency spikes, and jitter before production use.
- **Multi-Cluster (Independent Cluster per Site):**
  - **Recommended Practice:** This approach aligns with Red Hat's recommended practice and avoids the strict low-latency network requirements for the control plane.
  - **Failure Isolation:** Each cluster is an independent failure domain, preventing a network issue or outage in one site from impacting another site's cluster.
  - **Management Overhead:** Requires managing multiple independent clusters, though this is the intended use case for tools like Advanced Cluster Management (ACM).
  - **Application-Level DR:** Failover is not automatic at the cluster level. It must be managed at the application level (e.g., via ACM policies) and data level (e.g., using OpenShift API for Data Protection (OADP) and replication technologies like ODF Regional-DR).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-07

**Title**
Intra-Site Availability Zone / Failure Domain Strategy

**Architectural Question**
Within a single site or region, how will OpenShift cluster nodes (Control Plane, Compute) be distributed across available Availability Zones (AZs) or Failure Domains (FDs) for high availability?

**Issue or Problem**
Lack of distribution across failure domains can lead to a Single Point of Failure (SPoF) if a physical location, rack, or infrastructure zone experiences an outage, impacting the control plane (etcd) quorum and worker node availability.

**Assumption**
N/A

**Alternatives**

- Single AZ/FD Deployment (No HA)
- Three or More AZ/FD Deployment (Recommended HA for Standard/Compact)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Single AZ/FD Deployment (No HA):** Simplifies network planning and latency management since all nodes reside in one logical or physical area. However, this subjects the entire cluster to a site-wide or rack-level outage event.
- **Three or More AZ/FD Deployment (Recommended HA for Standard/Compact):** Provides maximum resilience by ensuring the control plane's etcd quorum members and worker nodes are distributed across physically isolated domains. This is the preferred approach for production clusters. The core mechanism relies on maintaining strict network latency requirements for etcd; specifically, the suggested Round-Trip Time (RTT) between control plane nodes is **less than 33 ms (with a maximum under 66 ms)** to ensure stability and avoid missed heartbeats.

**Implications**

- **Single AZ/FD Deployment (No HA):** Significantly increases the risk of a Single Point of Failure (SPoF) for OpenShift infrastructure services and the cluster state (etcd).
- **Three or More AZ/FD Deployment (Recommended HA for Standard/Compact):** Requires careful network design to manage inter-AZ latency. Requires that the underlying platform supports multiple availability zones/failure domains (FDs). This approach is necessary to ensure that High Availability workloads can be correctly distributed using node labels (e.g., `topology.kubernetes.io/zone`) as mandated by default TopologySpreadConstraint policies applied to replicated pods in OpenShift.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BASE-08

**Title**
Platform infrastructure

**Status: [MANUAL REVIEW REQUIRED]**

**Architectural Question**
On which specific infrastructure platform(s) will OpenShift Container Platform be installed?

**Issue or Problem**
The choice of underlying infrastructure platform directly impacts the available installation methods, supported features, operational complexity, performance characteristics, and required team skill sets. More than one platform can be selected.

**Assumption**
Cloud model has been selected.

**Alternatives**

- Self-Managed Public Cloud (AWS, Azure, GCP, OCI, IBM Cloud, Azure Stack Hub, ALIBABA Cloud)
- Bare Metal / On-Premise Virtualized (vSphere, RHOSP, Bare Metal, Nutanix, IBM Power, IBM Z/LinuxONE, External/None)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Self-Managed Public Cloud:** Supports Installer-Provisioned Infrastructure (IPI) on platforms including AWS, Azure, GCP, Azure Stack Hub, and IBM Cloud Classic/VPC. User-Provisioned Infrastructure (UPI) maximizes flexibility and is supported on AWS, Azure, GCP, OCI, Azure Stack Hub, and ALIBABA Cloud.
- **Bare Metal / On-Premise Virtualized:** Provides full hardware control. Supported IPI options include vSphere, RHOSP, Bare Metal, and Nutanix. UPI is supported on platforms including vSphere, RHOSP, Bare Metal, IBM Power®, IBM Z®/IBM® LinuxONE, and External/None.

**Implications**

- **Self-Managed Public Cloud:** IPI mode abstracts infrastructure management via the Machine API, simplifying cluster scaling and node lifecycle. Requires cloud credentials and IAM setup. UPI requires manual management of underlying resources and does not support the Machine API post-installation.
- **Bare Metal / On-Premise Virtualized:** For UPI deployment, administrators must manually manage all underlying infrastructure components. IPI and Assisted/Agent Installer automate provisioning of infrastructure. For Bare Metal IPI, core infrastructure resources (networking, load balancing, storage, bootstrap machine) must be provided by the user.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-09

**Title**
Cluster Topology

**Architectural Question**
What OpenShift topology should be deployed based on resource availability, HA requirements, and scale for each cluster?

**Issue or Problem**
Selecting the cluster topology determines the minimum node count, control plane resilience, resource usage efficiency, and suitability for specific use cases (e.g., edge). This choice impacts High Availability (HA) capabilities within a site and influences multi-site strategies.

**Assumption**
Platform infrastructure supports the chosen topology.

**Alternatives**

- Standard HA Topology (3+ Control Plane, N+ Workers)
- Compact HA Topology (3 Combined Control/Worker)
- Two-Node OpenShift with Arbiter (TNA)
- Two-Node OpenShift with Fencing (TP)
- Single Node OpenShift (SNO)
- Hosted Control Planes (HCP)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Standard HA Topology (3+ Control Plane, N+ Workers):** Provides maximum resilience, scalability, and separation of control plane functions from application workloads onto dedicated worker nodes. Recommended for large or general-purpose production clusters.
- **Compact HA Topology (3 Combined Control/Worker):** Reduces the hardware footprint and provides a smaller, more resource-efficient cluster. It is suitable for smaller production environments that require high availability, as the three control plane nodes are configured to be schedulable (running workloads).
- **Two-Node OpenShift with Arbiter (TNA):** A compact, cost-effective OpenShift Container Platform topology that provides high availability (HA). The topology uses two control plane nodes and a lightweight arbiter node to maintain etcd quorum and prevent split brain.
- **Two-Node OpenShift with Fencing (TP):** Designed for distributed or edge environments where deploying a full three-node cluster is impractical, providing HA with a reduced hardware footprint. Fencing, managed by Pacemaker, isolates unresponsive nodes so the remaining node can safely continue operation.
- **Single Node OpenShift (SNO):** Ideal for edge computing workloads, portable clouds, and environments with intermittent connectivity or severe resource constraints, such as 5G radio access networks (RAN).
- **Hosted Control Planes (HCP):** A feature that enables hosting the control plane as pods on a management cluster, optimizing infrastructure costs required for the control planes and improving cluster creation time. This model decouples the control plane from the data plane, providing resiliency.

**Implications**

- **Standard HA Topology:** Requires a minimum of three control plane machines and at least two compute machines. Requires maintaining separate physical hosts for the cluster machines to ensure high availability.
- **Compact HA Topology:** Infrastructure components (monitoring, registry, ingress) often share resources with the control plane, requiring careful sizing. If resource constraints exist, workload partitioning is strongly recommended.
- **Two-Node OpenShift with Arbiter (TNA):** Requires 2 control plane nodes and 1 arbiter node. The arbiter node must meet minimum system requirements.
- **Single Node OpenShift (SNO):** The major tradeoff is the **lack of high availability**, as failure of the single node stops the cluster. Requires a minimum of 8 vCPUs and 120GB of storage.
- **Hosted Control Planes (HCP):** The control plane runs in a single namespace on a management cluster. A Single-Node OpenShift cluster is explicitly not supported as a management cluster.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-10

**Title**
Control Plane Schedulability Configuration

**Architectural Question**
Should control plane nodes be configured to accept application workloads (be schedulable) by setting the `mastersSchedulable` parameter to true?

**Issue or Problem**
Configuring control plane nodes to accept application workloads increases resource utilization and efficiency for smaller clusters but requires explicitly overriding the default Kubernetes manifest configuration, potentially leading to additional subscription costs.

**Assumption**
Cluster topology is defined.

**Alternatives**

- Configure Control Plane Nodes as Schedulable
- Configure Control Plane Nodes as Unschedulable (Default)

**Decision**
#TODO: Document decision.#

**Justification**

- **Configure Control Plane Nodes as Schedulable:** This configuration is required for 3-node/Compact HA clusters to efficiently run application workloads. It maximizes the resource utilization of the control plane nodes.
- **Configure Control Plane Nodes as Unschedulable (Default):** This configuration ensures separation between critical platform components and user workloads, providing dedicated stability and resilience, which is typically recommended for large or Standard HA clusters. This relies on the default manifest setting of `mastersSchedulable: false`.

**Implications**

- **Configure Control Plane Nodes as Schedulable:** Additional subscriptions are required because configuring control plane nodes as schedulable causes them to be treated as compute nodes for licensing purposes. If the cluster has zero dedicated compute nodes, the application ingress load balancer must be configured to route HTTP/HTTPS traffic to the control plane nodes.
- **Configure Control Plane Nodes as Unschedulable (Default):** Requires the deployment of separate worker nodes for hosting application workloads (Standard HA topology).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-11

**Title**
Infrastructure nodes

**Architectural Question**
Should platform services (e.g., Ingress routers, internal image registry, monitoring, logging, etc.) be isolated onto a dedicated pool of nodes, or co-located with application workloads?

**Issue or Problem**
Platform services are critical for cluster operation and consume significant resources (CPU, memory, network I/O). Co-locating them with application workloads can lead to resource contention ("noisy neighbor" effect), impacting the stability of both the platform and the applications. However, creating dedicated nodes increases infrastructure cost and management overhead.

**Assumption**
Cluster has a standard HA topology.

**Alternatives**

- **Co-located on General Worker Nodes:** Platform services are deployed on the default worker pool alongside all other applications.
- **Dedicated Infrastructure Nodes:** A separate pool of worker nodes is created and reserved (using taints and labels) to run only platform services.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Co-located on General Worker Nodes:** This is the default behavior. It minimizes the number of required nodes and is simpler for small clusters or non-production environments where performance isolation is not a strict requirement.
- **Dedicated Infrastructure Nodes:** This is the recommended practice for production and large-scale clusters. It provides strong resource isolation, preventing application workloads from impacting critical platform services. It also simplifies resource management, licensing (e.g., not running OpenShift platform services on nodes licensed for specific software), and chargeback for application teams.

**Implications**

- **Co-located on General Worker Nodes:** Requires careful sizing of the general worker pool to account for both application and platform overhead. ResourceQuotas and LimitRanges are critical to prevent contention.
- **Dedicated Infrastructure Nodes:** Requires creating and managing a separate MachineSet (on platforms that support it) or a manually configured node pool. Platform operators (like ingress, registry, monitoring) must be configured to tolerate the `node-role.kubernetes.io/infra` taint and use node selectors to run on this pool. This requires at least two (preferably three) additional nodes for high availability.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-BASE-12

**Title**
Dedicated Infrastructure Node Count for HA

**Architectural Question**
What is the minimum required size (replica count) for the dedicated infrastructure node pool to ensure high availability of critical platform services (e.g., Ingress, Registry, Monitoring)?

**Issue or Problem**
The decision to isolate infrastructure services onto dedicated nodes requires defining the node count necessary to meet site-level High Availability (HA) requirements, balancing operational costs against service resilience.

**Assumption**
Dedicated Infrastructure Nodes strategy has been selected.

**Alternatives**

- 2 Dedicated Infrastructure Nodes
- 3 Dedicated Infrastructure Nodes

**Decision**
#TODO: Document decision.#

**Justification**

- **2 Dedicated Infrastructure Nodes:** Minimizes the additional infrastructure footprint and costs while still providing basic High Availability (HA) against a single node failure. This configuration requires at least two additional nodes for high availability.
- **3 Dedicated Infrastructure Nodes:** This is the preferred practice for production and large-scale clusters, providing maximum redundancy and aligning with the recommended count for control plane resilience, ensuring platform services can survive a single domain failure and allow maintenance with zero platform service interruption.

**Implications**

- **2 Dedicated Infrastructure Nodes:** This configuration requires careful planning. While providing basic HA, the cluster may experience performance degradation or instability during node maintenance or failure events, as the remaining node(s) must handle the full load.
- **3 Dedicated Infrastructure Nodes:** Highest infrastructure and operational overhead due to managing the additional machines, but offers strong resource isolation and fault tolerance.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## OCP-BASE-13

**Title**
Boot disks encryption

**Architectural Question**
Will the RHCOS boot disks be encrypted, and which key management mechanism will be used for automated unlocking upon node boot?

**Issue or Problem**
Servers often require full disk encryption (LUKS) for security compliance. A decision must be made on whether to encrypt, and if so, how to manage the decryption keys to allow for automated, unattended reboots.

**Assumption**
Platform infrastructure is vSphere or baremetal.

**Alternatives**

- No disk encryption (Default)
- TPM v2 Only Unlock
- Tang Server Only Unlock
- TPM v2 and Tang Server Combination

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No disk encryption (Default):** This is the default behavior. It simplifies installation and node provisioning, as no additional key management infrastructure (TPM, Tang) or configuration is required. It relies solely on physical data center security for data-at-rest protection.
- **TPM v2 Only Unlock:** This method uses the on-board TPM v2 chip to seal the decryption key. The key is only released if the boot measurements (PCRs) are correct, ensuring the system's boot chain has not been tampered with. This is a high-security, self-contained solution.
- **Tang Server Only Unlock:** This method uses a network-bound key release. The node fetches its decryption key from a highly available Tang server on the network during boot. This decouples the key from the hardware state, simplifying operational events like firmware updates.
- **TPM v2 and Tang Server Combination:** This is the most resilient automated method. The node can be configured to unlock if either the TPM measurements are correct or it can successfully contact the Tang server. This provides the security of TPM binding while adding the operational flexibility of Tang.

**Implications**

- **No disk encryption (Default):** Simplest and fastest provisioning. No external dependencies for boot. Fails to meet many security and compliance standards for data-at-rest encryption.
- **TPM v2 Only Unlock:** High security, as the key is bound to the hardware state. No external infrastructure (like Tang) is needed. Node recovery after expected changes (like a BIOS or firmware update) can be complex.
- **Tang Server Only Unlock:** Decouples the key from the hardware state (TPM PCRs), making firmware updates non-disruptive. Creates a hard dependency on the network and the Tang servers.
- **TPM v2 and Tang Server Combination:** Provides the "best of both worlds": high security (TPM) and operational flexibility (Tang).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BASE-14

**Title**
Mirrored images registry (Disconnected Environments)

**Architectural Question**
In a disconnected environment, which mirrored images registry solution will be used to provide required container images to the cluster?

**Issue or Problem**
In a disconnected environment, the cluster needs access to Red Hat software (release images, operators) via a local mirror registry for installation and updates.

**Assumption**
Environment is disconnected.

**Alternatives**

- Filesystem-based Mirror (using `oc mirror` or `oc adm release mirror`)
- Dedicated Mirror Registry Server (e.g., Quay, Nexus, Artifactory)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Filesystem-based Mirror:** Uses oc mirror (preferred) to create a simple mirror (filesystem or basic registry push). Minimum requirement for mirroring essential OCP software.
- **Dedicated Mirror Registry Server:** Leverages a full-featured registry (existing or new) as the single source for both mirrored Red Hat content and internal application images. This is the preferred enterprise approach.

**Implications**

- **Filesystem-based Mirror:** Primarily for Red Hat content, not a full registry (no UI, advanced RBAC, scanning unless paired). Simpler setup for core content, less suitable for applications. Requires manual sync.
- **Dedicated Mirror Registry Server:** Preferred enterprise approach. Requires ensuring the registry supports OCP content formats (Operator catalogs) and the mirroring process. Leverages existing HA, security, and management features.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BASE-15

**Title**
Hardware Acceleration Strategy

**Architectural Question**
Will the OpenShift platform be architected to support hardware acceleration (e.g., GPUs, TPUs, HPUs) for AI/ML, data science, or high-performance computing workloads?

**Issue or Problem**
Specialized workloads often require hardware acceleration to meet performance and latency requirements. Enabling this capability impacts hardware procurement, cluster sizing, operator management (e.g., NVIDIA GPU Operator), and scheduling strategies. A strategic decision is needed to prepare the infrastructure for these resources.

**Assumption**
N/A

**Alternatives**

- **General Purpose Compute Only:** Rely solely on standard CPU-based compute nodes.
- **Hardware Acceleration Enabled:** Architect the cluster to support and manage specialized accelerator hardware nodes.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **General Purpose Compute Only:** Simplifies hardware standardization and reduces cost. Suitable for general microservices, web applications, and lighter data processing tasks that do not require massive parallel processing.
- **Hardware Acceleration Enabled:** Essential for training deep learning models, large-scale inference, and heavy data processing tasks. Requires integrating specialized hardware (e.g., NVIDIA GPUs) and management operators.

**Implications**

- **General Purpose Compute Only:** Precludes running high-performance AI/ML models efficiently. May lead to extremely high CPU usage and poor performance for specific mathematical workloads.
- **Hardware Acceleration Enabled:** Increases infrastructure cost and complexity. Requires specific node labels, taints, and tolerations to ensure correct workload placement. Introduces dependencies on hardware vendors (e.g., NVIDIA, Intel, AMD).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-16

**Title**
Virtualization Strategy

**Architectural Question**
Will the OpenShift platform be configured to host Virtual Machines (VMs) alongside containerized workloads (Converged Infrastructure)?

**Issue or Problem**
Many organizations have legacy applications that cannot be immediately containerized but need to run in close proximity to modern cloud-native services. A decision is required on whether to manage VMs within OpenShift or rely on external hypervisors (vSphere, RHV).

**Assumption**
Platform Infrastructure supports virtualization (Bare Metal is preferred; Nested Virtualization is possible but performance-limited).

**Alternatives**

- **Containers Only (No Virtualization):** The platform hosts only containerized workloads. VMs remain on legacy hypervisors.
- **Converged Containers & VMs (OpenShift Virtualization):** The platform hosts both containers and VMs using KubeVirt technology.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Containers Only (No Virtualization):** Keeps the platform simple and focused on cloud-native patterns. Reduces the "noisy neighbor" risk of heavy VM monoliths affecting microservices.
- **Converged Containers & VMs (OpenShift Virtualization):** Enables infrastructure consolidation ("modernize in place"). Allows legacy VMs to share the same network/storage fabric as containers, reducing latency and operational silos. It is a prerequisite for running Windows Containers (via WMCO) or Hosted Control Planes (HCP) on Bare Metal.

**Implications**

- **Containers Only:** Requires maintaining separate legacy hypervisor infrastructure/licensing.
- **Converged Containers & VMs (OpenShift Virtualization):**
  - **Bare Metal** is strongly recommended for production performance.
  - Requires enabling the **OpenShift Virtualization Operator**.
  - Impacts **Storage** decisions (Block storage/RWX is often required for VM disks and Live Migration).
  - Impacts **Networking** (L2/Multus is often required for VMs to look like "real servers" on the network).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
