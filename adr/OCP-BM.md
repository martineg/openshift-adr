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

- **User-Provisioned Infrastructure (UPI):** Requires the user to manually provision and configure all cluster infrastructure (including networking, DNS, load balancers, and storage) and install Red Hat Enterprise Linux CoreOS (RHCOS) on hosts using generated Ignition configuration files. This approach offers maximum customizability. Required if both TPM and Tang for disk encryption is required.
- **Installer-Provisioned Infrastructure (IPI):** Delegates the infrastructure bootstrapping and provisioning to the installation program. For bare metal, this process automates provisioning using the host’s Baseboard Management Controller (BMC) by leveraging the Bare Metal Operator (BMO) features.
- **Agent-based Installer (ABI):** Provides the convenience of the Assisted Installer but enables installation locally for disconnected environments or restricted networks. It uses a lightweight agent booted from a discovery ISO to facilitate provisioning.
- **Assisted Installer:** A web-based SaaS service designed for connected networks that simplifies deployment by providing a user-friendly interface, smart defaults, and pre-flight validations, generating a discovery image for the bare metal installation.
- **Image-based Installer (IBI):** Significantly reduces the deployment time of single-node OpenShift clusters by enabling the preinstallation of configured and validated instances on target hosts, supporting rapid reconfiguration and deployment even in disconnected environments.

**Implications**

- **User-Provisioned Infrastructure (UPI):** Implies the highest operational overhead because the user must manage and maintain all infrastructure resources (Load Balancers, Networking, Storage) throughout the cluster lifecycle. It requires additional validation and configuration to use the Machine API capabilities. Supports No encryption, TPM v2 Only, Tang Server Only, and the TPM v2 and Tang Server Combination for disk encryption.
- **Installer-Provisioned Infrastructure (IPI):** Requires integration with the BMO and related provisioning infrastructure. Once installed, it allows OpenShift Container Platform to manage the operating system and supports using the Machine API for node lifecycle management. Supports only TPM for disk encryption, excluding Tang Server Only and the combined TPM/Tang method.
- **Agent-based Installer (ABI):** Ideal for disconnected environments and provides features like integrated tools for configuring nodes. Supports only TPM for disk encryption, excluding Tang Server Only and the combined TPM/Tang method.
- **Assisted Installer:** Requires a working internet connection during the preparation phase. Supports only TPM for disk encryption, excluding Tang Server Only and the combined TPM/Tang method.
- **Image-based Installer (IBI):** Primarily intended for Single-Node OpenShift (SNO) cluster deployments. Does not support disk encryption.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-02

**Title**
UPI Worker Node Operating System Selection (RHCOS vs RHEL)

**Architectural Question**
Which operating system (RHCOS or RHEL) will be standardized for compute (worker) nodes in user-provisioned infrastructure (UPI) bare metal clusters?

**Issue or Problem**
The choice between RHCOS and RHEL for compute machines in UPI environments dictates the Day 2 operational model: RHEL provides flexibility but shifts OS lifecycle management entirely to the user, while RHCOS ensures consistency and uses the Machine Config Operator (MCO) for updates, supporting the standard immutable infrastructure model.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Standardize on Red Hat Enterprise Linux CoreOS (RHCOS) workers
- Standardize on Red Hat Enterprise Linux (RHEL) workers

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Standardize on Red Hat Enterprise Linux CoreOS (RHCOS) workers:** This ensures the standard immutable OS image is used and allows the Machine Config Operator to manage the OS lifecycle via cluster upgrades, simplifying ongoing maintenance and consistency.
- **Standardize on Red Hat Enterprise Linux (RHEL) workers:** This allows the use of a traditional Linux OS (e.g., RHEL 8.6+ or RHEL 9 depending on OCP version), providing maximum customizability for specialized applications or legacy configurations, and leveraging existing enterprise RHEL operational toolchains.

**Implications**

- **Standardize on Red Hat Enterprise Linux CoreOS (RHCOS) workers:** Supports the default cluster operational model. All cluster changes are applied by Operators. SSH access is not recommended for routine use.
- **Standardize on Red Hat Enterprise Linux (RHEL) workers:** The organization takes full responsibility for all operating system life cycle management and maintenance of the compute nodes, including updates, patching, and required tasks. The cluster upgrade process will not automatically update the OS on these nodes.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## OCP-BM-03

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
- **GitOps Zero Touch Provisioning (ZTP):** A declarative, pipeline-based approach where cluster definitions (`ClusterInstance`, `PolicyGenerator`) are managed in Git and applied by OpenShift GitOps (Argo CD) to the RHACM Hub.

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

## OCP-BM-04

**Title**
Bare Metal Fleet Cluster Upgrade Strategy

**Architectural Question**
How will large-scale, distributed bare metal cluster updates (OCP version upgrades) be managed and orchestrated from the central hub cluster?

**Issue or Problem**
Managing simultaneous upgrades across a large fleet of bare metal clusters, particularly Single Node OpenShift (SNO) clusters at the edge, requires a robust orchestration mechanism that can handle sequencing, image consistency, and minimal disruption. A choice must be made between the currently supported policy-driven approach and the image-based method designed for rapid edge updates.

**Assumption**

- Cluster topology is Single-Node (SNO)
- Provisioning workflow is GitOps ZTP.

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

## OCP-BM-05

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

## OCP-BM-06

**Title**
Bare Metal Operator Enrollment Policy for Existing UPI Hosts

**Architectural Question**
When enabling the Bare Metal Operator (BMO) on a User-Provisioned Infrastructure (UPI) cluster for Day 2 automation, should existing, already-installed nodes (e.g., control plane) be enrolled only for inventory and status purposes, or prepared for full BMO lifecycle management (remediation, re-provisioning)?

**Issue or Problem**
Integrating existing UPI nodes into the BMO system for inventory and management visibility risks accidental re-provisioning or state corruption if the BMO attempts to manage the node's lifecycle without the correct configuration flag.

**Assumption**
The Bare Metal Operator (BMO) is enabled on a UPI cluster.

**Alternatives**

- Enroll as Fully Managed Hosts
- Enroll as Externally Provisioned Hosts (Inventory Only)

**Decision**
#TODO: Document decision.#

**Justification**

- **Enroll as Fully Managed Hosts:** This allows the BMO to perform full node lifecycle management (remediation, scaling), treating the UPI node similarly to an IPI node, provided it conforms to Ironic standards.
- **Enroll as Externally Provisioned Hosts (Inventory Only):** This strategy allows the cluster administrator to use the BMO to manage existing hosts solely for inventory purposes and to observe status, ensuring the host is recognized without attempting to re-provision the underlying operating system.

**Implications**

- **Enroll as Fully Managed Hosts:** Increased risk of unintended node re-provisioning if the original UPI installation deviated from the BMO/Ironic expectations or if the `externallyProvisioned` flag is mistakenly omitted.
- **Enroll as Externally Provisioned Hosts (Inventory Only):** Requires explicitly setting the `spec.externallyProvisioned: true` specification in the `BareMetalHost` Custom Resource to prevent the BMO from re-provisioning the host.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-07

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

## OCP-BM-11

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

## OCP-BM-12

**Title**
IPI Provisioning Network DHCP Management Mode

**Architectural Question**
When utilizing a dedicated provisioning network during Installer-Provisioned Infrastructure (IPI) deployment, should the cluster allow Ironic to manage DHCP services, or should it rely on an existing external DHCP server?

**Issue or Problem**
The default IPI installation attempts to run an Ironic-managed DHCP service (`ironic-dnsmasq`) on the provisioning network. If another DHCP server is already present on this non-routable network, this causes conflicts and installation failure unless the provisioning network mode is explicitly changed to unmanaged.

**Assumption**
A dedicated provisioning network is configured for IPI deployment.

**Alternatives**

- Managed Provisioning Network (Ironic DHCP)
- Unmanaged Provisioning Network (External DHCP)

**Decision**
#TODO: Document decision.#

**Justification**

- **Managed Provisioning Network (Ironic DHCP):** This is the default `Managed` provisioning network setting. It automatically enables the `ironic-dnsmasq` DHCP server on the provisioner node, isolating the operating system provisioning traffic onto a non-routable network segment.
- **Unmanaged Provisioning Network (External DHCP):** This is configured by setting `provisioningNetwork` to a setting other than `Managed`. This is required if a DHCP server is already running on the provisioning network, as relying on an existing external server avoids conflicts with Ironic's integrated DHCP service.

**Implications**

