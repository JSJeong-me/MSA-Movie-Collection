# Integration Test Scenarios

## Overview
This document defines integration test scenarios across service boundaries in the current in-memory architecture.
It focuses on API-level and service-to-service collaboration behavior.

## Scope
- API Gateway routing/auth context behavior
- Movie -> Search asynchronous event propagation
- Collection/Review synchronous movie validation dependency
- Notification event-driven behavior
- Auth + User lifecycle coupling (event-driven)

---

## 1) Gateway Integration

### Scenario: Gateway routes request to target service
- Goal: Verify path-based downstream routing behavior.
- Given:
  - Gateway application service is initialized.
- When:
  - Request path `/movies` is routed.
- Then:
  - Target service is `movie-service`.

### Scenario: Gateway rejects protected request without authorization header
- Goal: Validate edge-level auth guard behavior.
- Given:
  - Protected path request.
- When:
  - Authorization header is missing.
- Then:
  - Gateway returns unauthorized response contract.

### Scenario: Gateway enriches downstream request context
- Goal: Ensure request/auth metadata propagation.
- Given:
  - RequestContext with request/correlation id.
  - AuthContext with user id/role.
- When:
  - Enrichment is applied.
- Then:
  - Downstream metadata includes request id, correlation id, user id, and role.

---

## 2) Movie -> Search Event Integration

### Scenario: MovieCreated event creates search document
- Goal: Verify asynchronous read-model synchronization.
- Given:
  - Search service subscribed to event bus.
  - Movie command service publishes `MovieCreated` event.
- When:
  - New movie is created.
- Then:
  - Search index document is created.
  - Search query by keyword returns the created movie.

### Scenario: MovieUpdated event updates indexed fields
- Goal: Keep Search projection aligned with catalog mutations.
- Given:
  - Existing indexed movie document.
- When:
  - Movie title/metadata is updated in Movie Service.
- Then:
  - Search document reflects updated fields.

### Scenario: MovieDeleted event removes search document
- Goal: Preserve search/catalog lifecycle consistency.
- Given:
  - Existing indexed movie document.
- When:
  - Movie is deactivated/deleted in Movie Service.
- Then:
  - Search document is removed (or marked inactive per policy).

---

## 3) Collection Integration (Sync Validation)

### Scenario: Add movie to collection with valid movie id
- Goal: Validate cross-service dependency via MovieValidationPort.
- Given:
  - Existing user-owned collection.
  - Movie validation returns `exists=true`.
- When:
  - Add movie to collection is requested.
- Then:
  - Membership is added.
  - Collection query returns the new movie id.

### Scenario: Add movie to collection with invalid movie id
- Goal: Prevent invalid foreign references.
- Given:
  - Existing collection.
  - Movie validation returns `exists=false`.
- When:
  - Add movie to collection is requested.
- Then:
  - Command is rejected with validation failure.

---

## 4) Review/Rating Integration (Sync Validation + Async Event)

### Scenario: Create review after movie existence validation
- Goal: Ensure review write path enforces movie boundary.
- Given:
  - Review service command flow.
  - Movie validation returns `exists=true`.
- When:
  - Create review is requested.
- Then:
  - Review is persisted.
  - `ReviewCreated` event is published.

### Scenario: Update rating emits RatingUpdated and refreshes search summary
- Goal: Validate rating-to-search integration chain.
- Given:
  - Existing movie and search document.
- When:
  - User creates/updates rating.
- Then:
  - `RatingUpdated` event is emitted.
  - Search indexed rating summary fields are updated according to projection policy.

---

## 5) Notification Integration

### Scenario: UserCreated event triggers welcome notification
- Goal: Validate event-consumer-driven notification creation.
- Given:
  - NotificationEventHandler connected to command service.
- When:
  - `UserCreated` event is consumed.
- Then:
  - Notification dispatch is invoked.
  - Notification log is persisted for target user.

### Scenario: Notification read-state transition
- Goal: Verify command/query consistency for user inbox.
- Given:
  - Existing notification log item.
- When:
  - Mark-as-read command is executed.
- Then:
  - Query result shows read flag as true.

---

## 6) Auth + User Lifecycle Integration

### Scenario: User registration event creates auth credential
- Goal: Keep profile and credential ownership decoupled but consistent.
- Given:
  - User registration completed.
  - UserCreated event is emitted to AuthEventHandler.
- When:
  - Auth handler processes UserCreated event.
- Then:
  - Credential record is created in auth repository.

### Scenario: User deactivation event disables auth credential
- Goal: Prevent login after profile lifecycle deactivation.
- Given:
  - Existing active credential.
- When:
  - UserDeactivated event is consumed by AuthEventHandler.
- Then:
  - Credential is marked inactive.
  - Subsequent login/refresh is rejected.

---

## Suggested Execution Strategy
1. Service-layer integration tests (without HTTP server boot)
- Validate event bus, repositories, and application services wiring.

2. API integration tests (FastAPI TestClient)
- Validate request/response contracts and router-to-service delegation.

3. Cross-service flow tests
- Verify end-to-end chains such as:
  - Movie create -> Search query reflects item
  - Review rating update -> Search rating field changes
  - User created -> Notification log exists

---

## Candidate Test File Layout
- `tests/integration/test_gateway_integration.py`
- `tests/integration/test_movie_search_integration.py`
- `tests/integration/test_collection_integration.py`
- `tests/integration/test_review_rating_integration.py`
- `tests/integration/test_notification_integration.py`
- `tests/integration/test_auth_user_lifecycle_integration.py`
