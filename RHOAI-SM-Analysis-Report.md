# RHOAI-SM ADR Analysis Report - RHOAI 3.3

**Analysis Date:** 2026-03-09
**Source Documentation:** Red Hat OpenShift AI Self-Managed 3.3
**Target:** 53 existing RHOAI-SM ADRs
**Governance:** adr_governance_rules.md, adr_exclusions.md, adr_prefix_dictionary.md

---

## Executive Summary

**Total ADRs Reviewed:** 53
**Updates Required:** 2
**Removals Required:** 0
**New ADRs Needed:** 0

The RHOAI-SM ADR set is comprehensive and well-aligned with RHOAI 3.3 capabilities. Two ADRs require updates to address technical accuracy issues: one violates the versioning policy by referencing legacy architecture, and one has an incomplete component list missing new RHOAI 3.3 capabilities.

---

## RHOAI-SM-02

**Title:** Update Channel Strategy

**Status:** Updates required

**Rationale:** Violates the Versioning Policy (Section 5, adr_governance_rules.md). The ADR references legacy 2.x channels and describes historical architectural breaks. For RHOAI 3.3 deployments, only the current 3.x channel options are architecturally relevant. The "Stable-2.x Channel" alternative describes legacy behavior unsuitable for forward-looking architecture documentation.

**Updated Architectural Question:** Which update channel will be selected for the Red Hat OpenShift AI Operator?

**Updated Issue:** The operator update channel determines the feature set, stability level, and update cadence. Channel selection affects the availability of new capabilities, technology preview features, and the frequency of updates.

**Updated Assumption:** Fresh installation of RHOAI 3.x is being performed on a supported OpenShift Container Platform cluster.

**Updated Alternatives:**

- fast Channel
- stable Channel

**Updated Justification:**

- **fast Channel:** Provides access to the latest RHOAI features and capabilities, including technology preview features. Delivers updates more frequently. Suitable for development, testing, and organizations that prioritize early access to new functionality.
- **stable Channel:** Provides production-ready releases with a focus on stability. Updates are delivered after additional validation. Suitable for production environments prioritizing stability over immediate feature access.

**Updated Implications:**

- **fast Channel:** Enables access to technology preview features and the latest capabilities. May include features not yet recommended for production workloads. Requires more frequent update testing and validation cycles. Organizations must evaluate technology preview features against risk tolerance.
- **stable Channel:** Reduces exposure to early-stage features. Provides a more conservative update schedule. May delay access to new capabilities compared to fast channel. Recommended for production environments with strict change control requirements.

**Updated Parties:**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner

---

## RHOAI-SM-05

**Title:** Red Hat OpenShift AI Capabilities Enablement Strategy

**Status:** Updates required

**Rationale:** Incomplete component list. The ADR lists only four high-level components (Workbenches, Data Science Pipelines, Model Serving, Distributed Workloads) but RHOAI 3.3 includes additional major enableable components in the DataScienceCluster specification: Model Registry, TrustyAI, Training Operator (Training Hub), and Feature Store. The "Full MLOps Platform" alternative incorrectly implies these four components represent "All Capabilities" when additional components exist.

**Updated Architectural Question:** Which high-level functional components will be enabled within the DataScienceCluster to define the scope of the AI platform?

**Updated Issue:** OpenShift AI provides a modular suite of tools. Enabling all components increases the cluster resource footprint (CPU, Memory, CRDs) and operational surface area. A strategic decision is needed to define whether the platform acts as a full end-to-end MLOps suite or a specialized environment (e.g., Serving-only, Exploration-only, or MLOps Governance-focused).

**Updated Assumption:** Red Hat OpenShift AI instances have been defined.

**Updated Alternatives:**

- Full MLOps Platform (All Capabilities)
- Exploration & Training Only
- Production Serving Only
- MLOps Governance & Observability Focus
- Custom/Selective Enablement

**Updated Justification:**

- **Full MLOps Platform (All Capabilities):** Enable all major components including Workbenches, Data Science Pipelines, Model Serving (KServe), Distributed Workloads, Model Registry, TrustyAI, Training Hub, and Feature Store. Provides a complete end-to-end workflow from experimentation to production inference with full governance and observability. Standard configuration for general-purpose Data Science teams.
- **Exploration & Training Only:** Enable Workbenches, Distributed Workloads, and Training Hub; disable Model Serving. Optimizes the cluster for model development and heavy computation (Ray/CodeFlare). Suitable for development clusters where models are trained but not served for production traffic.
- **Production Serving Only:** Enable Model Serving (KServe), Model Registry, and TrustyAI; disable Workbenches, Pipelines, and Training Hub. Reduces attack surface and resource overhead by removing interactive components. Ideal for strictly controlled production inference clusters where artifacts are promoted via GitOps.
- **MLOps Governance & Observability Focus:** Enable Model Registry, TrustyAI, Model Serving, and Data Science Pipelines while potentially disabling resource-intensive training components. Optimizes for model lifecycle governance, compliance monitoring, and production observability use cases.
- **Custom/Selective Enablement:** Granular selection based on specific use case requirements. Allows precise resource optimization by enabling only necessary components.

**Updated Implications:**

- **Full MLOps Platform:** Requires significant cluster resources (CPU/Memory) to host control plane components for all services (Workbenches, KServe, KubeRay, Kueue, Model Registry DB, Pipelines DB, TrustyAI, Training Operator, Feature Store). Requires deciding configuration for dependent services like S3 Object Storage, databases (PostgreSQL for Model Registry, MariaDB/MySQL for Pipelines), and vector databases (if using Feature Store or RAG capabilities).
- **Exploration & Training Only:** Eliminates the overhead of Istio/Knative/KServe if inference is not required. Reduces dependencies on external S3 storage for model serving artifacts. Focuses resources on compute-intensive workloads (GPU, distributed training).
- **Production Serving Only:** Data Scientists cannot log in to write code. Requires a robust CI/CD pipeline to promote trained models into the serving environment. Eliminates training-related resource consumption and security exposure.
- **MLOps Governance & Observability Focus:** Balances governance requirements (Model Registry for lineage, TrustyAI for fairness/bias monitoring) with operational constraints. May require coordination with separate training environments.
- **Custom/Selective Enablement:** Requires managing the DataScienceCluster resource configuration carefully to ensure dependencies are correctly handled (e.g., Kueue for Distributed Workloads, S3 for Model Registry and KServe, databases for Model Registry and Pipelines).

**Updated Parties:**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Lead Data Scientist

---

## Analysis Notes

**Comprehensive Coverage Confirmed:**

All major RHOAI 3.3 capabilities are covered by existing ADRs:
- Guardrails: RHOAI-SM-49
- Model Registries: RHOAI-SM-08, RHOAI-SM-47
- Accelerators (NVIDIA/Intel/AMD): RHOAI-SM-26, RHOAI-SM-27, RHOAI-SM-28, RHOAI-SM-29
- Llama Stack: RHOAI-SM-44, RHOAI-SM-48
- Monitoring (Distributed Workloads, KServe, TrustyAI): RHOAI-SM-35, RHOAI-SM-40, RHOAI-SM-41, RHOAI-SM-42
- Training Hub: RHOAI-SM-53
- Feature Store: RHOAI-SM-51, RHOAI-SM-52
- Distributed Workloads (Ray/Kueue): RHOAI-SM-32, RHOAI-SM-33, RHOAI-SM-34, RHOAI-SM-35

**No Removals Required:**

All 53 ADRs represent valid architectural choices per the Quality and Validity Rules (Section 2, adr_governance_rules.md). No ADRs describe misconfigurations, deprecated features, or non-decisions. No matches found in adr_exclusions.md Section 1 (Forbidden Topics).

**No New ADRs Required:**

The existing ADR set comprehensively covers all architectural decision points in RHOAI 3.3. Individual component enablement decisions (Model Registry, TrustyAI, Training Hub, Feature Store, Llama Stack, Guardrails) are already documented in dedicated ADRs (RHOAI-SM-08, 42, 44, 49, 51, 53).

---

**Report Complete**