- **Managed Provisioning Network (Ironic DHCP):** This network must be isolated and cannot have an external DHCP server if configured as `Managed`.
- **Unmanaged Provisioning Network (External DHCP):** The administrator is fully responsible for deploying and managing the highly available external DHCP service on the provisioning network to assign IP addresses to the bare metal nodes.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-13

**Title**
IPI/Assisted Provisioning Boot Mechanism

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

## OCP-BM-14

**Title**
Ironic RHCOS Image Transfer Protocol (Virtual Media)

**Architectural Question**
When deploying OpenShift Container Platform using virtual media for RHCOS image transfer via the Baseboard Management Controller (BMC), should the transfer rely on unencrypted HTTP or TLS-encrypted HTTPS?

**Issue or Problem**
When omitting the provisioning network, virtual media transfer is required. Using unencrypted HTTP for image transfer introduces a data security risk during the provisioning phase. However, enabling TLS/HTTPS adds operational complexity related to certificate trust management.

**Assumption**
Installation utilizes Virtual Media BMC addressing (e.g., `redfish-virtualmedia` or `idrac-virtualmedia`).

**Alternatives**

- HTTP Image Transfer (Port 6180)
- HTTPS/TLS Image Transfer (Port 6183)

**Decision**
#TODO: Document decision.#

**Justification**

- **HTTP Image Transfer (Port 6180):** This is the default HTTP port for image access. It simplifies the setup as it avoids the requirement for provisioning and managing TLS certificates for the provisioning service.
- **HTTPS/TLS Image Transfer (Port 6183):** This enhances security by encrypting the RHCOS image transfer. Port 6183 is the required TLS port for virtual media installation.

**Implications**

- **HTTP Image Transfer (Port 6180):** The RHCOS image is transferred unencrypted, which may not meet security or compliance mandates.
- **HTTPS/TLS Image Transfer (Port 6183):** Requires that the provisioner node and control plane nodes have port 6183 open on the baremetal network interface. Requires careful management of the certificate authority chain to ensure the BMC trusts the server.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-15

**Title**
UPI Provisioning Boot Mechanism

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

## OCP-BM-16

**Title**
Ignition Configuration Integrity Validation Strategy

**Architectural Question**
How will the authenticity and integrity of the fetched Ignition Configuration files be validated during Red Hat Enterprise Linux CoreOS (RHCOS) node installation?

**Issue or Problem**
During manual RHCOS installation (ISO/PXE), the Ignition config files are downloaded from an HTTP/S server. Without verification, the system is vulnerable to fetching tampered configurations. If relying on HTTP, a hash is required for integrity validation.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Validate using SHA512 Hash over HTTP/S
- Validate using HTTPS TLS/CA Trust (without explicit hash)
- Disable Integrity Validation (Insecure)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Validate using SHA512 Hash over HTTP/S:** This approach provides a strong integrity check regardless of the network protocol (HTTP or HTTPS). Using the `--ignition-hash` is required when the Ignition config file is obtained through an HTTP URL to validate its authenticity.
- **Validate using HTTPS TLS/CA Trust (without explicit hash):** If the Ignition configuration files are provided through an HTTPS server that uses TLS, the certificate authority (CA) can be added to the system trust store before running `coreos-installer`, ensuring integrity and confidentiality during transfer.
- **Disable Integrity Validation (Insecure):** This simplifies installation and debugging by removing the dependency on HTTPS certificate authorities or manually verifying the SHA512 digest. Supported via the `--insecure-ignition` option.

**Implications**

- **Validate using SHA512 Hash over HTTP/S:** Requires the administrator to obtain the SHA512 digest for each Ignition config file and pass it using the `--ignition-hash` option to `coreos-installer`.
- **Validate using HTTPS TLS/CA Trust (without explicit hash):** If using a custom CA, requires adding the internal certificate authority (CA) to the system trust store via `coreos-installer` before installation.
- **Disable Integrity Validation (Insecure):** **Not recommended for production.** This leaves the node vulnerable to accepting a compromised Ignition configuration file if the network or download URL is manipulated (Man-in-the-Middle).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-BM-17

**Title**
RHCOS Live Installer Custom CA Trust Strategy

**Architectural Question**
How will a custom Certificate Authority (CA) required to access secure installation artifacts (like the Ignition Config over HTTPS) be trusted by the Red Hat Enterprise Linux CoreOS (RHCOS) live installer environment during User-Provisioned Infrastructure (UPI) boot?

**Issue or Problem**
If the Ignition configuration files are served over HTTPS secured by a non-standard or corporate Certificate Authority (CA), the minimal live RHCOS installer environment (booted from ISO/PXE) will fail to download the configurations unless the custom CA is explicitly trusted. The standard mechanism for augmenting the cluster's trust bundle applies only after the node installs and boots.

**Assumption**
The cluster installation method is User-Provisioned Infrastructure (UPI) or PXE/ISO installation. The Ignition Configuration file URL uses HTTPS secured by a custom CA.

**Alternatives**

- Customize Live Media with Embedded CA (--ignition-ca)
- Rely on Default RHCOS Trust Bundle (Use HTTP or Public CA)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Customize Live Media with Embedded CA (--ignition-ca):** This method provides the required trust for network-based installations that rely on a custom Certificate Authority (CA) during the minimal boot phase. It is achieved by using the `coreos-installer iso customize` or `coreos-installer pxe customize` subcommands with the `--ignition-ca cert.pem` flag.
- **Rely on Default RHCOS Trust Bundle (Use HTTP or Public CA):** This approach simplifies the installation process by avoiding the media customization step. If relying on the default RHCOS trust bundle, the Ignition config must either be obtained over plain HTTP, requiring the SHA512 hash validation (via `--ignition-hash`), or accessed via HTTPS signed by a CA already present in the RHCOS trust bundle.

**Implications**

- **Customize Live Media with Embedded CA (--ignition-ca):** Requires a pre-processing step to customize ("stamp") the ISO or initramfs file with the CA certificate before booting the media. This process ensures that the live environment can securely fetch the Ignition configuration files over HTTPS.
- **Rely on Default RHCOS Trust Bundle (Use HTTP or Public CA):** If HTTPS with a custom CA is required for the Ignition URL, this option will result in the live installer failing to establish a secure connection, leading to installation failure. If the Ignition configuration is obtained via HTTP, the administrator must supply the SHA512 digest to `coreos-installer` using the `--ignition-hash` option to validate the content's integrity.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-BM-18

**Title**
RHCOS Artifact Sourcing Strategy

**Architectural Question**
How will the necessary Red Hat Enterprise Linux CoreOS (RHCOS) installation artifacts (kernel, initramfs, rootfs, or ISO image) be reliably sourced for the cluster deployment process?

**Issue or Problem**
Sourcing RHCOS installation files directly from the public image mirror might lead to version misalignment or compatibility issues, especially if the artifacts have changed since the last installer release. A robust method is required to guarantee the correct, compatible artifacts are used for installation.

**Assumption**
N/A

**Alternatives**

- Source artifacts via openshift-install coreos print-stream-json utility (Recommended)
- Source artifacts directly from the RHCOS image mirror page

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Source artifacts via openshift-install coreos print-stream-json utility (Recommended):** The recommended way to obtain the correct version of RHCOS images is from the output of the `openshift-install` command. This ensures compatibility with the specific OpenShift Container Platform version being installed.
- **Source artifacts directly from the RHCOS image mirror page:** While possible, this method requires manually verifying that the downloaded images are the highest version less than or equal to the OpenShift Container Platform version being installed.

**Implications**

- **Source artifacts via openshift-install coreos print-stream-json utility (Recommended):** Requires access to the `openshift-install` executable during the preparation phase.
- **Source artifacts directly from the RHCOS image mirror page:** Increases the operational risk of using incompatible kernel/rootfs/initramfs files, potentially leading to installation failure.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-19

**Title**
RHCOS Day-1 Customization and Network Configuration Strategy

**Architectural Question**
Which mechanism will be used to apply Day-1 configurations—specifically complex network settings (bonding, VLANs) and disk partitions—to RHCOS nodes during UPI installation?

