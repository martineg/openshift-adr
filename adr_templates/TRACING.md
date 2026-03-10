# ARCHITECTURE DECISION RECORDS FOR: Red Hat OpenShift Distributed Tracing

## TRACING-01: Trace Collection and Instrumentation Strategy

**Architectural Question**
What strategy will be used to deploy the Red Hat build of OpenTelemetry Collector (OTC) and instrument applications to send traces?

**Issue or Problem**
A method is needed to automatically or manually inject instrumentation into applications and route the collected telemetry data to the central tracing backend.

**Assumption**
N/A

**Alternatives**

- Sidecar Injection (OTEL Collector Sidecar Mode)
- Centralized Collector (OTEL Collector Deployment/DaemonSet Mode)

**Decision**
#TODO: Document the decision for application instrumentation and collection deployment.#

**Justification**

- **Sidecar Injection:** To simplify the developer experience by having the OpenTelemetry Collector run as a sidecar in the application pod, automatically receiving data via localhost. This removes the need for application teams to manually configure network endpoints.
- **Centralized Collector (Deployment/DaemonSet Mode):** To consolidate telemetry collection outside of application pods, minimizing resource consumption in the application runtime environment. This requires applications to be configured manually with the correct OTLP endpoint (e.g., `OTEL_EXPORTER_OTLP_ENDPOINT`).

**Implications**

- **Sidecar Injection:** Requires the OpenTelemetry Operator to be configured for sidecar mode and the use of the `sidecar.opentelemetry.io/inject` annotation on application deployments. Increases resource usage slightly within each application pod.
- **Centralized Collector:** Requires configuration of network policies and routing to ensure that application pods can reach the central Collector deployment (Deployment or DaemonSet mode). Requires applications to be instrumented to send data directly to the collector service endpoint.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## TRACING-02: Trace Storage and Aggregation Solution

**Architectural Question**
Which Red Hat Distributed Tracing Platform architecture will be used for trace storage, aggregation, and query?

**Issue or Problem**
A robust and scalable backend system is required to persist trace data collected by the OpenTelemetry Collector and enable efficient querying and visualization.

**Assumption**
N/A

**Alternatives**

- TempoStack (Microservices Mode)
- TempoMonolithic (Monolithic Mode) (TP)

**Decision**
#TODO: Document the decision for the trace backend architecture.#

**Justification**

- **TempoStack (Microservices Mode):** To deploy a highly available and horizontally scalable tracing backend based on Grafana Tempo, suitable for production workloads and large data volumes. This architecture separates components like the Distributor, Ingester, and Query Frontend for high scalability.
- **TempoMonolithic (Monolithic Mode) (TP):** To deploy a single-container instance containing all Tempo components (Compactor, Distributor, Ingester, Query Frontend). This mode is preferred for small deployments, demonstrations, testing, or as a migration path from the deprecated Jaeger all-in-one deployment.

**Implications**

- **TempoStack (Microservices Mode):** Requires external object storage (e.g., ODF, S3, GCS, Azure Blob Storage) for persistence. Provides separation of resource utilization across multiple components and supports horizontal scaling.
- **TempoMonolithic (TP):** Is a **Technology Preview** feature, meaning it is not supported under production SLAs and does not scale horizontally.
- **General:** Requires the installation of the Tempo Operator. Visualization is achieved through the Jaeger UI exposed via the Query Frontend or the Distributed Tracing UI plugin of the Cluster Observability Operator.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## TRACING-03

**Title**
Collector Deployment Mode

**Architectural Question**
How will the OpenTelemetry Collector be deployed to balance resource usage and scalability?

**Issue or Problem**
The Collector can run as a DaemonSet (one per node), a Deployment (scaled horizontally), or a Sidecar. This choice impacts CPU/RAM usage and network topology.

**Assumption**
OpenTelemetry is enabled.

**Alternatives**

- **DaemonSet Mode:** Runs on every node. Receives traces from local pods.
- **Deployment Mode:** Runs as a scalable service. Centralized processing.
- **Sidecar Mode:** Injected into every application pod.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **DaemonSet:** Good for infrastructure correlation (node metadata). Efficient for high-volume node-local traffic.
- **Deployment:** Decouples collector scaling from node count. Best for processing/filtering logic (tail sampling).
- **Sidecar:** Simplifies app configuration (send to localhost). High resource overhead (N sidecars for N apps).

