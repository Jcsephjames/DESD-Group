# Functional Scope – Chosen Major Functionalities

Both chosen functionalities are drawn from **Use Case 1: Producer Product Listing and Inventory Management**. They divide the use case into two distinct processes: publishing a new product and managing an existing product’s inventory and seasonal availability.

## 1. Chosen Functionality 1: Product Submission, Validation and Publication
**Scope:** End-to-end process from submission of a new product by a registered producer through validation, verification of any claimed organic certification, and publication to customers.

**Key elements:**
- Capture of mandatory product information: product name, description, category, price, available quantity, availability period and farm origin.
- Capture of relevant additional information, such as harvest date, allergen details, organic certification and best-before date.
- Validation of mandatory information; request corrections from the producer if information is missing or invalid.
- Verification of any claimed organic certification using an external or simulated verification service.
- Exception paths for failed verification and verification service unavailability.
- Publication and customer visibility once all required information has been successfully validated.

**Why chosen:**
This functionality combines producer interaction through forms, automated validation, external service integration and alternative paths. It maps directly to the new-product listing portion of Use Case 1 and provides a distinct operational BPMN process suitable for Camunda user tasks, service tasks, gateways and error handling.

## 2. Chosen Functionality 2: Inventory and Seasonal Availability Management
**Scope:** Management of an existing product’s quantity and seasonal availability, including automatic changes to whether the product is available for new orders.

**Key elements:**
- Allow the producer to update an existing product’s available quantity.
- Allow the producer to update the product’s seasonal availability period.
- Automatically make the product unavailable for new orders when stock reaches zero.
- Allow the product to become available again when stock is replenished and it remains within its seasonal availability period.
- Keep the product unavailable if stock is replenished but it is outside its seasonal availability period.

**Why chosen:**
This functionality combines producer updates with automated stock and seasonal availability rules. It maps directly to the ongoing inventory management portion of Use Case 1 and provides a separate operational BPMN process with user tasks, automated decisions and alternative paths. It demonstrates how the marketplace maintains accurate product availability after publication.

Together, these functionalities cover Use Case 1 with clear boundaries. Functionality 1 ends when a validated product is published; Functionality 2 handles subsequent inventory and seasonal availability management. Initial quantity and availability information is captured during submission, while later updates and availability decisions belong to Functionality 2.

## 3. Scope Exclusions
**Customer Multi-Vendor Order, Checkout and Payment (Use Case 2)**
This is outside the chosen use case and is therefore excluded from the two selected functionalities. Checkout, order decomposition, payment processing and commission calculation are not part of the selected functional scope.

**Food Quality Incident and Customer Traceability (Use Case 3)**
This is also outside the chosen use case and is excluded from the two selected functionalities.

**Standalone Producer Onboarding / Registration**
Use Case 1 starts with a registered producer. Producer registration is therefore treated as a precondition rather than a selected functionality.
