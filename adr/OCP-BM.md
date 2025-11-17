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

- **User-Provisioned Infrastructure (UPI):** Requires the user to manually provision and configure all cluster infrastructure (including networking, DNS, load balancers, and storage) and install Red Hat Enterprise Linux CoreOS (RHCOS) on hosts using generated Ignition configuration files. This approach offers **maximum customizability**. Required if both TPM and Tang for disk encryption is required.
- **Installer-Provisioned Infrastructure (IPI):** Delegates the infrastructure bootstrapping and provisioning to the installation program. For bare metal, this process automates provisioning using the host’s Baseboard Management Controller (BMC) by leveraging the Bare Metal Operator (BMO) features.
- **Agent-based Installer (ABI):** Provides the convenience of the Assisted Installer but enables installation **locally for disconnected environments or restricted networks**. It uses a lightweight agent booted from a discovery ISO to facilitate provisioning.
- **Assisted Installer:** A web-based SaaS service designed for **connected networks** that simplifies deployment by providing a user-friendly interface, smart defaults, and pre-flight validations, generating a discovery image for the bare metal installation.
- **Image-based Installer (IBI):** Significantly reduces the deployment time of single-node OpenShift clusters by enabling the preinstallation of configured and validated instances on target hosts, supporting rapid reconfiguration and deployment even in disconnected environments.

**Implications**

- **User-Provisioned Infrastructure (UPI):** Implies the **highest operational overhead** because the user must manage and maintain all infrastructure resources (Load Balancers, Networking, Storage) throughout the cluster lifecycle. It requires additional validation and configuration to use the Machine API capabilities. Support both TPM and Tang for disk encryption.
- **Installer-Provisioned Infrastructure (IPI):** Requires integration with the BMO and related provisioning infrastructure. For bare metal IPI, the user must provide all cluster infrastructure resources, including the bootstrap machine, networking, load balancing, storage, and individual cluster machines. Once installed, it allows OpenShift Container Platform to manage the operating system and supports using the Machine API for node lifecycle management. Only support TPM for disk encryption.
- **Agent-based Installer (ABI):** Ideal for **disconnected environments** and provides features like integrated tools for configuring nodes (e.g., disk encryption or LVM storage configuration). Requires the user to provide all cluster infrastructure and resources (networking, load balancing, storage). Only support TPM for disk encryption.
- **Assisted Installer:** Requires a working internet connection during the preparation phase (unless steps are followed for a disconnected approach). It simplifies deployment by handling Ignition configuration generation and supports **full integration for bare metal platforms**. Only support TPM for disk encryption.
- **Image-based Installer (IBI):** Primarily intended for **Single-Node OpenShift (SNO) cluster deployments**, often managed using a hub-and-spoke architecture via Red Hat Advanced Cluster Management (RHACM) and the multicluster engine for Kubernetes Operator (MCE). Does not support disk encryption.

  **Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-02

**Title**
RHCEnable Bare Metal Operator (BMO) for UPI

**Architectural Question**
Will the Bare Metal Operator (BMO) be enabled for a User-Provisioned Infrastructure (UPI) deployment?

**Issue or Problem**
A standard UPI installation does not include the Bare Metal Operator, meaning all Day 2 operations (like node remediation, scaling, or hardware management) are fully manual. Enabling BMO on UPI adds this automation but requires additional configuration.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- BMO will not be enabled
- BMO will be enabled

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **BMO will not be enabled:** This maintains a pure UPI model where the platform has no control over the physical hardware, relying on manual intervention or external automation for all node lifecycle management.
- **BMO will be enabled:** This creates a "hybrid" model that combines the Day 1 control of UPI with the Day 2 automation benefits of IPI, such as automated node remediation and hardware inspection.

**Implications**

- **BMO will not be enabled:** The organization is fully responsible for all Day 2 bare metal operations, and ADRs related to BMCs (remediation, protocol, NC-SI) are not applicable.
- **BMO will be enabled:** Subsequent ADRs for BMC protocols, NC-SI, and automated remediation must be addressed, and the operator must be manually installed and configured post-installation.

  **Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-03

**Title**
RHCOS Provisioning Method for Bare Metal Nodes

**Architectural Question**
How will Red Hat Enterprise Linux CoreOS (RHCOS) be provisioned onto the bare metal nodes when using UPI method deployment?

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

## OCP-BM-04

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

## OCP-BM-05

**Title**
Provisioning Network Strategy for Installer-Provisioned Bare Metal

**Architectural Question**
Will a dedicated provisioning network be used during IPI cluster deployment?

**Issue or Problem**
The Installer-Provisioned Infrastructure (IPI) deployment model, especially on bare metal, defaults to leveraging an optional, segregated provisioning network to manage tasks like DHCP, TFTP, and operating system deployment via Ironic. Deciding whether to utilize this network or provision entirely over the routable bare metal network dictates hardware requirements (NIC count) and the mandatory use of certain Baseboard Management Controller (BMC) protocols (virtual media).