**Issue or Problem**
Standard kernel arguments (`ip=`, `bond=`) are often insufficient or error-prone for enterprise bare metal deployments requiring complex network topologies (LACP bonds, multiple VLANs) or static IPs. A standardized method is required to inject these configurations reliably into the installation media to ensure successful bootstrapping and fetching of the ignition configuration.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Kernel Arguments (Standard/Simple)
- ISO/PXE Customization with Embedded Keyfiles (Advanced/Complex)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Kernel Arguments (Standard/Simple):** Uses standard boot parameters (e.g., `ip=dhcp`, `coreos.inst.ignition_url=`) passed via the bootloader. This is sufficient for simple, single-interface DHCP environments but becomes unmanageable for complex bonding or static IP configurations due to character string complexity and lack of persistence features.
- **ISO/PXE Customization with Embedded Keyfiles (Advanced/Complex):** Uses `coreos-installer iso/pxe customize` to embed **NetworkManager Keyfiles** (`.nmconnection`) and `MachineConfig` manifests directly into the initramfs of the installation media. This is the **preferred and most robust method** for enterprise deployments, as it supports complex LACP bonding, VLAN tagging, and static IPs natively without relying on fragile kernel argument strings.

**Implications**

- **Kernel Arguments (Standard/Simple):** Works identically for ISO and PXE. High risk of syntax errors for complex networking. Changes require editing boot menus or PXE config files. Cannot apply configurations that exceed the kernel command line length limit.
- **ISO/PXE Customization with Embedded Keyfiles (Advanced/Complex):** Requires a pre-processing step to "stamp" the ISO or initramfs with the configuration before booting. Enables "Infrastructure as Code" for the network config but adds a build step to the provisioning workflow.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-20

**Title**
RHCOS Customization Timing Strategy (Live vs Permanent Ignition)

**Architectural Question**
Should Day-0 configuration tasks (e.g., advanced disk partitioning) be performed using a temporary Live Install Ignition config, or incorporated into the standard, persistent Permanent Install Ignition config via wrapped manifests?

**Issue or Problem**
The Live Install Ignition config runs immediately on boot and is required for complex, one-time setup (like advanced disk partitioning) that cannot be managed by the Machine Config Operator (MCO). However, using this mechanism adds a pre-processing step to the provisioning workflow.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).
Custom Day-0 tasks requiring non-MCO methods are needed (e.g., advanced partitioning).

**Alternatives**

- Utilize Permanent Install Ignition Config (Embedded Manifests)
- Utilize Live Install Ignition Config (ignition.config.url)

**Decision**
#TODO: Document decision.#

**Justification**

- **Utilize Permanent Install Ignition Config (Embedded Manifests):** This method is preferred for standard cluster components and configurations that are consistently managed by the Machine Config Operator (MCO) throughout the cluster lifecycle.
- **Utilize Live Install Ignition Config (ignition.config.url):** This is intended specifically for performing configuration tasks that must occur once and cannot be applied again later, such as complex disk partitioning.

**Implications**

- **Utilize Permanent Install Ignition Config (Embedded Manifests):** This method cannot be used for highly specialized, one-time changes like complex custom disk partitioning.
- **Utilize Live Install Ignition Config (ignition.config.url):** This requires appending specific kernel arguments (e.g., `ignition.config.url=`, `ignition.firstboot`, `ignition.platform.id=metal`) to the installation media, increasing setup complexity.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-21

**Title**
RHCOS Live Network Configuration Persistence Strategy (UPI)

**Architectural Question**
When performing a manual User-Provisioned Infrastructure (UPI) installation of RHCOS from a live environment, how will the network configuration detected or used by the live installer be persisted to the installed system?

**Issue or Problem**
During manual RHCOS installation (ISO/PXE), the temporary live environment successfully obtains network settings (IP, DNS). This configuration must be transferred robustly to the permanent OS installation for successful first boot and Ignition fetch, and this persistence can be handled either implicitly by copying the live environment's state or explicitly via declarative mechanisms.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Explicit Configuration (NetworkManager Keyfiles/Kernel Arguments)
- Implicit Configuration (Copy Network Flag)

**Decision**
#TODO: Document decision.#

**Justification**

- **Explicit Configuration (NetworkManager Keyfiles/Kernel Arguments):** This approach utilizes declarative configuration (NetworkManager Keyfiles embedded via `coreos-installer customize` or kernel arguments) to ensure the target OS configuration is strictly deterministic. It maintains consistency and is independent of how the live system initially derived its network settings.
- **Implicit Configuration (Copy Network Flag):** This method simplifies the installation process by transferring the existing, validated network configuration used by the running live system directly to the installed operating system using the `--copy-network` flag with `coreos-installer install`.

**Implications**

- **Explicit Configuration (NetworkManager Keyfiles/Kernel Arguments):** This requires a pre-processing step (like customizing the ISO/PXE image with `--network-keyfile`) or configuring kernel argument strings, adding complexity to the provisioning build step.
- **Implicit Configuration (Copy Network Flag):** Achieved via the `--copy-network` option. This approach relies on the live environment successfully detecting or configuring the network correctly, making the persistence based on an implicit state transfer rather than a declared manifest.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-BM-22

**Title**
RHCOS Node Day-1 DNS Resolver Redundancy Strategy

**Architectural Question**
When statically configuring RHCOS nodes during UPI deployment, should multiple DNS server addresses be provided to the installer to enhance Day-1 connectivity and resilience?

**Issue or Problem**
During manual installation (UPI) with static IP addresses, RHCOS relies on kernel arguments to define networking. If only a single DNS server is configured and that server is unreachable, the bootstrapping process will fail as the node cannot resolve endpoints like the Ignition configuration server URL.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).
The cluster machines are configured with static IP addresses during RHCOS installation.

**Alternatives**

- Configure Multiple Redundant DNS Servers
- Configure Only a Single Primary DNS Server

**Decision**
#TODO: Document decision.#

**Justification**

- **Configure Multiple Redundant DNS Servers:** This method provides stronger resilience for the RHCOS nodes during the critical bootstrapping phase by listing multiple upstream DNS resolvers using multiple `nameserver=` kernel arguments. This is achieved by adding a `nameserver=` entry for each server.
- **Configure Only a Single Primary DNS Server:** This simplifies the configuration required in the kernel argument string. It is only sufficient if the specified DNS server is guaranteed to be highly available during the installation phase.

**Implications**

- **Configure Multiple Redundant DNS Servers:** Requires meticulous coordination with the network team to identify and correctly configure all redundant enterprise DNS servers within the boot parameters.
- **Configure Only a Single Primary DNS Server:** Introduces a Single Point of Failure (SPoF) for initial host-level name resolution, increasing the risk of installation failure.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## OCP-BM-23

**Title**
Multi-NIC Strategy for RHCOS Core Network (UPI)

**Architectural Question**
Should the core cluster network connectivity for RHCOS nodes leverage a single interface/bond, or multiple distinct, non-aggregated physical network interfaces (NICs)?

**Issue or Problem**
Utilizing multiple discrete physical network interfaces allows for traffic segmentation at the physical layer, but increases the complexity of network bootstrapping compared to a single aggregated interface.

**Assumption**
Cluster uses User-Provisioned Infrastructure (UPI).

**Alternatives**

- Single Interface or Aggregated Interface (Bonding)
- Multiple Discrete Network Interfaces (Configured Separately)

**Decision**
#TODO: Document decision.#

**Justification**

- **Single Interface or Aggregated Interface (Bonding):** This approach simplifies initial configuration and reduces the number of kernel arguments required during installation. It provides redundancy at the link layer while presenting a single logical interface to the OS.
- **Multiple Discrete Network Interfaces (Configured Separately):** This allows for strict physical isolation of traffic types (e.g., separating management traffic from data traffic on different physical hardware) without relying on VLAN tagging over a shared bond.

**Implications**

- **Single Interface or Aggregated Interface (Bonding):** May limit flexibility if strict physical air-gapping between network segments is required.
- **Multiple Discrete Network Interfaces (Configured Separately):** Requires careful planning and configuration of multiple kernel arguments (e.g., multiple `ip=` entries) during the RHCOS installation process. Increases the complexity of the Day 1 configuration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-24

**Title**
Bare Metal Network Bridge Configuration Tooling Strategy

**Architectural Question**
Which method will be standardized for configuring the Open vSwitch (OVS) br-ex bridge network on bare metal nodes, balancing simplicity for single-NIC setups against flexibility for advanced and multi-NIC post-installation changes?

**Issue or Problem**
The choice of tooling (shell script vs. MachineConfig/NMState) determines whether post-installation network changes are supported and limits the ability to define advanced network configurations (e.g., specific interfaces or complex topologies) for the br-ex bridge.

**Assumption**
N/A

**Alternatives**

