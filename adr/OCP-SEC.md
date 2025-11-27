# ARCHITECTURE DECISION RECORDS FOR: OpenShift Container Platform - Security and Compliance

## OCP-SEC-01

**Title**
FIPS Compliance Requirement

**Architectural Question**
Will OpenShift Container Platform be configured to operate in FIPS mode to meet regulatory requirements?

**Issue or Problem**
FIPS (Federal Information Processing Standards) 140-2 compliance requires the system to use validated cryptographic modules, which necessitates specific operating system and cluster configuration choices prior to installation.

**Assumption**
N/A

**Alternatives**

- FIPS Mode Enabled
- FIPS Mode Disabled

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **FIPS Mode Enabled:** Required for clusters operating in highly regulated environments (e.g., US government, financial sector). When FIPS mode is enabled, core components use RHEL cryptographic libraries validated for FIPS 140-2/140-3 on **x86_64, ppc64le, and s390x** architectures.
- **FIPS Mode Disabled:** Standard mode. Provides maximum compatibility and performance, as not all Kubernetes components or workload dependencies may be FIPS validated.

**Implications**

- **FIPS Mode Enabled:** Requires that the underlying RHCOS/RHEL operating system is booted in FIPS mode. Cluster features or operators relying on non-FIPS compliant cryptography may not function or may require specific configuration changes.
- **FIPS Mode Disabled:** May not meet mandated security requirements for certain regulatory environments.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-02

**Title**
SSH Key Algorithm Selection for FIPS Mode Clusters

**Architectural Question**
If the OpenShift cluster is configured to operate in FIPS mode, which SSH key algorithm should be mandated for the administrative SSH public key included in the installation configuration?

**Issue or Problem**
The standard default SSH key algorithm (`ed25519`) is not FIPS-compliant, and its use is restricted when the cluster is configured to operate in FIPS mode. Using a non-compliant key will violate security mandates and potentially block remote access to RHCOS nodes for debugging or disaster recovery.

**Assumption**
FIPS mode is enabled for the cluster installation.

**Alternatives**

- RSA or ECDSA Algorithms
- ED25519 Algorithm

**Decision**
#TODO: Document decision.#

**Justification**

- **RSA or ECDSA Algorithms:** These algorithms are FIPS-compliant and **must be used** to generate the SSH key if the cluster is installed with FIPS mode enabled. This ensures compliance and continuous operational access.
- **ED25519 Algorithm:** This algorithm is specifically identified as **non-FIPS compliant** and should not be used if the cluster is configured for FIPS mode.

**Implications**

- **RSA or ECDSA Algorithms:** Requires an explicit administrative step to use `ssh-keygen -t rsa` or `ecdsa` during setup instead of relying on the system default (if the default is ED25519).
- **ED25519 Algorithm:** If used in a FIPS cluster, it may prevent the core user from accessing the nodes via SSH due to the cryptographic libraries rejecting the non-compliant key.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-SEC-03

**Title**
TLS Security Profile Selection

**Architectural Question**
Which cluster-wide TLS security profile will be applied to the Ingress Controller and control plane components to govern cryptographic ciphers and TLS versions?

**Issue or Problem**
Different organizations have different requirements for cryptographic strength versus client compatibility. Using older ciphers ensures legacy clients can connect but increases security risk. Using modern ciphers improves security but may break older clients.

**Assumption**
N/A

**Alternatives**

- **Intermediate Profile (Default):** Balances security and compatibility. Supports TLS 1.2 and 1.3 with a broad set of strong ciphers.
- **Modern Profile:** Enforces strict security. Requires TLS 1.3 and drops support for older ciphers.
- **Old Profile:** Maximize compatibility with legacy clients/browsers. Not recommended for secure environments.
- **Custom Profile:** Manually defined list of ciphers.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Intermediate Profile:** The safe default. Meets most compliance standards (like NIST) while ensuring standard browsers and tools can connect.
- **Modern Profile:** Required for high-security environments (e.g., requiring Forward Secrecy) where all clients are known to support TLS 1.3.
- **Old Profile:** Only selected if specific legacy hardware/software must interact with the cluster API or Ingress.