**Assumption**
Cluster installation method is Installer-Provisioned Infrastructure (IPI).

**Alternatives**

- A dedicated provisioning network is used for deploying the cluster
- The provisioning will be performed on the routable bare metal network

**Justification**

- **A dedicated provisioning network is used for deploying the cluster:** This method is the default Managed provisioning network setting. It automatically enables the Ironic-dnsmasq DHCP server on the provisioner node and is required for deployments using PXE booting. Using this network isolates the operating system provisioning traffic onto a non-routable network segment.
- **The provisioning will be performed on the routable bare metal network:** This approach is configured by setting `provisioningNetwork: "Disabled"` in the `install-config.yaml` file. This simplifies networking requirements by eliminating the need for a dedicated physical NIC for provisioning. This option enables the use of the Assisted Installer.

**Implications**

- **A dedicated provisioning network is used for deploying the cluster:** Requires a dedicated physical network interface (NIC1) on all nodes, distinct from the routable baremetal network (NIC2). This network must be isolated and cannot have an external DHCP server if configured as Managed.
- **The provisioning will be performed on the routable bare metal network:** This approach mandates the use of virtual media BMC addressing options (such as `redfish-virtualmedia` or `idrac-virtualmedia`). The BMCs must be accessible from the routable bare metal network. If disabled, the installation program requires two IP addresses on the bare metal network for provisioning services.

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert

---

## OCP-BM-06

**Title**
Network Controller Sideband Interface (NC-SI) Support Enforcement

**Architectural Question**
For OpenShift Container Platform bare metal deployments utilizing hardware where the Baseboard Management Controller (BMC) shares a system Network Interface Card (NIC) via NC-SI, how must the cluster ensure continuous BMC connectivity during power events?

**Issue or Problem**
OpenShift Container Platform require NC-SI compliant hardware when the BMC shares a system NIC. Without the correct configuration, powering down the host can cause the loss of BMC connectivity (NC-SI connection loss), interrupting bare metal provisioning or management operations.

**Assumption**
Cluster installation method is IPI / Assisted Installer / Agent-based installer / IBI or UPI with Bare Metal Operator enabled.

**Alternatives**

- BMC uses Network Controller Sideband Interface (NC-SI) for management traffic
- BMC uses a dedicated network interface for management traffic

**Justification**

- **BMC uses Network Controller Sideband Interface (NC-SI) for management traffic:** This approach reduces the overall physical network port requirement per server by allowing the BMC to share a system NIC with the host for management traffic. This method is supported on OpenShift Container Platform if the hardware is NC-SI compliant. However, this configuration mandates the use of the `DisablePowerOff` feature to ensure soft reboots do not result in the loss of BMC connectivity.
- **BMC uses a dedicated network interface for management traffic:** This method enhances performance and improves security by isolating the BMC traffic onto a separate physical NIC and network, avoiding the complications and dependencies inherent in NC-SI deployments. This avoids the specific requirement to utilize the `DisablePowerOff` feature.

**Implications**

- **BMC uses Network Controller Sideband Interface (NC-SI) for management traffic:** Requires verification that BMCs and NICs support NC-SI. The `BareMetalHost` resource must be explicitly configured with `disablePowerOff: true` to prevent loss of BMC connectivity during host power-off states.
- **BMC uses a dedicated network interface for management traffic:** This requires additional physical NIC hardware dedicated solely to out-of-band management. If a separate management network is implemented, the provisioner node must have routing access to this network for a successful installer-provisioned installation.

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert

---

## OCP-BM-07

**Title**
BMC protocol

**Architectural Question**
Which Baseboard Management Controller (BMC) protocol (Redfish, IPMI, or proprietary) should be standardized for automated provisioning, hardware inspection, and ongoing bare metal host lifecycle management using the Bare Metal Operator (BMO)?

**Issue or Problem**
The Bare Metal Operator (BMO) requires reliable, consistent, and secure connectivity to the BMC for key operations such as power management, image deployment, and hardware inspection. Different protocols offer varying levels of security, support for modern features (like firmware management), and compatibility across diverse hardware vendors, necessitating a standardized choice for cluster management.

**Assumption**
The cluster installation method is Installer-Provisioned Infrastructure (IPI) or the Bare Metal Operator (BMO) is installed and operational for post-installation management, scaling, or remediation tasks.

**Alternatives**

- Redfish
- IPMI
- Other proprietary protocol

**Justification**

- **Redfish:** This is the industry-standard, modern API recommended for hardware management. It enables advanced Bare Metal Operator features such as inspecting and configuring BIOS/Firmware settings (`HostFirmwareSettings`) and updating network interface controller (NIC) firmware (`HostFirmwareComponents`), which rely on Redfish support. Furthermore, Redfish BMC addressing is required for managed Secure Boot deployments, and for using Bare Metal as a Service (BMaaS) (TP).
- **IPMI:** IPMI is an older, widely supported protocol. It is required in specific environments, such as IBM Cloud Bare Metal (Classic) deployments, where Redfish may not be tested or supported. It is supported if hardware does not support Redfish network boot.
- **Other proprietary protocol:** This covers vendor-specific protocols (e.g., Fujitsu iRMC, Cisco CIMC) that are explicitly supported by Ironic/BMO. It is necessary when the fleet uses hardware that primarily relies on these interfaces for BMC connectivity.

