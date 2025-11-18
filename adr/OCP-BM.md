# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Bare metal platform installation specificities

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
Bare Metal Provisioning Workflow

**Architectural Question**
How will the provisioning of bare metal clusters be orchestrated and automated to ensure reproducibility and scale?

**Issue or Problem**
Bare metal provisioning involves complex steps (BMC interaction, ISO booting, host discovery). Performing these manually or via ad-hoc scripts is error-prone and inconsistent. A workflow is needed that leverages the Centralized Fleet Management strategy (RHACM).

**Assumption**

- Cluster is managed by RHACM.
- Cluster installation method is Agent-based Installer (ABI), Assisted Installer, or Image-based Installer (IBI)

**Alternatives**

- **Manual / Imperative Provisioning (Console/API):** Operators manually define clusters and hosts using the RHACM web console or trigger provisioning via imperative scripts/API calls to the Assisted Service.
- **GitOps Zero Touch Provisioning (ZTP):** A declarative, pipeline-based approach where cluster definitions are managed in Git and applied by OpenShift GitOps (Argo CD) to the RHACM Hub.

**Decision**
#TODO: Document the decision#

**Justification**

- **Manual / Imperative Provisioning (Console/API):** Simplifies the user experience for Day 0 ("ClickOps") or allows for custom integration via API scripts. However, it lacks a native audit trail, makes disaster recovery harder (no "state" in Git), and is difficult to scale consistently across hundreds of sites.
- **GitOps Zero Touch Provisioning (ZTP):** Treats infrastructure-as-code. The entire cluster definition (hardware, network, configuration) is versioned in Git. This is the standard Red Hat solution for mass-scale edge deployments, enabling "factory-precaching" and ensuring the actual state always matches the desired state in Git.

**Implications**

- **Manual / Imperative Provisioning:** Deployment intent is not stored in Git, increasing the risk of configuration drift over time.
- **GitOps Zero Touch Provisioning (ZTP):** Requires setting up an Argo CD pipeline on the Hub. Establishes strict requirements for downstream decisions, such as the need for `watchAllNamespaces` on the BMO and specific firmware management via `ClusterInstance`.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-03

**Title**
Bare Metal Operator (BMO) for UPI

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

## OCP-BM-04

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
- **Install RHCOS using PXE (Network Boot):** To enable highly automated, "zero-touch" provisioning of RHCOS for a large number of UPI nodes. This method is preferred when scalable provisioning with network infrastructure support is available.

**Implications**

- **Install RHCOS using ISO:** Requires minimal-to-no additional network infrastructure. High operational overhead. Requires manual intervention (or complex scripting) on every node's BMC for large-scale UPI deployments.
- **Install RHCOS using PXE (Network Boot):** Enables full, scalable, "zero-touch" provisioning, which is ideal for large-scale UPI deployments. Requires significant prerequisite infrastructure (DHCP, TFTP, Web servers) and network configuration (IP helpers, etc.), adding complexity.

  **Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-05

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

## OCP-BM-06

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

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **A dedicated provisioning network is used for deploying the cluster:** This method is the default Managed provisioning network setting. It automatically enables the Ironic-dnsmasq DHCP server on the provisioner node and is required for deployments using PXE booting. Using this network isolates the operating system provisioning traffic onto a non-routable network segment.
- **The provisioning will be performed on the routable bare metal network:** This approach is configured by setting `provisioningNetwork: "Disabled"` in the `install-config.yaml` file. This simplifies networking requirements by eliminating the need for a dedicated physical NIC for provisioning. This option enables the use of the Assisted Installer.

**Implications**

- **A dedicated provisioning network is used for deploying the cluster:** Requires a dedicated physical network interface (NIC1) on all nodes, distinct from the routable baremetal network (NIC2). This network must be isolated and cannot have an external DHCP server if configured as Managed.
- **The provisioning will be performed on the routable bare metal network:** This approach mandates the use of virtual media BMC addressing options (such as `redfish-virtualmedia` or `idrac-virtualmedia`). The BMCs must be accessible from the routable bare metal network. If disabled, the installation program requires two IP addresses on the bare metal network for provisioning services.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert

---

## OCP-BM-07

**Title**
Network Controller Sideband Interface (NC-SI) Support Enforcement

**Architectural Question**
For OpenShift Container Platform bare metal deployments utilizing hardware where the Baseboard Management Controller (BMC) shares a system Network Interface Card (NIC) via NC-SI, how must the cluster ensure continuous BMC connectivity during power events?