- Configure br-ex using the configure-ovs.sh Shell Script (Single NIC/Simple Default)
- Configure br-ex using NMState Configuration embedded in a MachineConfig

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Configure br-ex using the configure-ovs.sh Shell Script (Single NIC/Simple Default):** This approach is simpler and should be used if the environment requires a single Network Interface Controller (NIC) and default network settings. It minimizes initial complexity.
- **Configure br-ex using NMState Configuration embedded in a MachineConfig:** This method is recommended when advanced configurations are required, such as deploying the bridge on a different interface, supporting post-installation changes to the bridge network, or implementing configurations not possible with the shell script (e.g., complex multi-interface setups).

**Implications**

- **Configure br-ex using the configure-ovs.sh Shell Script (Single NIC/Simple Default):** This script does not support making post-installation changes to the bridge. Using the script for advanced configurations may result in the bridge failing to connect multiple network interfaces.
- **Configure br-ex using NMState Configuration embedded in a MachineConfig:** Requires defining and managing an NMState configuration file and corresponding MachineConfig object. This process involves base64 encoding the configuration and embedding it in the manifest.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-25

**Title**
Cluster Node Hostname Assignment Strategy (User-Provisioned Infrastructure)

**Architectural Question**
How will the hostnames for OpenShift cluster nodes (RHCOS) in a User-Provisioned Infrastructure (UPI) deployment be determined and maintained?

**Issue or Problem**
In UPI deployments, RHCOS nodes must obtain a hostname during boot. If this is not explicitly provided by DHCP, the system defaults to using reverse DNS lookup, which can be slow and result in critical system services detecting the hostname as "localhost". A stable and quickly resolved hostname is required for node readiness and CSR generation.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- DHCP-Provided Hostnames (Recommended)
- Reverse DNS Lookup (Default Fallback)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **DHCP-Provided Hostnames (Recommended):** This approach minimizes operational risk by ensuring the hostname is obtained quickly and reliably during network initialization. It simplifies Day 1 setup and bypasses manual DNS record configuration errors in environments that use DNS split-horizon implementations.
- **Reverse DNS Lookup (Default Fallback):** This requires minimal specific configuration on the DHCP server side, relying solely on the presence of accurate PTR records in the DNS infrastructure.

**Implications**

- **DHCP-Provided Hostnames (Recommended):** Requires ensuring the DHCP server is configured to provide persistent IP addresses, DNS server information, and hostnames to all cluster machines for long-term management.
- **Reverse DNS Lookup (Default Fallback):** Node initialization can be delayed while the reverse DNS lookup occurs, potentially causing system services to incorrectly start with "localhost" as the hostname.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-26

**Title**
Host Network Bonding Mode for High Availability (OVS)

**Architectural Question**
When configuring high availability for bare metal node network interfaces, should the solution rely on standard kernel bonding methods or utilize the specialized OVS balance-slb mode?

**Issue or Problem**
When provisioning bare metal nodes for high-performance workloads (like OpenShift Virtualization), standard bonding modes (like active-backup or LACP) may not effectively distribute traffic for OVN-Kubernetes pods or VMs that share the same physical link characteristics (MAC/VLAN). A mode is needed to ensure true load balancing for this traffic.

**Assumption**
The cluster hosts performance-sensitive workloads (e.g., virtualization) that rely on OVS-based networking for High Availability.

**Alternatives**

- Standard NetworkManager/Kernel Bonding
- Open vSwitch (OVS) balance-slb Mode

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Standard NetworkManager/Kernel Bonding:** Relies on the host OS/NetworkManager for bonding implementation (e.g., active-backup). While simpler to configure, it does not guarantee load distribution for OVN-Kubernetes traffic which uses consistent MAC/VLAN combinations.
- **Open vSwitch (OVS) balance-slb Mode:** This mode is specifically designed and supported for virtualization workloads on bare metal. It natively supports source load balancing for OVN-Kubernetes CNI plugin traffic, ensuring that traffic from different VM ports is balanced over the physical interface links.

**Implications**

- **Standard NetworkManager/Kernel Bonding:** May lead to sub-optimal performance or lack of true load balancing for OVN-Kubernetes/VM traffic, impacting HA and resource utilization.
- **Open vSwitch (OVS) balance-slb Mode:** Requires complex network configuration, potentially involving OVS bonding modes like `balance-slb`, managed via MachineConfig/NMState configuration during installation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

--

## OCP-BM-27

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
- **Secure Boot will be enabled manually:** This approach utilizes the node's native Secure Boot feature, which is supported during IPI deployments when using Redfish virtual media. This is also the only supported method for UPI deployment. This method provides flexibility across more diverse hardware platforms compared to the Managed option and avoids reliance on a Technology Preview feature.
- **Secure Boot will be enabled through Managed Secure Boot (TP):** This option automates Secure Boot provisioning by setting `bootMode: "UEFISecureBoot"` in the `install-config.yaml` file. It streamlines node configuration and management, and crucially, does not require using Redfish virtual media for the installation.

**Implications**

- **Secure Boot will not be enabled:** This approach might fail to meet security or regulatory compliance standards that require verifying the integrity of the boot chain.
- **Secure Boot will be enabled manually:** Requires manual configuration of UEFI boot mode and Secure Boot settings on each control plane and worker node. This is the only supported method when using UPI deployment. Furthermore, Red Hat explicitly supports this manual configuration for IPI only when the installation uses Redfish virtual media.
- **Secure Boot will be enabled through Managed Secure Boot (TP):** This feature is only supported on specific hardware models: 10th generation HPE hardware and 13th generation Dell hardware running firmware version 2.75.75.75 or greater. This capability is currently designated as a Technology Preview (TP) feature.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-28

**Title**
Bare Metal Host Firmware Configuration Management

**Architectural Question**
How will host firmware settings (BIOS/UEFI) be applied, validated, and maintained to ensure consistency and compliance across the bare metal fleet?

**Issue or Problem**
Managing firmware settings manually across a fleet of physical servers leads to configuration drift, inconsistent node behavior, and increased troubleshooting time. A standardized method is required to ensure that every host is provisioned with the exact same BIOS/UEFI configuration defined by the platform standards.

**Assumption**
Provisioning workflow is GitOps ZTP.

**Alternatives**

- Manual/Out-of-Band Configuration
- Automated Configuration via GitOps ZTP/ClusterInstance

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Manual/Out-of-Band Configuration:** Relies on server administrators manually configuring BIOS settings via vendor consoles (e.g., iDRAC, iLO) or ad-hoc scripts. This is prone to human error and makes auditing the actual state of the fleet difficult.
- **Automated Configuration via GitOps ZTP/ClusterInstance:** Uses the **Infrastructure-as-Code** model. Firmware settings are defined in a `HardwareProfile` file stored in Git and referenced by the `ClusterInstance` (`biosConfigRef`). The underlying automation (BMO) applies these settings during provisioning, ensuring every node matches the definition in Git.

**Implications**

- **Manual/Out-of-Band Configuration:** High operational overhead. No automated way to detect or remediate if a server's settings drift from the standard.
- **Automated Configuration via GitOps ZTP/ClusterInstance:** Requires creating and maintaining hardware profile files (e.g., `.profile`) in the Git repository. Provides a single source of truth for hardware configuration, simplifying audits and disaster recovery.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-29

**Title**
RHCOS Node Console Access Strategy

**Architectural Question**
Which console mechanism (Graphical, Serial, or both) will be configured as the primary interface for OpenShift Container Platform nodes installed on bare metal to facilitate troubleshooting and out-of-band access?

**Issue or Problem**
Bare metal RHCOS nodes installed from a boot image use default kernel settings, which typically results in the graphical console being primary and the serial console being disabled. This may conflict with operational requirements, such as accessing the emergency shell for debugging or if the underlying infrastructure only provides serial console access.

**Assumption**
N/A

**Alternatives**

- Default Console Configuration (Graphical Primary, Serial Disabled)
- Serial Console Configuration (Serial Primary, Graphical Secondary)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Console Configuration (Graphical Primary, Serial Disabled):** This setting is inherited from the boot image. It uses kernel default settings, which is standard but may prevent remote interactive access if the platform does not easily expose the graphical console.
- **Serial Console Configuration (Serial Primary, Graphical Secondary):** Explicitly configures the serial console (e.g., `console=ttyS0,<options>`). This is necessary for environments where console access is crucial for management or when the cloud platform does not provide interactive access to the graphical console.

**Implications**

- **Default Console Configuration (Graphical Primary, Serial Disabled):** Requires careful evaluation to ensure troubleshooting capabilities meet disaster recovery requirements if the graphical console is not easily accessible.
- **Serial Console Configuration (Serial Primary, Graphical Secondary):** Requires adding one or more `console=` arguments (e.g., `console=tty0 console=ttyS0`) to the APPEND line during PXE installation, or using the `--console` option with `coreos-installer` during ISO installation to set the serial port as the primary console.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-30

