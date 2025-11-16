# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Specifics of baremetal installation

## OCP-BM-01

**Title**
OCP installation method on baremetal infrastructure

**Architectural Question**
Which OCP installation method will be used to deploy a cluster on baremetal infrastructure?

**Issue or Problem**
The choice of installation method for Bare Metal impacts the level of automation, network prerequisites (like PXE), and how the cluster interacts with the physical hardware.

**Assumption**
N/A

**Alternatives**

- User-Provisioned Infrastructure (UPI)
- Installer-Provisioned Infrastructure (IPI)
- Agent-based Installer (ABI)
- Assisted Installer
- Image-based Installer (IBI)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **User-Provisioned Infrastructure (UPI):** Requires the user to manually provision and configure all cluster infrastructure (including networking, DNS, load balancers, and storage) and install Red Hat Enterprise Linux CoreOS (RHCOS) on hosts using generated Ignition configuration files. This approach offers **maximum customizability**.
- **Installer-Provisioned Infrastructure (IPI):** Delegates the infrastructure bootstrapping and provisioning to the installation program. For bare metal, this process automates provisioning using the host’s Baseboard Management Controller (BMC) by leveraging the Bare Metal Operator (BMO) features.
- **Agent-based Installer (ABI):** Provides the convenience of the Assisted Installer but enables installation **locally for disconnected environments or restricted networks**. It uses a lightweight agent booted from a discovery ISO to facilitate provisioning.
- **Assisted Installer:** A web-based SaaS service designed for **connected networks** that simplifies deployment by providing a user-friendly interface, smart defaults, and pre-flight validations, generating a discovery image for the bare metal installation.
- **Image-based Installer (IBI):** Significantly reduces the deployment time of single-node OpenShift clusters by enabling the preinstallation of configured and validated instances on target hosts, supporting rapid reconfiguration and deployment even in disconnected environments.

**Implications**

- **User-Provisioned Infrastructure (UPI):** Implies the **highest operational overhead** because the user must manage and maintain all infrastructure resources (Load Balancers, Networking, Storage) throughout the cluster lifecycle. It requires additional validation and configuration to use the Machine API capabilities.
- **Installer-Provisioned Infrastructure (IPI):** Requires integration with the BMO and related provisioning infrastructure. For bare metal IPI, the user must provide all cluster infrastructure resources, including the bootstrap machine, networking, load balancing, storage, and individual cluster machines. Once installed, it allows OpenShift Container Platform to manage the operating system and supports using the Machine API for node lifecycle management.
- **Agent-based Installer (ABI):** Ideal for **disconnected environments** and provides features like integrated tools for configuring nodes (e.g., disk encryption or LVM storage configuration). Requires the user to provide all cluster infrastructure and resources (networking, load balancing, storage).
- **Assisted Installer:** Requires a working internet connection during the preparation phase (unless steps are followed for a disconnected approach). It simplifies deployment by handling Ignition configuration generation and supports **full integration for bare metal platforms**.
- **Image-based Installer (IBI):** Primarily intended for **Single-Node OpenShift (SNO) cluster deployments**, often managed using a hub-and-spoke architecture via Red Hat Advanced Cluster Management (RHACM) and the multicluster engine for Kubernetes Operator (MCE).

  **Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-02

**Title**
RHCOS Provisioning Method for Bare Metal Nodes

**Architectural Question**
How will Red Hat Enterprise Linux CoreOS (RHCOS) be provisioned onto the bare metal nodes?

**Issue or Problem**
The method chosen to boot and install RHCOS on physical hardware dictates the required network infrastructure (e.g., PXE services) and the level of manual effort (e.g., ISO mounting). This decision is a prerequisite for User-Provisioned method.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Install RHCOS using ISO (via Virtual Media or USB)
- Install RHCOS using PXE (Network Boot)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Install RHCOS using ISO:** This is straightforward for a small number of nodes. The administrator must manually provide the Ignition configuration file during installation.
- **Installer-Provisioned Infrastructure (IPI):** Enables fully automated, "zero-touch" provisioning for a large number of nodes.

**Implications**

- **Install RHCOS using ISO:** Requires minimal-to-no additional network infrastructure. High operational overhead. Requires manual intervention (or complex scripting) on every node's BMC for large-scale UPI deployments.
- **Installer-Provisioned Infrastructure (IPI):** Enables full, scalable, "zero-touch" provisioning, which is ideal for large-scale UPI deployments. Requires significant prerequisite infrastructure (DHCP, TFTP, Web servers) and network configuration (IP helpers, etc.), adding complexity.

  **Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-03

**Title**
RHCOS Day-1 Customization Method

**Architectural Question**
Which technique will be used to apply non-standard, Day-1 settings (like static networking, disk partitions, or console settings) during the UPI installation of RHCOS?