**Issue or Problem**
OpenShift Container Platform require NC-SI compliant hardware when the BMC shares a system NIC. Without the correct configuration, powering down the host can cause the loss of BMC connectivity (NC-SI connection loss), interrupting bare metal provisioning or management operations.

**Assumption**
Bare Metal Operator is enabled.

**Alternatives**

- BMC uses Network Controller Sideband Interface (NC-SI) for management traffic
- BMC uses a dedicated network interface for management traffic

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **BMC uses Network Controller Sideband Interface (NC-SI) for management traffic:** This approach reduces the overall physical network port requirement per server by allowing the BMC to share a system NIC with the host for management traffic. This method is supported on OpenShift Container Platform if the hardware is NC-SI compliant. However, this configuration mandates the use of the `DisablePowerOff` feature to ensure soft reboots do not result in the loss of BMC connectivity.
- **BMC uses a dedicated network interface for management traffic:** This method enhances performance and improves security by isolating the BMC traffic onto a separate physical NIC and network, avoiding the complications and dependencies inherent in NC-SI deployments. This avoids the specific requirement to utilize the `DisablePowerOff` feature.

**Implications**

- **BMC uses Network Controller Sideband Interface (NC-SI) for management traffic:** Requires verification that BMCs and NICs support NC-SI. The `BareMetalHost` resource must be explicitly configured with `disablePowerOff: true` to prevent loss of BMC connectivity during host power-off states.
- **BMC uses a dedicated network interface for management traffic:** This requires additional physical NIC hardware dedicated solely to out-of-band management. If a separate management network is implemented, the provisioner node must have routing access to this network for a successful installer-provisioned installation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert

---

## OCP-BM-08

**Title**
BMC protocol

**Architectural Question**
Which Baseboard Management Controller (BMC) protocol (Redfish, IPMI, or proprietary) should be standardized for automated provisioning, hardware inspection, and ongoing bare metal host lifecycle management using the Bare Metal Operator (BMO)?

**Issue or Problem**
The Bare Metal Operator (BMO) requires reliable, consistent, and secure connectivity to the BMC for key operations such as power management, image deployment, and hardware inspection. Different protocols offer varying levels of security, support for modern features (like firmware management), and compatibility across diverse hardware vendors, necessitating a standardized choice for cluster management.

**Assumption**
Bare Metal Operator is enabled.

**Alternatives**

- Redfish
- IPMI
- Other proprietary protocol

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Redfish:** This is the industry-standard, modern API recommended for hardware management. It enables advanced Bare Metal Operator features such as inspecting and configuring BIOS/Firmware settings (`HostFirmwareSettings`) and updating network interface controller (NIC) firmware (`HostFirmwareComponents`), which rely on Redfish support. Furthermore, Redfish BMC addressing is required for managed Secure Boot deployments, and for using Bare Metal as a Service (BMaaS) (TP).
- **IPMI:** IPMI is an older, widely supported protocol. It is required in specific environments, such as IBM Cloud Bare Metal (Classic) deployments, where Redfish may not be tested or supported. It is supported if hardware does not support Redfish network boot.
- **Other proprietary protocol:** This covers vendor-specific protocols (e.g., Fujitsu iRMC, Cisco CIMC) that are explicitly supported by Ironic/BMO. It is necessary when the fleet uses hardware that primarily relies on these interfaces for BMC connectivity.

**Implications**

- **Redfish:** Requires ensuring hardware and BMC firmware meet the necessary compatibility versions validated for Redfish virtual media installation. If self-signed certificates are used, `disableCertificateVerification: True` must be configured in the `install-config.yaml` or `BareMetalHost` object. Enables the most robust lifecycle management features via BMO/Ironic.
- **IPMI:** **IPMI does not encrypt communications** and requires use over a secured or dedicated management network. It cannot be used for managed Secure Boot deployments. If PXE booting is used with IPMI, a provisioning network is mandatory.
- **Other proprietary protocol:** Management capabilities (especially advanced features like firmware configuration) may be limited to specific BMO drivers (like Fujitsu iRMC or HP iLO) and might not support the full range of vendor-independent Redfish capabilities.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-09

**Title**
BMC Credential Security and Storage Strategy

**Architectural Question**
How will the highly sensitive Baseboard Management Controller (BMC) credentials, necessary for Bare Metal Operator (BMO) operation, Agent-based Installation (ABI), and GitOps Zero Touch Provisioning (ZTP), be securely stored and accessed by the OpenShift control plane?

