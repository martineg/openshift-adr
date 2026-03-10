# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Hosted Control Planes (HCP)

## OCP-HCP-01

**Title**
Management Cluster Hosting Platform

**Architectural Question**
On which infrastructure platform will the Management Cluster—responsible for hosting the control planes of the Hosted Clusters—be deployed?

**Issue or Problem**
The choice of the underlying platform for the Management Cluster dictates the capabilities, isolation models, and storage/networking prerequisites for the Hosted Control Planes. It determines whether the control planes run as standard pods (Cloud) or KubeVirt VMs (Bare Metal/OpenStack).

**Assumption**
**Cluster Topology** is set to Hosted Control Planes (HCP).

**Alternatives**

- **Public Cloud (AWS):** Control planes run as standard pods on AWS infrastructure.
- **Bare Metal / On-Premise (KubeVirt):** Control planes run as pods (or VMs for isolation) on physical nodes using OpenShift Virtualization.
- **OpenStack:** Control planes run on OpenStack instances.

**Decision**
#TODO: Document the decision for the Management Cluster.#

**Justification**

- **Public Cloud (AWS):** Simplifies the architecture by leveraging native cloud load balancers and storage. Ideal for reducing the footprint of the control plane in cloud environments.
- **Bare Metal / On-Premise (KubeVirt):** Enables the "HyperShift" model on-premise. Maximizes density by stacking multiple control planes on physical hardware. Requires **OpenShift Virtualization** to be enabled on the Management Cluster to host the control plane workloads effectively.
- **OpenStack:** Integrates with OpenStack tenancy models, allowing the Management Cluster to vend clusters to different OpenStack projects.

**Implications**

- **Public Cloud (AWS):** Requires AWS credentials and potentially PrivateLink configuration for secure API access.
- **Bare Metal / On-Premise (KubeVirt):** The Management Cluster must be sized significantly larger to handle the compute/memory pressure of multiple etcd and API server instances. Requires robust storage performance (IOPS) on the Management Cluster to prevent etcd latency.
- **OpenStack:** Dependent on OpenStack Octavia (Load Balancing) and Cinder (Storage) performance.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-HCP-02

**Title**
Control Plane Availability Policy

**Architectural Question**
What level of high availability (HA) will be configured for the hosted control plane components (specifically etcd and API server)?

**Issue or Problem**
Unlike standalone OpenShift (which defaults to 3 control plane nodes), Hosted Control Planes allow for "Single Replica" deployments. A decision is needed to balance cost/resource consumption against Service Level Agreements (SLAs).

**Assumption**
N/A

**Alternatives**

- **Highly Available (3 Replicas):** Standard configuration for production.
- **Single Replica (Dev/Test):** Minimal footprint for non-production.

**Decision**
#TODO: Document the decision for each Hosted Cluster.#

**Justification**

- **Highly Available (3 Replicas):** Ensures the control plane can survive the failure of a pod, node, or availability zone (if configured) within the Management Cluster. Mandatory for production SLAs.
- **Single Replica (Dev/Test):** Significantly reduces the resource cost of the control plane (1/3rd the compute/storage). Ideal for ephemeral clusters, sandbox environments, or edge sites where control plane uptime is not critical.

**Implications**

- **Highly Available (3 Replicas):** Consumes 3x compute and storage resources on the Management Cluster per hosted cluster. Requires inter-pod anti-affinity rules to ensure replicas land on different management nodes.
- **Single Replica (Dev/Test):** **Zero redundancy.** If the management node hosting the control plane pod fails or is patched, the hosted cluster's API becomes unavailable (though worker nodes/workloads may continue running headless).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-HCP-03

**Title**
Management Cluster Multi-Tenancy and Isolation Strategy

**Architectural Question**
How will hosted control planes be isolated from each other within the shared Management Cluster to prevent "noisy neighbor" issues or security breaches?

**Issue or Problem**
The Management Cluster is a shared resource. Without explicit isolation, a busy control plane (high API churn) could starve others of CPU/Network, or a compromised control plane could theoretically attack peers.

**Assumption**
Multiple Hosted Clusters will run on the same Management Cluster.

**Alternatives**

- **Soft Isolation (Namespace Only):** Control planes share the management nodes' compute pool.
- **Hard Isolation (Dedicated Nodes/Taints):** Control planes are pinned to specific dedicated nodes within the Management Cluster via `NodePool` labels and taints.

**Decision**
#TODO: Document the decision for the Management Cluster.#

**Justification**

- **Soft Isolation (Namespace Only):** Maximizes bin-packing efficiency. Kubernetes scheduler handles resource contention via Requests/Limits. Simplest to manage.
- **Hard Isolation (Dedicated Nodes/Taints):** Physically separates control planes (e.g., "Prod Control Planes" on Node Set A, "Dev Control Planes" on Node Set B). Prevents non-prod usage from impacting production API latency.

