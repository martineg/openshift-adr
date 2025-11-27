# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - OpenStack platform installation specificities

## OCP-OSP-01

**Title**
OCP installation method on OSP infrastructure

**Architectural Question**
Which OCP installation method will be used to deploy a cluster on OpenStack infrastructure?

**Issue or Problem**
The choice of installation method for OpenStack impacts the level of automation and integration with OpenStack services like Neutron, Cinder, and Nova.

**Assumption**
N/A

**Alternatives**

- User-Provisioned Infrastructure (UPI)
- Installer-Provisioned Infrastructure (IPI)

**Decision**
#TODO: Document the decision for the OpenStack cluster.#

**Justification**

- **User-Provisioned Infrastructure (UPI):** The user manually provisions the necessary OpenStack resources (VMs, networks, load balancers, security groups) before using the installer to deploy OpenShift. Provides maximum customization.
- **Installer-Provisioned Infrastructure (IPI):** Recommended for maximum integration. The OpenShift installer automatically provisions and manages the cluster infrastructure within OpenStack, leveraging Nova, Neutron, and Cinder APIs.

**Implications**

- **User-Provisioned Infrastructure (UPI):** High administrative overhead for setup and Day 2 scaling. Customization benefits must outweigh ongoing management complexity.
- **Installer-Provisioned Infrastructure (IPI):** Simplifies installation and uses the Machine API for dynamic scaling and lifecycle management of nodes. Requires comprehensive OpenStack credentials with provisioning permissions.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-OSP-02

**Title**
Cloud Credential Management Strategy

**Architectural Question**
How will the OpenShift Cloud Credential Operator (CCO) manage authentication with the OpenStack Identity (Keystone) service?

**Issue or Problem**
OpenShift components need to authenticate with OpenStack to provision resources (machines, volumes, load balancers). The credential mode impacts the security posture (least privilege) and operational complexity of credential rotation.

**Assumption**
Cluster installation method is Installer-Provisioned Infrastructure (IPI).

**Alternatives**

- **Mint Mode (Default):** The CCO uses a high-privileged admin credential to dynamically create ("mint") short-lived, scoped application credentials for each component.
- **Passthrough Mode:** The CCO passes the provided `clouds.yaml` credentials directly to all components.
- **Manual Mode:** The administrator manually creates and manages application credentials for each component secrets.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Mint Mode:** Recommended for security. Ensures least privilege by creating granular, revocable credentials for each operator (e.g., Ingress, Storage) automatically. Requires the initial install user to have permission to create Application Credentials.
- **Passthrough Mode:** Simplest configuration but least secure. All cluster components share the same high-privileged credential. If that credential is compromised, the entire OpenStack project is vulnerable.
- **Manual Mode:** Required for high-security environments where the installer is not allowed to create credentials dynamically. High operational overhead.

**Implications**

- **Mint Mode:** Requires the OpenStack user to have a role permitting `application_credential_create`.
- **Passthrough Mode:** Credential rotation is difficult (must update cluster secrets manually).
- **Manual Mode:** Credentials do not rotate automatically; operational burden to manage lifecycle.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-OSP-03

**Title**
OpenStack Project Tenancy

**Architectural Question**
How will the OpenShift cluster resources be isolated within the OpenStack platform?

**Issue or Problem**
The OpenShift cluster (control plane, compute nodes) will consume OpenStack resources (VMs, volumes, networks, ports). A decision must be made on how to isolate these resources from other tenants and projects within OpenStack.

**Assumption**
N/A

**Alternatives**

- Single OpenStack Project
- Dedicated OpenStack Project per Cluster

**Decision**
#TODO: Document the decision for the OpenStack cluster.#

**Justification**

- **Single OpenStack Project:** To co-locate the OpenShift cluster resources within an existing, shared OpenStack project. This may be done to share quotas or network resources with other (non-OCP) applications.
- **Dedicated OpenStack Project per Cluster:** To create a new, dedicated OpenStack project for each OpenShift cluster (e.g., ocp-prod-project, ocp-nonprod-project). This is the recommended approach for isolation.

**Implications**

- **Single OpenStack Project:** Requires careful management of OpenStack quotas (vCPU, RAM, Cinder volumes) to prevent the OCP cluster from consuming all resources or being starved by "noisy neighbors" in the same project.
- **Dedicated OpenStack Project per Cluster:** Provides a clear boundary for security, quota management, and chargeback. It ensures the OpenShift cluster's resources are managed independently, which is critical for production stability.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-OSP-04

**Title**
Primary Network Interface Topology

**Architectural Question**
Will the OpenShift cluster nodes attach to a self-service Tenant Network (VXLAN/Geneve) or a pre-provisioned Provider Network (VLAN/Flat)?

**Issue or Problem**
The choice of primary network dictates the cluster's integration with the datacenter network, performance characteristics (double encapsulation), and requirements for Floating IPs.

**Assumption**
N/A

**Alternatives**

- **Tenant Network (Self-Service/Overlay):** OpenShift creates its own isolated network within the OpenStack project.
- **Provider Network (Bridged/Underlay):** OpenShift nodes attach directly to a datacenter network managed by OpenStack administrators.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Tenant Network:** Provides isolation and self-service. Does not require pre-configuration by network admins. Traffic is encapsulated (VXLAN), which may incur a performance penalty and requires Floating IPs for external access.
- **Provider Network:** Delivers higher performance (no double encapsulation) and simpler routing (nodes get "real" datacenter IPs). Reduces dependency on OpenStack Neutron virtual routers.

**Implications**

- **Tenant Network:** Mandatory if using IPI defaults in many environments. Requires Floating IPs for API/Ingress accessibility.
- **Provider Network:** Requires the OpenStack admin to pre-create the network and share it with the OCP project. Eliminates the need for Floating IPs if the provider network is routable.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-OSP-05