**Issue or Problem**
The automated bare metal workflow requires storing BMC login credentials (username/password) as Kubernetes Secrets (referenced by bmcCredentialsName). These secrets grant full out-of-band control over physical hosts (e.g., power cycle, firmware updates, OS installation). Protecting these secrets is critical for platform security.

**Assumption**
Bare Metal Operator is enabled.

**Alternatives**

- Standard Kubernetes Secrets with OCP/etcd Encryption
- External Secret Management System Integration

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Standard Kubernetes Secrets with OCP/etcd Encryption:** This is the native pattern used by the Agent Installer and GitOps ZTP (via `bmcCredentialsName`). Protection relies on Role-Based Access Control (RBAC) and application-layer encryption in etcd (if enabled). This simplifies deployment as no external dependencies are introduced during installation.
- **External Secret Management System Integration:** Credentials are stored exclusively outside of the Kubernetes cluster (e.g., in HashiCorp Vault or CyberArk). OCP components/operators would retrieve the secrets just-in-time via an integration service (e.g., external Secrets Operator). This approach offers stronger separation of duties and auditing for access to critical infrastructure credentials.

**Implications**

- **Standard Kubernetes Secrets with OCP/etcd Encryption:** If an attacker gains sufficient privilege to read Kubernetes Secrets, the BMC credentials for all managed hosts are exposed. Requires stringent RBAC enforcement on the namespace containing the secrets.
- **External Secret Management System Integration:** Increases Day 1 complexity by requiring deployment and highly available integration with the external secret system. Adds an external dependency that must be reachable and operational for BMO functions (like host remediation and provisioning) to succeed.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-10

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

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Secure Boot will not be enabled:** This simplifies installation and avoids the complex hardware compatibility constraints associated with enabling Secure Boot.
- **Secure Boot will be enabled manually:** This approach utilizes the node's native Secure Boot feature, which is supported during IPI deployments when using **Redfish virtual media**. This is also the only supported method for UPI deployment. This method provides flexibility across more diverse hardware platforms compared to the Managed option and avoids reliance on a Technology Preview feature.
- **Secure Boot will be enabled through Managed Secure Boot (TP):** This option automates Secure Boot provisioning by setting `bootMode: "UEFISecureBoot"` in the `install-config.yaml` file. It streamlines node configuration and management, and crucially, does **not** require using Redfish virtual media for the installation.

**Implications**

- **Secure Boot will not be enabled:** This approach might fail to meet security or regulatory compliance standards that require verifying the integrity of the boot chain.
- **Secure Boot will be enabled manually:** Requires manual configuration of UEFI boot mode and Secure Boot settings on _each_ control plane and worker node. This is the only supported method when using UPI deployment. Furthermore, Red Hat explicitly supports this manual configuration for IPI only when the installation uses Redfish virtual media.
- **Secure Boot will be enabled through Managed Secure Boot (TP):** This feature is only supported on specific hardware models: **10th generation HPE hardware** and **13th generation Dell hardware** running firmware version **2.75.75.75 or greater**. This capability is currently designated as a Technology Preview (TP) feature.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-11

**Title**
BMO Provisioning Boot Mechanism

**Architectural Question**
Which boot mechanism (iPXE or Redfish Virtual Media) should be standardized for provisioning bare metal hosts managed by the Bare Metal Operator (BMO)?

**Issue or Problem**
Automated bare metal provisioning (as used by IPI, ABI, and AI) requires a reliable method for the BMO/Ironic service to boot the discovery ISO on the physical host. The choice of method is constrained by network infrastructure and BMC capabilities.

**Assumption**
Cluster installation method is IPI, Agent-based Installer (ABI), or Assisted Installer (AI).

**Alternatives**

- iPXE Booting (Network Boot)
- Redfish Virtual Media Booting

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **iPXE Booting (Network Boot):** Provides fast, zero-touch provisioning typically favored in centralized data centers. It relies on robust PXE/DHCP/TFTP infrastructure.
- **Redfish Virtual Media Booting:** Leverages the BMC's ability to mount a remote ISO image, ensuring reliability even if the host's primary network configuration is complex. This is a common requirement for edge or disconnected deployments using ABI/AI.

**Implications**

- **iPXE Booting (Network Boot):** Requires a provisioning network and adherence to network prerequisites like DHCP, TFTP, and Web servers.
- **Redfish Virtual Media Booting:** This is the mandatory choice if Provisioning Network is not used. It requires that the BMC supports the Virtual Media feature via the chosen Redfish/IPMI protocol.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert

---

## OCP-BM-12

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

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Configure and use supported Hardware RAID volumes for the installation drive:** Leveraging hardware RAID provides disk redundancy and potential performance improvements managed entirely by the hardware controller/BMC interface, which is supported for specific configurations.
- **Configure the installation drive without using Hardware RAID:** This simplifies the underlying storage configuration and avoids potential compatibility issues, focusing solely on software volumes, although internal cluster components like etcd manage their own redundancy.

**Implications**

- **Configure and use supported Hardware RAID volumes for the installation drive:** Requires specifying the logical drives within the `hardwareRAIDVolumes` parameter of the installation configuration. Incorrect configuration or use with unsupported BMC versions or RAID levels may lead to unsupported clusters or installation failure.
- **Configure the installation drive without using Hardware RAID:** Node resiliency relies solely on the underlying physical disk health, which might not be desirable for critical bare metal components if a disk fails.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BM-13

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

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Dedicated partition for `/var/lib/containers`:** This is the recommended approach for workload partitioning and robustness, explicitly setting up a separate partition, formatted with `xfs` and mounted using `prjquota` for appropriate resource handling. This practice isolates volatile container data storage from the core OS filesystems.
- **Co-locate `/var/lib/containers` on the root partition:** Simplifies the initial installation process by relying on the default RHCOS partitioning scheme. However, this risks system instability if container images or ephemeral volumes consume excessive disk space, impacting the root filesystem.

**Implications**

- **Dedicated partition for `/var/lib/containers`:** Requires custom Ignition configuration overrides within the installation manifest. This adds complexity to the installation process.
- **Co-locate `/var/lib/containers` on the root partition:** Higher risk of disk exhaustion affecting system stability if container usage is heavy or unpredictable. Management of disk quotas becomes less granular.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-14

**Title**
Bare Metal Node Image Pre-caching Strategy for Disconnected/Edge Deployments

**Architectural Question**
How will required container images (OCP release, operators, application base images) be transferred and prepared on bare metal edge nodes prior to or during installation/upgrade to minimize network latency and bandwidth dependency?

**Issue or Problem**
In disconnected environments or at the far edge, pulling large container images during installation or upgrade (JIT pull) can be slow or unreliable. A structured method is needed to pre-position images on the node's container storage partition, supporting efficient Zero Touch Provisioning (ZTP) and Image-Based Upgrades (IBU).

**Assumption**
GitOps ZTP is used.
Cluster is on the edge.
Nodes utilize disk partitioning to include a shared container partition (`/var/lib/containers`).

**Alternatives**

- Client-side Image Pre-caching via Ignition/IBU
- Just-In-Time (JIT) Pull during Installation and Runtime

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Client-side Image Pre-caching via Ignition/IBU:** This method significantly reduces installation time and network load, which is critical for far edge or constrained environments. It integrates seamlessly with ZTP using `ignitionConfigOverride` to configure mount points and launch services to extract pre-cached images before the cluster installation fully proceeds..
- **Just-In-Time (JIT) Pull during Installation and Runtime:** This simplifies the pre-install setup since no manual image pre-packaging or partition management is required. It relies on the network being stable and high-bandwidth enough to pull all necessary images when needed.

**Implications**

- **Client-side Image Pre-caching via Ignition/IBU:** Requires careful configuration of OS disk partitioning (e.g., separating `/var/lib/containers`) and precise Ignition/systemd units to manage mounting and extraction of compressed image artifacts (tarballs) before core services start. This adds complexity to the Day 1 manifests.
- **Just-In-Time (JIT) Pull during Installation and Runtime:** Risk of installation/upgrade failure or significant delays due to network instability or slow download speeds, common challenges at the far edge.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-BM-15

**Title**
Bare Metal Operator Namespace Scope

**Architectural Question**
Should the Bare Metal Operator (BMO) be configured to manage BareMetalHost resources across all namespaces in the cluster?

**Issue or Problem**
To enable features like Bare Metal as a Service (BMaaS) or GitOps ZTP, the BMO must be configured to find and manage BareMetalHost resources created outside its default namespace. Deciding this scope is a fundamental configuration for the BMO.

**Assumption**

- The Bare Metal Operator (BMO) is enabled on the cluster.
- The cluster fulfills a management role: It is either an ACM Hub Cluster managing a ZTP fleet OR a centralized BMaaS provider allocating physical nodes to various namespaces.