**Implications**

- **Intermediate Profile:** Allows TLS 1.2.
- **Modern Profile:** **Breaks clients** that do not support TLS 1.3. May impact older CI/CD tools or external integrations.
- **Custom Profile:** High maintenance burden to update cipher lists as vulnerabilities are discovered.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-04

**Title**
Compliance Automation Strategy

**Architectural Question**
How will regulatory compliance (e.g., STIG, PCI-DSS) be enforced, tracked, and remediated across the cluster lifecycle, considering the FIPS decision?

**Issue or Problem**
Continuous auditing against configuration standards (e.g., DISA-STIG, FedRAMP, PCI-DSS) is necessary to maintain security posture and readiness, complementing the foundational FIPS setting if enabled.

**Assumption**
N/A

**Alternatives**

- Manual Policy Enforcement (External Audits)
- Compliance Operator (Automated Scanning/Remediation)
- Policy Automation via RHACM/ZTP

**Decision**
#TODO#

**Justification**

- **Manual Policy Enforcement (External Audits):** Relies on external tools and manual processes to check cluster configurations against standards. High effort and reactive remediation.
- **Compliance Operator (Automated Scanning/Remediation):** Recommended automated solution. The Compliance Operator uses OpenSCAP profiles (Platform/Node) to automatically run scans and generate machine configuration remediations for standards like STIG, PCI-DSS (v4), and FedRAMP.
- **Policy Automation via RHACM/ZTP:** For fleet management, leverages RHACM PolicyGenerator resources to distribute and enforce security and compliance policies across multiple clusters declaratively.

**Implications**

- **Manual Policy Enforcement (External Audits):** High potential for configuration drift and difficulty in maintaining continuous compliance.
- **Compliance Operator (Automated Scanning/Remediation):** Requires installing and maintaining the Compliance Operator. Automated remediations (e.g., those affecting SSHD or KubeletConfig) must be carefully reviewed before application.
- **Policy Automation via RHACM/ZTP:** Enables centralized compliance enforcement across a multi-cluster fleet but introduces dependency on RHACM infrastructure.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-05

**Title**
Audit Log Policy Configuration

**Architectural Question**
What level of detail will be captured in the Kubernetes API Server audit logs?

**Issue or Problem**
Audit logs are essential for forensic analysis. However, logging too much detail (like request bodies) generates massive amounts of data, impacting performance and storage costs. Logging too little prevents effective auditing of _what_ changed.

**Assumption**
N/A

**Alternatives**

- **Default Policy (Metadata Only):** Logs who, what, when, and the response status. Does not log the payload.
- **WriteRequestBodies:** Logs the metadata AND the full payload (body) for modification requests (create, update, patch).
- **AllRequestBodies:** Logs payloads for every request, including reads.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Policy:** Sufficient for tracking "Who did it". Minimizes I/O load and storage requirements.
- **WriteRequestBodies:** Essential for security auditing. Allows admins to see exactly _what_ changed in a resource (e.g., seeing the specific bad value injected into a ConfigMap), not just that it changed.
- **AllRequestBodies:** Extreme verbosity. Usually only enabled for short debugging sessions or highest-security environments with massive storage capacity.

**Implications**

- **Default Policy:** Cannot reconstruct the state of an object from logs alone.
- **WriteRequestBodies:** Significantly increases the volume of logs sent to the auditing system (LOG-01/LOG-02). **Sensitive data** in request bodies (Secrets, ConfigMaps) might be logged; requires strict access control on the logs themselves.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-06

**Title**
Identity Provider Selection

**Architectural Question**
Which authentication identity provider (IdP) will OpenShift use for user login?

**Issue or Problem**
Choosing the right IdP is foundational to user access and authorization, requiring alignment with existing enterprise directories or modern security standards.

**Assumption**
N/A

**Alternatives**

