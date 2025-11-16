# Implement Authorization Code Protection (PKCE)

## Overview

PKCE (Proof Key for Code Exchange) is a security enhancement for OAuth 2.1 authorization code flows for when the client is a public client (e.g., mobile app) that cannot safely store a client secret.

In a standard OAuth authorization code flow, the client exchanges an authorization code for tokens. But if an attacker intercepts that authorization code (e.g., via redirect interception), they can exchange it for tokens themselves. PKCE prevents that by proving that the client presenting the authorization code is the same one that initiated the request. This is accomplished using a client-generated verifier and a hash-based challenge mechanism described below.

**NOTE**: MCP clients **MUST** implement PKCE according to [OAuth 2.1 Section 7.5.2][OAuth 2.1 Section 7.5.2].

## How It Works

ChatGPT, acting as the MCP client, performs the authorization code flow with PKCE using the `S256` code challenge.

1. The client (ChatGPT) generates a random string called a `code_verifier`, then derives a `code_challenge` from it: `code_challenge = BASE64URL(SHA256(code_verifier))`.
2. The client starts the OAuth 2.1 flow and sends the `code_challenge` to the authorization server: `/authorize?code_challenge`.
3. After successful login, the client receives the authorization code.
4. To exchange the code for tokens, the client must send the original `code_verifier`.
5. The server recomputes `SHA256(code_verifier)` and checks it matches the original `code_challenge`.
   1. If they match → token is issued.
   2. If not → request is rejected.

## Acceptance Criteria

* Ensure the authorization server provides the `code_challenge_methods_supported` field, which includes `S256` in its Authorization Server Metadata.
* Instrument the `/authorize` endpoint with `code_challenge` verification:
  * Was a code challenge (`code_challenge`) included in the parameters of the request?
  * Was a code challenge method (`code_challenge_method`) included in the parameters of the request?
    * **NOTE**: This **MUST** be `S256`.
  * Store the `code_challenge` value temporarily (Redis).
    * **NOTE**: Since the `code_challenge` is associated with a unique authorization code, it can be used to uniquely identify the code challenge value in Redis:
      **Example**

      ```
      SET auth:code:HXaz4hNg... '{"code_challenge":"eCe/nK...","client_id":"..."}' EX 600
      ```

## Resources

* [3.4 Authorization Code Protection](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#authorization-code-protection)
* [Custom auth with OAuth 2.1](https://developers.openai.com/apps-sdk/build/auth#custom-auth-with-oauth-21)

[OAuth 2.1 Section 7.5.2]: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-7.5.2