**Alternatives**

- BMO Watches All Namespaces (Watch-All)
- BMO Watches Specific/Limited Namespaces (Default)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **BMO Watches All Namespaces (Watch-All):** This is **required for BMaaS and GitOps ZTP**. It allows the BMO on the **Hub Cluster** to discover `BareMetalHost` CRs created in any namespace (e.g., a spoke cluster namespace) and provision them.
- **BMO Watches Specific/Limited Namespaces (Default):** This is the default behavior. BMO will only discover and provision hosts defined in its own `openshift-machine-api` namespace. All other `BareMetalHost` CRs in the cluster are ignored.

**Implications**

- **BMO Watches All Namespaces (Watch-All):** The BMO `Provisioning` CR must be patched to set `watchAllNamespaces: true`, enabling advanced, cluster-wide provisioning workflows.
- **BMO Watches Specific/Limited Namespaces (Default):** The cluster is isolated, and advanced, multi-namespace provisioning workflows like BMaaS and GitOps ZTP are not possible.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-16

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
- **Node Health Check (NHC) with BareMetal Operator (BMO) Remediation:** This is the most robust, fully automated solution. It attempts to recover the node by "turning it off and on again" via its BMC. This requires a reliable IPI installation and stable Redfish/IPMI connectivity. Furthermore, the BMO facilitates the **Cluster API management of compute nodes (TP)** for dynamic lifecycle management. Advanced operational features, such as performing **live updates to HostFirmwareSettings (TP)** or **HostFirmwareComponents (TP)**, are available through BMO, but utilizing live updates requires setting the **HostUpdatePolicy (TP)** resource to `onReboot`. **We do not recommend that you perform live updates to the BMC for test purposes, especially on earlier generation hardware**

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-17

**Title**
Bare Metal Node Firmware Management

**Architectural Question**
How will ongoing firmware updates (BIOS, BMC, NIC) for bare metal nodes be managed and automated post-installation?

**Issue or Problem**
Managing firmware updates manually (BIOS, BMC, NICs) across a bare metal fleet is complex, time-consuming, and prone to error, posing maintenance and compliance risks. A standardized, automatable process is required, especially when leveraging the Bare Metal Operator (BMO) for node lifecycle management, utilizing resources like `HostFirmwareComponents` and `HostUpdatePolicy`.

**Assumption**
Cluster installation method is IPI / Assisted Installer / Agent-based installer / IBI or UPI with Bare Metal Operator enabled.

**Alternatives**

- Automated Management via HostFirmware/HostUpdate CRs
- External/Vendor Management Tools

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Automated Management via HostFirmware/HostUpdate CRs:** Leverages native BMO capabilities (`HostFirmwareComponents`, `HostUpdatePolicy`) to apply, track, and manage firmware versions for components like BIOS, BMC, and NICs directly through Kubernetes Custom Resources, supporting automated updates and inspection.
- **External/Vendor Management Tools:** Relies on existing organizational tools (e.g., vendor-specific console or infrastructure automation) to perform firmware updates. This allows separation of concerns if the platform team is not responsible for hardware maintenance.

**Implications**

- **Automated Management via HostFirmware/HostUpdate CRs:** Requires defining, testing, and maintaining `HostFirmwareComponents` and `HostUpdatePolicy` CRs. The process may cause node disruption and require coordination (e.g., node draining).
- **External/Vendor Management Tools:** Updates are decoupled from the OpenShift workflow, potentially simplifying BMO configuration, but resulting in a manual process that requires coordinating external maintenance windows with cluster availability (e.g., node draining, cluster remediation).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-18

**Title**
Bare Metal Fleet Cluster Upgrade Strategy

**Architectural Question**
How will large-scale, distributed bare metal cluster updates (OCP version upgrades) be managed and orchestrated from the central hub cluster?

**Issue or Problem**
Managing simultaneous upgrades across a large fleet of bare metal clusters, particularly Single Node OpenShift (SNO) clusters at the edge, requires a robust orchestration mechanism that can handle sequencing, image consistency, and minimal disruption. A choice must be made between the currently supported policy-driven approach and the image-based method designed for rapid edge updates.

**Assumption**

- Cluster topology is Single-Node (SNO)
- Cluster is managed using ZTP.

**Alternatives**