- HTPasswd
- LDAP
- OpenID Connect (OIDC)
- Other Providers (e.g., Keystone)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **HTPasswd:** Simple, self-contained authentication. Suitable only for PoCs or small, isolated clusters.
- **LDAP:** Integrates with existing enterprise directories (AD, OpenLDAP). Common in established enterprises.
- **OpenID Connect (OIDC):** Integrates with modern IdPs (Keycloak, Okta, Azure AD). Recommended for flexibility, security (MFA, SSO), and feature richness.
- **Other Providers:** Leverages specific existing systems (Keystone for OpenStack) or social providers (GitHub).

**Implications**

- **HTPasswd:** Manual user management, does not scale.
- **LDAP:** Requires secure connectivity (LDAPS) and query configuration. Group sync needs.
- **OpenID Connect (OIDC):** Recommended. Requires managing client IDs/secrets, relies on external IdP infrastructure.
- **Other Providers:** Integration complexity varies.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-07

**Title**
Identity Provider Group Synchronization

**Architectural Question**
How will user groups from the external identity provider be synchronized with OpenShift for RBAC?

**Issue or Problem**
OpenShift needs awareness of external IdP groups to manage permissions effectively via RBAC. A synchronization strategy is needed.

**Assumption**
Identity Provider is configured.

**Alternatives**

- No Group Synchronization (Manual RBAC)
- LDAP Group Sync Operator (for LDAP)
- Claim-based Group Sync (for OIDC)
- On-demand Group Sync (Legacy LDAP)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Group Synchronization:** Simplifies IdP config by managing all groups/bindings manually in OpenShift. Avoids IdP dependency for authorization.
- **LDAP Group Sync Operator:** Robust, scalable, recommended method for LDAP. Periodically syncs IdP groups to OpenShift `Group` resources.
- **Claim-based Group Sync (OIDC):** Standard for OIDC. Group memberships are included in the user's token/claims during login and mapped dynamically.
- **On-demand Group Sync (Legacy LDAP):** Older LDAP mechanism, fetches groups only on login. Not recommended for new deployments.

**Implications**

- **No Group Synchronization:** High operational burden, managing RBAC per-user. Does not scale.
- **LDAP Group Sync Operator:** Reliable, near-real-time group reflection for LDAP. Most manageable for enterprise RBAC with LDAP.
- **Claim-based Group Sync (OIDC):** Efficient for OIDC. Relies on IdP correctly issuing group claims in tokens.
- **On-demand Group Sync (Legacy LDAP):** Can cause performance issues and stale group info.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-08

**Title**
Multi-Tenant Identity Provider Integration

**Architectural Question**
How will the platform support multiple distinct identity providers, potentially for different tenants?

**Issue or Problem**
Integrating multiple IdPs for different user groups (e.g., internal vs. external partners) requires a strategy to manage the login experience and authentication flows.

**Assumption**
Multiple, distinct IdPs are required.

**Alternatives**

- Native OpenShift Multi-IdP Configuration
- Brokered IdP Configuration with Keycloak

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Native OpenShift Multi-IdP Configuration:** Uses built-in functionality to configure multiple IdPs directly in OpenShift. Simplest infrastructure approach.
- **Brokered IdP Configuration with Keycloak:** Uses a central identity broker (Red Hat build of Keycloak) as the single OCP entry point. Keycloak then connects to all upstream tenant IdPs.

**Implications**

- **Native OpenShift:** All configured IdPs appear as login options for _all_ users, which cannot be customized/restricted and can be confusing.
- **Brokered IdP (Keycloak):** Adds Keycloak as a critical component to manage. Provides a unified login entry point and allows advanced features (custom branding per tenant, attribute mapping).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-09

**Title**
OAuth Token Duration Policy

**Architectural Question**
What duration will be configured for OpenShift OAuth access tokens?

**Issue or Problem**
The default access token duration is 24 hours. Security compliance standards (e.g., NIST, PCI-DSS) often mandate shorter session lifetimes to reduce the risk of compromised credentials.

**Assumption**
IdP is configured.

**Alternatives**

