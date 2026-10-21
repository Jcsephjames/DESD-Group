# Functional Scope – Chosen Major Functionalities

Both chosen functionalities are drawn from **Use Case 1: Producer Product Listing and Inventory Management**. They divide the use case into two distinct processes: publishing a new product and managing an existing product’s inventory and seasonal availability.

## 1. Chosen Functionality 1: Product Submission, Validation and Publication

**Scope:** End-to-end process from submission of a new product by a registered producer through validation, verification of any claimed organic certification, and publication to customers.

**Product Backlog**

1. **Create a product form**
   - **Priority:** Must have
   - **Acceptance criteria:** A registered producer can enter product name, description, category, price, available quantity, availability period and farm origin, together with relevant optional harvest date, allergen, organic certification and best-before information.
2. **Validate and standardise product details**
   - **Priority:** Must have
   - **Acceptance criteria:** The system checks mandatory fields and expected data formats, including valid prices, non-negative quantities and an availability end date that does not precede its start date. Invalid submissions cannot progress, and accepted dates and numeric values are stored in consistent formats.
3. **Allow producers to correct missing or invalid product details and resubmit**
   - **Priority:** Must have
   - **Acceptance criteria:** The producer is shown which fields need correction, can amend the submission without re-entering valid details, and can resubmit it for validation.
4. **Verify claimed certificates**
   - **Priority:** Must have
   - **Acceptance criteria:** When organic certification is claimed, the system submits the certification details to an external or simulated verification service and records the outcome. Products without an organic claim skip this check.
5. **Handle certification verification service unavailability**
   - **Priority:** Must have
   - **Acceptance criteria:** If the verification service is unavailable, the submission remains unpublished and pending verification, the producer is informed, and verification can be retried without creating a duplicate listing.
6. **Handle failed certificates**
   - **Priority:** Must have
   - **Acceptance criteria:** If certification verification fails, the product remains unpublished and the producer is informed. The producer can correct the certification details or remove the organic claim and resubmit for the applicable validation checks.
7. **Publish to marketplace**
   - **Priority:** Must have
   - **Acceptance criteria:** A product becomes visible to customers only after mandatory information and any claimed organic certification pass validation. Its availability for new orders follows the stock and seasonal availability rules in Functionality 2.
8. **Marketplace product database** 
    - **Priority:** Must have
    - **Acceptance criteria:** An SQL database owned by the marketplace allows producers to add to it  

**Key elements:**

- Capture of mandatory product information: product name, description, category, price, available quantity, availability period and farm origin.
- Capture of relevant additional information, such as harvest date, allergen details, organic certification and best-before date.
- Validation of mandatory information; request corrections from the producer if information is missing or invalid.
- Verification of any claimed organic certification using an external or simulated verification service.
- Exception paths for failed verification and verification service unavailability.
- Publication and customer visibility once all required information has been successfully validated.

**Why chosen:**
This functionality combines producer interaction through forms, automated validation, external service integration and alternative paths. It maps directly to the new-product listing portion of Use Case 1 and provides a distinct operational BPMN process suitable for Camunda user tasks, service tasks, gateways and error handling.

## 2. Chosen Functionality 2: Product and Seasonal Availability Management

**Scope:** Management of an existing product’s quantity and seasonal availability, including automatic changes to whether the product is available for new orders.

**Product Backlog**

1. **Allow producers to update stock quantities**
   - **Priority:** Must have
   - **Acceptance criteria:** A producer can update the quantity of their own existing product to a non-negative value. The saved quantity triggers a reassessment of the product’s availability; invalid values are rejected with an explanation.
2. **Allow producers to create an ASAN (advanced shipping notice)**
   - **Priority:** Could have — proposed extension beyond the explicit requirements of Use Case 1
   - **Acceptance criteria:** A producer can record a notice against their own product with an expected replenishment quantity and arrival date. Creating the notice does not increase available stock or make the product available before the stock quantity is actually updated.
3. **Allow producers to update product information and seasonal availability**
   - **Priority:** Must have for seasonal availability updates; Could have for broader product information edits
   - **Acceptance criteria:** A producer can update their own product’s availability dates, with invalid date ranges rejected and availability reassessed after saving. If broader information edits are implemented, changed details undergo the applicable validation and certification checks before appearing on the marketplace.
4. **Allow the marketplace to automatically update the available season**
   - **Priority:** Must have
   - **Acceptance criteria:** The system automatically reassesses whether a product is within the producer’s recorded availability period when that period starts or ends, without requiring the producer to manually change its availability status.
5. **Automatically make the product unavailable for out-of-date stock, zero-quantity stock and out-of-season stock**
   - **Priority:** Must have for zero-stock and seasonal rules; Could have for expiry-based withdrawal
   - **Acceptance criteria:** A product cannot be ordered when its quantity is zero or the current date is outside its availability period. If expiry-based withdrawal is implemented, stock past its recorded best-before date is also made unavailable under the agreed project rule.
6. **Allow products that are in season and in stock to become automatically available to the marketplace**
   - **Priority:** Must have
   - **Acceptance criteria:** An already validated and published product automatically becomes available for new orders when its quantity is positive and it is within its availability period. Replenishment outside that period does not restore availability; any implemented expiry restriction must also be satisfied.
7. **Update the product’s marketplace availability**
   - **Priority:** Must have
   - **Acceptance criteria:** Changes determined by the stock and seasonal rules are reflected in the customer-facing listing and whether new orders are permitted, without requiring a new product submission. This item applies the availability decisions from items 4–6 rather than defining a separate publication process.

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