**Title**
RHCOS Installation Boot Device Selection

**Architectural Question**
Will Red Hat Enterprise Linux CoreOS (RHCOS) be installed and booted from local internal storage (e.g., NVMe, SATA SSD) or from network-attached SAN storage (iSCSI/Fibre Channel)?

**Issue or Problem**
The choice of boot device impacts storage management, failure domains, and the complexity of the installation process. Integrating with existing Storage Area Networks (SANs) requires specific installation steps (Zoning, LUN masking, WWN/IQN configuration) not needed for local disk deployment.

**Assumption**
N/A

**Alternatives**

- Local Disk Installation (Internal NVMe/SSD/HDD)
- SAN Storage (iSCSI/Fibre Channel)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Local Disk Installation (Internal NVMe/SSD/HDD):** This is the default, simpler installation path, requiring less complex networking and kernel configuration during the RHCOS installation boot process.
- **SAN Storage (iSCSI/Fibre Channel):** This is required to leverage centralized, highly available, and potentially multi-pathed SAN infrastructure for the OS root disk. It supports fully diskless machines (Boot from SAN) and allows the OS disk to survive physical server chassis replacement.

**Implications**

- **Local Disk Installation (Internal NVMe/SSD/HDD):** Resilience relies entirely on the local disk health (e.g., RAID, if configured). Storage capacity and performance are confined to the internal server limits.
- **SAN Storage (iSCSI/Fibre Channel):** Significantly increases installation complexity. For iSCSI: Requires configuration of the target portal, IQN, and LUN, either manually or via iBFT. For Fibre Channel: Requires HBAs, correct fabric zoning, and LUN masking to the HBA's WWN. Both require the multipath configuration to be enabled during installation to prevent I/O errors.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-31

**Title**
iSCSI Boot Configuration Method for RHCOS

**Architectural Question**
When using an iSCSI boot device for RHCOS, should the configuration be handled manually via the live installer shell/scripts and kernel arguments, or automatically via iBFT (iSCSI Boot Firmware Table)?

**Issue or Problem**
Installing RHCOS onto iSCSI requires the initiator and target information (IQN, LUN, etc.) to be passed to the kernel and the `coreos-installer`. A choice must be made between highly automated firmware integration (iBFT) and explicit manual configuration/scripting.

**Assumption**
iSCSI boot device is used

**Alternatives**

- Manual/Scripted iSCSI Configuration
- iBFT/Firmware-Based iSCSI Configuration

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Manual/Scripted iSCSI Configuration:** Allows explicit control over the entire iSCSI mounting and unmounting process utilizing **coreos-installer scripting hooks** (`--pre-install` / `--post-install`) to run `iscsiadm` commands manually. This is the standard method for implementing complex Day 1 storage logic that cannot be handled by firmware.
- **iBFT/Firmware-Based iSCSI Configuration:** Enables a more automated, cleaner configuration path for diskless machines by allowing the RHCOS installer to read the iSCSI parameters directly from the BIOS firmware during boot. This simplifies the kernel argument configuration during PXE/ISO boot.

**Implications**

- **Manual/Scripted iSCSI Configuration:** Higher setup complexity requiring maintenance of external scripts and detailed kernel parameter passing during boot, but offers maximum flexibility, especially if the firmware is older or iBFT support is unreliable.
- **iBFT/Firmware-Based iSCSI Configuration:** Requires ensuring BIOS/UEFI firmware is correctly configured to expose the iSCSI parameters. If not properly configured, installation will fail without manual overrides.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-32

**Title**
RHCOS Multipathing Enablement Strategy (Boot and Secondary Disks)

**Architectural Question**
Will multipathing be explicitly enabled for Red Hat Enterprise Linux CoreOS (RHCOS) disks (primary boot or secondary data disks) during installation to enhance resilience against hardware failure?

**Issue or Problem**
Multipathing is essential for highly available storage backends (especially iSCSI/Fibre Channel), providing redundant data paths. Failure to enable it at installation time prevents its use for the boot disk. Furthermore, secondary disks (like `/var/lib/containers`) require a different configuration mechanism (Ignition/Systemd) than the boot disk (Kernel Arguments).

**Assumption**
Installation Boot Device or Secondary Storage is a SAN device.

**Alternatives**

- Enable Multipathing at Installation Time
- Rely on Default Single-Path Configuration

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Enable Multipathing at Installation Time:** This is the recommended approach for providing stronger resilience.
  - **For Primary Boot Disks:** Configured via kernel arguments (`rd.multipath=default`) passed to the installer.
  - **For Secondary Data Disks:** Configured using **Ignition/Butane manifests** to define the necessary `multipathd` systemd units and filesystem mounts, ensuring consistency from Day 1.
- **Rely on Default Single-Path Configuration:** This avoids the complexity of installing Multipathd and configuring the device mapper during the Day 1 installation process. Suitable only if the underlying storage provides a single path or redundancy is handled at the array level.

**Implications**

- **Enable Multipathing at Installation Time:** Mandatory in setups where non-optimized paths result in I/O system errors.
  - **Boot Disk:** Requires explicit kernel arguments.
  - **Secondary Disk:** Requires maintaining custom Butane/Ignition manifests. Failure to configure the systemd units correctly via Ignition will result in secondary disks mounting as single paths, creating a hidden Single Point of Failure.
- **Rely on Default Single-Path Configuration:** Increases the vulnerability of the node to a Single Point of Failure (SPoF) if a network path, cable, or HBA connected to the storage array fails. Not recommended for production environments requiring high availability.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-33

**Title**
RHCOS Multipath Installation Target Naming

**Architectural Question**
When installing RHCOS onto a primary multipathed SAN storage device, should the `coreos-installer` target the generic device mapper path or the unique World Wide Name (WWN) symlink?

**Issue or Problem**
When multiple multipath devices are connected or device enumeration changes, using non-explicit device names can reduce installation reliability. A clear, persistent naming convention for the installation target device is required to maintain automation robustness.

**Assumption**
Installation Boot Device is SAN device.
Multipathing to be enabled.

**Alternatives**

- Use World Wide Name (WWN) Symlink
- Use Generic Device Mapper Path

**Decision**
#TODO: Document decision.#

**Justification**

- **Use World Wide Name (WWN) Symlink:** This approach is explicitly recommended when multiple multipath devices are connected to the machine, or when greater explicitness is required, because the symlink provides persistence in device identification. The WWN symlink is available in `/dev/disk/by-id` and represents the target multipathed device.
- **Use Generic Device Mapper Path:** This method simplifies the command line argument (e.g., `/dev/mapper/mpatha`).

**Implications**

- **Use World Wide Name (WWN) Symlink:** Requires an explicit step to identify the WWN ID of the target multipathed device, and the installation command must reference the persistent path (e.g., `/dev/disk/by-id/wwn-<wwn_ID>`).
- **Use Generic Device Mapper Path:** If multiple multipath devices exist or if device mapping changes unpredictably, this path may be less reliable for automated provisioning compared to the explicit WWN symlink.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-34

**Title**
RHCOS Installation Drive Identification Strategy

**Architectural Question**
How should the installation target disk device (e.g., local disk, non-multipath SAN LUN) be specified to the `coreos-installer` during Red Hat Enterprise Linux CoreOS (RHCOS) installation to ensure persistence and reliability?

**Issue or Problem**
Using ephemeral device paths (e.g., `/dev/sda`) can lead to installation failure or inconsistent behavior if the kernel enumerates devices differently across reboots or installations, disrupting automation scripts. A persistent naming convention is required for robust deployment automation.

**Assumption**
Installation target is a local disk or single-path SAN LUN.

**Alternatives**

- Volatile Device Path Naming
- Persistent Device Path Naming

**Decision**
#TODO: Document decision.#

**Justification**

- **Volatile Device Path Naming:** This approach simplifies command usage (e.g., using `/dev/sda`) and is explicitly allowed for the `coreos.inst.install_dev` kernel argument.
- **Persistent Device Path Naming:** This is the recommended practice for identifying devices (e.g., through `/dev/disk/by-id` symlinks). It prevents errors related to device enumeration changes upon reboot, which is critical for reliable automation and large-scale deployments. For multipath devices, using the World Wide Name (WWN) symlink available in `/dev/disk/by-id` is explicitly recommended over simpler paths.

**Implications**