- **Default Duration (24 Hours):** Convenient for developers; reduces login frequency.
- **Short Duration (e.g., 1-8 Hours):** Enhances security by forcing re-authentication more frequently. Recommended for production.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Duration:** Balances security with user experience. Suitable for non-prod.
- **Short Duration:** Mitigates the impact of token theft. Aligns with "Zero Trust" principles by ensuring user identity is re-verified frequently.

**Implications**

- **Default Duration:** Higher risk window if a token is leaked.
- **Short Duration:** Users (CLI and Console) must log in more often. Automation relying on user tokens will break frequently (Service Accounts should be used instead).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-10

**Title**
Kubeadmin User Removal Policy

**Architectural Question**
Will the default `kubeadmin` superuser account be removed after configuring a permanent Identity Provider?

**Issue or Problem**
The `kubeadmin` user is a temporary bootstrap administrator with full cluster privileges and a password stored in a secret. Leaving it enabled creates a persistent security risk (brute force, leaked secret).

**Assumption**
A permanent IdP (`OCP-SEC-06`) and Admin RBAC (`OCP-MGT-02`) are verified working.

**Alternatives**

- **Retain Kubeadmin:** Keep the user as a "break-glass" emergency account.
- **Remove Kubeadmin:** Delete the user and the associated secret.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Retain Kubeadmin:** Provides a fallback if the external IdP fails.
- **Remove Kubeadmin:** Eliminates a critical attack vector. Best practice for production.

**Implications**

- **Retain Kubeadmin:** Password secret must be rotated and secured. Audit logs will show "kubeadmin" actions, obscuring the actual human identity.
- **Remove Kubeadmin:** If the IdP fails, admins must use the physical/cloud console to access the system via SSH and `system:admin` certificates (which bypass OAuth).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-11

**Title**
Security Context Constraint (SCC) / Pod Security Admission (PSA) Policy

**Architectural Question**
What default level of security enforcement (privileges) will be applied to user application workloads (pods)?

**Issue or Problem**
The security context policy (SCC/PSA) defines container privileges. This balances application flexibility against cluster security needs (Principle of Least Privilege).

**Assumption**
N/A

**Alternatives**

- Restricted Profile (Recommended Baseline)
- Baseline Profile (Mid-level Access)
- Permissive Exceptions (Privileged or Custom SCCs)

**Decision**
#TODO#

**Justification**

- **Restricted Profile (Recommended Baseline):** Applies the most secure standard (e.g., restricted-v2 SCC / Kubernetes PSA restricted profile) to pods, enforcing constraints like forbidding host networking, volume mounts, and the use of the root user.
- **Baseline Profile (Mid-level Access):** A more relaxed standard (e.g., PSA baseline profile) that allows default pod operation while preventing known privilege escalations. Suitable for compatibility requirements.
- **Permissive Exceptions (Privileged or Custom SCCs):** Assigns highly privileged access (e.g., `privileged` SCC or disabling enforcement) necessary for specific infrastructure components, storage operators (e.g., ODF), or legacy applications requiring host access.

**Implications**

- **Restricted Profile (Recommended Baseline):** May require modification or adaptation of application images and manifests that assume high privileges (e.g., running as root, using host paths).
- **Baseline Profile (Mid-level Access):** Provides greater compatibility than Restricted but introduces minor security flexibility tradeoffs.
- **Permissive Exceptions (Privileged or Custom SCCs):** Compromises the Principle of Least Privilege and significantly increases the attack surface of the workload and the host node.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-SEC-12

**Title**
Admission Control Strategy (Custom Policies)

**Architectural Question**
How will custom organizational policies (beyond basic SCC/PSA) regarding resource definitions and configurations be enforced?

**Issue or Problem**
Custom, granular policy enforcement (e.g., requiring specific labels, preventing use of deprecated APIs, enforcing resource limits) is needed for compliance and governance beyond default admission plugins.

**Assumption**
Need for custom policy enforcement exists.

**Alternatives**

