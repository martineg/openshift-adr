# ARCHITECTURE DECISION RECORDS FOR: OpenShift GitOps

## GITOPS-01

**Title**
Platform GitOps Deployment Scope

**Architectural Question**
Will platform configuration (NodeConfigs, Networking, Operator subscriptions) be managed locally within each cluster or centrally from a dedicated hub/management cluster?

**Issue or Problem**
Platform management for multiple clusters (fleet management) requires standardization and governance. Choosing the right scope impacts consistency, scalability, and recovery posture.

**Assumption**
Multiple managed OpenShift clusters exist, necessitating a multi-cluster management strategy.

**Alternatives**

- Local/Decentralized Scope
- Centralized Hub Scope (Managed by RHACM)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Local/Decentralized Scope:** Each managed cluster hosts its own configuration Argo CD instance responsible only for local platform settings. This ensures the cluster remains operational and manageable even if network connectivity to a central hub is temporarily lost. This model can leverage Infrastructure Nodes to isolate GitOps control plane workloads for cost management and maintenance separation.
- **Centralized Hub Scope (Managed by RHACM):** Leverages a central OpenShift cluster (the Hub) running Red Hat Advanced Cluster Management (RHACM) and Argo CD ApplicationSets. This approach uses RHACM PolicyGenerator CRs to enforce compliance and roll out consistent configurations (e.g., policy updates, MachineConfigs) across the entire fleet declaratively, which is fundamental to GitOps ZTP deployments. Scalability can be enhanced using Dynamic Scaling of Shards (TP) and the Round-Robin Sharding Algorithm (TP), especially when managing a large fleet of clusters.

**Implications**

- **Local/Decentralized Scope:** Requires custom tooling outside of the cluster itself to orchestrate configuration updates consistently across the entire fleet, leading to potential configuration drift. Requires care when scheduling components on Infrastructure Nodes, as manually added node selectors/tolerations might be overwritten by the GitOpsService configuration.
- **Centralized Hub Scope (Managed by RHACM):** Provides centralized visibility and control (Single Pane of Glass). It requires the Hub cluster and the RHACM infrastructure to be highly available. This model is commonly used for large-scale management, particularly in edge computing scenarios. Adoption of Dynamic Scaling of Shards (TP) or the Round-Robin Sharding Algorithm (TP) means relying on features that are not supported with Red Hat production service level agreements (SLAs).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## GITOPS-02

**Title**
Argo CD Instance Scoping (Instance Architecture)

**Architectural Question**
What is the scoping strategy for the Argo CD instance(s) deployed by the OpenShift GitOps Operator?

**Issue or Problem**
The choice of Argo CD scope (cluster-wide or namespace-specific) impacts security, multi-tenancy capabilities, operational overhead, and administrative separation between platform management and application delivery.

**Assumption**
OpenShift GitOps (Argo CD) is the chosen engine for declarative configuration management.

**Alternatives**

- Single Cluster-Scoped Instance (Shared)
- Dual Instance (Dedicated Platform Instance + Application Instance(s))
- Namespace-Scoped Instances (Application Delivery Only)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Single Cluster-Scoped Instance (Shared):** Provides the simplest operational profile with the lowest overhead. Suitable when administrative separation between platform configuration and applications is not a primary concern. The default instance is cluster-scoped. The new ability to define local users in the Argo CD CR simplifies creating API tokens for automation tasks. The decision to reduce reliance on external SSO/RBAC is reinforced by the removal of support for Keycloak-based authentication starting in OpenShift GitOps 1.18. SSO reliance now defaults to Dex, which integrates with the OpenShift OAuth server.
- **Dual Instance (Dedicated Platform Instance + Application Instance(s)):** Provides strict separation of concerns, ensuring platform administration tasks are isolated from application rollouts. The platform team manages the Cluster-scoped instance, while application teams utilize dedicated instances or segregated resources. The inclusion of local users allows administrators to declaratively define dedicated users and manage their API tokens in the Argo CD CR for automation scenarios. The removal of support for Keycloak-based authentication (as of GitOps 1.18) mandates migration to Dex or a self-managed Red Hat Build of Keycloak (RHBK) instance for external identity providers.
- **Namespace-Scoped Instances (Application Delivery Only):** Maximizes security and blast radius reduction by limiting each Argo CD instance to a single namespace (project). The availability of local user management reduces the reliance on external SSO/RBAC configurations for automation accounts required in these segregated instances. The removal of support for Keycloak-based authentication (as of GitOps 1.18) means automation relying on SSO must use Dex or alternative authentication methods.

**Implications**

- **Single Cluster-Scoped Instance (Shared):** Any configuration error in one domain (e.g., application) could potentially impact cluster-wide stability. Higher privileges are required for the single Argo CD instance.
- **Dual Instance (Dedicated Platform Instance + Application Instance(s)):** Increases management complexity due to multiple Argo CD installations and potentially overlapping configuration files.
- **Namespace-Scoped Instances (Application Delivery Only):** The NamespaceManagement CR enables tenants to delegate control of their own namespaces to Argo CD instances without requiring direct cluster administrator action. Cluster administrators must explicitly enable this feature in the Subscription CR using the environment variable `ALLOW_NAMESPACE_MANAGEMENT_IN_NAMESPACE_SCOPED_INSTANCES` and specify allowed namespaces in the Argo CD CR. The explicit use of the `.spec.sso` parameter is now required for SSO configuration, as the older `.spec.dex` parameter is no longer supported from OpenShift GitOps v1.10.0 onwards.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## GITOPS-03

**Title**
Repository Structure

**Architectural Question**
What is the strategy for structuring the Git repositories that store configuration manifests?

**Issue or Problem**
The organization of Git repositories is the foundation of a GitOps practice. The choice between a monorepo versus multirepo impacts access control, CI/CD pipeline complexity, and change promotion.

**Assumption**
A GitOps operational model will be used.

**Alternatives**

- Monorepo
- Multirepo (Repo per Component)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Monorepo:** To simplify dependency management and atomic changes across multiple components by keeping all platform and application manifests in a single repository. This strategy requires advanced tooling, such as Argo CD ApplicationSets, to handle logical separation across tenants and clusters.
- **Multirepo (Repo per Component):** To provide strong ownership and access control by giving each team or application its own repository. This aligns well with a microservices architecture.

**Implications**

- **Monorepo:** Leveraging Argo CD application sets in non-control plane namespaces remains a Technology Preview (TP) feature. Allowing ApplicationSet resources in non-control plane namespaces can result in the exfiltration of secrets through malicious API endpoints in Source Code Manager (SCM) Provider or Pull Request (PR) generators. To prevent unauthorized access, the Operator disables the SCM Provider and PR generators by default, requiring administrators to explicitly define a list of allowed SCM Providers (`.spec.applicationSet.scmProviders`) in the Argo CD CR to use these generators.
- **Multirepo (Repo per Component):** Increases the number of repositories, secrets, and webhooks to manage. Requires cross-repository tooling if dependencies exist between components.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## GITOPS-04

**Title**
Multi-tenancy Application/ApplicationSet Placement Strategy

**Architectural Question**
Should multi-tenant application deployments leverage the new features allowing Applications and ApplicationSets to be defined in user-owned (non-control plane) namespaces, and if so, what governance model will be enforced?

**Issue or Problem**
In multi-tenant environments, isolating deployment logic (Applications and ApplicationSets) to tenant namespaces increases autonomy and reduces the blast radius. However, enabling these features requires explicit cluster administrator action and introduces security concerns if misused.

**Assumption**
Multi-tenancy must support isolation between application delivery teams (tenants).

**Alternatives**

- Standard Deployment from Control Plane (Legacy/GA)
- Applications in any namespace (GA) + ApplicationSets in non-control plane namespaces (TP)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Applications in any namespace (GA) + ApplicationSets in non-control plane namespaces (TP):** This approach maximizes security and flexibility for isolated teams by allowing them to manage their Application/ApplicationSet resources within their own namespaces. The Applications feature is Generally Available (GA) since OpenShift GitOps 1.13.0. Leveraging ApplicationSets in non-control plane namespaces greatly improves scalability and deployment pattern repeatability for tenants, although this part is **Technology Preview (TP)**.
- **Standard Deployment from Control Plane (Legacy/GA):** Retains tight central control, as applications are managed solely from the `openshift-gitops` control plane namespace. This provides strong governance but reduces tenant autonomy.

**Implications**

- **Applications in any namespace (GA) + ApplicationSets in non-control plane namespaces (TP):** Requires the cluster administrator to explicitly enable and configure target namespaces in the ArgoCD CR using `.spec.sourceNamespaces`. Administrators must also enforce strict separation by creating **user-defined AppProject instances** in the control plane namespace and ensuring tenants do not configure non-control plane namespaces in privileged AppProjects to **prevent privilege escalations**. Relying on ApplicationSets in non-control plane namespaces means relying on a feature that is **not supported with Red Hat production service level agreements (SLAs) (TP)**.
- **Standard Deployment from Control Plane (Legacy/GA):** Increases centralized management overhead and may reduce tenant flexibility.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## GITOPS-05

**Title**
Secret Management Strategy

**Architectural Question**
How will secrets be securely managed and exposed to applications deployed via GitOps?

**Issue or Problem**
Storing unencrypted secrets in Git is a major security risk. A secure solution is required to manage secrets (e.g., API keys, passwords) and make them available to applications at runtime.

**Assumption**
Applications require secrets, and a GitOps operational model will be used.

**Alternatives**

- Vault/External Secrets Manager (e.g., Sealed Secrets)
- External Secrets Operator (TP)
- Secrets Store CSI Driver (SSCSI)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Vault/External Secrets Manager (e.g., Sealed Secrets):** To provide a robust, community-accepted method for securely encrypting secrets stored in Git, requiring manual decryption/injection at deployment time or relying on third-party tooling outside the standard OLM ecosystem.
- **External Secrets Operator (TP):** To leverage the specialized Red Hat Operator (based on upstream external-secrets) for securely integrating with external secret management systems (like dedicated vaults), pulling secrets dynamically at runtime to avoid storing sensitive data in the Git repository entirely.
- **Secrets Store CSI Driver (SSCSI):** To use the modern approach for securely retrieving secrets from external stores (like HashiCorp Vault or AWS Secrets Manager) and mounting them directly as a volume into application pods at runtime, enhancing security and efficiency

**Implications**

- **Vault/External Secrets Manager (e.g., Sealed Secrets):** The encryption key is managed within the cluster, creating a dependency on the controller's availability. Sharing secrets across clusters requires sharing the private key. The Red Hat OpenShift GitOps Operator manages the core Argo CD secret (`argocd-secret`). Modifying this secret using external secret management solutions (like Vault or the External Secrets Operator/plugins) is warned against, as it can cause reconciliation conflicts or unpredictable behavior. The Argo CD CR now supports configuring sensitive annotation masking in the Argo CD web UI/CLI via the `.spec.extraConfig.resource.sensitive.mask.annotations` field, which prevents the accidental exposure of sensitive information stored in annotations on Secret resources.
- **External Secrets Operator (TP):** This feature is marked as **Technology Preview (TP)**, meaning it is **not supported with Red Hat production service level agreements (SLAs)** and might not be functionally complete. Requires integration and maintenance of the External Secrets Operator and the chosen external secret store. The Red Hat OpenShift GitOps Operator manages the core Argo CD secret (`argocd-secret`). Modifying this secret using external secret management solutions (like Vault or the External Secrets Operator/plugins) is warned against, as it can cause reconciliation conflicts or unpredictable behavior. The Argo CD CR now supports configuring sensitive annotation masking in the Argo CD web UI/CLI via the `.spec.extraConfig.resource.sensitive.mask.annotations` field, which prevents the accidental exposure of sensitive information stored in annotations on Secret resources.
- **Secrets Store CSI Driver (SSCSI):** Requires additional configuration and setup of the SSCSI Driver Operator, providers (e.g., AWS, Vault), and appropriate Kubernetes Service Account permissions for role binding to the external vault. This approach prevents sensitive data from existing in Kubernetes secrets. The Argo CD CR now supports configuring sensitive annotation masking in the Argo CD web UI/CLI via the `.spec.extraConfig.resource.sensitive.mask.annotations` field, which prevents the accidental exposure of sensitive information stored in annotations on Secret resources.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## GITOPS-06

**Title**
Local User Management and API Token Strategy

**Architectural Question**
What is the preferred method for generating and managing non-human (automation) API tokens for Argo CD access?

**Issue or Problem**
Automation tasks (e.g., CI/CD pipelines, monitoring integrations) require API tokens to interact with Argo CD. A standard method is required to provision, secure, and manage the lifecycle of these tokens, balancing the need for long-lived tokens with security best practices.

**Assumption**
OpenShift SSO (Dex) is the primary method for human user authentication. Dedicated API tokens are required for automation.

**Alternatives**

- SSO Integration (Automated Token Generation via external means)
- Local User Management (via Argo CD CR)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Local User Management (via Argo CD CR):** Provides **built-in support for managing local users** intended for automation scenarios that require API tokens. Allows declarative definition of users, automatic token generation/renewal, configuration of token lifetimes, and secure storage in Kubernetes secrets. This simplifies creating API tokens for automation tasks compared to relying solely on external SSO systems.
- **SSO Integration (Automated Token Generation via external means):** Relies on potentially more complex external systems (e.g., Vault or custom logic interacting with OIDC) to mint tokens, but aligns identity management with existing corporate security policies (N/A: Not supported natively in Argo CD CR for automation users). The removal of support for Keycloak-based authentication (as of GitOps 1.18) mandates migration to Dex or a self-managed Red Hat Build of Keycloak (RHBK) instance for external identity providers if SSO is required.

**Implications**

- **Local User Management (via Argo CD CR):** Requires administrators to declaratively manage local user definitions and token configurations within the Argo CD Custom Resource. The Argo CD Operator handles the token lifecycle, including automatic renewal for tokens with set lifetimes greater than 0h. **Disabled users cannot log in or use an API token**, but their configuration is preserved.
- **SSO Integration (Automated Token Generation via external means):** Requires managing external integration components and ensuring the proper RBAC configuration outside of the Argo CD CR itself.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Operations Expert

---

## GITOPS-07

**Title**
Argo CD Control Plane Workload Sizing

**Architectural Question**
What baseline resource requests and limits (CPU/Memory) should be applied to core Argo CD control plane workloads (Application Controller, Repo Server, Server, Redis, ApplicationSet Controller) to ensure stability and compatibility with resource quotas?

**Issue or Problem:**
Deploying Argo CD instances in namespaces with resource quotas requires defining resource requests and limits, otherwise, the Operator installation may fail. Standardized sizing is needed for consistent performance and operational stability.

**Assumption**
Argo CD workloads must run reliably in environments constrained by quotas. Initial sizing can be derived from the default workload configuration specified by Red Hat.

**Alternatives**

- Default Operator Settings
- Standardized Low Profile
- Standardized High Profile

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Operator Settings:** Using the default resource requests and limits provided by the Operator ensures compatibility and avoids failure in namespaces with quotas. Example requests include **250m CPU and 1Gi memory for the Application Controller**, and **250m CPU and 512Mi memory for the ApplicationSet Controller**.
- **Standardized Low Profile:** Setting explicit minimum requests helps **guarantee minimum resources** for stability, while slightly higher limits can prevent unbounded resource consumption in shared environments. This is achieved by defining the `.spec.<component>.resources` field in the Argo CD CR.

**Implications**

- **Standardized Low Profile:** Custom sizing ensures compliance with resource quotas upon deployment. Patches may be required post-installation to update specific components if resource usage changes. **Increasing memory limits for Redis** might be necessary when managing a large number of resources.
- **Default Operator Settings:** These settings reflect the necessary minimums and limits for the default installation but might require overrides if the cluster needs to accommodate significantly high load or extremely strict quotas.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
