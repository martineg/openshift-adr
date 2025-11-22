# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Networking

## OCP-NET-01

**Title**
Machine IP Range

**Architectural Question**
Which IP address range will be used for the cluster nodes (control plane, compute machines)?

**Issue or Problem**
The machine network CIDR defines the node IP range. This range must be routable within the organization's network for administrative access and communication with infrastructure services (DNS, NTP).

**Assumption**
N/A

**Alternatives**

- Default Machine Network CIDR
- Custom Machine Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Machine Network CIDR:** Uses the default CIDR suggested by the installation program (Platform Specific, e.g., 10.0.0.0/16 for IPI). This simplifies setup if the range does not conflict with existing networks.
- **Custom Machine Network CIDR:** Required if the default range conflicts with existing data center networks, or if specific IP address schemes must be followed for compliance or network segmentation purposes.

**Implications**

- **Default Machine Network CIDR:** Requires verification that this range is unique and non-overlapping within the organizational network.
- **Custom Machine Network CIDR:** This range must be routable within the organization's existing network infrastructure (firewalls, routers) to ensure control plane and worker nodes can communicate with infrastructure services (DNS, NTP).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-02

**Title**
Node IP Address Management

**Architectural Question**
How will the cluster nodes (Control Plane and Compute) obtain their IP addresses from the Machine IP Range?

**Issue or Problem**
IP Address Management (IPAM) affects node address predictability, critical for setup, security policies, and installation method compatibility.

**Assumption**
N/A
**Alternatives**

- DHCP
- Static IP Configuration

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **DHCP:** Simplifies node provisioning by automatically assigning IPs. Reduces manual configuration.
- **Static IP Configuration:** Ensures persistent, predictable node IPs, often required by enterprise network/security policies, especially in production.

**Implications**

- **DHCP:** Requires a highly available DHCP server, ideally with reservations. Simplifies node scaling/replacement.
- **Static IP Configuration:** Increases manual configuration effort during install and scaling. Requires a robust external IPAM process to avoid conflicts.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-03

**Title**
DNS Forwarding Configuration

**Architectural Question**
How will the cluster's internal DNS resolve external hostnames?

**Issue or Problem**
Cluster-internal DNS (CoreDNS) forwards requests for external domains to upstream resolvers. This behavior might need overriding to use specific enterprise DNS servers.

**Assumption**
N/A

**Alternatives**

