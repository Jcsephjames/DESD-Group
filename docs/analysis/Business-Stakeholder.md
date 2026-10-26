# Stakeholder and Business Process Analysis

**UFCFTR-30-3 Task 1 – Local Food Multi-Vendor Marketplace**  
**Sprint 1**

## 1. Purpose and scope

The Bristol Regional Food Network connects local food producers with customers within 20 miles of Bristol. The selected work supports trustworthy listings and accurate stock and seasonal availability.

Both selected functionalities belong to **Use Case 1: Producer Product Listing and Inventory Management**:

1. **Product Submission, Validation and Publication:** submit a new product, validate its details, verify any organic claim and publish the listing.
2. **Product and Seasonal Availability Management:** maintain an existing product’s stock and availability dates, and automatically update its marketplace availability.

## 2. Stakeholders and their needs

| Stakeholder | Main needs and interests | Role in the selected scope |
|---|---|---|
| **Local producers** | List products easily; correct mistakes without losing valid entries; understand publication or verification problems; keep stock and seasonal dates accurate. | Submit product and certification details, resolve validation failures and maintain their own listings. |
| **Young professionals and families** | Clear product descriptions, prices, origin and relevant food information, with reliable availability and organic claims. | View published listings and identify products currently available. |
| **Community groups** | Reliable information about local produce and quantities to support catering planning. | Use published product information and availability to assess suitable supplies. |
| **Independent restaurants and cafés** | Accurate stock and seasonal information to support ingredient and menu planning. | Assess products from local producers using marketplace listings. |
| **Marketplace operator** | Maintain a consistent product catalogue, prevent unverified claims from being published and keep customer-facing availability accurate. | Own the catalogue and business rules; rely on the platform to validate, publish and update availability automatically. |


## 3. Stakeholder requirements and functional alignment

| ID | Stakeholder requirement 
|---|---|
| **SR1** | **Producers need a complete product submission form.** Capture name, description, category, price, quantity, availability period, farm origin and whether organic certification is claimed. Capture certification details for a claim, plus relevant harvest, allergen and best-before information where applicable. | 
| **SR2** | **Producers need clear validation and an easy correction process.** Identify missing or invalid fields, retain correct entries and allow correction and resubmission within the same process without reloading the page. Standardise accepted dates and numbers; do not save partial invalid products. |
| **SR3** | **Customers and the operator need trustworthy organic claims.** Verify claimed certification and record the result. Failed verification must block publication and explain the problem to the producer, who can correct the details or remove the claim and resubmit. |
| **SR4** | **Producers need recoverable verification failures.** If the certification service is unavailable, keep the submission unpublished and pending verification, inform the producer and allow a retry without creating a duplicate listing. |
| **SR5** | **The operator needs a controlled, persistent product catalogue.** Store accepted product records in the marketplace’s SQL database. Publish a listing only after mandatory details and any claimed organic certification pass the required checks. | 
| **SR6** | **Producers need safe stock updates.** Allow them to change their own existing product’s quantity to a non-negative value. Reject invalid values with an explanation and preserve the original product; reassess availability after a successful update. | 
| **SR7** | **Producers need seasonal availability management.** Allow changes to their own product’s availability dates, reject invalid date ranges and reassess availability after saving. Automatically reassess when a recorded availability period starts or ends. | 
| **SR8** | **Customers need accurate product visibility and availability.** An already validated and published product is available for new orders only when it has positive stock and is in season. Show in-season, zero-stock products with 0 stock, but hide out-of-season products. Reflect changes automatically without a new submission. |


## 4. Main business processes

### Process 1: Product submission, validation and publication

**Trigger:** a registered producer submits a new product.  
**Participants:** producer, marketplace platform and, for organic claims, certification service.

1. Capture product information and validate mandatory fields and formats.
2. Return validation errors for correction while retaining valid entries.
3. Verify any organic claim and record the outcome; skip this check for products without a claim.
4. Handle failed verification through correction or claim removal. Handle service unavailability by retaining an unpublished submission for retry.
5. After successful checks, publish the accepted product and apply Functionality 2’s stock and seasonal rules.

**Outcome:** a validated, published listing, or an unpublished submission awaiting correction or verification.

### Process 2: Product and seasonal availability management

**Trigger:** initial publication, a stock/date update, or the start/end of a recorded season.  
**Participants:** producer and marketplace platform; customers receive updated listing information.

1. Validate and save producer changes; invalid updates leave the original product unchanged.
2. Check stock and whether the current date falls within the availability period.
3. Hide out-of-season products and products with 0 stock. Display in-season, Neither is available for new orders.
4. Automatically enable availability for validated, published products with positive stock that are in season.
5. Update the listing without a new submission.

**Outcome:** accurate marketplace visibility and availability.


## 6. Responsibilities and modelling implications

- **Producers** own the accuracy of their product, certification, stock and seasonal information; updates apply to their own products.
- **The operator** owns the catalogue and business rules. The platform automates validation, publication and availability; no manual approval workflow is specified.
- **Customers** depend on producers for accurate information and the marketplace for reliable listings. Clear origin, relevant allergen details and honest organic claims support trust.
- **Certification service dependency:** distinguish a failed verification from service unavailability and provide the corresponding recovery path.
- **Responsible design:** protect producer and certification data, use readable forms and messages, and present product claims accurately.
- **Modelling:** BPMN should cover the two selected processes, correction loops, conditional verification, retry paths and seasonal reassessment. i* models should represent the stakeholder goals and dependencies above.
