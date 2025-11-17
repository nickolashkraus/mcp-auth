# Implement Authorization Callback Endpoint in Authorization Server (`/authorize/callback`)

## Overview

The authorization callback endpoint (`/authorize/callback`) is responsible for the actual authorization of the user given the provided credentials. For our implementation, the user provides their credentials (username/password) and authentication is handled by [Function-Health/member-app-middleware][Function-Health/member-app-middleware]. After successful authentication, an authorization code is returned, which is a temporary, single-use credential that proves the user authorized the client (ChatGPT).

## Implementation Details

The `/authorize` endpoint initiates the flow (validating `client_id`, `redirect_uri`, `code_challenge`, `scope`, `resource`, etc.) and typically displays a login/consent form. When the user submits the form, the authorization server receives a `POST` request to `/authorize/callback` with the provided credentials. This endpoint is responsible for:

**1. Authenticating the user**
Verifies the username/password of the user in Firebase.

**2. Re-validating the original authorization request context**
The form request contains the following inputs:
  * `client_id`
  * `code_challenge`
  * `code_challenge_method`
  * `redirect_uri`
  * `resource`
  * `response_type`
  * `scope`
  * `state`
At the very least, `state` is verified to prevent CSRF attacks. We may also want to confirm the *transaction* has not expired and ensure it still references the same `client_id`, `redirect_uri`, `code_challenge`, `resource`, `scopes`, etc. The server should ignore the user-provided `redirect_uri` and instead use the value stored when `/authorize` created the transaction.

**NOTE**: A possible implementation uses ephemeral storage to persist the authentication request transaction for a short amount of time.

**3. Issuing the authorization code**
Generates a single-use authorization code (`authorization_code`) tied to the authentication request flow transaction. The authorization code should be persisted (e.g., Redis/PostgreSQL) along with the client metadata (`client_id`, `redirect_uri`, `code_challenge`, `code_challenge_method`, `resource`, and `scopes`). The authorization code should have a short expiration (e.g., 5 minutes) and be marked as consumable once. Storing `resource` and `scopes` exactly as provided ensures `/token` can validate them and propagate them into the resulting access token.

**4. Redirecting the user back to the client**
The user's browser receives a redirection to the original redirect URI (ChatGPT) with the `code` and `state` (if provided) in the request URL parameters. If authentication fails, redirect with an OAuth error (`error=access_denied` or `error=login_required`). See [Error Handling][Error Handling].

## Acceptance Criteria

* The authorization callback endpoint (`/authorize/callback`) accepts user credentials from the login form initiated at `/authorize`.
* The endpoint validates the authorization request and returns OAuth-compliant errors when authentication fails.
* On success, the endpoint issues a single-use authorization code that captures `client_id`, `redirect_uri`, `code_challenge`, `code_challenge_method`, `resource`, `scope`, and `user_id`, and persists it for validation when the authorization token is used to retrieve an access token (`/token`).
* The endpoint redirects to the `redirect_uri` with the `code` (and `state`, when supplied) parameters, or returns an OAuth error per [RFC 6749][RFC 6749] when validation fails.

**NOTE**: We may want to consider using [Authlib][Authlib] for an [Authorization Server][Authorization Server] implementation that generates authorization codes.

[Error Handling]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#error-handling
[RFC 6749]: https://datatracker.ietf.org/doc/html/rfc6749
[Authlib]: https://authlib.org
[Authorization Server]: https://docs.authlib.org/en/latest/flask/2/authorization-server.html