**Implications**

- **DaemonSet:** Uses resources on every node, even if no apps are tracing.
- **Deployment:** Requires LoadBalancer/Service for apps to reach it.
- **Sidecar:** Increases Pod resource requests. Updates require app redeployment.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## TRACING-04

**Title**
Trace Object Storage Backend

**Architectural Question**
Which object storage solution will be used to persist Tempo trace data?

**Issue or Problem**
Tempo requires an S3-compatible backend.

**Assumption**
TempoStack is selected.

**Alternatives**

- **OpenShift Data Foundation (ODF/MCG):** On-cluster S3.
- **External Cloud S3 (AWS/Azure/GCP):** Managed object storage.
- **MinIO:** Simple, self-hosted.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **ODF:** Keeps data local. Integrated support.
- **External Cloud S3:** Infinite scale, offloads management.
- **MinIO:** Good for testing or simple on-prem setups without ODF.

**Implications**

- **ODF:** Consumes cluster storage resources.
- **Cloud S3:** Egress costs. Requires managing cloud credentials (STS recommended).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## TRACING-05

**Title**
Multi-Tenancy Strategy

**Architectural Question**
Will Tempo be configured in multi-tenant mode to isolate trace data between teams?

**Issue or Problem**
Without multi-tenancy, all traces are visible to anyone with read access.

**Assumption**
N/A

**Alternatives**

- **Single Tenant (Global):** All traces shared.
- **Multi-Tenant:** Traces isolated by tenant ID (often Namespace).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Single Tenant:** Simple. Good for small teams or debugging.
- **Multi-Tenant:** Essential for large shared clusters. Enforces RBAC on trace data.

**Implications**

- **Multi-Tenant:** Requires Gateway/Auth configuration (often via sidecar or gateway). Clients must send `X-Scope-OrgID` header.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## TRACING-06

**Title**
Instrumentation Strategy (Auto vs Manual)

**Architectural Question**
Will applications rely on the OpenTelemetry Operator's auto-instrumentation injection or manual code instrumentation?

**Issue or Problem**
Developers can manually add OTEL SDKs to code, or Ops can inject agents at runtime.

**Assumption**
N/A

**Alternatives**

- **Auto-Instrumentation (Operator Injection):** Zero-code.
- **Manual Instrumentation:** Developers add SDKs.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Auto-Instrumentation:** Rapid adoption. No code changes needed. Ideal for Java/Python/Nodejs.
- **Manual Instrumentation:** Full control over spans/tags. Required for compiled languages (Go) or custom logic.

**Implications**

- **Auto-Instrumentation:** Adds initialization overhead to Pod start.
- **Manual:** Maintenance burden on dev teams.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Application team leadership
- Person: #TODO#, Role: OCP Platform Owner

---

## TRACING-07

**Title**
Sampling Strategy

**Architectural Question**
What sampling strategy will be used to control trace volume?

**Issue or Problem**
Tracing 100% of requests is expensive and often unnecessary.

**Assumption**
N/A

**Alternatives**

- **Head Sampling (Probabilistic):** Random % of traces kept at start.
- **Tail Sampling:** Decisions made after trace completes (keep errors/slow traces).
- **100% Sampling:** Keep everything.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Head Sampling:** Low overhead. Good for general trends.
- **Tail Sampling:** High value (keeps the "interesting" broken traces). High resource cost (must buffer traces in memory).

**Implications**

- **Tail Sampling:** Requires `Deployment` mode Collector with significant RAM.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## TRACING-08

**Title**
Visualization Interface Strategy

**Architectural Question**
Which UI will be used to visualize traces?

**Issue or Problem**
Users need a frontend to search traces.

**Assumption**
N/A

**Alternatives**

- **Console Plugin (Distributed Tracing UI):** Embedded in OCP Console.
- **Standalone Jaeger UI:** Dedicated URL.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Console Plugin:** Seamless experience. Single sign-on.
- **Standalone Jaeger UI:** Familiar to legacy users. Advanced query features may appear here first.

**Implications**

- **Console Plugin:** Requires enabling the plugin.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---