- Default DNS Forwarding (Use Node's Upstream Resolvers)
- Override DNS Forwarding (Specify Upstream Corporate DNS Servers)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Forwarding:** Standard behavior, sufficient if node-level DNS resolvers (from DHCP or static config) correctly reach all required internal/external domains.
- **Override Forwarding:** Explicitly directs cluster DNS queries to specific corporate DNS servers. Necessary when node resolvers are unsuitable or fine-grained control is required (e.g., split DNS).

**Implications**

- **Default:** Relies on correct underlying infrastructure network config (DHCP options, node setup).
- **Override:** Cluster external name resolution depends on availability/correctness of specified upstream DNS servers. Managed via `dns.operator.openshift.io` CR.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-04

**Title**
Node Name Resolution Strategy (DNS Search Zone vs FQDN)

**Architectural Question**
How will OpenShift ensure the Kubernetes API server can reliably resolve node names when they are potentially distributed across different network zones?

**Issue or Problem**
If nodes reside in different zones, relying solely on short hostnames may cause resolution failure unless a default DNS search zone is correctly configured.

**Assumption**
Nodes might be distributed across different network zones/failure domains.

**Alternatives**

- Rely on Default DNS Search Zone Configuration
- Enforce Full FQDN Resolution for all Node Objects and DNS Requests

**Decision**
#TODO: Document decision.#

**Justification**

- **Rely on Default DNS Search Zone Configuration:** This allows the API server to successfully resolve hostnames based on short names by leveraging the configured search path.
- **Enforce Full FQDN Resolution for all Node Objects and DNS Requests:** This supported approach ensures unambiguous reference to hosts by their fully-qualified domain names in all DNS requests and node objects, removing reliance on zone-specific DNS search paths.

**Implications**

- **Rely on Default DNS Search Zone Configuration:** This approach requires careful configuration of the default DNS search zone to allow the API server to correctly resolve node names across zones.
- **Enforce Full FQDN Resolution for all Node Objects and DNS Requests:** This requires meticulous, consistent configuration to ensure FQDNs are used everywhere (node objects and DNS records).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-05

**Title**
Cluster Core Time Synchronization Source

**Architectural Question**
What specific time synchronization source (Public vs. Internal/Enterprise NTP) will be configured for OpenShift Container Platform nodes by default to maintain chrony stability?

**Issue or Problem**
Accurate time synchronization is critical for cluster operation (etcd stability, certificate validity, logging consistency). By default, OpenShift clusters use a public NTP server, which must be overridden if the deployment is disconnected or requires synchronization with a highly accurate internal enterprise time service for compliance.

**Assumption**
N/A

**Alternatives**

- Rely on Public NTP Server (Default)
- Configure Internal Enterprise NTP Server (Custom)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Rely on Public NTP Server (Default):** Simplifies deployment when direct internet access is available, leveraging widely used and reliable time sources.
- **Configure Internal Enterprise NTP Server (Custom):** Essential for disconnected environments or environments requiring time synchronization only from internal, authenticated, or compliant enterprise sources.

**Implications**

- **Rely on Public NTP Server (Default):** Requires open firewall egress rules to external NTP sources (UDP port 123) for all nodes, which may conflict with network security policies.
- **Configure Internal Enterprise NTP Server (Custom):** Requires defining and managing the internal time servers (via chrony service configuration) in the cluster setup, often necessary if the cluster is deployed in a disconnected network.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-NET-06

**Title**
Outbound Connectivity (External Firewall/Proxy)

**Architectural Question**
How will cluster egress traffic destined for external networks (e.g., Internet, other corporate networks) be managed by external firewalls and/or proxies?

**Issue or Problem**
Corporate security requires controlling outbound connections. This impacts cluster installation, updates, OperatorHub access, workload external service access, and requires coordination with network security teams.

**Assumption**
Cluster is in a connected environment.

**Alternatives**

- Direct Outbound (Potentially behind Firewall Rules)
- Via HTTP/S Proxy Server

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Direct Outbound:** Simplifies cluster configuration if external firewalls allow required traffic (potentially restricted by rules).
- **Via HTTP/S Proxy:** Necessary when direct outbound access is blocked. Centralizes egress control and filtering at the proxy server, aligning with common enterprise security patterns.

**Implications**

- **Direct Outbound:** Requires firewall rules allowing access to Red Hat registries, telemetry, cloud APIs (if applicable), and any external services needed by workloads. Firewall rule management is critical.
- **Via Proxy:** Requires configuring OpenShift cluster-wide proxy settings during installation (for core components) and potentially per-workload proxy settings. Cluster functionality depends on proxy availability and correct configuration (including trusting proxy CA).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-07

**Title**
Outbound HTTPS Trust Management Strategy (Proxy/Custom CA)

**Architectural Question**
When utilizing an HTTPS proxy or connecting to external services signed by a corporate Certificate Authority (CA), how will the cluster ensure that the custom CA is trusted by RHCOS nodes and core components?

**Issue or Problem**
If a cluster uses an HTTPS proxy whose identity certificate is signed by an authority not present in the default Red Hat Enterprise Linux CoreOS (RHCOS) trust bundle, core cluster functionality (updates, OperatorHub access, provisioning) will fail unless the custom CA is added to the system trust store.

**Assumption**
Outbound Connectivity utilizes an HTTPS proxy or connects to external services requiring a custom trust chain.

**Alternatives**

- Rely Solely on Default RHCOS Trust Bundle (No Custom CA)
- Augment Trust Bundle via additionalTrustBundle Configuration

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Rely Solely on Default RHCOS Trust Bundle (No Custom CA):** This simplifies installation as no additional configuration or external CA management is required, relying entirely on the CAs provided by the RHCOS system trust bundle.
- **Augment Trust Bundle via additionalTrustBundle Configuration:** This is required if the proxy's identity certificate is signed by an authority outside the RHCOS trust bundle, allowing the installation program to generate a Config Map (`user-ca-bundle`) that merges the custom CA with the RHCOS trust bundle.

**Implications**

- **Rely Solely on Default RHCOS Trust Bundle (No Custom CA):** Connection to corporate proxy servers or external services that rely on internal CAs will fail, leading to cluster functional failures (e.g., updates, image pulls) if the proxy is mandatory.
- **Augment Trust Bundle via additionalTrustBundle Configuration:** Requires the administrator to obtain and correctly configure the CA certificate in the `install-config.yaml` file, creating a dependency on the correct management of this custom trust store.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-08

**Title**
Custom CA Trust Bundle Application Policy

**Architectural Question**
When augmenting the cluster's default trust bundle with a custom Certificate Authority (CA) via `additionalTrustBundle`, should the resultant trusted CA ConfigMap be applied only when a cluster-wide proxy is configured, or should it be referenced universally?

**Issue or Problem**
The `additionalTrustBundlePolicy` configuration dictates whether the custom trust bundle ConfigMap (`user-ca-bundle`) is referenced in the cluster's Proxy object only (`Proxyonly`) or always (`Always`), impacting cluster connectivity assurance, especially if the proxy configuration changes post-installation.

**Assumption**
A trust bundle via additionalTrustBundle configuration is used to configure Certificate Authority (CA).

**Alternatives**

- Proxy-Only Policy (Default)
- Always-Apply Policy

**Decision**
#TODO: Document decision.#

**Justification**

- **Proxy-Only Policy (Default):** This leverages the default cluster setting where the custom CA trust bundle is referenced only when the HTTP/HTTPS proxy is configured. This simplifies configuration if the proxy is transient or optional.
- **Always-Apply Policy:** This ensures the custom CA is always referenced by the Proxy object's trusted CA field. This is useful if critical external services, regardless of proxy usage, rely on the custom CA, guaranteeing consistency even if the cluster proxy configuration is removed or disabled.

**Implications**

- **Proxy-Only Policy (Default):** Requires setting `additionalTrustBundlePolicy` to `Proxyonly` or omitting the field, as `Proxyonly` is the default value. If the cluster proxy is disabled or removed, the custom CA may stop being referenced by the Proxy object's trusted CA field.
- **Always-Apply Policy:** Requires explicitly setting the `additionalTrustBundlePolicy` parameter to `Always`. This establishes a hard dependency on the correct management of the CA certificate provided in the `additionalTrustBundle` field.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-09

**Title**
External Firewall Rule Granularity (Connected Environments)

**Architectural Question**
If using direct outbound connectivity (behind firewalls) in a connected environment, how granular will the firewall rules be?

**Issue or Problem**
Firewall rules for direct outbound access must balance security (least privilege) with operational feasibility (allowing necessary Red Hat and workload traffic).

**Assumption**
Cluster is in a connected environment and outbound connectivity is set to Direct Outbound.

**Alternatives**

- Open/Broad Firewall Policy
- Restricted Firewall Policy (Whitelisting specific FQDNs/IPs)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Open/Broad Policy:** Simplifies operations, allowing broad cluster access to external resources (e.g., allow all HTTPS outbound). Assumes security is managed elsewhere (e.g., higher-level firewalls).
- **Restricted Policy:** Enforces least privilege, allowing communication only with documented Red Hat endpoints and required third-party services. Essential for high-security environments.

**Implications**

- **Open Policy:** Increases cluster security surface area. Simpler firewall management.
- **Restricted Policy:** Requires rigorous maintenance to track/update necessary external FQDNs/IPs for OCP updates, telemetry, OperatorHub, cloud APIs, etc. Changes by Red Hat or providers require immediate firewall updates.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-10

**Title**
Load Balancer Strategy (API & Ingress)

**Architectural Question**
Which load balancer solution will expose the OpenShift API and application ingress traffic?

**Issue or Problem**
A load balancer is needed for external access to the cluster API and applications. Choice impacts cost, performance, features, automation, and operational responsibility.

**Assumption**
N/A

**Alternatives**

- Default Platform Load Balancer (Cloud Provider LBaaS / On-Prem Keepalived/HAProxy)
- User-Managed Load Balancer (e.g., F5, NetScaler, external HAProxy)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Platform Load Balancer:** Leverages tightly integrated, automatically configured LB (cloud native service or built-in on-prem solution). Simplest approach, especially with IPI.
- **User-Managed Load Balancer:** Utilizes existing enterprise-standard LB offering advanced features, specific security compliance, and aligning with current operational workflows. Required for UPI.

**Implications**

- **Default:** Functionality limited by the platform's default LB. Configuration managed automatically by OCP (simpler but less flexible). Cost typically included or based on cloud usage.
- **User-Managed:** Requires manual configuration and integration for API and Ingress Operator Services. Operations team retains full control and responsibility (lifecycle, HA, features). Adds operational overhead but allows advanced customization. The Load Balancer MUST be configured to use the /readyz endpoint (not a generic TCP check) for the Kubernetes API pool. The LB must probe every 5-10 seconds and remove the API server instance from the pool within 30 seconds of /readyz returning an error. Failure to configure this correctly will result in API instability and traffic blackholing during node updates.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-NET-11

**Title**
API and Application Ingress Load Balancer Topology Strategy

**Architectural Question**
Should the Kubernetes API and Application Ingress endpoints be exposed via a single, consolidated load balancer instance, or should they utilize separate, dedicated load balancer infrastructure?

**Issue or Problem**
Consolidating Kubernetes API (TCP 6443) and application ingress traffic (TCP 80/443) onto a single load balancer instance complicates scaling and isolation, risking performance degradation if application traffic impacts critical cluster API availability.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Consolidated Load Balancer Model
- Separate Load Balancer Model (Recommended for Production)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Consolidated Load Balancer Model:** Simplifies the load balancing infrastructure by utilizing a single instance to handle both the Kubernetes API and application Ingress traffic.
- **Separate Load Balancer Model (Recommended for Production):** This approach provides the ability to scale the load balancer infrastructure for the API and application ingress traffic in isolation. This separation is recommended for production scenarios.

**Implications**

- **Consolidated Load Balancer Model:** If session persistence is configured for the API load balancer, it might cause performance issues from excess application traffic. Deploying both on the same infrastructure increases the risk of application traffic impacting the Kubernetes API availability.
- **Separate Load Balancer Model (Recommended for Production):** Requires provisioning and managing at least two distinct load balancer instances (or pools of instances), increasing infrastructure complexity and cost.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-NET-12

**Title**
CNI Plugin Selection (Platform Specific)

**Architectural Question**
Which Container Network Interface (CNI) plugin will manage Pod networking?

**Issue or Problem**
The CNI plugin choice impacts network features, performance, and integration with the underlying infrastructure (especially relevant for OpenStack).

**Assumption**
N/A

**Alternatives**

- **Default:** OVN-Kubernetes CNI (Platform Agnostic)
- **OpenStack Specific:** Kuryr-Kubernetes CNI

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OVN-Kubernetes CNI:** Standard, platform-agnostic OCP networking stack. Creates a virtual overlay network independent of underlying infrastructure. Generally recommended for simplicity and consistency.
- **Kuryr-Kubernetes CNI (OpenStack Only):** Achieves higher network performance on OpenStack by eliminating "double overlay". Creates Neutron ports for pods and uses Octavia LBs for services. Makes pods first-class OpenStack network citizens.

**Implications**

- **OVN-Kubernetes:** Simplest, standard, universally supported. Performance usually sufficient. Traffic traverses OCP SDN overlay.
- **Kuryr (OpenStack Only):** Significant performance benefits, simplified network tracing (pod IPs visible on OSP network). Consumes Neutron ports rapidly, risking quota exhaustion. More complex configuration, specialized CNI.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader (Especially for OpenStack decision)

---

## OCP-NET-13

**Title**
Pod Network CIDR Selection

**Architectural Question**
Which internal IP address range will be used for Pod networking?

**Issue or Problem**
The Pod network CIDR provides IPs for pods within the cluster's SDN. It must not overlap with any existing network reachable from the cluster (including Machine and Service networks) to avoid routing failures.

**Assumption**
N/A

**Alternatives**

- Default Pod Network CIDR (e.g., 10.128.0.0/14)
- Custom Pod Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Pod Network CIDR:** Use defaults for simplicity when confirmed not to overlap.
- **Custom Pod Network CIDR:** Specify a custom range when the default overlaps with existing networks, ensuring correct pod routing to/from external services.

**Implications**

- **Default:** Simplifies installation but requires enterprise-wide network validation to prevent conflicts.
- **Custom:** Requires pre-planning and coordination with network admins to select an appropriate unused IP range.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-14

**Title**
Service Network CIDR Selection

**Architectural Question**
Which IP address range will be used for the Cluster Service network?

**Issue or Problem**
A dedicated, non-overlapping IP range is needed for ClusterIP Services. Conflicts with existing networks will make cluster services unreachable.

**Assumption**
N/A

**Alternatives**

- Default Service Network CIDR (e.g., 172.30.0.0/16)
- Custom Service Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Service Network CIDR:** Use defaults for simplicity when confirmed not to overlap.
- **Custom Service Network CIDR:** Specify a custom range when the default overlaps, preventing routing conflicts and ensuring service reachability.

**Implications**

- **Default:** Simplifies installation. Failure to verify non-overlap leads to service connectivity issues.
- **Custom:** Requires coordination with the network team to select and reserve a suitable IP range provided during installation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-15

**Title**
Advanced CNI Parameter Configuration Strategy (Install-Config vs Custom Manifest)

**Architectural Question**
Should critical, Container Network Interface (CNI)-specific network parameters (e.g., IPsec mode, MTU, Geneve port, internal OVN subnets) be configured directly in the primary installation configuration file or via subsequent custom Cluster Network Operator manifests?

**Issue or Problem**
OpenShift installation splits network configuration into two phases: Phase 1 (pre-manifest creation, via `install-config.yaml`) and Phase 2 (post-manifest creation, via custom manifest files). Relying solely on Phase 1 limits access to specialized CNI settings (like OVN-Kubernetes parameters), while relying on Phase 2 requires creating extra files, and crucially, Phase 2 configurations cannot override conflicting settings already defined in Phase 1.

**Assumption**
Advanced network configuration (e.g., OVN-Kubernetes customization) is required.

**Alternatives**

- Configure CNI Parameters via Install-Config (Phase 1)
- Configure CNI Parameters via Custom Manifests (Phase 2)

**Decision**
#TODO: Document decision.#

**Justification**

- **Configure CNI Parameters via Install-Config (Phase 1):** This phase defines high-level network fields like `networking.networkType`, `networking.clusterNetwork`, and `networking.serviceNetwork`. This approach simplifies the overall setup as these values are managed directly within the primary installation file.
- **Configure CNI Parameters via Custom Manifests (Phase 2):** This method is used to specify advanced network configurations that are not directly available in Phase 1. Creating a customized Cluster Network Operator manifest (e.g., `cluster-network-03-config.yml`) allows defining specific CNI settings, such as enabling IPsec for OVN-Kubernetes or overriding OVN overlay parameters like MTU or Geneve Port.

**Implications**

- **Configure CNI Parameters via Install-Config (Phase 1):** The available configuration options are limited to the high-level network fields present in the initial `install-config.yaml`.
- **Configure CNI Parameters via Custom Manifests (Phase 2):** Requires manually creating and maintaining a supplementary manifest file (`cluster-network-03-config.yml`). Furthermore, administrators must be aware that the values defined in these custom manifests during Phase 2 cannot override values already specified in the `install-config.yaml` file (Phase 1).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-16

**Title**
OVN-Kubernetes Overlay Network Parameter Configuration

**Architectural Question**
Should the default network parameters for the OVN-Kubernetes Geneve overlay (MTU and Geneve Port) be accepted or explicitly configured during installation?

**Issue or Problem**
The OVN-Kubernetes Geneve overlay parameters, such as the maximum transmission unit (MTU) and Geneve Port, must be correctly configured to ensure efficient network performance. The default MTU detection might be inappropriate or inconsistent in certain network environments, and the Geneve Port (default 6081) cannot be changed after installation, requiring an early decision to prevent future conflicts.

**Assumption**
CNI Plugin Selection is OVN-Kubernetes.

**Alternatives**

- Rely on Automatic/Default Parameters
- Explicitly Define Custom Parameters

**Decision**
#TODO: Document decision.#

**Justification**

- **Rely on Automatic/Default Parameters:** The MTU is detected automatically based on the MTU of the primary network interface, which is normally sufficient and simplifies installation. Using the default Geneve Port (6081) minimizes configuration complexity.
- **Explicitly Define Custom Parameters:** This is necessary if the underlying network topology mandates a specific MTU value (to avoid fragmentation) or if the default Geneve Port (6081) conflicts with existing network services, requiring a different port.

**Implications**

- **Rely on Automatic/Default Parameters:** Failure to correctly detect the MTU or a conflict with the default Geneve Port may lead to network failures. It is generally advised that you do not need to override the detected MTU.
- **Explicitly Define Custom Parameters:** Requires setting the `mtu` and `genevePort` fields in the `ovnKubernetesConfig` object. Note that the `genevePort` value cannot be changed after cluster installation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-17

**Title**
OVN-Kubernetes Internal Subnet Configuration Strategy

**Architectural Question**
Will the OVN-Kubernetes CNI plugin use its default internal CIDR ranges for the Transit and Join subnets, or will custom CIDRs be configured to prevent overlap with existing corporate networks?

**Issue or Problem**
OVN-Kubernetes uses specific default IPv4 and IPv6 subnets internally for the distributed transit switch (`internalTransitSwitchSubnet`) and cluster joins (`internalJoinSubnet`). If these default ranges overlap with the organization's existing network infrastructure, routing failures can occur, requiring customization before installation.

**Assumption**
CNI Plugin Selection is set to OVN-Kubernetes.

**Alternatives**

- Use Default OVN-Kubernetes Internal Subnets
- Specify Custom OVN-Kubernetes Internal Subnets

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Use Default OVN-Kubernetes Internal Subnets:** Simplifies configuration and relies on standard, tested defaults when no conflicts are known.
- **Specify Custom OVN-Kubernetes Internal Subnets:** Required if the default internal subnets overlap with existing network ranges, ensuring correct operation and avoiding routing conflicts between the cluster and external services.

**Implications**

- **Use Default OVN-Kubernetes Internal Subnets:** Requires upfront validation to ensure the default CIDR ranges (e.g., `100.88.0.0/16`) do not conflict with the host network.
- **Specify Custom OVN-Kubernetes Internal Subnets:** Adds complexity during installation by requiring configuration of the `ovnKubernetesConfig` object. The chosen custom range must be large enough (e.g., Transit switch subnet needs one IP per node) and must not overlap with other cluster or host subnets.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-18

**Title**
OVN-Kubernetes Internal Masquerade Subnet Configuration

**Architectural Question**
Should the default internal IPv4/IPv6 masquerade subnet used by OVN-Kubernetes for host-to-service traffic be modified from its default values?

**Issue or Problem**
The internal masquerade subnet (e.g., default IPv4 is `169.254.169.0/29`) is used internally by OVN-Kubernetes to enable host-to-service traffic. This internal range might conflict with other special-purpose CIDRs or restricted network ranges within the corporate environment.

**Assumption**
CNI Plugin Selection is set to OVN-Kubernetes.

**Alternatives**

- Use Default Internal Masquerade Subnet
- Specify Custom Internal Masquerade Subnet

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Use Default Internal Masquerade Subnet:** This simplifies configuration by relying on the standard, known internal IP ranges used by OVN-Kubernetes.
- **Specify Custom Internal Masquerade Subnet:** This is required if the default range conflicts with existing infrastructure to ensure stable host-to-service communication.

**Implications**

- **Use Default Internal Masquerade Subnet:** There is a risk of conflict, particularly with the IPv4 range, as the default `169.254.169.0/29` may overlap with the instance metadata endpoint `169.254.169.254` commonly used in cloud/virtualized environments.
- **Specify Custom Internal Masquerade Subnet:** Requires selecting a new, non-conflicting IP range and providing it via the `gatewayConfig.ipv4` or `gatewayConfig.ipv6` object configurations.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-19

**Title**
OVN-Kubernetes Egress Traffic Routing Via Host Network Stack

**Architectural Question**
Should OVN-Kubernetes egress traffic be processed through the host networking stack to allow utilization of kernel routing tables, or should it exit directly via the OVN network model for optimized performance?

**Issue or Problem**
By default, OVN processes egress traffic directly. However, highly specialized installations (e.g., those relying on specific routes in the kernel routing table) may require sending egress traffic through the host networking stack via the `routingViaHost: true` setting in `gatewayConfig`. This choice impacts hardware offloading capabilities.

**Assumption**
CNI Plugin Selection is set to OVN-Kubernetes.

**Alternatives**

- Egress Traffic Processed by OVN (Default)
- Egress Traffic Routed via Host Networking Stack

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Egress Traffic Processed by OVN (Default):** This method maintains processing within the OVN overlay, maximizing performance benefits and utilizing hardware offloading features where available. Recommended for general use.
- **Egress Traffic Routed via Host Networking Stack:** Required for specialized applications that rely on manually configured routes in the host's kernel routing table, ensuring that egress traffic is subject to host routing rules.

**Implications**

- **Egress Traffic Processed by OVN (Default):** Specialized host routes defined outside of OVN will not affect pod egress traffic.
- **Egress Traffic Routed via Host Networking Stack:** If this field is set to `true`, the performance benefits of Open vSwitch hardware offloading are lost because the egress traffic is processed by the host networking stack.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-NET-20

**Title**
OVN-Kubernetes IPsec Encryption Mode

**Architectural Question**
Should OVN-Kubernetes be configured to encrypt traffic using IPsec, and if so, what scope of traffic (pod-to-pod only, or pod-to-external and pod-to-pod) will be encrypted?

**Issue or Problem**
A decision is needed to balance the security requirement of encrypted network traffic against potential performance overhead and the operational scope of encryption.

**Assumption**
CNI Plugin Selection is OVN-Kubernetes.

**Alternatives**

- Disabled (No IPsec)
- Full IPsec Mode
- External IPsec Mode

**Decision**
#TODO: Document decision.#

**Justification**

- **Disabled (No IPsec):** This approach minimizes performance overhead and operational complexity associated with managing encrypted tunnels.
- **Full IPsec Mode:** This option maximizes security by enabling IPsec for both pod traffic and network traffic with external hosts.
- **External IPsec Mode:** This approach enables IPsec selectively for network traffic with external hosts only.

**Implications**

- **Disabled (No IPsec):** Network traffic between pods and to external hosts is unencrypted at the network layer.
- **Full IPsec Mode:** This mode requires setting `ipsecConfig: mode: Full` and introduces cryptographic overhead to both internal and external traffic, potentially impacting latency and throughput.
- **External IPsec Mode:** This mode adds cryptographic overhead only to external traffic, with internal pod-to-pod communication remaining unencrypted.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-21

**Title**
OVN-Kubernetes Cluster Route Advertisement Strategy

**Architectural Question**
Should OVN-Kubernetes be configured to advertise cluster network routes (Pod CIDRs) externally to surrounding network infrastructure?

**Issue or Problem**
External network components (like routers or security devices) require knowledge of the internal Pod Network CIDRs for successful routing. By default, these routes are internal to the SDN. Explicitly advertising them is necessary for deep network integration scenarios.

**Assumption**
N/A

**Alternatives**

- Route Advertisement Disabled (Default)
- Route Advertisement Enabled

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Route Advertisement Disabled (Default):** Minimizes configuration complexity and relies on the standard OVN overlay network model where cluster network routes are not imported or advertised.
- **Route Advertisement Enabled:** Allows external network devices to learn and route directly to Pod network CIDRs. This capability requires the deployment and configuration of the FRR routing capability provider.

**Implications**

- **Route Advertisement Disabled (Default):** External services cannot directly route to individual pod IP addresses without using mechanisms like Egress IPs or relying on NAT functionality.
- **Route Advertisement Enabled:** Requires specifying the FRR provider within the `additionalRoutingCapabilities` field in the Network configuration object. Requires additional configuration via `RouteAdvertisements` custom resources.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## OCP-NET-22

**Title**
OVN-Kubernetes IP Forwarding Scope for Managed Interfaces

**Architectural Question**
Should the cluster nodes function as generic IP routers for non-Kubernetes traffic, or should IP forwarding be restricted to enhance security?

**Issue or Problem**
The `ipForwarding` specification in the Network resource controls whether OVN-Kubernetes managed interfaces drop or forward traffic not explicitly related to Kubernetes. This decision impacts security (least privilege) versus flexibility (supporting existing host/legacy routing).

**Assumption**
CNI Plugin Selection is set to OVN-Kubernetes.

**Alternatives**

- Restricted IP Forwarding (New Install Default)
- Global IP Forwarding (Upgrade Default)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Restricted IP Forwarding (New Install Default):** Enhances the security posture of new installations by setting IP forwarding to drop all non-Kubernetes related traffic on OVN-Kubernetes managed interfaces. This aligns with the Principle of Least Privilege.
- **Global IP Forwarding (Upgrade Default):** Allows forwarding of all IP traffic. This may be required for compatibility with legacy services or external components relying on broader host-level routing rules.

**Implications**

- **Restricted IP Forwarding (New Install Default):** Requires careful planning to ensure that specialized host traffic that needs IP forwarding is correctly handled outside of OVN-Kubernetes managed interfaces.
- **Global IP Forwarding (Upgrade Default):** Reduces security isolation compared to the restricted setting.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-23

**Title**
Network Diagnostics Operator Deployment Strategy

**Architectural Question**
Should the cluster intentionally disable the core OpenShift Network Diagnostics functionality to conserve resources or reduce the management footprint?

**Issue or Problem**
For highly optimized, resource-constrained environments (like Edge or vDU workloads), reducing platform overhead is critical. The default configuration includes network components that consume resources but are deemed non-essential if comprehensive external monitoring is already in place.

**Assumption**
N/A

**Alternatives**

- Default Network Diagnostics (Enabled)
- Disabled Network Diagnostics

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Network Diagnostics (Enabled):** Provides valuable built-in troubleshooting tools for validating networking health, simplifying Day 2 operations and identifying connectivity issues proactively.
- **Disabled Network Diagnostics:** **Setting `disableNetworkDiagnostics: true` in the Network CR** explicitly removes this feature, reducing the overall platform footprint and conserving CPU/memory resources.

**Implications**

- **Default Network Diagnostics (Enabled):** Consumes node resources (CPU/memory) via associated diagnostic pods and daemon sets.
- **Disabled Network Diagnostics:** Removes a built-in diagnostic safety net. Troubleshooting complex network failures must rely solely on external tools or manual inspection.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-24

**Title**
Ingress Controller Strategy

**Architectural Question**
How will ingress controllers be deployed and managed for routing external traffic to applications?

**Issue or Problem**
Strategy impacts multi-tenancy, performance isolation, security, custom domain usage, and resource consumption.

**Assumption**
N/A

**Alternatives**

- Default OpenShift Ingress Controller (Shared)
- Dedicated OpenShift Ingress Controllers (Per Tenant/App Group)
- Third-Party Ingress Controller (e.g., Nginx Ingress Operator)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default:** Simplest, uses out-of-the-box controller for all routes under the default apps domain (`*.apps.cluster.domain`).
- **Dedicated:** Creates separate controllers for different apps/tenants using `IngressController` CR. Allows custom domains, performance/security isolation.
- **Third-Party:** Integrates vendor-specific controller for advanced features or existing expertise.

**Implications**

- **Default:** All routes share one controller. Risk of "noisy neighbor" performance issues. Limits domain flexibility. Least resource usage.
- **Dedicated:** Increases cluster resource consumption (CPU, RAM per controller replica). Requires config for new controller and route scoping (custom domains, route labels/selectors). Provides isolation.
- **Third-Party:** Org responsible for full lifecycle management. Domain flexibility but requires manual integration and potentially different operational model.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-NET-25

**Title**
Ingress Controller Replica Count

**Architectural Question**
How many replicas will be deployed for each ingress controller instance (default and dedicated)?

**Issue or Problem**
Replica count determines HA and traffic handling capacity. Insufficient replicas cause bottlenecks or outages.

**Assumption**
N/A
**Alternatives**

- Default Replica Count (Typically 2)
- Custom Replica Count (Scaled based on load/HA needs)

**Decision**
#TODO: Document the decision for each cluster and each ingress controller pool.#

**Justification**

- **Default (2):** Baseline HA, suitable for non-prod or low traffic.
- **Custom:** Scale replicas up (or down) to match expected load and meet specific HA requirements (e.g., survive node/AZ failure) for production.

**Implications**

- **Default (2):** Basic redundancy. May not handle high volume or survive multi-node/AZ failure without degradation.
- **Custom:** Allows scaling for production loads (including bursty AI inference traffic). Each replica consumes additional CPU/memory. Requires monitoring to determine appropriate count.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-NET-26

**Title**
SSL/TLS Termination Strategy

**Architectural Question**
Where will SSL/TLS encryption for application ingress traffic be terminated?

**Issue or Problem**
Decision impacts security posture, certificate management complexity, and ability to enforce end-to-end encryption.

**Assumption**
N/A
**Alternatives**

- **Edge Termination:** TLS terminates at Ingress Controller; traffic to Pod is HTTP.
- **Passthrough Termination:** TLS terminates at the Pod; Ingress Controller routes encrypted TCP.
- **Re-encryption Termination:** TLS terminates at Ingress Controller, which then initiates a new TLS connection to the Pod.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Edge:** Simplifies certificate management (centralized at Ingress). Offloads TLS processing from pods.
- **Passthrough:** Achieves true end-to-end encryption (client to pod). Often required for high security/compliance.
- **Re-encryption:** Ensures traffic is encrypted both externally and internally within the cluster. Balances security and L7 routing capability.

**Implications**

- **Edge:** Traffic between Ingress and Pod is unencrypted. May violate security policies. Allows L7 inspection/routing at Ingress.
- **Passthrough:** Ingress cannot inspect L7 traffic (no path-based routing, header manipulation). Certificate management decentralized to app teams.
- **Re-encryption:** Minor performance overhead (double encryption). Requires certificate management at both Ingress and Pods. Allows L7 inspection/routing.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-27

**Title**
Access Control for Cluster Metrics Port (TCP 1936)

**Architectural Question**
Should the Ingress load balancer be configured to expose TCP port 1936, or should access be restricted to prevent external exposure of internal host-level metrics and statistics?

**Issue or Problem**
TCP port 1936 is used for host level services (Metrics) and is accessible for an OpenShift Container Platform cluster because each control plane node needs access to this port. Avoid using the Ingress load balancer to expose this port, as doing so might result in the exposure of sensitive information related to Ingress Controllers.

**Assumption**
N/A

**Alternatives**

- Expose Port 1936 via Ingress Load Balancer
- Restrict Port 1936 Access to Internal Nodes Only

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Expose Port 1936 via Ingress Load Balancer:** Allows external systems direct access to host-level metrics (e.g., node exporter) through the Ingress path. This is explicitly advised against due to the risk of exposing sensitive information.
- **Restrict Port 1936 Access to Internal Nodes Only:** Recommended practice to ensure sensitive host-level statistics and metrics are not exposed externally via the Ingress load balancer.

**Implications**

- **Expose Port 1936 via Ingress Load Balancer:** Increased security risk due to the potential exposure of sensitive statistics and metrics.
- **Restrict Port 1936 Access to Internal Nodes Only:** Requires maintaining firewall rules or load balancer configuration to explicitly block external traffic destined for port 1936.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-NET-28

**Title**
Default Network Policy (Pod Isolation)

**Architectural Question**
What default network policy will govern pod communication _within_ and _between_ namespaces?

**Issue or Problem**
Default policy sets the baseline security posture for pod network isolation, impacting security risk and developer workflow (need to create explicit allow rules).

**Assumption**
N/A

**Alternatives**

- **Default Open:** All pods can communicate freely across all namespaces.
- **Allow Same-Namespace:** Pods within a namespace can communicate freely; cross-namespace traffic is denied by default.
- **Default Deny (Zero Trust):** All traffic (within and between namespaces) is denied by default.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Open:** Maximizes ease of deployment/debugging initially. Lowest security.
- **Allow Same-Namespace:** Improves security by isolating projects. Requires explicit `NetworkPolicy` for cross-namespace communication. Good balance for many orgs.
- **Default Deny:** Strongest security (Zero Trust). Requires developers to define explicit allow policies for _all_ required traffic (in-namespace and cross-namespace).

**Implications**

- **Default Open:** No network segmentation. Increases blast radius of compromised pod.
- **Allow Same-Namespace:** Isolates projects. Developers must create policies for intended cross-project traffic.
- **Default Deny:** Strongest security. Significant effort for developers to define/maintain detailed `NetworkPolicy` objects for applications to function.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## OCP-NET-29

**Title**
Administrative Network Policy Strategy (Cluster-wide)

**Architectural Question**
Will cluster-scoped administrative network policies (`AdminNetworkPolicy`/`BaselineAdminNetworkPolicy`) enforce baseline security rules above tenant-controlled `NetworkPolicy`?

**Issue or Problem**
Standard `NetworkPolicy` is namespace-scoped, allowing project owners to potentially bypass critical platform security requirements. A cluster-scoped mechanism enables centralized enforcement.

**Assumption**
Cluster uses OVN-Kubernetes CNI.

**Alternatives**

- Implement AdminNetworkPolicy (ANP) - Mandatory Rules
- Implement BaselineAdminNetworkPolicy (BANP) - Default Rules (Overridable)
- Rely Solely on Standard NetworkPolicy

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **ANP:** Enforces mandatory, non-overridable rules (Allow, Deny, Pass actions) for high-priority traffic (control plane, security boundaries). Highest precedence.
- **BANP:** Sets default baseline rules (Allow or Deny) that _can_ be overridden by standard `NetworkPolicy`. Provides a starting point for tenants.
- **Standard Only:** Minimizes complexity, accepting all network rules are managed at namespace level by project owners.

**Implications**

- **ANP/BANP:** Requires rigorous testing to avoid disrupting core platform functions (monitoring, operators). ANP ensures critical rules cannot be bypassed. BANP provides guidance but allows tenant flexibility. Requires OVN-Kubernetes CNI.
- **Standard Only:** Compliance or Zero Trust architectures harder to enforce consistently across all projects. Simpler operationally.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-30

**Title**
OVN-Kubernetes Network Policy Audit Log Destination

**Architectural Question**
Where should the audit logs generated by OVN-Kubernetes network policy events be sent for persistence and auditing?

**Issue or Problem**
Granular audit logging of network policy decisions is often required for regulatory compliance. The default configuration uses internal settings, which may not meet enterprise persistence requirements. The decision dictates the logging destination and configuration of parameters like rate limiting.

**Assumption**
CNI Plugin Selection is set to OVN-Kubernetes.

**Alternatives**

- Send to Local Systemd Journal (libc)
- Send to External Syslog Server (udp)
- Disable Additional Audit Logging (null)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Send to Local Systemd Journal (libc):** This destination integrates with the local host's systemd journal via the libc `syslog()` function. This is simpler operationally but relies on local host configuration for retention policies.
- **Send to External Syslog Server (udp):** This is necessary for centralizing compliance logging. It allows integration with external Security Information and Event Management (SIEM) tools by directing output to a specific host and port.
- **Disable Additional Audit Logging (null):** This minimizes CPU and network overhead by explicitly preventing the logs from being sent to an additional destination.

**Implications**

- **Send to Local Systemd Journal (libc):** Requires management of internal parameters like `maxFileSize` and `maxLogFiles` to ensure log rotation and prevent disk exhaustion.
- **Send to External Syslog Server (udp):** Requires establishing a dependency on a reachable external syslog server and configuring the log `rateLimit` (default is 20 messages per second per node) to prevent overwhelming the server.
- **Disable Additional Audit Logging (null):** Compromises the ability to perform compliance auditing based on OVN network policy enforcement events.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-NET-31

**Title**
Egress IP Address Strategy

**Architectural Question**
How will outbound traffic from specific pods/projects ensure a predictable source IP address when connecting to external services requiring IP whitelisting?

**Issue or Problem**
External services (databases, legacy APIs) often use firewalls allowing access only from specific source IPs. Default pod egress uses the node IP, which is unpredictable.

**Assumption**
N/A

**Alternatives**

- No Egress IP Configuration
- Egress IP per Project/Namespace
- Egress IP for Specific Pods (via selectors)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Egress IP:** For environments where fixed source IPs aren't needed.
- **Egress IP per Project:** Assigns a static source IP for all outbound traffic from a project. Simplifies external firewall management.
- **Egress IP for Specific Pods:** Provides dedicated egress IP for a pod subset (via labels), allowing fine-grained control.

**Implications**

- **No Egress IP:** Pods egress via unpredictable node IPs.
- **Egress IP per Project:** Requires reserving IPs on the node network. Egress IP must be hosted on a node in the same subnet. Simple for project-wide rules.
- **Egress IP for Specific Pods:** More granular but increases config complexity (labeling pods, managing multiple EgressIP objects).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-32

**Title**
Secondary Network Strategy (Multus / SR-IOV)

**Architectural Question**
How will pods connect to additional, specialized networks (e.g., VLANs, high-performance NICs) beyond the primary cluster network?

**Issue or Problem**
Certain apps (Telco, HPC, AI/ML data ingest, legacy systems) require direct access to specific physical, VLAN-based, or high-performance networks.

**Assumption**
N/A

**Alternatives**

- No Secondary Networks
- Layer 2 CNI Plugin (Macvlan/Ipvlan via Multus)
- SR-IOV Network Device Plugin (via Multus)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Secondary Networks:** Simplest config for standard enterprise apps without specialized connectivity needs.
- **Layer 2 CNI (Macvlan/Ipvlan):** Integrates pods directly into existing physical/VLAN networks, making them L2 citizens on those networks. Uses Multus CNI meta-plugin.
- **SR-IOV Plugin:** Provides pods direct, high-performance access to physical NIC VFs (Virtual Functions), bypassing host network stack. Critical for lowest latency/highest throughput (AI/ML ingest, inference, Telco NFV). Uses Multus.

**Implications**

- **No Secondary Networks:** Cannot host apps with specialized network requirements.
- **Layer 2 CNI:** Requires careful IPAM for the secondary network. Multus manages multiple network attachments (`NetworkAttachmentDefinition` CRs).
- **SR-IOV:** Critical for high-performance AI/ML/Telco. Requires SR-IOV capable NICs on workers. Complex config (BIOS, kernel, SR-IOV Network Operator). Provides near bare-metal network performance to pods.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader (for SR-IOV hardware)
- Person: #TODO#, Role: AI/ML Platform Owner (for SR-IOV use case)

---

## OCP-NET-33

**Title**
SR-IOV Virtual Function (VF) Driver Selection

**Architectural Question**
Which SR-IOV Virtual Function (VF) device type—`vfio-pci` or `netdevice`—will be standardized for use by high-performance application pods?

**Issue or Problem**
When configuring SR-IOV devices, the choice of the VF device driver type dictates how the network resource is presented to the container. This impacts latency, performance characteristics, and the flexibility for applications.

**Assumption**
Secondary Network Strategy includes SR-IOV.

**Alternatives**

- VFIO-PCI Driver (`vfio-pci`)
- Netdevice Driver (`netdevice`)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **VFIO-PCI Driver (`vfio-pci`):** Recommended when true hardware passthrough (Device Passthrough) is required, often for applications using Data Plane Development Kit (DPDK) or needing kernel bypass to achieve the lowest possible latency.
- **Netdevice Driver (`netdevice`):** Recommended when standard Linux network semantics (e.g., standard CNI features, DHCP) are required, offering higher flexibility for debugging and standard networking.

**Implications**

- **VFIO-PCI Driver (`vfio-pci`):** Applications must be designed to utilize device passthrough frameworks (like DPDK). The VF is not exposed as a traditional network interface to the OS.
- **Netdevice Driver (`netdevice`):** Provides simpler integration with standard container networking. However, this configuration might introduce additional latency compared to kernel-bypass methods.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-34

**Title**
SR-IOV Virtual Function Bonding Strategy

**Architectural Question**
How will multiple Single Root I/O Virtualization (SR-IOV) Virtual Functions (VFs) attached to a dual-port Network Interface Card (NIC) be configured for network resilience and high availability for application workloads?

**Issue or Problem**
For high-performance network components like SR-IOV VFs, a single virtual function presents a single failure path. Utilizing dual-port NICs to create a bond provides network high availability (HA) and load balancing capabilities.

**Assumption**
Secondary Network Strategy includes SR-IOV.

**Alternatives**

- Bond multiple SR-IOV Virtual Functions (VFs)
- Utilize separate, unbonded SR-IOV Virtual Functions (VFs)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Bond multiple SR-IOV Virtual Functions (VFs):** Supports the use of bonds for high availability (e.g., LACP), leveraging a single, high-speed dual port NIC partitioned into VFs. Critical for HA virtualization or performance-sensitive applications.
- **Utilize separate, unbonded SR-IOV Virtual Functions (VFs):** Simplifies configuration. May be sufficient for non-critical testing or development environments where HA is not a priority.

**Implications**

- **Bond multiple SR-IOV Virtual Functions (VFs):** Requires complex network configuration. Depending on the method, this may involve OVS bonding modes at the host level or bonding configurations within the Pod network namespace (e.g., using the Bonding CNI plugin).
- **Utilize separate, unbonded SR-IOV Virtual Functions (VFs):** Provides no network redundancy or HA across physical NIC ports for application workloads using the VFs.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-NET-35

**Title**
SR-IOV Virtual Function Bonding Mechanism

**Architectural Question**
Which mechanism will be implemented to establish the bond between multiple SR-IOV Virtual Functions (VFs) inside the application pods?

**Issue or Problem**
Once the decision to bond SR-IOV VFs for high availability is made, the implementation method depends on the driver type and where the bonding logic resides (Kernel vs. Userspace). This impacts how the network interface is presented to the containerized application.

**Assumption**
Secondary Network Strategy includes SR-IOV.
SR-IOV Virtual Function Bonding Strategy is set to "Bond multiple VFs".

**Alternatives**

- **Pod-level Kernel Bonding via Bonding CNI Plugin**
- **Application-level Userspace Bonding (DPDK)**

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Pod-level Kernel Bonding via Bonding CNI Plugin:** This utilizes the standard Kubernetes `bonding-cni` meta-plugin. It creates a standard Linux kernel bond interface (e.g., `bond0`) inside the pod's network namespace, aggregating the SR-IOV VFs. This is transparent to the application, which simply sees a highly available network interface with standard IP addressing.
- **Application-level Userspace Bonding (DPDK):** This delegates the bonding logic entirely to the application (using Data Plane Development Kit - DPDK). The Pod receives two distinct VFs, and the application handles load balancing and failover logic in userspace. This is generally required if `vfio-pci` drivers are used but can also be used with `netdevice`.

**Implications**

- **Pod-level Kernel Bonding via Bonding CNI Plugin:** Requires the SR-IOV driver to be `netdevice`. Simplifies application development as standard socket networking works over the bond. Requires defining `NetworkAttachmentDefinition` resources that chain the SR-IOV plugin with the Bonding plugin.
- **Application-level Userspace Bonding (DPDK):** Provides the absolute lowest latency and highest throughput by bypassing the kernel stack. However, it significantly increases application complexity; the application must be "network aware" and capable of initializing and managing the physical polling drivers (PMD) for the VFs.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
