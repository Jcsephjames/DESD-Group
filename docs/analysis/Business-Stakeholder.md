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





