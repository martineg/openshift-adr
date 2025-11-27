# ARCHITECTURE DECISION RECORDS FOR: OpenShift Logging

## LOG-01

**Title**
Logging Platform Solution

**Architectural Question**
Which solution will be used for collecting and analyzing container and platform logs?

**Issue or Problem**
A dedicated logging solution is required to gather, process, and make logs queryable for troubleshooting, capacity planning, and compliance auditing.

**Assumption**
N/A

**Alternatives**

- OpenShift Logging (LokiStack) using ViaQ Data Model
- OpenShift Logging (LokiStack) using OpenTelemetry (OTEL) Data Model (TP)
- External Log Collector (Forwarding Only)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OpenShift Logging (LokiStack) using ViaQ Data Model:** To deploy the integrated logging stack **(using the Vector collector)** which collects logs from platform and user workloads, providing visualization and storage within the cluster. This is the standard, supported approach for on-cluster visibility and the default data model when forwarding logs to LokiStack.
- **OpenShift Logging (LokiStack) using OpenTelemetry (OTEL) Data Model (TP):** To deploy the integrated logging stack utilizing the OpenTelemetry data model. This is a **(TP)** feature not recommended for production due to lack of production SLAs, but it aligns with modern observability standards and is planned to become the future default.
- **External Log Collector (Forwarding Only):** To rely exclusively on an external log aggregation tool, configuring the cluster only to forward logs without storing or querying them internally. This minimizes resource consumption on the cluster but eliminates immediate in-cluster visibility.

**Implications**

- **OpenShift Logging (LokiStack) using ViaQ Data Model:** Requires sizing the local log store appropriately and consumes worker node resources for storage and indexing.
- **OpenShift Logging (LokiStack) using OpenTelemetry (OTEL) Data Model (TP):** This is a (TP) feature. Requires careful configuration, including setting schema version v13 on the LokiStack CR for structured metadata support.
- **External Log Collector (Forwarding Only):** Requires network configuration to reach the external collector. Cluster health monitoring relies heavily on the external system.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## LOG-02

**Title**
Log Forwarding

**Architectural Question**
Will logs be forwarded to an external, long-term storage or analysis system?

**Issue or Problem**
On-cluster log storage is typically for short-term retention. For long-term archival, compliance, and advanced analytics, logs must be forwarded to a centralized, external system.

**Assumption**
N/A

**Alternatives**

- External Log Forwarding Enabled
- External Log Forwarding Disabled

**Decision**
#TODO: Document the decision.#

**Justification**

- **External Log Forwarding Enabled:** To satisfy compliance requirements for long-term data retention and to enable correlation with logs from outside the OpenShift clusters (e.g., infrastructure logs). This forwarding can be configured using standard external output types (e.g., Splunk, Elasticsearch, Syslog) or by using the OpenTelemetry Protocol (OTLP) output (TP). If OTLP output is used, the ClusterLogForwarder CR must include the annotation `observability.openshift.io/tech-preview-otlp-output: "enabled"` (TP).
- **External Log Forwarding Disabled:** To minimize complexity and eliminate reliance on external logging infrastructure, suitable when short-term, on-cluster logs are sufficient.

**Implications**

- **External Log Forwarding Enabled:** Requires provisioning and configuring an external logging platform (e.g., Splunk, Elasticsearch, or cloud native services). Requires cluster resources for the forwarding components (e.g., Vector). If OTLP output is used, it is a (TP) feature that is not supported with Red Hat production SLAs, and requires the `observability.openshift.io/tech-preview-otlp-output: "enabled"` annotation on the ClusterLogForwarder CR.
- **External Log Forwarding Disabled:** Limits auditability and long-term troubleshooting capability. All log data relies entirely on the sizing and retention policy of the internal log store.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## LOG-03

**Title**
On-Cluster Log Storage Sizing (LokiStack)

**Architectural Question**
What will be the size of the on-cluster log store?