- **Volatile Device Path Naming:** This carries a high risk of installation failure if the device naming changes (e.g., `/dev/sda` becomes `/dev/sdb`), which is common in environments where device enumeration is not strictly controlled.
- **Persistent Device Path Naming:** Requires an additional step in the automation workflow to identify the persistent device path (e.g., `by-id`, `by-path`, or `by-wwn`) of the target installation disk before executing `coreos-installer`.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-35

**Title**
Hardware RAID Configuration for Bare Metal Installation Drive

**Architectural Question**
How should hardware RAID be configured for the OpenShift Container Platform installation drive on bare metal nodes, ensuring compatibility with supported BMCs and adhering to Red Hat requirements?

**Issue or Problem**
The choice of hardware RAID must align with Red Hat requirements: only specific Hardware RAID volumes (e.g., Dell iDRAC, Fujitsu iRMC) are supported on the installation drive, and software RAID is not supported. This decision determines whether to utilize supported hardware RAID features or configure nodes without RAID for the installation drive.

**Assumption**
Installation Boot Device is Local Device.

**Alternatives**

- Configure and use supported Hardware RAID volumes for the installation drive.
- Configure the installation drive without using Hardware RAID.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Configure and use supported Hardware RAID volumes for the installation drive:** Leveraging hardware RAID provides disk redundancy and potential performance improvements managed entirely by the hardware controller/BMC interface, which is supported for specific configurations.
- **Configure the installation drive without using Hardware RAID:** This simplifies the underlying storage configuration and avoids potential compatibility issues, focusing solely on software volumes, although internal cluster components like etcd manage their own redundancy.

**Implications**

- **Configure and use supported Hardware RAID volumes for the installation drive:** Requires ensuring the hardware, BMC firmware, and RAID levels match the supported configurations (e.g., Dell iDRAC firmware 6.10.30.20+ for levels 0, 1, 5).
- **Configure the installation drive without using Hardware RAID:** Simplifies the underlying storage configuration, avoiding configuration complexities, but relies solely on software volumes for redundancy (e.g., etcd).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BM-36

**Title**
Control Plane Storage Performance Validation Strategy

**Architectural Question**
How will the storage performance for etcd (on control plane nodes) be validated to ensure cluster stability?

**Issue or Problem**
Etcd is extremely sensitive to disk write latency. If the storage cannot sustain a specific performance metric (fsync duration < 10ms at the 99th percentile), the cluster will experience instability, leader elections, and potential outages. A decision is needed on whether to enforce a strict pre-flight validation check or rely on hardware specifications.

**Assumption**
N/A

**Alternatives**

- Pre-flight Benchmark Validation (Strict)
- Specification-Based Provisioning (Standard)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Pre-flight Benchmark Validation (Strict):** This treats performance as a hard prerequisite. It creates a "Go/No-Go" gate based on real-world metrics. For example, running the standard Red Hat etcd test: `fio --rw=write --ioengine=sync --fdatasync=1 --directory=/var/lib/etcd ...`. If the 99th percentile result is > 10ms, the hardware is rejected. This guarantees stability but adds time to the provisioning process.
- **Specification-Based Provisioning (Standard):** This approach trusts the infrastructure provider's SLA. It significantly speeds up deployment by skipping manual testing. It is appropriate when using standardized, known-good SKUs (e.g., Enterprise NVMe or a specific Tier 1 SSD model) where performance variance is known to be low.

**Implications**

- **Pre-flight Benchmark Validation (Strict):** Requires a pre-install automation step to run the fio container (e.g., `quay.io/cloud-bulldozer/etcd-perf`) on bare metal. This catches "bad drives" or "noisy neighbor" issues early but increases deployment complexity.
- **Specification-Based Provisioning (Standard):** Removes the validation overhead. However, it introduces the risk of "silent" performance degradation where a disk meets the throughput spec but fails the latency requirement (fsync), which may only be discovered during a production outage.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert

---

## OCP-BM-37

**Title**
Bare Metal Minimum Boot Disk Capacity Strategy

**Architectural Question**
What is the standardized minimum capacity for the primary boot drive across the bare metal fleet to support lifecycle operations, logging, and partitioning requirements?

**Issue or Problem**
While OpenShift supports small boot drives (e.g., 120GB for SNO), advanced configurations such as separate `/var` partitioning, image pre-caching for edge upgrades (IBU), or retention of verbose failure logs require significantly more space. Failing to standardize on a sufficient minimum capacity prevents the adoption of these resiliency patterns later in the cluster lifecycle.

**Assumption**
**RHCOS Installation Boot Device Selection** has been defined.

**Alternatives**

- Minimal Capacity (e.g., 120GB)
- Expanded Capacity (e.g., 500GB or greater)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Minimal Capacity (e.g., 120GB):** Meets the absolute minimum requirements for a Single Node OpenShift (SNO) or standard node deployment. It reduces hardware costs but leaves very little headroom for Day 2 operations, log retention, or custom partitioning.
- **Expanded Capacity (e.g., 500GB or greater):** Recommended for production environments. This provides the necessary storage buffer to safely implement **General /var Partitioning**, store pre-cached update images (saving bandwidth at the edge), and retain system logs during failure triage without triggering disk pressure evictions.

**Implications**

- **Minimal Capacity (e.g., 120GB):** Severely restricts the ability to use custom disk partitioning. The separate `/var` partitioning strategy is **not recommended** and likely impossible on this size due to the overhead of the immutable OS partitions.
- **Expanded Capacity (e.g., 500GB or greater):** Increases the per-node hardware cost. Enables robust "Image-Based Upgrade" workflows by allowing multiple OS versions (stateroots) to coexist on the disk. Supports isolating volatile data (`/var`) to protect the root filesystem.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-38

**Title**
RHCOS /var Partitioning Strategy (General Data Isolation)

**Architectural Question**
Should the core RHCOS boot disk be partitioned to include a separate, dedicated partition for the entire `/var` directory to manage system log/data growth and simplify subsequent node reinstallation?

**Issue or Problem**
Allowing the potentially volatile contents of the `/var` directory (which holds data like logs and container images) to remain solely on the root partition risks system instability due to aggressive application logging or large data growth consuming the root filesystem space. Implementing a dedicated partition isolates this volatile data.

**Assumption**
The cluster will utilize large disk sizes (e.g., > 100GB) and may host applications requiring logging or large caches that reside in `/var`.

**Alternatives**

- Dedicated Partition for /var
- Co-locate /var on the Root Partition (Default)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Dedicated Partition for /var:** This approach prevents data growth within `/var` (such as audit data or logs) from filling up the root file system. It is recommended for disk sizes larger than 100GB, and especially larger than 1TB. This method also supports reinstalling OpenShift Container Platform while keeping the `/var` data intact, accelerating recovery by preventing the need for massive container pulls post-reinstall.
- **Co-locate /var on the Root Partition (Default):** This option relies on the default disk partitioning created during the RHCOS installation, which simplifies the initial configuration process.

**Implications**

- **Dedicated Partition for /var:** This configuration increases complexity during the installation process, as it requires setting up a custom MachineConfig manifest (e.g., using a Butane config). Additionally, when a separate `/var` partition is created, mixing different instance types for compute nodes is not supported if those instance types do not have the same storage device name.
- **Co-locate /var on the Root Partition (Default):** This configuration carries a high risk of disk exhaustion affecting system stability if container usage, logs, or other system data within `/var` is heavy or unpredictable.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-39

**Title**
Bare Metal Node OS Disk Partitioning for Container Storage

**Architectural Question**
How should the root disk be partitioned on bare metal nodes to accommodate container runtime storage (`/var/lib/containers`), specifically concerning separation from the operating system partition, and what filesystem options should be used?

**Issue or Problem**
If the container storage (`/var/lib/containers`) directory resides on the same partition as its parent filesystem (Root or `/var`), aggressive application logging or large image pull caches can lead to the node running out of disk space. This potentially causes instability by starving the OS or critical logging services.

**Assumption**
General /var Partitioning Strategy is defined.

**Alternatives**

- Dedicated partition for `/var/lib/containers`
- Co-locate `/var/lib/containers` on the parent partition (Root or `/var`)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Dedicated partition for `/var/lib/containers`:** This is the recommended approach for workload partitioning and robustness, explicitly setting up a separate partition, formatted with `xfs` and mounted using `prjquota` for appropriate resource handling. This practice isolates volatile container data storage from the core OS filesystems.
- **Co-locate `/var/lib/containers` on the parent partition (Root or `/var`):** Simplifies the initial installation process by relying on the default partitioning scheme. However, this risks system instability if container images or ephemeral volumes consume excessive disk space, impacting the underlying filesystem.