- Policy-Driven Rollout using TALM and PolicyGenerator CRs
- Image-Based Group Upgrade (IBGU) (TP)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Policy-Driven Rollout using TALM and PolicyGenerator CRs:** This is the standard, generally available approach for managing configurations and upgrades via policies, enabling granular control over rollout sequencing, customization, and remediation actions.
- **Image-Based Group Upgrade (IBGU) (TP):** This methodology is designed to reduce deployment time significantly, especially for SNO clusters. It leverages the Lifecycle Agent (LCA) to deploy new operating system images (stateroots), making it suitable for rapid, consistent rollouts in edge environments.

**Implications**

- **Policy-Driven Rollout using TALM and PolicyGenerator CRs:** Upgrades rely on ensuring policy compliance across the fleet, which may involve individual cluster reboots initiated by configuration changes (e.g., Node Tuning Operator). This approach requires meticulous policy management but is fully supported.
- **Image-Based Group Upgrade (IBGU) (TP):** Is a Technology Preview feature only and is not supported with Red Hat production SLAs. While offering faster, image-based upgrades, reliance on this method for production clusters introduces support risk.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-19

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

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Kernel Module Management (KMM) Operator:** KMM is designed to simplify the lifecycle management of kernel modules by automating the build process, tracking kernel versions, and optionally signing the resulting kernel objects.
- **Manual build and DaemonSet deployment (Driver Toolkit approach):** This method requires manually fetching the Driver Toolkit image, building the module outside the cluster, and creating DaemonSets for deployment and pre/post-start hooks. This is highly complex and error-prone during RHCOS updates.

**Implications**

- **Kernel Module Management (KMM) Operator:** Requires installing and maintaining the KMM Operator and associated secrets/config maps. Provides high operational stability by ensuring modules match the current running kernel version automatically.
- **Manual build and DaemonSet deployment (Driver Toolkit approach):** High maintenance burden, as module compatibility must be manually verified and re-deployed on every kernel update or cluster upgrade.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-BM-20

**Title**
Bare Metal Host Firmware Configuration

**Architectural Question**
How will host firmware settings (BIOS/UEFI) be applied, validated, and maintained to ensure consistency and compliance across the bare metal fleet?

**Issue or Problem**
Managing firmware settings manually across a fleet of physical servers leads to configuration drift, inconsistent node behavior, and increased troubleshooting time. A standardized method is required to ensure that every host is provisioned with the exact same BIOS/UEFI configuration defined by the platform standards.

**Assumption**
GitOps ZTP is used

**Alternatives**

- Manual/Out-of-Band Configuration
- Automated Configuration via GitOps ZTP

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Manual/Out-of-Band Configuration:** Relies on server administrators manually configuring BIOS settings via vendor consoles (e.g., iDRAC, iLO) or ad-hoc scripts. This is prone to human error and makes auditing the actual state of the fleet difficult.
- **Automated Configuration via GitOps ZTP:** Uses the **Infrastructure-as-Code** model. Firmware settings are defined in a `HardwareProfile` file stored in Git and referenced by the CR (`biosConfigRef`). The underlying automation (BMO) applies these settings during provisioning, ensuring every node matches the definition in Git.

**Implications**

- **Manual/Out-of-Band Configuration:** High operational overhead. No automated way to detect or remediate if a server's settings drift from the standard.
- **Automated Configuration via GitOps ZTP:** Requires creating and maintaining hardware profile files (e.g., `.profile`) in the Git repository. Provides a single source of truth for hardware configuration, simplifying audits and disaster recovery.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-21

**Title**
Bare Metal Kernel Selection: Real-Time Kernel Implementation

**Architectural Question**
Should the OpenShift Container Platform nodes leverage the Real-Time Kernel for low-latency performance, and how will this requirement be enforced and configured across the cluster nodes?

**Issue or Problem**
Bare metal deployments for demanding workloads, such as virtual Distributed Unit (vDU) applications in Telco environments, require guaranteed low latency and high performance. The standard RHCOS kernel may introduce unacceptable jitter or delay, necessitating the use of the Real-Time (RT) kernel.

**Assumption**
Workloads require strict low-latency guarantees, typically falling into the CNF/vDU/AI/ML categories.

**Alternatives**

- Enable Real-Time Kernel via Performance Profile
- Enable Workload Partitioning

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Enable Real-Time Kernel via Performance Profile:** This is the recommended approach for running low-latency applications on OpenShift Container Platform. Enabling the RT kernel through the `PerformanceProfile` custom resource is crucial for isolating CPU resources and achieving performance guarantees required by vDU applications.
- **Use Default Standard Kernel:** This simplifies cluster management and updates, as the standard kernel is fully supported and requires fewer specialized tunings. It avoids the overhead associated with the RT kernel but cannot guarantee the low latency required for critical applications.