- Rely on Default Admission Control Only
- Implement Custom Policies via Dynamic Admission Webhooks (e.g., OPA Gatekeeper, Kyverno)
- Implement Custom Policies via Declarative Admission Policies (Kubernetes ValidatingAdmissionPolicy - CEL)

**Decision**
#TODO#

**Justification**

- **Default Admission Control Only:** Relies only on built-in controllers (`LimitRanger`, `ResourceQuota`, SCC/PSA). Simple but offers limited custom policy flexibility.
- **Dynamic Admission Webhooks:** Extends admission via external webhook servers (Gatekeeper, Kyverno). Powerful for complex validating/mutating policies but adds components to manage.
- **Declarative Admission Policies (CEL):** Uses modern Kubernetes API (`ValidatingAdmissionPolicy`) with Common Expression Language (CEL). Avoids external webhook servers but limited to validation policies and CEL expressiveness.

**Implications**

- **Default Only:** Limited custom policy enforcement.
- **Webhooks:** Adds external components requiring security, HA, maintenance. Failure policy (`Fail` vs `Ignore`) impacts behavior on webhook errors.
- **Declarative (CEL):** Simpler infrastructure. Policy complexity limited by CEL budget/features. Requires careful testing of CEL expressions.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-13

**Title**
Container Image Trust and Signature Verification

**Architectural Question**
What solution will enforce image authenticity by verifying signatures for container images consumed by the cluster?

**Issue or Problem**
Supply chain integrity requires ensuring images originate from trusted sources and haven't been tampered with. Verification must be enforced before images run.

**Assumption**
Supply chain security is a requirement.

**Alternatives**

- No Verification
- OpenShift Policy Enforcement (ImagePolicy/Sigstore)
- External Verification Tools (Admission Webhooks)

**Decision**
#TODO#

**Justification**

- **No Verification:** Simplest approach, relying solely on access control (RBAC) to the registry, not validating image content origin or integrity.
- **OpenShift Policy Enforcement (ImagePolicy/Sigstore):** Recommended solution. Uses `ImagePolicy` or `ClusterImagePolicy` resources to define policies that enforce signature verification (e.g., Sigstore) for specific image registries/scopes before the image can be pulled and run.
- **External Verification Tools (Admission Webhooks):** Leverages a third-party policy engine (e.g., Gatekeeper, Kyverno) integrated via admission webhooks to validate image metadata or signatures against external sources.

**Implications**

- **No Verification:** Leaves the cluster vulnerable to supply chain attacks or unauthorized image modifications.
- **OpenShift Policy Enforcement (ImagePolicy/Sigstore):** Requires configuring trusted signing authorities and ensures that unauthorized or untrusted images are blocked at the cluster API level. MCO automatically verifies release image signatures.
- **External Verification Tools (Admission Webhooks):** Requires deployment and maintenance of additional policy enforcement infrastructure, which must integrate reliably with the OpenShift image registry workflow.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-14

**Title**
Container Vulnerability Scanning Strategy

**Architectural Question**
How will container images be scanned for known vulnerabilities (CVEs) before and during execution on the platform?

**Issue or Problem**
Trusting an image source does not guarantee the image is free of vulnerabilities. Continuous scanning is required to detect new CVEs in running workloads.

**Assumption**
Image Registry Strategy is defined.

**Alternatives**

- **Registry-Side Scanning Only (e.g., Quay):** Images are scanned at rest in the registry.
- **Platform-Side Scanning (e.g., Red Hat Advanced Cluster Security - ACS):** Images are scanned at build time, in the registry, and monitored at runtime.
- **External Scanner:** Reliance on 3rd party tools in the CI/CD pipeline.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Registry-Side Scanning:** Good baseline. Catches issues before pull. Does not protect against zero-day vulnerabilities discovered in images _already running_.
- **Platform-Side Scanning (ACS):** Recommended for comprehensive security. Connects CVEs to running pods, allowing prioritization based on exposure (e.g., "Fix the CVE in the pod exposed to the internet first").

**Implications**