**Implications**

- **Dedicated partition for `/var/lib/containers`:** Requires custom Ignition configuration overrides within the installation manifest (e.g., `ClusterInstance` or `BareMetalHost` definition). This adds complexity to the installation process.
- **Co-locate `/var/lib/containers` on the parent partition (Root or `/var`):** Higher risk of disk exhaustion affecting system stability if container usage is heavy or unpredictable. Management of disk quotas becomes less granular.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-40

**Title**
Control Plane Etcd Storage Partitioning Strategy

**Architectural Question**
Should etcd data storage (`/var/lib/etcd`) on control plane nodes be isolated onto a dedicated partition separate from the root (or `/var`) filesystem to ensure performance and prevent resource conflicts?

**Issue or Problem**
Etcd is extremely sensitive to disk performance, requiring a 10 ms p99 fsync duration. If etcd data is co-located with other volatile system data (logs, container images), aggressive writing or system maintenance operations may introduce contention and jitter, risking cluster instability and leader elections.

**Assumption**
General /var Partitioning Strategy is defined.

**Alternatives**

- Dedicated partition for `/var/lib/etcd`
- Co-locate `/var/lib/etcd` on the parent partition

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Dedicated partition for `/var/lib/etcd`:** This separates the critical etcd workload from the operating system and other volatile system data (like logs in `/var/log`), mitigating the risk of data growth or I/O contention affecting etcd performance.
- **Co-locate `/var/lib/etcd` on the parent partition:** This is the default RHCOS partitioning scheme, simplifying the initial installation process by avoiding custom Ignition configurations.

**Implications**

- **Dedicated partition for `/var/lib/etcd`:** Requires custom MachineConfig or Butane manifest configurations during the installation phase to define and mount the separate partition.
- **Co-locate `/var/lib/etcd` on the parent partition:** Increases the risk of disk exhaustion or I/O contention affecting etcd, potentially leading to performance instability or cluster outages if the underlying storage does not meet the strict latency requirements.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-41

**Title**
RHCOS Partition Retention Strategy during Reinstallation (UPI)

**Architectural Question**
When reinstalling Red Hat Enterprise Linux CoreOS (RHCOS) on User-Provisioned Infrastructure (UPI) nodes, should existing data partitions be automatically preserved or overwritten, and which mechanism should be used?

**Issue or Problem**
When performing an RHCOS reinstallation, particularly to recover a node or perform an OS upgrade, existing data partitions (e.g., separate `/var` partitions created during Day 1 configuration) must either be explicitly preserved or risk being overwritten by the `coreos-installer`. A strategy is needed to ensure continuity of data or configuration residing on these preserved partitions.

**Assumption**
N/A

**Alternatives**

- Retain Existing Partitions (By Label or Index)
- Overwrite All Partitions (Clean Slate Installation)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Retain Existing Partitions (By Label or Index):** This allows for preservation of non-OS data (e.g., application logs, `/var/lib/containers` contents) during a reinstall or upgrade, accelerating recovery by preventing the need for massive container pulls post-reinstall. This is achieved using `coreos-installer` arguments like `--save-partlabel` or `--save-partindex`.
- **Overwrite All Partitions (Clean Slate Installation):** This is the default or simplified approach where all existing data is wiped clean, ensuring no remnants of old partitions interfere with the new installation. This is simpler operationally but results in data loss if external backups are not used.

**Implications**

- **Retain Existing Partitions (By Label or Index):** Requires meticulous use of specific kernel arguments (e.g., `coreos.inst.save_partlabel=data*` or `coreos.inst.save_partindex=5-`) during the PXE/ISO boot process. Increases complexity during the OS installation phase.
- **Overwrite All Partitions (Clean Slate Installation):** Requires applications and storage layers to handle the recreation and re-synchronization of all data post-installation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BM-42

**Title**
Bare Metal Node Image Pre-caching Strategy for Disconnected/Edge Deployments

**Architectural Question**
How will required container images (OCP release, operators, application base images) be transferred and prepared on bare metal edge nodes prior to or during installation/upgrade to minimize network latency and bandwidth dependency?

**Issue or Problem**
In disconnected environments or at the far edge, pulling large container images during installation or upgrade (JIT pull) can be slow or unreliable. A structured method is needed to pre-position images on the node's container storage partition, supporting efficient Zero Touch Provisioning (ZTP) and Image-Based Upgrades (IBU).

**Assumption**
Provisioning workflow is GitOps ZTP.
Cluster is on the edge.
Nodes utilize disk partitioning to include a shared container partition (`/var/lib/containers`).

**Alternatives**

- Client-side Image Pre-caching via Ignition/IBU
- Just-In-Time (JIT) Pull during Installation and Runtime

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Client-side Image Pre-caching via Ignition/IBU:** This method significantly reduces installation time and network load, which is critical for far edge or constrained environments. It integrates seamlessly with ZTP using `ignitionConfigOverride` (configured via `ClusterInstance`) to configure mount points and launch services to extract pre-cached images before the cluster installation fully proceeds..
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

## OCP-BM-43

**Title**
Internal Image Registry Management State on Bare Metal UPI

**Architectural Question**
Should the built-in Image Registry Operator's default `Removed` state on bare metal User-Provisioned Infrastructure (UPI) clusters be explicitly switched to `Managed` post-installation, or should the platform rely exclusively on an external image registry?

**Issue or Problem**
On bare metal UPI environments that do not provide default shared storage, the OpenShift Image Registry Operator bootstraps itself in a `Removed` management state to allow installation to complete. If the registry remains `Removed`, image building and pushing of application images are disabled. A decision is required to determine the long-term image hosting strategy (internal or external) and mandate the necessary post-installation operational steps.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Switch Internal Registry to Managed State Post-Install
- Maintain Removed State (Rely Exclusively on External Registry)

**Decision**
#TODO: Document decision.#

**Justification**

- **Switch Internal Registry to Managed State Post-Install:** This enables the use of the built-in, cluster-managed image registry. This simplifies integration with OpenShift builds and standard platform services once appropriate persistent storage is provisioned.
- **Maintain Removed State (Rely Exclusively on External Registry):** This approach minimizes the cluster footprint and ensures that all core OCP components and applications rely on an existing external corporate image registry (e.g., Quay, Artifactory, Nexus), leveraging existing security and management infrastructure.

**Implications**

- **Switch Internal Registry to Managed State Post-Install:** Requires manual intervention by the cluster administrator to edit the `configs.imageregistry/cluster` resource to change `managementState: Removed` to `Managed` after installation. Subsequently, persistent storage must be configured (RWX is required for high availability).
- **Maintain Removed State (Rely Exclusively on External Registry):** Disables the ability to use the cluster’s internal image building capabilities, requiring all image dependencies (including custom RHOAI notebook images) to be pulled from the external registry. The cluster network must allow external pull access for all nodes and application namespaces must be configured with pull secrets.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BM-44

**Title**
Storage Architecture for the Internal Image Registry

**Architectural Question**
How should storage be architected for the OpenShift Internal Image Registry, balancing bare metal infrastructure limitations (RWO/RWX availability) with performance, enterprise object storage requirements, and non-production simplicity?

**Issue or Problem**
OpenShift Container Platform's internal image registry requires high-availability storage (supporting multiple replicas) for production clusters. On bare metal, achieving native ReadWriteMany (RWX) access is challenging. A decision must be made between deploying complex RWX solutions, utilizing dedicated Object Storage (S3 API), settling for low-resilience ReadWriteOnce (RWO) storage, or utilizing ephemeral storage for non-critical environments.

**Assumption**
Internal Image Registry Management State is set to "Managed".

**Alternatives**

