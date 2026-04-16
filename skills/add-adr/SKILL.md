---
name: Add ADR Template
description: This skill should be used when adding a new ADR template to the openshift-adr library. It applies when the user says "add a new ADR about X", "create an ADR for X", "we need a new ADR for X", or describes a new architectural decision that should be captured as a reusable template. It handles the full workflow: governance validation, content generation, file append, and renumbering. It should be preferred over manually editing adr_templates/ files directly.
---

## Repository context

- ADR template library: `~/wrk/rh/openshift-adr/`
- Template files: `adr_templates/<PREFIX>.md`
- Governance rules: `dictionaries/adr_governance_rules.md`
- Exclusions: `dictionaries/adr_exclusions.md`
- Prefix dictionary: `dictionaries/adr_prefix_dictionary.md`
- Roles dictionary: `dictionaries/adr_parties_role_dictionnary.md`

All file reads and writes happen inside `~/wrk/rh/openshift-adr/`.

---

## Step 1 — Parse intent

Extract from the user's message:
- **Topic**: what the ADR is about
- **Prefix**: the product/domain prefix (e.g. `OCP-NET`, `RHOAI-SM`). If not stated, infer it in Step 2.

If the topic is unclear, ask one focused question before continuing.

---

## Step 2 — Determine prefix

Read `dictionaries/adr_prefix_dictionary.md`.

Map the topic to the most specific matching prefix. When multiple prefixes could apply, prefer the domain-specific one over `OCP-BASE` — `OCP-BASE` is only for cross-cutting platform strategy (topology, sizing, multi-site, compliance standards). Use the scope hierarchy:

- Physical hardware / BIOS / OS installation → `OCP-BM`
- Platform-specific (AWS, vSphere, bare metal install) → `OCP-<PLATFORM>`
- Day 2 networking, CNI, ingress, DNS → `OCP-NET`
- Security, RBAC, compliance → `OCP-SEC`
- Storage CSI, StorageClass → `OCP-STOR`
- Upgrades, Machine Config, day 2 ops → `OCP-MGT`
- Cross-cutting strategy only → `OCP-BASE`

**Note:** Some OpenShift-related domains use their own top-level prefix rather than the `OCP-*` namespace. `GITOPS`, `VIRT`, `ODF`, `PIPELINES`, `OSSM`, and others are standalone prefixes — not sub-domains of `OCP`. Do not force these topics into an `OCP-*` prefix. The prefix dictionary is the authoritative source for all such products.

Tell the user the prefix you selected and why before proceeding.

---

## Step 3 — Governance validation

Read `dictionaries/adr_governance_rules.md` and `dictionaries/adr_exclusions.md`.

**Check 1 — Exclusion list (hard block):**
If the topic matches any entry in Section 1 (Forbidden Topics), stop immediately and explain why the topic is excluded. Do not proceed.

**Check 2 — Quality rules:**
Ask yourself: is this a choice between two or more supported, viable architectural strategies? If the "alternatives" would be "correct configuration vs. misconfiguration", this is invalid — unless it qualifies under one of the six Allowed Exceptions (Deployment Guardrail, Security Policy, Risk Acceptance, Simplicity vs. Capability, Platform-Specific Gaps, Backing Service Selection).

If invalid and no exception applies: stop and explain the governance issue clearly. Suggest how the user might reframe the topic as a valid ADR if possible.

If it qualifies under an Allowed Exception: proceed, but note the exception type in your output.

**Check 3 — Duplicate scan:**
Read the existing `adr_templates/<PREFIX>.md`. If an ADR with the same or very similar question already exists, tell the user which one (by ID and title) and ask whether they want to update the existing ADR instead, or confirm that the new one covers meaningfully distinct ground.

If the topic is cross-cutting or could plausibly belong to `OCP-BASE`, also read `adr_templates/OCP-BASE.md` and check for overlapping questions there.

---

## Step 4 — Generate ADR content

Generate a fully-fleshed ADR using the structure below. The number is a placeholder (`NN`) — renumbering in Step 6 will assign the real number.

Use the existing ADRs in `adr_templates/<PREFIX>.md` as style reference: match their depth of analysis, tone, and specificity of consequences. Aim for 2–3 alternatives. Never mention specific OCP version numbers.

```
## <PREFIX>-NN

**Title**
<Concise, specific title — e.g. "DNS Resolver Selection" not "DNS">

**Architectural Question**
<The specific strategic question being answered, as a single sentence>

**Issue or Problem**
<Why this decision is needed — the architectural tension or operational constraint that makes this a real choice>

**Assumption**
<Stated dependency or constraint, or "N/A">

**Alternatives**

- **<Option A>:** <One-sentence description of the option>
- **<Option B>:** <One-sentence description of the option>
[- **<Option C>:** <Only if genuinely distinct and viable>]

**Decision**
#TODO: Document the decision.#

**Justification**

- **<Option A>:** <Why an architect would choose this — its strengths in context>
- **<Option B>:** <Why an architect would choose this — its strengths in context>

**Implications**

- **<Option A>:** <Concrete consequences, risks, or follow-on requirements>
- **<Option B>:** <Concrete consequences, risks, or follow-on requirements>

**Agreeing Parties**

- Person: #TODO#, Role: <Role>
- Person: #TODO#, Role: <Role>
- Person: #TODO#, Role: <Role>
```

**Selecting Agreeing Parties roles** — use only roles from `dictionaries/adr_parties_role_dictionnary.md`. Choose 2–3 roles that reflect who genuinely owns the decision:

| Prefix group | Typical roles |
|---|---|
| OCP-NET | Enterprise Architect, Network Expert, OCP Platform Owner |
| OCP-SEC | Enterprise Architect, Security Expert, OCP Platform Owner |
| OCP-STOR / ODF | Enterprise Architect, Storage Expert, OCP Platform Owner |
| OCP-MGT | Enterprise Architect, Operations Expert, OCP Platform Owner |
| OCP-BASE | Enterprise Architect, Infra Leader, OCP Platform Owner |
| OCP-BM | Enterprise Architect, Infra Leader, OCP Platform Owner |
| RHOAI-SM | Enterprise Architect, AI/ML Platform Owner, Lead Data Scientist |
| GITOPS / PIPELINES | Enterprise Architect, DevOps Engineer, OCP Platform Owner |
| VIRT | Enterprise Architect, Infra Leader, OCP Platform Owner |

Show the user the generated ADR and ask for confirmation before writing to disk.

---

## Step 5 — Append and renumber

**Append** the new ADR to the end of `adr_templates/<PREFIX>.md`.

Add a blank line before the new `## <PREFIX>-NN` header to separate it cleanly from the previous ADR.

**Renumber** to assign the correct sequential ID:

```bash
python scripts/renumber_adrs.py <PREFIX>
```

---

## Step 6 — Confirm and summarise

After renumbering completes, read `adr_templates/<PREFIX>.md` and identify the last `## <PREFIX>-\d+` header — that is the confirmed assigned ID.

Tell the user:
- The assigned ADR ID (e.g. `OCP-NET-17`), confirmed from the file
- The file it was written to
- Suggested next steps: review the content, commit the change, and open a PR when satisfied.
