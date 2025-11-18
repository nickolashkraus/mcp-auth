# Implement Authorization Code Protection (PKCE)

## Overview

PKCE (Proof Key for Code Exchange) is a security enhancement for OAuth 2.1 authorization code flows for when the client is a public client (e.g., mobile app) that cannot safely store a client secret.

In a standard OAuth authorization code flow, the client exchanges an authorization code for tokens. But if an attacker intercepts that authorization code (e.g., via redirect interception), they can exchange it for tokens themselves. PKCE prevents that by proving that the client presenting the authorization code is the same one that initiated the request. This is accomplished using a client-generated verifier and a hash-based challenge mechanism described below.

**NOTE**: MCP clients **MUST** implement PKCE according to [OAuth 2.1 Section 7.5.2][OAuth 2.1 Section 7.5.2].

## How It Works

ChatGPT, acting as the MCP client, performs the authorization code flow with PKCE using the `S256` code challenge.

1. The client generates a random `code_verifier` using the [RFC 7636][RFC 7636] alphabet (`A-Z`, `a-z`, `0-9`, `-._~`) with a length between 43 and 128 characters.
2. The client derives a `code_challenge` from it: `code_challenge = BASE64URL_NO_PADDING(SHA256(code_verifier))`. **NOTE**: Only the `S256` method is supported.
3. The client starts the OAuth 2.1 flow and sends the `code_challenge` and `code_challenge_method=S256` to the authorization server: `/authorize?...&code_challenge=...&code_challenge_method=S256`.
4. After successful login, the client receives the authorization code.
5. To exchange the code for tokens, the client must send the original `code_verifier` in the `/token` request body.
6. The authorization server recomputes `SHA256(code_verifier)`, encodes it with base64url (no padding), and compares it to the stored `code_challenge`:
   * If they match → the token response is issued.
   * If not → the request is rejected with `invalid_grant`.

## Acceptance Criteria

* Ensure the authorization server provides the `code_challenge_methods_supported` field, which includes `S256` in its Authorization Server Metadata.
* Instrument the `/authorize` endpoint with PKCE enforcement:
  * Require both `code_challenge` and `code_challenge_method` parameters.
  * Reject requests unless `code_challenge_method == "S256"`.
  * Store the `code_challenge` value temporarily (e.g., Redis) keyed by the issued authorization code so it can be retrieved during `/token`.
    ```
    SET auth:code:HXaz4hNg... '{"code_challenge":"eCe/nK...","client_id":"..."}' EX 600
    ```
* Instrument the `/token` endpoint with PKCE validation:
  * Require a `code_verifier` parameter.
  * Look up the stored `code_challenge` for the provided authorization code.
  * Recompute `BASE64URL_NO_PADDING(SHA256(code_verifier))` and compare it to the stored challenge.
  * Reject the request with `invalid_grant` if any step fails.

## Resources

* [Authorization Code Protection][Authorization Code Protection]
* [Custom Auth with OAuth 2.1][Custom Auth with OAuth 2.1]

[OAuth 2.1 Section 7.5.2]: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-7.5.2
[RFC 7636]: https://datatracker.ietf.org/doc/html/rfc7636
[Authorization Code Protection]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#authorization-code-protection
[Custom Auth with OAuth 2.1]: https://developers.openai.com/apps-sdk/build/auth#custom-auth-with-oauth-21