- Dedicated Object Storage (S3 API Compatible)
- ReadWriteMany (RWX) Access Mode (PVC)
- ReadWriteOnce (RWO) Access Mode (PVC)
- Ephemeral Storage (EmptyDir)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Dedicated Object Storage (S3 API Compatible):** This approach leverages object storage (such as Red Hat OpenShift Data Foundation's Multicloud Gateway or an external S3 provider) for the image repository. Object storage is highly scalable and natively supports high availability (HA) required for image registries. ODF is the preferred option when Object (MCG) storage capabilities are necessary.
- **ReadWriteMany (RWX) Access Mode (PVC):** This access mode is required to deploy an image registry that supports high availability with two or more replicas. It is typically implemented using shared file system storage.
- **ReadWriteOnce (RWO) Access Mode (PVC):** This access mode is supported only when the image registry has one replica and explicitly requires the `Recreate` rollout strategy during upgrades.
- **Ephemeral Storage (EmptyDir):** This simplifies configuration and is available only for non-production clusters. It minimizes setup complexity as no underlying persistent storage solution is required.

**Implications**

- **Dedicated Object Storage (S3 API Compatible):** Requires the installation and maintenance of an Object Storage solution (e.g., ODF/MCG). This decouples image storage scalability from local block or file storage limitations.
- **ReadWriteMany (RWX) Access Mode (PVC):** Requires coordination to provision storage that supports RWX access mode, which is necessary for HA scaled registries.
- **ReadWriteOnce (RWO) Access Mode (PVC):** The cluster must accept reduced resiliency, as the registry cannot have more than one replica. Block storage volumes, which typically use RWO, are supported but explicitly not recommended for use with the image registry on production clusters.
- **Ephemeral Storage (EmptyDir):** **All container images are lost** if the registry pod restarts or the node fails. This configuration must be used for only non-production clusters (e.g., Lab/Sandbox) where image rebuilds are acceptable.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BM-45

**Title**
Internal Image Registry Persistent Volume Claim (PVC) Provisioning Strategy

**Architectural Question**
Should the Persistent Volume Claim (PVC) required for the OpenShift Internal Image Registry storage be instantiated automatically using cluster defaults, or manually pre-provisioned for explicit configuration control?

**Issue or Problem**
The image registry must have persistent storage to operate in a managed/production state. Relying solely on the cluster default storage configuration (automatic PVC creation) may result in inadequate size, performance, or access mode configuration necessary for HA production registries (which typically require ReadWriteMany access).

**Assumption**
The Internal Image Registry will be switched to the Managed management state post-installation.

**Alternatives**

- Rely on Default Automatic PVC Creation
- Manually Pre-provision Custom PVC

**Decision**
#TODO: Document decision.#

**Justification**

- **Rely on Default Automatic PVC Creation:** This approach minimizes configuration complexity as the default OpenShift setting creates an `image-registry-storage` PVC automatically when the `claim` field is left blank in the registry configuration.
- **Manually Pre-provision Custom PVC:** This method allows administrators to define explicit storage parameters, such as access mode (RWX is required for two or more replicas/HA) and capacity, and ensures compatibility if specialized requirements exist, such as using block storage with a `Recreate` rollout strategy.

**Implications**

- **Rely on Default Automatic PVC Creation:** The resulting storage configuration is bound by the cluster's default StorageClass, which may not meet the high-availability requirements (e.g., if the default StorageClass only provides ReadWriteOnce access).
- **Manually Pre-provision Custom PVC:** Requires creating a PersistentVolumeClaim object (e.g., via a `pvc.yaml` file) and explicitly editing the registry configuration to reference the custom PVC, adding manual complexity to the installation and setup process.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## OCP-BM-46

**Title**
Bare Metal Kernel Selection: Real-Time Kernel Implementation

**Architectural Question**
Should the OpenShift Container Platform nodes leverage the Real-Time Kernel for low-latency performance, and how will this requirement be enforced and configured across the cluster nodes?

**Issue or Problem**
Bare metal deployments for demanding workloads, such as virtual Distributed Unit (vDU) applications in Telco environments, require guaranteed low latency and high performance. The standard RHCOS kernel may introduce unacceptable jitter or delay, necessitating the use of the Real-Time (RT) kernel.

**Assumption**
Low-latency workloads are required, consistent with the Hardware Acceleration Strategy.

**Alternatives**

- Enable Real-Time Kernel via Performance Profile
- Use Default Standard Kernel

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

## OCP-BM-47

**Title**
Simultaneous Multithreading (SMT) Configuration Strategy

**Architectural Question**
Should Simultaneous Multithreading (SMT), often referred to as hyperthreading, be globally enabled or disabled on cluster nodes via the installation configuration?

**Issue or Problem**
SMT is enabled by default to increase core performance and maximize resource efficiency. However, disabling SMT is sometimes required for strict security profiles (to mitigate side-channel attacks) or specific performance-critical workloads (like vDU or high-frequency trading) that require dedicated physical cores to eliminate "noisy neighbor" interference on the pipeline.

**Assumption**
N/A

**Alternatives**

- SMT Enabled (Default)
- SMT Disabled (Security/Performance Optimized)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **SMT Enabled (Default):** This maximizes the total thread count and overall throughput of the machine. It is the standard setting for general-purpose container workloads.
- **SMT Disabled (Security/Performance Optimized):** Disabling SMT provides stronger CPU isolation. This is often mandatory for Real-Time/vDU workloads to guarantee deterministic latency, or for environments requiring mitigation of specific processor side-channel vulnerabilities (e.g., L1TF/Foreshadow) where software mitigation is insufficient.

**Implications**

- **SMT Enabled (Default):** May leave the cluster vulnerable to specific side-channel security threats inherent to hyperthreading architectures. Latency-sensitive applications may experience jitter due to thread contention on the same physical core.
- **SMT Disabled (Security/Performance Optimized):** Dramatically decreases the total vCPU capacity of the cluster (typically by 50%). This requires careful capacity planning and potentially increases the hardware footprint/subscriptions required. This setting is applied via the `install-config.yaml` (compute/controlPlane hyperthreading) or Day 2 MachineConfigs.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-48

**Title**
Workload Partitioning (CPU Isolation)

**Architectural Question**
What strategy will be implemented for dedicating CPU resources (workload partitioning) to isolate performance-sensitive tenant workloads from host and OpenShift platform processes?

**Issue or Problem**
For bare metal deployments hosting performance-critical or low-latency workloads (like RAN Distributed Units, or vDU applications), unpartitioned CPU usage leads to performance jitter due to contention between application pods and platform/kernel components. Defining isolated and reserved CPU sets is critical to meet required performance constraints.

**Assumption**
Low-latency workloads are required.

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

## OCP-BM-49

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

## OCP-BM-50

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

## OCP-BM-51

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

## OCP-BM-52

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

## OCP-BM-53

**Title**
Bare Metal Firmware Update Application Timing Policy

**Architectural Question**
When leveraging the Bare Metal Operator (BMO) for node firmware management (BIOS, BMC, NICs) via `HostFirmwareComponents` or `HostFirmwareSettings`, should updates be applied immediately (live update) or deferred until a scheduled node reboot?

**Issue or Problem**
This decision defines whether disruptive firmware updates are applied immediately (requiring coordination) or aligned with planned OS reboots, balancing rapid deployment against maximum control and reliability.

**Assumption**
The Bare Metal Operator (BMO) is enabled and managing node firmware configurations.

**Alternatives**

- Immediate Application (Live Update) (TP)
- Deferred Application (Update on Next Reboot)

**Decision**
#TODO: Document decision.#

**Justification**

- **Immediate Application (Live Update) (TP):** This option allows for rapid deployment of firmware updates, as the firmware change is performed while the host is provisioned or active. This can be achieved by utilizing BMO's advanced features, such as `HostFirmwareSettings` live updates.
- **Deferred Application (Update on Next Reboot):** This method provides maximum control and reliability, ensuring that disruptive firmware updates are performed during a planned maintenance window or scheduled operating system reboot. This approach requires setting the `HostUpdatePolicy` resource to `onReboot`.

**Implications**

- **Immediate Application (Live Update) (TP):** Live updates to the BMC are generally not recommended for testing, especially on earlier generation hardware. This process may cause node disruption and require coordination (e.g., node draining). Some advanced features supporting this may also be Technology Preview (TP).
- **Deferred Application (Update on Next Reboot):** This simplifies maintenance coordination by aligning the disruptive firmware update process with the operating system update schedule. This requires defining, testing, and maintaining the `HostUpdatePolicy` Custom Resource.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-54

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
- **Node Health Check (NHC) with BareMetal Operator (BMO) Remediation:** This is the most robust, fully automated solution. It attempts to recover the node by "turning it off and on again" via its BMC.

**Implications**

- **No Automated Remediation:** High operational burden and slow recovery times. Not recommended for a production cluster.
- **Node Health Check (NHC) with Self Node Remediation:** Provides software-level remediation. It ensures workloads are moved but does not fix the underlying node, which will remain unavailable until manually repaired.
- **Node Health Check (NHC) with BareMetal Operator (BMO) Remediation:** This requires a reliable IPI installation and stable Redfish/IPMI connectivity. The BMO facilitates the Cluster API management of compute nodes (TP) for dynamic lifecycle management. It also enables access to advanced operational features, such as firmware management via HostFirmwareSettings/HostFirmwareComponents, including live updates (TP).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---