**Issue or Problem**
The default RHCOS installation setting is often insufficient for enterprise bare metal. We must apply custom configurations (e.g., static IP addresses, network bonds, custom disk partitions, or serial console settings) at installation time. The chosen method impacts automation, complexity, and maintainability.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Kernel Arguments
- `MachineConfig` via Ignition
- `coreos-installer` Live Shell

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Kernel Arguments:** This is a simple, direct method for passing basic boot settings. It is required for core parameters like static IP (`ip=...`) and the Ignition URL (`coreos.inst.ignition_url=`).
- **`MachineConfig` via Ignition:** This is the standard, declarative method for all complex OS configurations. `MachineConfig` manifests are placed in the `manifests/` directory and automatically bundled into the final Ignition files, making it ideal for managing partitions , files, or services (like custom NTP) as code.
- **`coreos-installer` Live Shell:** This is a manual, interactive method used for debugging or special cases. By booting the ISO or PXE image to a shell (by omitting `coreos.inst.install_dev`), an administrator can run coreos-installer with unique flags like `--copy-network` or `--save-part` label.

**Implications**

- **Kernel Arguments:** Works identically for both ISO and PXE. Becomes unmanageable, unreadable, and error-prone for anything beyond basic settings (e.g., complex bonding). Cannot be used for settings that lack a kernel argument (e.g., custom disk partitions).
- **`MachineConfig` via Ignition:** This is the most robust, scalable, and maintainable solution for UPI. It is idempotent and supports all configuration types. The configuration is version-controlled with the other install manifests. Adds one layer of abstraction (Manifest -> Ignition file) which requires understanding the installer workflow.
- **`coreos-installer` Live Shell:** Provides the only path for special flags like `--copy-network`. This is a **fully manual** process that breaks "zero-touch" automation. Scales very poorly and is only suitable for troubleshooting or provisioning single, non-standard nodes.

  **Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-04

**Title**
Hardware RAID Configuration for Bare Metal Installation Drive

**Architectural Question**
How should hardware RAID be configured for the OpenShift Container Platform installation drive on bare metal nodes, ensuring compatibility with supported BMCs and adhering to Red Hat requirements?

**Issue or Problem**
OpenShift Container Platform documentation explicitly supports using hardware RAID on the installation drive for nodes managed by specific BMCs, such as Dell iDRAC (firmware version 6.10.30.20 or later, RAID levels 0, 1, and 5) and Fujitsu iRMC (RAID levels 0, 1, 5, 6, and 10). However, **software RAID is not supported** on the installation drive. A decision is required on whether to utilize supported hardware RAID features or configure nodes without hardware RAID for the installation drive.

**Assumption**
BMCs (Baseboard Management Controllers) support hardware RAID volumes for the root installation drive.

**Alternatives**

- Configure and use supported Hardware RAID volumes for the installation drive.
- Configure the installation drive without using Hardware RAID.

**Justification**

- **Configure and use supported Hardware RAID volumes for the installation drive:** Leveraging hardware RAID provides disk redundancy and potential performance improvements managed entirely by the hardware controller/BMC interface, which is supported for specific configurations.
- **Configure the installation drive without using Hardware RAID:** This simplifies the underlying storage configuration and avoids potential compatibility issues, focusing solely on software volumes, although internal cluster components like etcd manage their own redundancy.

**Implications**

- **Configure and use supported Hardware RAID volumes for the installation drive:** Requires specifying the logical drives within the `hardwareRAIDVolumes` parameter of the installation configuration. Incorrect configuration or use with unsupported BMC versions or RAID levels may lead to unsupported clusters or installation failure.
- **Configure the installation drive without using Hardware RAID:** Node resiliency relies solely on the underlying physical disk health, which might not be desirable for critical bare metal components if a disk fails.

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BM-05

**Title**
Root File System Encryption and Automated Unlock Mechanism

**Architectural Question**
If disk encryption (LUKS) is required for the bare metal nodes, which key management mechanism will be used to enable automated unlocking of the RHCOS root volume upon node boot?

**Issue or Problem**
Bare metal servers often require full disk encryption for security compliance. Without an automated mechanism, nodes cannot reboot unattended, which inhibits automated maintenance and recovery features.

**Assumption**
LUKS encryption is configured for the RHCOS root file system on bare metal nodes.

**Alternatives**

- TPM v2 Only Unlock (Policy-Based Decryption) (TP)
- TPM v2 and Tang Server Combination (Policy-Based Decryption) (TP)

**Justification**