**Implications**

- **Enable Real-Time Kernel via Performance Profile:** Requires the use of the Node Tuning Operator and specific configurations in the `PerformanceProfile` (e.g., setting `realTimeKernel: enabled: true`). Changes to this kernel may require node reboots for application. This configuration is mandated for VDU workloads.
- **Use Default Standard Kernel:** May lead to performance instability, resource jitter, or failure to meet Service Level Objectives (SLOs) for latency-sensitive applications.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert

---

## OCP-BM-22

**Title**
Workload Partitioning (CPU Isolation)

**Architectural Question**
What strategy will be implemented for dedicating CPU resources (workload partitioning) to isolate performance-sensitive tenant workloads from host and OpenShift platform processes?

**Issue or Problem**
For bare metal deployments hosting performance-critical or low-latency workloads (like RAN Distributed Units, or vDU applications), unpartitioned CPU usage leads to performance jitter due to contention between application pods and platform/kernel components. Defining isolated and reserved CPU sets is critical to meet required performance constraints.

**Assumption**
Low-latency or high-performance application workloads (like vDUs) must be isolated on dedicated CPU cores, likely requiring the real-time kernel.

**Alternatives**

- No Partitioning (Default)
- Enable Workload Partitioning

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Partitioning (Default):** This is the simplest operational model. All platform and application pods are scheduled across all available CPU cores, which is sufficient for workloads without real-time or low-latency requirements.
- **Enable Workload Partitioning:** This is the required method for isolating performance-sensitive workloads. It involves creating a `PerformanceProfile` to divide the node's CPUs into a `reserved` set (for platform/OS processes) and an `isolated` set (exclusively for tenant workloads).

**Implications**

- **No Partitioning (Default):** This configuration will not support real-time workloads like vDUs, as platform and application CPU contention will cause unacceptable performance jitter and potential service failure.
- **Enable Workload Partitioning:** This adds configuration complexity, requiring a `PerformanceProfile` and `Tuned` CRs. It also "costs" CPU cores, as the `reserved` cores are permanently removed from the schedulable capacity for general pods, but this is necessary to guarantee performance for isolated workloads.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert

---

## OCP-BM-23

**Title**
Container Runtime Selection for Bare Metal Performance Workloads

**Architectural Question**
Should the default CRI-O container runtime be replaced or augmented with CRUN to optimize performance for latency-sensitive workloads on bare metal nodes?

**Issue or Problem**
To support stringent latency and high-performance requirements typical of applications like virtual Distributed Units (vDU), relying solely on the default container runtime may not be sufficient. Utilizing an optimized runtime like CRUN is often recommended for these performance-sensitive environments.

**Assumption**
Performance-sensitive workloads (e.g., vDU) will be deployed on the bare metal cluster.

**Alternatives**

- Default Container Runtime (CRI-O)
- Optimized Container Runtime (CRUN)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Container Runtime (CRI-O):** Simplifies installation and operational maintenance by relying on the standard, supported container engine bundled with Red Hat Enterprise Linux CoreOS (RHCOS).
- **Optimized Container Runtime (CRUN):** This option is strongly recommended for performance workloads, such as vDU, to achieve specific low-latency optimization.

**Implications**

- **Default Container Runtime (CRI-O):** May lead to sub-optimal latency performance for critical telecommunication or AI/ML workloads.
- **Optimized Container Runtime (CRUN):** **It is strongly recommended to include `crun` manifests as part of the additional install-time manifests**. This requires defining `ContainerRuntimeConfig` manifests (e.g., `enable-crun-master.yaml`, `enable-crun-worker.yaml`) via the GitOps ZTP pipeline or equivalent mechanism.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-24

**Title**
Precision Time Protocol (PTP) Configuration Strategy for Low-Latency Workloads

**Architectural Question**
How will highly accurate time synchronization be achieved and managed on bare metal nodes to meet the strict timing requirements of low-latency applications (e.g., vDU)?

**Issue or Problem**
Standard Network Time Protocol (NTP) often lacks the precision required by workloads such as vDU (Virtual Distributed Unit) applications, which require Precision Time Protocol (PTP) synchronization to function correctly. A standardized mechanism is needed to deploy and manage PTP services across the cluster nodes.