- **Registry-Side Scanning:** Passive. Ops teams must manually check registry reports.
- **Platform-Side Scanning (ACS):** Requires installing ACS (Central/Sensor). Consumes cluster resources. Can enforce deployment policies (e.g., "Block deployments with CVSS > 7").

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-15

**Title**
Data Protection (etcd) Encryption

**Architectural Question**
Should sensitive API resources stored in etcd (Secrets, ConfigMaps, Routes, OAuth tokens) be encrypted at the application layer?

**Issue or Problem**
Etcd stores sensitive data. Application-layer encryption adds protection if underlying storage encryption is compromised (e.g., exposed etcd backup).

**Assumption**
Protection of sensitive configuration data at rest is required.

**Alternatives**

- No Application-Layer Encryption (Rely on Storage Encryption Only)
- Platform-Managed Encryption (AES-CBC / AES-GCM)

**Decision**
#TODO#

**Justification**

- **No Application-Layer Encryption:** Relies solely on lower-level security (RHCOS disk encryption, TPM/Tang). Simpler, avoids potential performance impact or complexity during rollout.
- **Platform-Managed Encryption:** Provides an **additional security layer** for sensitive resources (Secrets, OAuth tokens). Supports AES-CBC and AES-GCM. If FIPS mode is enabled, uses FIPS-approved `aes cbc`.

**Implications**

- **No Application-Layer Encryption:** Exposes Secrets, ConfigMaps, tokens if etcd data/backups are accessed without underlying disk encryption.
- **Platform-Managed Encryption:** **Only encrypts values, not keys** (resource types, namespaces, object names remain clear). Encryption keys file (`static_kuberesources_<...>.tar.gz`) MUST be stored securely and separately from etcd snapshots for DR. Adds minor encryption/decryption overhead.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-16

**Title**
Cloud Credential Management Mode Strategy

**Architectural Question**
How will the OpenShift Cloud Credential Operator (CCO) manage authentication with the underlying cloud provider API (AWS, Azure, GCP, OpenStack)?

**Issue or Problem**
OpenShift components need permissions to provision cloud resources (load balancers, storage). The method of granting these permissions impacts the security blast radius and operational complexity.

**Assumption**
Cluster is deployed on a cloud provider (IPI/UPI).

**Alternatives**

- **Mint Mode (Default for IPI):** CCO uses a high-privileged admin credential to mint short-lived, scoped secrets.
- **Passthrough Mode:** Components share a global static credential.
- **Manual Mode with STS/Workload Identity:** Administrator manually provisions short-term credentials via the cloud's IAM (AWS STS, Azure Workload ID).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Mint Mode:** Good balance of automation and security.
- **Passthrough Mode:** Least secure. One key rules them all.
- **Manual Mode (STS):** Highest security. No long-term secrets stored in the cluster.

**Implications**

- **Mint Mode:** Installer needs Admin rights.
- **Passthrough:** Credential rotation is painful.
- **Manual Mode:** High setup complexity (IAM roles, OIDC providers) but preferred for high-compliance environments.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-17

**Title**
Centralized Secret Management Integration

**Architectural Question**
What method will safely externalize and inject sensitive configuration data (secrets) into application workloads, especially those managed by GitOps?

**Issue or Problem**
Secrets must not be stored unencrypted in Git. A mechanism is needed to securely retrieve credentials from dedicated enterprise secret stores and make them available to pods at runtime.

**Assumption**
Applications require secrets; GitOps might be used; storing secrets directly in Git is forbidden.

**Alternatives**

- Rely Solely on Kubernetes Native Secrets (Potentially with GitOps encryption like Sealed Secrets)
- Integrate External Secret Store via External Secrets Operator (ESO) / Secrets Store CSI Driver (SSCSI)

**Decision**
#TODO#

**Justification**

- **Kubernetes Native Secrets:** Simplest K8s approach. Secrets stored as native objects, protected at rest by etcd encryption. Can be combined with GitOps tools like Sealed Secrets to encrypt secrets _before_ committing to Git.
- **External Secret Store Integration (ESO/SSCSI):** Recommended enterprise approach. Decouples app deployment from secret lifecycle, centralizes secret storage (Vault, Cloud KMS), enhances compliance/auditing. Secrets Store CSI Driver (SSCSI) mounts secrets as volumes, avoiding persistence on node after pod deletion. ESO can sync external secrets into K8s native secrets.