- **TPM v2 Only Unlock (Policy-Based Decryption) (TP):** This uses the Trusted Platform Module (TPM) chip on the host to seal the decryption key, ensuring the key is released only if the boot measurement is correct. This requires no external infrastructure dependency for unlocking.
- **TPM v2 and Tang Server Combination (Policy-Based Decryption) (TP):** This method uses a network-bound key release (Tang) in addition to TPM measurements, allowing recovery of the system even if the TPM measurements change (e.g., BIOS upgrade). The security threshold can be customized, requiring a subset of available Tang servers plus the local TPM to decrypt the root volume.

**Implications**

- **TPM v2 Only Unlock (Policy-Based Decryption):** Simplest configuration, but node recovery after expected changes (like firmware updates that break TPM measurements) may require manual intervention.
- **TPM v2 and Tang Server Combination (Policy-Based Decryption) (TP):** Requires deployment and maintenance of external Tang server infrastructure (highly available). Offers greater flexibility in node recovery and resilience against unintended TPM measurement changes.

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BM-06

**Title**
Bare Metal Node Remediation

**Architectural Question**
What is the strategy for automatically remediating unhealthy Bare Metal nodes?

**Issue or Problem**
A strategy is needed to automatically detect and recover failed physical nodes. This is critical for maintaining cluster health and HA for workloads, especially for stateful services that run directly on the nodes.

**Assumption**
N/A.

**Alternatives**

- No Automated Remediation
- Node Health Check (NHC) with Self Node Remediation
- Node Health Check (NHC) with BareMetal Operator (BMO) Remediation

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Automated Remediation:** To rely on manual detection (via monitoring) and manual intervention by an operator to troubleshoot and reboot physical nodes.
- **Node Health Check (NHC) with Self Node Remediation:** To deploy the Node Health Check operator, which monitors node health. When a node fails, the `SelfNodeRemediation` agent on other nodes will fence the unhealthy node and restart its workloads elsewhere.
- **Node Health Check (NHC) with BareMetal Operator (BMO) Remediation:** To use the NHC in combination with the BareMetal Operator (enabled by an IPI install). When NHC detects a failure, it triggers the BMO to power-cycle the node via its BMC, attempting a full hardware reboot.

**Implications**

- **No Automated Remediation:** High operational burden and slow recovery times. Not recommended for a production cluster.
- **Node Health Check (NHC) with Self Node Remediation:** Provides software-level remediation. It ensures workloads are moved but does not fix the underlying node, which will remain unavailable until manually repaired.
- **Node Health Check (NHC) with BareMetal Operator (BMO) Remediation:** This is the most robust, fully automated solution. It attempts to recover the node by "turning it off and on again" via its BMC. This requires a reliable IPI installation and stable Redfish/IPMI connectivity. Furthermore, the BMO facilitates the **Cluster API management of compute nodes (TP)** for dynamic lifecycle management. Advanced operational features, such as performing **live updates to HostFirmwareSettings (TP)** or **HostFirmwareComponents (TP)**, are available through BMO, but utilizing live updates requires setting the **HostUpdatePolicy (TP)** resource to `onReboot`. **We do not recommend that you perform live updates to the BMC on OpenShift Container Platform 4.20 for test purposes, especially on earlier generation hardware**

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-07

**Title**
Kernel Module and Device Plugin Management on Bare Metal using KMM

**Architectural Question**
What standard mechanism will be used to build, deploy, and manage out-of-tree kernel modules (like specialized GPU or NIC drivers) and their corresponding device plugins across bare metal cluster nodes?

**Issue or Problem**
Specialized hardware acceleration or networking components often require kernel modules and device plugins not included in the default Red Hat Enterprise Linux CoreOS (RHCOS) images. Deploying these manually leads to version misalignment and complex lifecycle management whenever kernel updates occur.

**Assumption**
The bare metal cluster will utilize specialized hardware requiring out-of-tree kernel drivers (e.g., GPUs or high-performance network adapters).

**Alternatives**

- Kernel Module Management (KMM) Operator
- Manual build and DaemonSet deployment (Driver Toolkit approach)

**Justification**

- **Kernel Module Management (KMM) Operator:** KMM is designed to simplify the lifecycle management of kernel modules by automating the build process, tracking kernel versions, and optionally signing the resulting kernel objects.
- **Manual build and DaemonSet deployment (Driver Toolkit approach):** This method requires manually fetching the Driver Toolkit image, building the module outside the cluster, and creating DaemonSets for deployment and pre/post-start hooks. This is highly complex and error-prone during RHCOS updates.

**Implications**

- **Kernel Module Management (KMM) Operator:** Requires installing and maintaining the KMM Operator and associated secrets/config maps. Provides high operational stability by ensuring modules match the current running kernel version automatically.
- **Manual build and DaemonSet deployment (Driver Toolkit approach):** High maintenance burden, as module compatibility must be manually verified and re-deployed on every kernel update or cluster upgrade.

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