**Implications**

- **Redfish:** Requires ensuring hardware and BMC firmware meet the necessary compatibility versions validated for Redfish virtual media installation. If self-signed certificates are used, `disableCertificateVerification: True` must be configured in the `install-config.yaml` or `BareMetalHost` object. Enables the most robust lifecycle management features via BMO/Ironic.
- **IPMI:** **IPMI does not encrypt communications** and requires use over a secured or dedicated management network. It cannot be used for managed Secure Boot deployments. If PXE booting is used with IPMI, a provisioning network is mandatory.
- **Other proprietary protocol:** Management capabilities (especially advanced features like firmware configuration) may be limited to specific BMO drivers (like Fujitsu iRMC or HP iLO) and might not support the full range of vendor-independent Redfish capabilities.

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-08

**Title**
Bare Metal Node Secure Boot Strategy

**Architectural Question**
Will Secure Boot be enabled on bare metal cluster nodes?

**Issue or Problem**
Secure Boot is often required for security compliance to ensure nodes only boot with trusted software. The implementation method chosen (disabled, manual, or managed) has different operational overheads, specific setup requirements (e.g., reliance on Redfish virtual media), and stringent hardware compatibility restrictions.

**Assumption**
The bare metal hardware supports UEFI boot mode and Secure Boot functionality.

**Alternatives**

- Secure Boot will not be enabled
- Secure Boot will be enabled manually
- Secure Boot will be enabled through Managed Secure Boot (TP)

**Justification**

- **Secure Boot will not be enabled:** This simplifies installation and avoids the complex hardware compatibility constraints associated with enabling Secure Boot.
- **Secure Boot will be enabled manually:** This approach utilizes the node's native Secure Boot feature, which is supported during IPI deployments when using **Redfish virtual media**. This is also the only supported method for UPI deployment. This method provides flexibility across more diverse hardware platforms compared to the Managed option and avoids reliance on a Technology Preview feature.
- **Secure Boot will be enabled through Managed Secure Boot (TP):** This option automates Secure Boot provisioning by setting `bootMode: "UEFISecureBoot"` in the `install-config.yaml` file. It streamlines node configuration and management, and crucially, does **not** require using Redfish virtual media for the installation.

**Implications**

- **Secure Boot will not be enabled:** This approach might fail to meet security or regulatory compliance standards that require verifying the integrity of the boot chain.
- **Secure Boot will be enabled manually:** Requires manual configuration of UEFI boot mode and Secure Boot settings on _each_ control plane and worker node. This is the only supported method when using UPI deployment. Furthermore, Red Hat explicitly supports this manual configuration for IPI only when the installation uses Redfish virtual media.
- **Secure Boot will be enabled through Managed Secure Boot (TP):** This feature is only supported on specific hardware models: **10th generation HPE hardware** and **13th generation Dell hardware** running firmware version **2.75.75.75 or greater**. This capability is currently designated as a Technology Preview (TP) feature.

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-09

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

## OCP-BM-10

**Title**
Bare Metal Node OS Disk Partitioning for Container Storage

**Architectural Question**
How should the root disk be partitioned on bare metal nodes to accommodate container runtime storage (`/var/lib/containers`), specifically concerning separation from the operating system partition, and what filesystem options should be used?

**Issue or Problem**
If the container storage (`/var/lib/containers`) directory resides on the same partition as the root filesystem, aggressive application logging or large image pull caches can lead to the control plane nodes or worker nodes running out of disk space, potentially causing instability or failure. Defining a dedicated partition ensures predictable capacity management and allows for specific filesystem tuning.

**Assumption**
N/A

**Alternatives**

- Dedicated partition for `/var/lib/containers`
- Co-locate `/var/lib/containers` on the root partition

**Justification**

- **Dedicated partition for /var/lib/containers:** This is the recommended approach for workload partitioning and robustness, explicitly setting up a separate partition, formatted with `xfs` and mounted using `prjquota` for appropriate resource handling. This practice isolates volatile container data storage from the core OS filesystems.
- **Co-locate /var/lib/containers on the root partition:** Simplifies the initial installation process by relying on the default RHCOS partitioning scheme. However, this risks system instability if container images or ephemeral volumes consume excessive disk space, impacting the root filesystem.

**Implications**

- **Dedicated partition for /var/lib/containers:** Requires custom Ignition configuration overrides within the installation manifest (e.g., `SiteConfig` or `BareMetalHost` definition). This adds complexity to the installation process.
- **Co-locate /var/lib/containers on the root partition:** Higher risk of disk exhaustion affecting system stability if container usage is heavy or unpredictable. Management of disk quotas becomes less granular.

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-11

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

## OCP-BM-12

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