**Issue or Problem**
The LokiStack component, which provides the on-cluster log store, must be sized appropriately to handle the log volume and retention requirements without consuming excessive cluster resources.

**Assumption**
The OpenShift Logging Operator is deployed with the LokiStack storage solution.

**Alternatives**

- 1x.demo
- 1x.pico
- 1x.extra-small
- 1x.small
- 1x.medium

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **1x.demo:** For demo use only, with no CPU/memory requests specified, offering no replication factor, and supporting 0 GB/day data transfer.
- **1x.pico:** For minimal resource consumption, suitable for development clusters or environments with very low log volume (50GB/day data transfer). This configuration offers HA support for all components and a replication factor of 2.
- **1x.extra-small:** For minimal resource consumption, suitable for development clusters or environments with very low log volume (100GB/day data transfer).
- **1x.small:** To provide a balanced, default starting size for most production or pre-production clusters with moderate log volume (500GB/day data transfer).
- **1x.medium:** For clusters with high log volume or longer on-cluster retention requirements (2TB/day data transfer).

**Implications**

- **1x.demo:** Lowest resource footprint, lowest capacity, suitable only for demonstration environments.
- **1x.pico:** Has the lowest resource footprint among HA supported sizes but also limited capacity for ingestion, storage, and querying, designed for 50GB/day.
- **1x.extra-small:** Has the lowest resource footprint among production sizes but limited capacity for ingestion, storage, and querying (100GB/day).
- **1x.small:** Provides a good baseline for performance and capacity (500GB/day). The size can be scaled up in the future if requirements change.
- **1x.medium:** Consumes more significant CPU, memory, and storage resources (2TB/day). This size should be chosen based on a clear understanding of the expected log volume.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner

---

## LOG-04

**Title**
LokiStack Object Storage Backend Selection

**Architectural Question**
Which object storage solution will be used as the persistent backend for LokiStack?

**Issue or Problem**
LokiStack requires an object storage backend to persist log data. The choice of backend dictates infrastructure setup, authentication configuration (e.g., secrets, STS/Workload ID), and region compatibility.

**Assumption**
LokiStack solution is selected and requires persistent object storage for log data.

**Alternatives**

- AWS S3
- Azure
- Google Cloud Platform (GCP)
- Minio
- OpenShift Data Foundation (ODF)
- Swift

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **AWS S3:** To leverage a native, highly-scalable, and managed cloud object store, integrating with other AWS services.
- **Azure:** To leverage native Azure Blob Storage, integrating with the Azure cloud ecosystem.
- **Google Cloud Platform (GCP):** To leverage native GCS, integrating with the GCP cloud ecosystem.
- **Minio:** To provide a high-performance, S3-compatible object store _within_ the OpenShift cluster or on-premises.
- **OpenShift Data Foundation (ODF):** To utilize the cluster's native, integrated ODF storage (via NooBaa) for a fully internal solution.
- **Swift:** To integrate with existing on-premises OpenStack Swift storage infrastructure.

**Implications**

- **AWS S3:** Requires configuring IAM roles/secrets for the Loki Operator (e.g., `logging-loki-s3` secret). Costs are based on AWS pricing.
- **Azure:** Requires configuring Storage Account credentials in the required secret. Costs are based on Azure pricing.
- **Google Cloud Platform (GCP):** Requires configuring GCP service account credentials in the required secret. Costs are based on GCP pricing.
- **Minio:** Consumes on-premises storage and cluster resources. Requires separate management of the Minio instance and credentials secret.
- **OpenShift Data Foundation (ODF):** Tightly couples logging storage to the cluster's ODF. Log storage will consume ODF capacity.
- **Swift:** Requires credentials and network access to the on-premises Swift endpoint, configured in the required secret.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## LOG-05

**Title**
Log Collector Tuning for Delivery Mode

