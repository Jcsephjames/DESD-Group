# Stakeholder and Business Process Analysis

## Purpose and scope

The Bristol Regional Food Network connects local food producers with customers within 20 miles of Bristol. This analysis focuses on the two selected functionalities: **Use Case 1, Producer Product Listing and Inventory Management**, and **Use Case 2, Customer Multi-Vendor Order, Checkout and Payment**.

The strategic BPMN should show how these functions support the wider marketplace. The operational BPMN models can later show their detailed steps, decisions and exception paths.

## Stakeholders

| Stakeholder | Needs and interests | Role in Use Cases 1 and 2 |
|---|---|---|
| **Local producers** | Simple product listing and seasonal stock updates; clear visibility of orders; at least 48 hours to prepare products. | Submit and maintain product details and stock, receive producer-specific order information, prepare orders and receive payment. |
| **Young professionals and families** | Convenient access to local produce without visiting several shops during restricted opening hours; useful search and browsing; clear product origin and harvest details. | Browse products, add items to a basket and place single- or multi-producer orders. |
| **Community groups** | Reliable local suppliers for catering, including educational institutions, care facilities and voluntary organisations. | Find producers and place orders through the marketplace. |
| **Independent restaurants and cafés** | Local ingredients with less administrative effort managing relationships with multiple small suppliers. | Discover products and order from one or more producers through a shared marketplace. |
| **Marketplace operator** | Coordinate the marketplace, support customers and producers, calculate the 5% commission, distribute payments and maintain clear transaction records. | Operate the platform and coordinate listings, orders and payments. |
| **Payment service** | Process payment requests securely and return success, decline or temporary-unavailability results. | Support checkout. Development and testing must use a simulated service, never live payments.|

## Main business processes

| Process | Main activities | Main participants |
|---|---|---|
| **Manage product listings and inventory** | Producer submits product name, description, category, price, quantity, availability period and farm origin. The marketplace validates the information, checks organic certification, publishes valid listings and supports later stock. Products with zero stock become unavailable. | Producer, marketplace|
| **Browse and select products** | Customer browses categories or searches for items and adds products from one or more producers to a basket. Product information should include relevant origin, harvest and best-before details. | Customer, marketplace, producers |
| **Validate basket and confirm checkout** | At checkout, the marketplace checks current availability and requested quantities. If stock is insufficient, the customer is asked to amend the basket. Otherwise, the customer reviews supplier responsibilities and delivery or collection arrangements before confirming. | Customer, marketplace, producers |
| **Create and distribute orders** | The marketplace creates an overall order and separates it into producer-specific order elements, retaining clear responsibilities and delivery or collection information. | Marketplace, customer, producers |
| **Process payment and commission** | The marketplace submits payment to the simulated payment service. On success, it confirms the order, updates inventory and notifies the relevant producers. It calculates the producer amounts and the network's 5% commission. Declines allow a retry; temporary service failure follows a suitable retry or exception path. | Customer, marketplace, payment service, producers |
| **Settle producer payments and retain records** | The marketplace distributes producer payments and maintains records for accounting and tax reporting. | Marketplace, producers |













































# Business and Stakeholder Analysis
**UFCFTR-30-3 Task 1 – Local Food Multi-Vendor Marketplace**  
**Sprint 1**

## 1. Enterprise Context
The enterprise is a multi-vendor online marketplace that enables local food producers to list and sell products directly to customers. Core value streams include product listing and inventory management, multi-vendor ordering and payment (with a 5% marketplace commission), and quality/incident handling. The system must support seasonal availability, organic certification verification, stock integrity, and rapid traceability.

## 2. Key Stakeholders / Actors
| Actor | Type | Primary Goals | Softgoals / Expectations | Key Dependencies |
|-------|------|---------------|--------------------------|------------------|
| **Producer** | Primary user | List products quickly, maintain accurate inventory and seasonal availability, receive orders and payments | Trust in fair commission, simple tools, protection of brand/quality reputation | Marketplace platform, Certification service (if organic) |
| **Customer** | Primary user | Discover local products, place multi-producer orders reliably, receive safe food | Accurate stock, clear allergen/origin info, timely notifications, fair pricing | Marketplace, Payment service, Producers |
| **Marketplace Platform / Admin** | System & organisational | Attract producers and customers, enforce rules, calculate commission, ensure food-safety readiness | Scalability, auditability, regulatory compliance, positive reputation | Producers, Customers, External services |
| **External Organic Certification Service** | External system | Provide reliable verification of organic claims | Availability, accuracy, security of data exchange | Marketplace (on organic claim) |
| **External Payment Service** | External system | Process payments securely | Reliability, clear success/decline responses | Marketplace, Customer |
| **Marketplace Operations / Quality Lead** | Internal role | Handle incidents, maintain trust | Rapid response capability, complete traceability records | All other actors |

## 3. Socio-Technical Relationships and Organisational Responsibilities
- Producers own product data and inventory accuracy; the marketplace owns publication rules, commission calculation, and platform integrity.
- Customers depend on the marketplace for stock truthfulness and on producers for product quality.
- External services are treated as potentially unreliable; the system must handle unavailability without losing data or user progress.
- Softgoals such as “trust”, “transparency of origin/allergens”, and “fairness of commission” influence design decisions (e.g., clear certification status, auditable commission breakdown).

## 4. Major Business Processes (strategic view)
1. Producer product listing and inventory lifecycle  
2. Customer multi-vendor order, checkout, payment and fulfilment notification  
3. Quality incident reporting and customer traceability (supporting process)  
4. Settlement / commission accounting (supporting)

These processes directly inform the strategic BPMN (high-level pools and message flows) and justify the selection of the two major functionalities for detailed development.

## 5. Legal, Ethical, Social and Professional (LESP) Considerations (high-level)
- **Legal/Regulatory:** Food labelling (allergens, best-before, origin), data protection (customer and producer data), consumer rights on payment and returns.
- **Ethical:** Accurate organic claims, transparent commission, fair treatment of small producers.
- **Social:** Support for local food systems, accessibility of product information.
- **Professional:** Clear audit trails, responsible handling of quality incidents, honest representation of capabilities in the system.

These considerations will be linked more tightly to specific design decisions in later sprints and the final demonstration.

## 6. Implications for Modelling and Development
The analysis provides the actor and goal foundation for the forthcoming i* SD and SR models and ensures the strategic BPMN reflects real organisational responsibilities and external dependencies. It also confirms that the two chosen functionalities address the highest-value stakeholder goals while remaining substantial enough for end-to-end Camunda automation.