**Title**
API and Ingress Access Strategy

**Architectural Question**
How will the OpenShift API and Ingress endpoints be exposed to external clients?

**Issue or Problem**
Users and external systems need to reach the cluster. On OpenStack, this often requires bridging the gap between the internal cluster network and the external world.

**Assumption**
N/A

**Alternatives**

- **Floating IP Addresses (FIP):** Assign public/routable Floating IPs to the API and Ingress Load Balancers.
- **Internal-Only Access (No FIP):** Cluster is accessible only from within the OpenStack network fabric (or via VPN/Direct Connect).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Floating IP Addresses:** Standard cloud pattern. Allows access from outside the OpenStack environment. Required if using Tenant Networks without VPNs.
- **Internal-Only Access:** Enhances security by keeping the cluster private. Suitable if the OpenStack environment is already on a routable corporate network or if using Provider Networks.

**Implications**

- **Floating IP Addresses:** Consumes limited Floating IP quota from OpenStack.
- **Internal-Only Access:** Requires clients (administrators, CI/CD) to have network reachability to the internal OpenStack network.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Security Expert

---

## OCP-OSP-06

**Title**
OpenStack Load Balancer Provider Selection

**Architectural Question**
Which OpenStack Octavia load balancer provider/driver will be used to back the OpenShift Service Load Balancers?

**Issue or Problem**
OpenShift requests Load Balancers from OpenStack Octavia. The choice of backing driver impacts performance, latency, and resource usage (VM sprawl).

**Assumption**
Cluster uses Installer-Provisioned Infrastructure (IPI) or Cloud Controller Manager.

**Alternatives**

- **Amphora Provider (Default):** Spawns a dedicated VM for each Load Balancer.
- **OVN Provider (High Performance):** Implements Load Balancing flows directly in the OVN SDN control plane.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Amphora Provider:** Mature, standard reference driver. Isolates load balancers in VMs. Can lead to significant resource consumption (1 VM per Service type=LoadBalancer) and slower provisioning.
- **OVN Provider:** Highly recommended for performance and density. No extra VMs required; LB is handled by OVS flows on the compute nodes. Significantly faster provisioning and lower latency.

**Implications**

- **Amphora Provider:** High resource overhead (CPU/RAM for Amphora VMs). Slower scale-up.
- **OVN Provider:** Requires the underlying OpenStack cloud to be running OVN networking. May have fewer advanced L7 features than full HAProxy-based Amphora (though usually sufficient for L4).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-OSP-07

**Title**
OpenStack Storage Integration

**Architectural Question**
How will OpenShift integrate with OpenStack's storage services (Cinder and Manila) for application persistent volumes?

**Issue or Problem**
The cluster needs to integrate with the OpenStack cloud provider to provision persistent storage for applications. This requires configuring OCP to communicate with the correct Cinder (block) and/or Manila (file) backends using their respective CSI drivers. This decision is separate from any ODF deployment.

**Assumption**
Applications requiring persistent storage will be deployed. The OpenStack environment has Cinder and potentially Manila services available.

**Alternatives**

- Cinder CSI Driver (Block Storage)
- Manila CSI Driver (File Storage)
- Both Cinder and Manila CSI Drivers

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Cinder CSI Driver (Block Storage):** To provide persistent block storage (RWO - ReadWriteOnce access mode) suitable for databases and single-pod consumer workloads. This is the most common integration.
- **Manila CSI Driver (File Storage):** To provide shared, distributed file storage (RWX - ReadWriteMany access mode) suitable for multi-pod consumer workloads requiring shared filesystem access (e.g., collaborative tools, web content).
- **Both Cinder and Manila CSI Drivers:** To offer a comprehensive range of native OpenStack storage solutions, supporting applications requiring both dedicated block storage and shared file capabilities.

**Implications**

- **Cinder CSI Driver:** Provisioning is restricted to ReadWriteOnce access mode. Requires careful selection and configuration of Cinder volume types within OpenStack to meet desired performance characteristics (e.g., SSD vs. HDD backing).
- **Manila CSI Driver:** Requires a fully configured, available, and performant Manila service backend within the OpenStack environment. Performance and reliability depend entirely on the Manila share provider configuration.
- **Both Cinder and Manila CSI Drivers:** Increases the number of storage options available but also requires managing the installation and lifecycle of two distinct CSI driver operators within OpenShift.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-OSP-08

**Title**
Control Plane Root Volume Strategy

**Architectural Question**
Should the Control Plane nodes boot from persistent Cinder volumes or ephemeral local disks?

**Issue or Problem**
Control Plane nodes are critical stateful workloads (etcd). Booting from network-attached storage (Cinder) offers flexibility but introduces latency dependency. Booting from local disk (Ephemeral) offers performance but ties the node to the hypervisor.

**Assumption**
OpenStack Compute flavors support the chosen method.

**Alternatives**

- **Cinder Root Volume:** Nodes boot from a persistent volume managed by Cinder.
- **Ephemeral Local Disk:** Nodes boot from the disk space local to the Nova Compute hypervisor.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Cinder Root Volume:** Allows for larger root disks than the Flavor might define. Supports features like volume snapshots or booting from specific storage backends (e.g., Ceph).
- **Ephemeral Local Disk:** Generally provides better I/O performance (if hypervisor has local SSDs) by avoiding network hops. Simpler, "cloud-native" immutable node pattern.

**Implications**

- **Cinder Root Volume:** Etcd performance is strictly bound by the Cinder backend latency. **Must use a high-performance Cinder type** (latency < 10ms) to prevent etcd instability.
- **Ephemeral Local Disk:** Data is lost if the instance is deleted (not an issue for IPI as it reprovisions). Performance depends on local hypervisor disk.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---
