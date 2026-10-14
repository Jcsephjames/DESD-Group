# Product Backlog and Sprint Plan – UFCFTR-30-3 Task 1
**Group Project: Local Food Multi-Vendor Marketplace**  
**Focus:** Producer Product Listing & Inventory Management + Customer Multi-Vendor Order, Checkout & Payment  
**Sprint 1 Review Date:** [Insert date]  
**Members (placeholders – replace with real names):** Member-1, Member-2, Member-3, Member-4

## 1. Roles and Responsibilities
- **Joseph** – Strategic modelling lead (BPMN ownership, traceability)
- **Billy & Faris** – Business analysis & stakeholder lead (analysis documents, LESP notes)
- **Leyla** – Planning & backlog  (this document, GitHub Projects/Issues, sprint tracking)
- **All** – Repository & process evidence lead (structure, README, contribution records, initial Camunda skeleton)


## 3. Prioritised Product Backlog
Items are prioritised by dependency order. Estimates are in story points (1 = small, 5 = large).

| ID | Item | Priority | Estimate | Assigned | Acceptance Criteria | Sprint |
|----|------|----------|----------|----------|---------------------|--------|
| B1 | Strategic BPMN model of the enterprise | Must | 5 | Joseph | High-level pools (Marketplace, Producer, Customer, External Certification, External Payment), major processes, message flows, appropriate abstraction, exported .bpmn + PNG, clear justification in README | 1 |
| B2 | Business & Stakeholder Analysis document | Must | 3 | Billy | Key actors, goals/softgoals, dependencies, organisational responsibilities, LESP notes, links to strategic processes | 1 |
| B3 | Functional Scope document (two chosen + alternatives) | Must | 2 | Faris | Clear description of both functionalities, justification against assessment criteria, brief alternatives | 1 |
| B4 | Initial product backlog & sprint plan | Must | 2 | Faris | Prioritised items, assignments | 1 |
| B5 | GitHub repository structure, README, and initial commits | Must | 2 | Leyla | Clear folder structure (models/, docs/, processes/), professional README, evidence of group activity | 1 |
| B6 | i* Strategic Dependency (SD) model | Should | 5 | Not Decided | Actors, goals, softgoals, dependencies, resources; started in Sprint 1, completed for Sprint 2 | 1–2 |
| B7 | i* Strategic Rationale (SR) model | Should | 5 | Not Decided | Actor rationale, tasks, softgoals, tensions; traceable to SD and BPMN | 2 |
| B8 | Operational BPMN – Product Listing & Inventory | Must | 8 | not Decided | Pools/lanes, user/service tasks, gateways, events, exceptions (validation fail, verification unavailable), stock rules | 2 |
| B9 | Operational BPMN – Multi-Vendor Order & Payment | Must | 8 | not Decided | Stock checks, producer-specific orders, 5% commission, payment paths (success/decline/retry/unavailable), notifications | 2 |
| B10 | Camunda project setup + executable process skeletons | Must | 5 | not Decided | Processes deployable, basic user tasks and forms started | 2 |
| B11 | Simulated organic verification service | Should | 3 | not Decided | Returns success/fail/unavailable; integrated via service task | 2–3 |
| B12 | Simulated payment service + commission logic | Should | 3 | not Decided | Success/decline/unavailable; calculates producer amounts + 5% commission | 2–3 |
| B13 | Inventory availability rules (zero stock, seasonal) | Must | 3 | not Decided | Automated unavailability and re-availability implemented | 3 |
| B14 | End-to-end demonstration readiness + LESP evaluation | Must | 5 | All | Full flows executable, exceptions handled, LESP linked to design decisions | 3 |
| B15 | Contribution Matrix & final repository tidy | Must | 1 | not Decided | Signed matrix, clean history, setup instructions | 3 |


## 4. Outline for Later Sprints
- **Sprint 2:** Complete i* SD/SR, detailed operational BPMNs for both functionalities, initial executable Camunda processes with forms and service tasks, continued repository evidence.
- **Sprint 3:** Full end-to-end automation, exception handling, service integration, LESP evaluation, demonstration readiness, and preparation for Task 2 integration.