**Assumption**
Performance-sensitive workloads (e.g., vDU) will be deployed on the bare metal cluster.

**Alternatives**

- Rely Solely on Standard NTP
- Managed PTP using the PTP Operator

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Rely Solely on Standard NTP:** Minimizes cluster complexity but fails to meet the time synchronization requirements for stringent low-latency workloads like vDU.
- **Managed PTP using the PTP Operator:** This approach ensures the cluster can support low latency applications by managing time synchronization through the **PTP Operator**. It allows for configuration of specific roles like `boundary` or `slave` using `PtpConfig` CRs.

**Implications**

- **Rely Solely on Standard NTP:** Critical applications (like vDU) will likely fail due to insufficient time synchronization precision.
- **Managed PTP using the PTP Operator:** Requires installing the PTP Operator and configuring appropriate `PtpConfig` resources for roles, interfaces, and options (e.g., `ptp4lOpts`, `phc2sysOpts`). Managing PTP requires ensuring interfaces are correctly configured for PTP, potentially using specific network interface cards (NICs), and integrating with kernel tuning profiles.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-25

**Title**
SR-IOV Virtual Function (VF) Driver Selection for Performance Workloads

**Architectural Question**
Which SR-IOV Virtual Function (VF) device type—`vfio-pci` or `netdevice`—will be standardized for use by high-performance application pods (e.g., vDU, AI/ML inference) requiring direct hardware access on bare metal nodes?

**Issue or Problem**
When configuring SR-IOV devices using the `SriovNetworkNodePolicy` Custom Resource, the choice of the VF device driver type (`vfio-pci` or `netdevice`) dictates how the network resource is presented to the container. This impacts latency, performance characteristics, and the flexibility for applications (e.g., requiring kernel bypass versus standard Linux networking).

**Assumption**
Performance-sensitive workloads (e.g., vDU) will be deployed on the bare metal cluster.
The cluster supports SR-IOV capable NICs.

**Alternatives**

- VFIO-PCI Driver (`vfio-pci`)
- Netdevice Driver (`netdevice`)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **VFIO-PCI Driver (`vfio-pci`):** Recommended when true hardware passthrough (Device Passthrough) is required, often for applications using Data Plane Development Kit (DPDK) or needing kernel bypass to achieve the lowest possible latency.
- **Netdevice Driver (`netdevice`):** Recommended when standard Linux network semantics (e.g., standard CNI features, DHCP, IP address management by the kernel) are required, offering higher flexibility for debugging and standard networking but potentially higher latency than VFIO.

**Implications**

- **VFIO-PCI Driver (`vfio-pci`):** Applications must be designed to utilize device passthrough frameworks (like DPDK). The VF is not exposed as a traditional network interface to the OS, complicating standard networking and monitoring tools.
- **Netdevice Driver (`netdevice`):** Provides simpler integration with standard container networking. However, this configuration might introduce additional latency compared to kernel-bypass methods.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-BM-26

**Title**
Network Diagnostics Operator Deployment Strategy

**Architectural Question**
Should the cluster intentionally disable the core OpenShift Network Diagnostics functionality to conserve resources or reduce the management footprint, especially in resource-constrained bare metal or edge deployments?

**Issue or Problem**
For highly optimized, resource-constrained environments (like those running vDU workloads), reducing platform overhead is critical. The default configuration may include network components that consume resources but are deemed non-essential if comprehensive external monitoring is already in place.

**Assumption**
The environment is resource-constrained (e.g., Single Node OpenShift or Compact HA) and requires minimizing non-application resource consumption.

**Alternatives**

- Default Network Diagnostics (Enabled)
- Disabled Network Diagnostics

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Network Diagnostics (Enabled):** Provides valuable built-in troubleshooting tools for validating networking health, simplifying Day 2 operations and identifying connectivity issues proactively.
- **Disabled Network Diagnostics:** **Setting `disableNetworkDiagnostics: true` in the Network CR** explicitly removes this feature, reducing the overall platform footprint and conserving CPU/memory resources, which is highly beneficial for edge sites.

**Implications**

- **Default Network Diagnostics (Enabled):** Consumes node resources (CPU/memory) via associated diagnostic pods and daemon sets.
- **Disabled Network Diagnostics:** Removes a built-in diagnostic safety net. Troubleshooting complex network failures must rely solely on external tools or manual inspection, increasing operational complexity when issues arise.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner
