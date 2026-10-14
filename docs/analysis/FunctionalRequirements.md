# Functional Scope – Chosen Major Functionalities

## 1. Chosen Functionality 1: Producer Product Listing and Inventory Management
**Scope:** End-to-end process from product submission by a registered producer through validation, optional organic certification check, publication, and ongoing inventory/seasonal management.

**Key elements:**
- Capture of mandatory and optional product data (name, description, category, price, quantity, availability period, farm origin, harvest date, allergens, organic certification, best-before).
- Validation of mandatory fields; return to producer for correction if invalid.
- External (or simulated) organic verification service call when claimed; handling of success, failure, and service unavailability.
- Publication and customer visibility once validated.
- Subsequent updates to quantity and seasonal availability.
- Automatic transition to unavailable when stock reaches zero; re-availability when stock is replenished and the product remains within its seasonal window.
- Clear exception paths.

**Why chosen:**  
This functionality is substantial, contains rich user interaction (forms), automated business rules (stock and seasonality), external service interaction, and multiple exception paths. It maps directly to Use Case 1, provides excellent material for operational BPMN and Camunda user tasks/forms/service tasks, and demonstrates inventory integrity—core to marketplace trust. It offers strong opportunities to show process variables, gateways, and error handling, supporting high marks in later sprints.

## 2. Chosen Functionality 2: Customer Multi-Vendor Order, Checkout and Payment
**Scope:** End-to-end process from a customer basket containing products from one or more producers through stock validation, order decomposition, commission calculation, payment, inventory update, and producer notification.

**Key elements:**
- Stock and availability check at checkout; amendment path if insufficient.
- Identification of involved producers and delivery/collection arrangements.
- Creation of marketplace order and producer-specific order elements.
- Calculation of amount due to each producer and the marketplace’s 5% commission.
- Submission to simulated payment service; success path (confirm, update inventory, notify producers), decline path (inform customer, allow retry), and temporary unavailability path (appropriate retry/exception rather than abrupt termination).

**Why chosen:**  
This functionality demonstrates multi-party coordination, business calculations, external service integration, and alternative/exception flows. Combined with Functionality 1 it covers the core commercial loop of the marketplace. It is highly suitable for Camunda (user tasks for review/confirmation, service tasks for payment and inventory, gateways for outcomes) and shows clear traceability from strategic processes to executable automation.

Together the two functionalities provide complementary end-to-end processes that are sufficiently complex for a first-class demonstration while remaining achievable within the sprint structure. They were discussed and agreed as the focus for detailed development.

## 3. Alternatives Functionalties
**Food Quality Incident and Customer Traceability (Use Case 3)**  
Strong for demonstrating traceability, notifications, and escalation. However, it is more reactive and incident-driven. It offers fewer opportunities for routine user-driven forms and commercial business rules compared with the listing and order processes. It remains a valuable supporting process that can be referenced in the strategic model and potentially extended in Task 2.

**Standalone Producer Onboarding / Registration**  
Useful but relatively linear and less rich in business decisions, external service interaction, and exception complexity than the two chosen functionalities. Onboarding can be assumed or lightly modelled at strategic level.