**Architectural Question**
What log delivery mode should be configured for the ClusterLogForwarder outputs to balance durability and throughput?

**Issue or Problem**
Log forwarding outputs support delivery modes that prioritize either avoiding log loss (AtLeastOnce) or maximizing performance/throughput (AtMostOnce). A production decision must be made regarding log fidelity requirements.

**Assumption**
The tuning specification is utilized, meaning the logging deployment uses the Vector collector.

**Alternatives**

- AtLeastOnce Delivery
- AtMostOnce Delivery

**Decision**
#TODO: Document the decision.#

**Justification**

- **AtLeastOnce Delivery:** To prioritize log durability and minimize data loss, which is essential for compliance and audit logs.
- **AtMostOnce Delivery:** To prioritize performance and high throughput, accepting the risk of log loss during a collector restart.

**Implications**

- **AtLeastOnce Delivery:** Logs that were read but not confirmed delivered before a crash might be resent, potentially causing some log duplication after a collector restart.
- **AtMostOnce Delivery:** Not suitable for audit or critical production logs, as data loss _will_ occur during restarts or crashes.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## LOG-06

**Title**
Enabling LokiStack-based Alerting and Recording Rules

**Architectural Question**
Should the LokiStack ruler component be enabled to support custom log-based alerts and recorded metrics?

**Issue or Problem**
Users require the ability to configure custom alerts (AlertingRule CRs) and record metrics (RecordingRule CRs) derived from log data using LogQL expressions, but this functionality is disabled by default.

**Assumption**
Customized log monitoring and alerting are necessary beyond the default platform alerts.

**Alternatives**

- Enable LokiStack Ruler (Custom Alerts/Metrics)
- Disable LokiStack Ruler (Rely on default alerts and external monitoring)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Enable LokiStack Ruler (Custom Alerts/Metrics):** To leverage Loki's native capabilities to define groups of LogQL expressions that trigger logging alerts and recorded metrics, providing granular, customized observability for application and infrastructure tenants.
- **Disable LokiStack Ruler (Rely on default alerts and external monitoring):** To minimize resource consumption on the cluster and rely solely on default platform alerts or external monitoring systems.

**Implications**

- **Enable LokiStack Ruler (Custom Alerts/Metrics):** Enabling the ruler requires additional CPU and memory resources for the LokiStack deployment. Administrators must configure necessary RBAC ClusterRoles/RoleBindings to grant users permissions to manage AlertingRule or RecordingRule resources.
- **Disable LokiStack Ruler (Rely on default alerts and external monitoring):** The inability to create custom, log-based alerts within the cluster. Troubleshooting must be done manually or via external tools.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## LOG-07

**Title**
Log Collector Resource Limits and Requests (Vector)

**Architectural Question**
What customized CPU and memory limits/requests should be set for the Vector log collector pods?

**Issue or Problem**
The resource allocation for the log collector DaemonSet needs careful tuning to ensure it can handle expected log volume without causing resource pressure on worker nodes, or running into performance issues.

**Assumption**
Cluster log volume is high enough to warrant customizing the default collector resource settings.

**Alternatives**

- Custom Collector Limits and Requests
- Default Collector Limits and Requests

**Decision**
#TODO: Document the decision.#

**Justification**

- **Custom Collector Limits and Requests:** To ensure stable log collection and forwarding across all nodes by setting CPU and memory limits (`spec.collector.resources`) appropriate for the expected log ingestion rate.
- **Default Collector Limits and Requests:** To simplify deployment and use the Red Hat-provided baseline, which is sufficient for most low-to-moderate log volume clusters.

**Implications**

- **Custom Collector Limits and Requests:** Requires continuous monitoring of the collector pods to confirm the defined limits are adequate under peak load, as insufficient limits can lead to pod eviction or missed logs.
- **Default Collector Limits and Requests:** May be insufficient for high-vector clusters, leading to collector performance issues or throttling.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: OCP Platform Owner
