# Unit Test Scenarios

## Overview
This document describes the unit test scenarios implemented for the current movie collection system skeleton.
Each scenario maps directly to executable tests under `tests/unit`.

## Test Files
- `tests/unit/test_movie_search_flow.py`
- `tests/unit/test_collection_scenarios.py`
- `tests/unit/test_review_rating_scenarios.py`
- `tests/unit/test_auth_notification_scenarios.py`

---

## 1) Movie -> Search Event Flow
Test file: `tests/unit/test_movie_search_flow.py`

### Scenario: Movie created event updates search index
- Goal: Verify end-to-end local event propagation from Movie Service to Search Service.
- Given:
  - Search event handlers are subscribed.
  - Movie command service is initialized with in-memory repository and event publisher.
- When:
  - A movie is created with title `Interstellar`.
  - Search query is executed with keyword `Interstellar`.
- Then:
  - Movie creation result is successful.
  - Search returns exactly one item.
  - Returned item's title is `Interstellar`.

---

## 2) Collection Scenarios
Test file: `tests/unit/test_collection_scenarios.py`

### Scenario: Add movie to collection succeeds
- Goal: Validate normal collection creation and movie membership addition.
- Given:
  - Collection service is initialized with in-memory collection repository.
  - Movie validation adapter accepts non-empty movie id.
- When:
  - A collection is created by user `u1`.
  - Movie `m1` is added to the collection.
  - Collection items are queried.
- Then:
  - Collection creation succeeds.
  - Add-movie operation succeeds.
  - Collection items contain `m1`.

### Scenario: Duplicate movie addition is rejected
- Goal: Prevent duplicate membership in one collection.
- Given:
  - Existing collection `c2`.
- When:
  - The same movie `m2` is added twice.
- Then:
  - First add succeeds.
  - Second add fails.
  - Failure reason is `already added`.

---

## 3) Review & Rating Scenarios
Test file: `tests/unit/test_review_rating_scenarios.py`

### Scenario: Create review and query by movie
- Goal: Ensure review persistence and read model retrieval by movie id.
- Given:
  - Review service with in-memory review/rating repositories.
- When:
  - User `u9` creates review `r1` for movie `m9`.
  - Reviews are queried by movie id `m9`.
- Then:
  - Review creation succeeds.
  - Query returns one review.
  - Review content is `great`.

### Scenario: Rating update reflected in summary
- Goal: Ensure rating mutation impacts rating summary projection.
- Given:
  - Review/rating services initialized.
- When:
  - User submits rating score `5` for movie `m9`.
  - Rating summary is queried for `m9`.
- Then:
  - Rating update succeeds.
  - Summary count is at least 1.
  - Summary average is at least 1.0.

---

## 4) Auth & Notification Scenarios
Test file: `tests/unit/test_auth_notification_scenarios.py`

### Scenario: Login and access-token verification
- Goal: Validate authentication command/query flow.
- Given:
  - In-memory auth repository contains credential for user `u1` / password `pw1`.
- When:
  - Login is requested.
  - Returned access token is verified.
- Then:
  - Login succeeds.
  - Token verification result is valid.
  - Verified user id is `u1`.

### Scenario: Dispatch notification and query user logs
- Goal: Validate notification dispatch and log persistence/query.
- Given:
  - In-memory notification dispatcher and repository.
- When:
  - Notification `n1` is dispatched to user `u1`.
  - Notifications are queried for user `u1`.
- Then:
  - One notification log is returned.
  - Message is `hello`.

---

## Execution
Run all unit tests:

```bash
pytest -q
```

Expected current result:
- `14 passed`