**Implications**

- **Native Secrets / Sealed Secrets:** Secrets (decrypted) exist within the cluster's etcd (Native) or as K8s Secret objects (Sealed Secrets decryption target). Vulnerable if RBAC/API access allows retrieval. Sealed Secrets requires managing the decryption key securely in-cluster.
- **External Store (ESO/SSCSI):** App deployment **depends on external secret store availability**. SSCSI Driver requires `privileged` SCC for pod service account. Provides better lifecycle management and auditing via the central store. ESO creates native K8s secrets, sharing similar risks as Native Secrets once synced.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-18

**Title**
Service Account Token Strategy (Bound vs Legacy)

**Architectural Question**
Will workloads relying on Service Account Tokens use legacy permanent secrets or Bound Service Account Tokens (Volume Projection)?

**Issue or Problem**
Legacy Service Account tokens are static secrets that never expire. If stolen, they are valid forever. Bound tokens are time-limited, audience-bound, and rotate automatically.

**Assumption**
Workloads use Service Accounts to talk to the Kubernetes API.

**Alternatives**

- **Legacy Secrets (Default behavior in older apps):** Mounting the static secret.
- **Bound Service Account Tokens:** Configuring `serviceAccountToken` volume projection.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Legacy Secrets:** Simple, backward compatible.
- **Bound Tokens:** significantly improves security. Tokens expire (e.g., 1 hour). Stolen tokens become useless quickly.

**Implications**

- **Legacy Secrets:** High risk of long-term credential theft.
- **Bound Tokens:** Applications _must_ reload the token from disk periodically (standard client-go does this). Incompatible with apps that read the token once at startup and never refresh.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: DevOps Engineer

---

## OCP-SEC-19

**Title**
Kubelet Serving Certificate Signing Request (CSR) Management Strategy for UPI

**Architectural Question**
How will the kubelet serving certificate requests (CSRs) for nodes managed via User-Provisioned Infrastructure (UPI) be managed and approved to ensure API server communication remains functional without manual intervention?

**Issue or Problem**
The default mechanism often requires manual approval for Kubelet server CSRs on UPI nodes during scaling or recovery, placing a significant operational burden on platform teams unless an automated custom mechanism is implemented.

**Assumption**
Cluster installation method is User-Provisioned Infrastructure (UPI).

**Alternatives**

- Rely on Manual Approval (Operator Intervention for Server CSRs)
- Implement Automated CSR Approval Mechanism

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Rely on Manual Approval (Operator Intervention for Server CSRs):** This minimizes initial configuration overhead by relying on human operators to run `oc adm certificate approve` for server CSRs. It places a significant operational burden on teams, especially during initial node installation, scaling, or recovery.
- **Implement Automated CSR Approval Mechanism:** This is the recommended approach for UPI clusters. It involves deploying a custom controller (like the Red Hat-provided Kubelet CSR Approver) that verifies the CSRs against a trusted source of truth (e.g., node labels or specific groups) and approves them automatically, ensuring consistent cluster operability.

**Implications**

- **Rely on Manual Approval (Operator Intervention for Server CSRs):** High operational overhead, leading to delays and potential cluster instability during scale-up or recovery events. Failure to approve the Kubelet serving certificate CSRs prevents the API server from connecting to the kubelet, causing operational commands (such as `oc exec`, `oc rsh`, and `oc logs`) to fail.
- **Implement Automated CSR Approval Mechanism:** Requires deploying and maintaining an external component (the custom controller), but ensures smooth day-2 operations and node lifecycle management. The automated method must implement checks to verify the validity of the Kubelet serving certificate requests, typically by confirming the request was submitted by the `node-bootstrapper` service account in the `system:node` or `system:admin` groups, and confirming the identity of the node.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: OCP Platform Owner

---