**Implications**

- **Soft Isolation:** Requires careful tuning of resource requests to prevent overcommitment. Security relies entirely on Namespace/NetworkPolicy boundaries.
- **Hard Isolation:** Increases hardware cost (potentially lower utilization). Reduces the "blast radius" of a node failure.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-HCP-04

**Title**
Service Publishing Strategy (API & Ingress)

**Architectural Question**
How will the Kubernetes API server and OAuth/Ingress services of the Hosted Cluster be exposed to clients (users and worker nodes) outside the Management Cluster?

**Issue or Problem**
Since the control plane runs as pods inside the Management Cluster, it does not have a native "Node IP" on the hosted network. Traffic must be routed from the outside world into these pods.

**Assumption**
**Management Cluster Hosting Platform** is defined.

**Alternatives**

- **LoadBalancer Service (Cloud/MetalLB):** Exposes services via a Layer 4 Load Balancer.
- **Route (Ingress):** Exposes services via the Management Cluster's Ingress Controller (SNI).
- **NodePort:** Exposes services via high ports on the Management nodes.

**Decision**
#TODO: Document the decision for each Hosted Cluster.#

**Justification**

- **LoadBalancer Service:** The standard, recommended approach for production. Provides a distinct, stable IP address (VIP) for the API server. Requires a cloud provider integration or **MetalLB Operator** on the Management Cluster.
- **Route (Ingress):** Cost-effective. multiplexes API traffic over port 443 using SNI (Server Name Indication). Good for environments with limited IP addresses.
- **NodePort:** Fallback for bare metal environments without MetalLB. Not recommended for production due to high-port usage complexity.

**Implications**

- **LoadBalancer Service:** Consumes one LB/VIP per hosted cluster. Highest cost but best compatibility.
- **Route (Ingress):** API traffic shares bandwidth with the Management Cluster's ingress. Requires clients to support SNI (most modern clients do).
- **NodePort:** Requires clients to connect to non-standard ports (e.g., 30001). Firewall rules become complex.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-HCP-05

**Title**
Node Pool Update Strategy

**Architectural Question**
How will worker nodes in the Hosted Cluster (`NodePools`) be updated during an OpenShift version upgrade or configuration change?

**Issue or Problem**
HCP introduces `NodePools`, which allow for different lifecycle strategies compared to standard MachineSets. The update method impacts disruption budgets and the speed of rollouts.

**Assumption**
Hosted Cluster uses `NodePools` for worker management.

**Alternatives**

- **In-Place Upgrade:** The OS is updated on the running node (rpm-ostree). The node reboots.
- **Replace Upgrade (Rolling Replacement):** New nodes are provisioned with the new version; old nodes are drained and deleted.

**Decision**
#TODO: Document the decision for each Node Pool.#

**Justification**

- **In-Place Upgrade:** Conserves infrastructure resources (no surge capacity needed). Preferred for Bare Metal or static environments where provisioning new hardware is slow.
- **Replace Upgrade (Rolling Replacement):** Ensures immutability. "Cattle, not pets" approach. Preferred for Cloud environments where provisioning is fast. Ensures a clean slate for every upgrade.

**Implications**

- **In-Place Upgrade:** Slower if the delta is large. Risk of update failure leaving a node in a degraded state.
- **Replace Upgrade:** Requires "Surge" capacity (extra quota) to spin up new nodes before deleting old ones.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-HCP-06

**Title**
Etcd Storage Class Selection for Management Cluster

**Architectural Question**
Which specific StorageClass will be used to back the etcd volumes for the hosted control planes?

**Issue or Problem**
The performance of the hosted clusters is critically dependent on the I/O latency of the etcd volumes running on the Management Cluster. Using a generic/slow storage class will cause cascading instability across all hosted clusters.

**Assumption**
**Storage provider** has been selected for the Management Cluster.

**Alternatives**

- **Default/Generic Storage:** Uses the cluster default (e.g., standard cloud disk).
- **Dedicated High-Performance Storage:** Uses a class specifically tuned for low latency (e.g., `io2`, `premium-ssd`, `local-storage`).

**Decision**
#TODO: Document the decision for the Management Cluster.#

**Justification**

- **Default/Generic Storage:** Simplifies configuration. Risk of poor performance if the default is HDD or throttled cloud storage.
- **Dedicated High-Performance Storage:** Mandatory for production stability. Etcd requires extremely low latency (fsync < 10ms). Using local NVMe (via LSO/LVM) or high-IOPS cloud volumes ensures the control planes remain healthy under load.

**Implications**

- **Default/Generic Storage:** May lead to "etcd leader election lost" errors during high API load.
- **Dedicated High-Performance Storage:** May incur higher storage costs. If using Local Storage, binds the control plane pod to specific nodes, potentially complicating failover.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner
