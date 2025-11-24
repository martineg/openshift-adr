# ARCHITECTURE DECISION RECORDS FOR: OpenShift Pipelines

## PIPELINES-01

**Title**
CI/CD Engine Selection

**Architectural Question**
Which technology will be the standardized engine for Continuous Integration and Continuous Delivery (CI/CD) workflows executed on the platform?

**Issue or Problem**
To automate builds and deployments, a supported CI/CD engine must be selected. The choice impacts the operational model (server-based vs. serverless), resource scaling, and developer experience.

**Assumption**
A CI/CD solution is required for building and deploying applications.

**Alternatives**

- **OpenShift Pipelines (Tekton):** Kubernetes-native, serverless CI/CD.
- **OpenShift Jenkins:** Traditional, server-based CI.
- **External CI (e.g., GitLab CI, GitHub Actions):** SaaS or external hosted runners.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OpenShift Pipelines (Tekton):** Standardizes on a modern, Kubernetes-native architecture. Pipelines run as Pods on-demand (Serverless), scaling to zero when unused. It integrates tightly with the platform's RBAC and quotas.
- **OpenShift Jenkins:** Leverages existing institutional knowledge and legacy Jenkinsfiles. Suitable for teams migrating complex, imperative Groovy pipelines that cannot easily be converted to YAML.
- **External CI:** Offloads the compute burden of builds to an external system.

**Implications**

- **OpenShift Pipelines (Tekton):**
  - Requires learning Tekton primitives (Task, Pipeline, Workspace).
  - Stateless execution requires external storage (PVC/S3) for artifact persistence between steps (see PIPELINES-02).
  - Native support for "Pipelines as Code" workflows.
- **OpenShift Jenkins:**
  - Requires managing a "Pet" Jenkins server (plugins, updates, memory scaling).
  - Often struggles with resource quotas in multi-tenant clusters compared to Tekton.
- **External CI:**
  - Requires configuring secure ingress/egress for the external runner to deploy into the OpenShift cluster.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: DevOps Lead

---

## PIPELINES-02

**Title**
Pipeline Execution Storage (Workspaces)

**Architectural Question**
What type of storage will be used for pipeline workspaces?

**Issue or Problem**
Pipelines require storage (workspaces) to clone source code, store intermediate artifacts, and share data between tasks. The choice of storage affects performance, cost, and data persistence.

**Assumption**
OpenShift Pipelines will be deployed.

**Alternatives**

- Ephemeral Storage (emptyDir)
- Persistent Volume Claims (PVCs)
- Ephemeral/Persistent Storage with Cache Step Actions (TP)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Ephemeral Storage (emptyDir):** Uses temporary, node-local storage (RAM or disk space) for the duration of the pipeline run. Ideal for cloning source code or storing temporary intermediate artifacts that must be shared between sequential tasks, but do not require persistence after the pipeline finishes.
- **Persistent Volume Claims (PVCs):** Uses persistent storage (e.g., ODF, native cloud storage) managed by a StorageClass. Necessary for tasks requiring cache volumes (e.g., dependency cache) or when outputs must be retained after the pipeline completes.
- **Ephemeral/Persistent Storage with Cache Step Actions (TP):** Leveraging step actions like cache-upload and cache-fetch (TP) allows preserving cache directories (dependencies) in remote storage (S3, GCS, OCI repository) to enhance performance between runs, irrespective of the core workspace configuration

**Implications**

- **Ephemeral Storage (emptyDir):** No explicit storage consumption cost, but transient data is lost if the pod restarts or the pipeline finishes. Requires tasks to fetch dependencies anew each run.
- **Persistent Volume Claims (PVCs):** Incurs storage consumption costs and management overhead for the PVC lifecycle. Must ensure the underlying storage class supports the required access mode (RWO or RWX, depending on sharing needs).
- **Ephemeral/Persistent Storage with Cache Step Actions (TP):** This is a Technology Preview feature and is not recommended for production workloads. It requires external storage configuration (S3, GCS, OCI repository) to preserve the cache directories.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert

---

## PIPELINES-03

**Title**
Limiting Aggregate Compute Resource Consumption

**Architectural Question**
How should aggregate compute resource consumption (CPU, memory) for all pipeline-generated pods be enforced if direct pipeline resource quotas are unavailable?

**Issue or Problem**
OpenShift Pipelines does not enable directly specifying the compute resource quota for a pipeline, potentially leading to unbounded resource use if only default limits (BestEffort) are set

**Assumption**
Performance must be maintained by limiting the total simultaneous compute resources consumed by CI/CD execution pods.

**Alternatives**

- Enforce Explicit Resource Requests/Limits on all Tasks/Steps
- Use PriorityClass and ResourceQuota

**Decision**
#TODO: Document the decision.#

**Justification**

- **Enforce Explicit Resource Requests/Limits on all Tasks/Steps:** Provides precise, granular control over resources consumed by each container.
- **Use PriorityClass and ResourceQuota:** Allows defining an aggregate hard quota (CPU, memory, pods) applied specifically to pipeline workloads identified by a designated `PriorityClass`, providing cluster-wide resource control over pipeline consumption..

**Implications**

- **Enforce Explicit Resource Requests/Limits on all Tasks/Steps:** Increases complexity and administrative burden; requires careful planning and definition for every step in every task.
- **Use PriorityClass and ResourceQuota:** Requires pre-defining a `PriorityClass` object and configuring a `ResourceQuota` with a `scopeSelector` matching that class. If requests/limits are missing on the pods, a compensating LimitRange might be necessary.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operation Expert

---

## PIPELINES-04

**Title**
Pipelines as Code (PaC) Adoption Strategy

**Architectural Question**
What strategy will be adopted for defining and executing CI/CD workflows using OpenShift Pipelines?

**Issue or Problem**
CI/CD pipelines should be managed declaratively alongside application source code to facilitate GitOps principles and version control of the entire development and deployment process.

**Assumption**
OpenShift Pipelines will be deployed.

**Alternatives**

- Manual Definition of Tekton Resources
- Pipelines as Code (PaC) Integration (using Repository CR)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Manual Definition of Tekton Resources:** To define and apply `Pipeline` and `PipelineRun` resources directly to the cluster, typically via CLI commands or application manifests. This offers maximum control but lacks the Git integration benefits of PaC.
- **Pipelines as Code (PaC) Integration (using Repository CR):** To leverage the **Repository custom resource (CR)**, repository webhooks, and GitOps commands (like in-line comments) to trigger and manage Tekton pipelines directly from the Git repository.This tightly aligns the CI/CD definition with the application source code.

**Implications**

- **Manual Definition of Tekton Resources:** Requires external orchestration (e.g., Jenkins, GitLab CI) to manage pipeline runs, increasing complexity.
- **Pipelines as Code (PaC) Integration:** Requires configuring webhooks on the source control system and deployment of the specialized PaC components within the cluster. Using the `pipelinesascode.tekton.dev/cancel-in-progress: "true"` annotation or global settings enables automatic cancellation-in-progress (TP) for stale runs, consuming fewer cluster resources. These global settings include `enable-cancel-in-progress-on-pull-requests` (TP) and `enable-cancel-in-progress-on-push` (TP). This feature is currently for testing and feedback. Furthermore, enabling PaC allows overriding a task in a remote pipeline definition by supplying a task definition with the same name (TP). The system automatically populates a new Pipelines as Code dynamic variable, `pull_request_number` (TP), for push events triggered by pull requests, allowing for a clear reference to the specific pull request associated with the push event and improving traceability. The reliance on remote resource resolution means adopting Artifact Hub or a self-hosted Tekton Hub instance, as the public instance of Tekton Hub (hub.tekton.dev) is deprecated and scheduled for removal.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## PIPELINES-05

**Title**
Pipeline Triggering Mechanism

**Architectural Question**
How will pipelines be initiated?

**Issue or Problem**
A strategy is needed to determine how pipelines are triggered. This affects the level of automation, integration with source control, and enabling event-driven workflows.

**Assumption**
OpenShift Pipelines (Tekton) will be used for CI/CD automation.

**Alternatives**

- Manual Triggering (CLI/Console)
- Git Webhooks via Tekton Triggers
- GitOps/ArgoCD Synchronization

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Manual Triggering (CLI/Console):** Simplest implementation, suitable for early development or troubleshooting, requiring no external integration setup.
- **Git Webhooks via Tekton Triggers:** To enable event-driven CI/CD, automatically running pipelines (Builds, Tests) immediately upon source code changes (e.g., git push, pull request open). Utilizes Common Expression Language (CEL) Interceptors for advanced event processing and filtering based on the event payload.
- **GitOps/ArgoCD Synchronization:** To enforce a declarative deployment state, allowing the GitOps tool to manage the continuous execution of promotion or synchronization pipelines. This option can rely on community tasks like argocd-task-sync-and-wait.

**Implications**

- **Manual Triggering (CLI/Console):** Lack of automation results in manual operational overhead for application release management.
- **Git Webhooks via Tekton Triggers:** Requires securing and managing webhook secrets and configuration. Enables fine-grained control over when pipelines run (e.g., running only if a specific result from a previous task is met). The functionality to trigger a pipeline run that does not match an event using comments (e.g., /retest) is a (TP) feature.
- **GitOps/ArgoCD Synchronization:** Requires defining pipelines that operate based on repository state rather than transient events. This aligns with GitOps principles but may not support rapid CI/test cycles.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert

---

## PIPELINES-06

**Title**
Manual Approval Gate Strategy

**Architectural Question**
What mechanism should be adopted to pause CI/CD workflows pending explicit human approval?

**Issue or Problem**
The release process requires a formal gate (e.g., security sign-off or production deployment approval) that mandates pausing the pipeline execution until an authorized user approves the continuation or rejects the task, potentially failing the pipeline.

**Assumption**
A formal approval step is mandatory in high-risk delivery paths (e.g., promotion to production).

**Alternatives**

- Manual Approval Gate (TP)
- External Ticketing System Integration (Out of Scope for Core Pipelines Feature)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Manual Approval Gate (TP):** To leverage the built-in mechanism provided by the manual approval gate controller to pause pipeline execution and await input from configured OpenShift Container Platform users.
- **External Ticketing System Integration:** To integrate with enterprise IT Service Management (ITSM) workflows (e.g., ServiceNow, Jira), ensuring approvals are recorded and managed within the organization's standard change management system rather than inside the cluster.

**Implications**

- **Manual Approval Gate (TP):** This feature is marked as **Technology Preview (TP)** and is not supported with Red Hat production service level agreements (SLAs). Requires enabling the manual approval gate controller.
- **External Ticketing System Integration:** Requires developing and maintaining custom Tekton Tasks to interact with external APIs. Increases complexity regarding authentication and network connectivity to the ticketing system. The pipeline logic must handle polling for status or complex webhook callbacks to resume execution.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## PIPELINES-07

**Title**
RHEL Entitlements Provisioning for Build Tasks

**Architectural Question**
How will the necessary Red Hat Enterprise Linux (RHEL) entitlements be securely provided to Buildah tasks within different pipeline namespaces?

**Issue or Problem**
Pipelines building RHEL-based container images require access to the `etc-pki-entitlement` secret, which must be mounted to the `rhel-entitlement` workspace in the Buildah task.

**Assumption**
RHEL entitlements are managed by the Insight Operator and available as the `etc-pki-entitlement` secret in `openshift-config-managed`.

**Alternatives**

- Manual Secret Copy
- Shared Resources CSI Driver Operator

**Decision**
#TODO: Document the decision.#

**Justification**

- **Manual Secret Copy:** Simplest operational approach if the number of pipeline namespaces is limited, requiring a single command to copy the secret using `oc get secret` and `jq`.
- **Shared Resources CSI Driver Operator:** Automates secret sharing across multiple namespaces, reducing operational overhead in large environments, and requiring configuration of a `SharedSecret` resource.

**Implications**

- **Manual Secret Copy:** Requires re-executing the copy command manually for every new pipeline namespace.
- **Shared Resources CSI Driver Operator:** Requires installation and enabling of the Shared Resources CSI Driver Operator.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## PIPELINES-08

**Title**
Pipeline Run and Task Run Pruning Strategy

**Architectural Question**
What strategy should be implemented for the automatic pruning of stale PipelineRun and TaskRun objects to conserve cluster resources?

**Issue or Problem**
Completed TaskRun and PipelineRun objects occupy physical resources, and automated cleanup is required for optimal resource utilization.

**Assumption**
Automated cleanup based on completion time or count retention limits must be globally configured.

**Alternatives**

- Job-based Pruner (Default)
- Event-based Pruner (TP)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Job-based Pruner (Default):** Provides periodic cleanup based on a configurable schedule (`schedule`) and retention policies (keep or keep-since).
- **Event-based Pruner (TP):** Prunes resources in near real time by listening for resource events, potentially offering faster cleanup compared to periodic jobs

**Implications**

- **Job-based Pruner (Default):** Runs periodically, meaning resource consumption might lag behind completion times
- **Event-based Pruner (TP):** This feature is Technology Preview (TP) and not recommended for production. Enabling this requires disabling the default job-based pruner in the TektonConfig CR.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
