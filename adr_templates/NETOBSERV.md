# ARCHITECTURE DECISION RECORDS FOR: Network Observability

## NETOBSERV-01

**Title**
Network Observability

**Architectural Question**
Will network flow data be collected for visibility and troubleshooting?

**Issue or Problem**
To understand and troubleshoot complex network interactions between services within the cluster, a tool is needed to capture and visualize network flow data.

**Assumption**
Deep visibility into pod-to-pod network traffic is required for troubleshooting.

**Alternatives**

- Network Observability Disabled
- Network Observability Enabled

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Network Observability Disabled:** To conserve resources if detailed network flow analysis is not a requirement.
- **Network Observability Enabled:** To provide deep visibility into network traffic, allowing operators to analyze flows, identify bottlenecks, and troubleshoot connectivity issues between pods and services.

**Implications**

- **Network Observability Disabled:** Troubleshooting network issues will rely on traditional tools like `ping`, `traceroute`, and manual log inspection.
- **Network Observability Enabled:** Requires the installation of the Network Observability Operator. The operator collects network flow data using eBPF and provides a topology view and filtering capabilities. This consumes additional CPU, memory, and storage resources.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## NETOBSERV-02

**Title**
Storage Architecture (Loki vs. Prometheus-Only)

**Architectural Question**
Will Network Observability store full flow logs in Loki or rely solely on Prometheus metrics?

**Issue or Problem**
Storing every network flow log (metadata) requires significant storage (Loki). Prometheus can store aggregated metrics (e.g., "bytes per namespace") cheaply but loses granular details.

**Assumption**
Network Observability is enabled.

**Alternatives**

- **Loki Stack Integration (Recommended):** Stores full flow logs. Enables "drill-down" troubleshooting, topology views, and conversation tracking.
- **Prometheus-Only Mode:** Disables Loki storage. Generates metrics from flows in-memory. Lowest resource footprint.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Loki Stack:** Essential for forensic analysis and deep debugging. Allows querying past flows.
- **Prometheus-Only:** Sufficient for high-level dashboards ("Which namespace uses the most bandwidth?") but useless for investigating specific connection errors.

**Implications**

- **Loki Stack:** Requires deploying LokiStack. Increases storage cost.
- **Prometheus-Only:** Topology view is limited. No historical flow log search.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## NETOBSERV-03

**Title**
Ingestion Architecture (Direct vs. Kafka)

**Architectural Question**
Will flow logs be sent directly to the collector or buffered via Kafka?

**Issue or Problem**
In high-traffic clusters, the volume of flow logs can overwhelm the collector or Loki, causing data loss. Kafka provides a buffer.

**Assumption**
Network Observability is enabled.

**Alternatives**

- **Direct Mode (Default):** Agents send flows directly to `flowlogs-pipeline`.
- **Kafka Mode:** Agents send flows to a Kafka topic; pipeline consumes from Kafka.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Direct Mode:** Simple. No extra infrastructure. Suitable for most standard clusters.
- **Kafka Mode:** Mandatory for hyperscale clusters or when flow rates exceed collector capacity. Decouples ingestion from processing.

**Implications**

- **Direct Mode:** Risk of dropped flows during traffic spikes.
- **Kafka Mode:** Requires Red Hat AMQ Streams (Kafka) operator. Significantly increases complexity and resource footprint.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## NETOBSERV-04

**Title**
eBPF Agent Privilege Strategy

**Architectural Question**
Will the eBPF agent run in privileged mode to enable advanced features, or unprivileged mode for security?

**Issue or Problem**
Certain eBPF hooks (Packet Drop tracking, SR-IOV monitoring) require `privileged: true` security context. Standard flow monitoring does not.

**Assumption**
Network Observability is enabled.

**Alternatives**

- **Unprivileged Mode (Default):** Safer. Standard flow tracking.
- **Privileged Mode:** Required for Packet Drop tracking and RTT measurements on some kernels.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Unprivileged:** Adheres to "Least Privilege". Sufficient for basic traffic visibility.
- **Privileged:** Unlocks "Packet Drop" feature (seeing _why_ packets were dropped by the kernel/OVS). Critical for debugging firewall/network policy issues.

**Implications**

- **Privileged:** Pods run as root with extensive capabilities. Security risk if compromised. Requires SCC adjustment.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

---

## NETOBSERV-05

**Title**
Advanced Feature Enablement (RTT/DNS/Drops)

**Architectural Question**
Which advanced eBPF tracking features (TCP Round-Trip Time, DNS Latency, Packet Drops) will be enabled?

**Issue or Problem**
Enabling these features increases the CPU overhead of the eBPF agent on every node.

**Assumption**
eBPF Agent is configured.

**Alternatives**

- **Basic Flow Tracking Only:** Source/Dest IPs, Ports, Bytes.
- **Extended Tracking:** Enable RTT, DNS, and/or Packet Drop tracking.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Basic:** Low overhead. Good for capacity planning.
- **Extended:** Provides APM-like metrics (Network Latency, DNS response times). Essential for distinguishing "Network Slow" vs "App Slow".

**Implications**

- **Extended:** Higher CPU usage on worker nodes. May require Privileged Mode (NETOBSERV-04).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## NETOBSERV-06

**Title**
Data Export Strategy

**Architectural Question**
Will network flow data be exported to external systems (e.g., Splunk, IPFIX collector)?

**Issue or Problem**
Internal storage (Loki) has retention limits. Security teams often require long-term retention of flow logs in a central SIEM.

**Assumption**
Network Observability is enabled.

**Alternatives**

- **Internal Only:** Data stays in Cluster Loki/Prometheus.
- **External Export:** Flows are forwarded to external collectors (Kafka, IPFIX, OTLP).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Internal Only:** Simple. Data sovereignty within the cluster.
- **External Export:** Integrates with enterprise security tools. Enables correlation with physical network logs.

**Implications**

- **External Export:** Increases egress bandwidth usage. Requires configuring `FlowCollector` exporters.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

---
