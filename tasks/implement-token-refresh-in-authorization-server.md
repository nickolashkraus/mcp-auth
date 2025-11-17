# Implement Token Refresh in Authorization Server (`/token`)

## Overview

Per the MCP authorization spec,

> Authorization servers **SHOULD** issue short-lived access tokens to reduce the impact of leaked tokens. For public clients, authorization servers **MUST** rotate refresh tokens as described in [OAuth 2.1 Section 4.3.1 "Token Endpoint Extension"][OAuth 2.1 Section 4.3.1].

An expiration time of 10-15 minutes for access tokens seems reasonable. This is added to the access token using the `exp` claim and is validated by the MCP server. If a token has expired, the MCP server returns an HTTP 401 response. If a token is invalid due to expiration, the client can use a *refresh token* to obtain a new access token without requiring the user to re-authenticate. Therefore, refresh tokens are short-lived credentials bound to the client.

## Implementation Details

The refresh token grant type is identified at the token endpoint with the `grant_type` value of `refresh_token`. Because refresh tokens are typically longer-lasting credentials used to request additional access tokens, the refresh token is bound to the client to which it was issued.

For example, the client makes the following HTTP request:

```
POST /token HTTP/1.1
Host: server.example.com
Authorization: Bearer <access-token>
Content-Type: application/json

grant_type=refresh_token
refresh_token=<refresh_token>
```

In addition to the processing rules in [OAuth 2.1 Section 3.2.2][OAuth 2.1 Section 3.2.2], the authorization server MUST:
* If client authentication is included in the request, ensure that the refresh token was issued to the authenticated client, OR if a `client_id` is included in the request, ensure the refresh token was issued to the matching client.
* Validate that the grant corresponding to this refresh token is still active.
* Validate the refresh token.

Authorization servers MUST utilize one of these methods to detect refresh token replay by malicious actors for public clients: 
* **Sender-constrained refresh tokens**: The authorization server cryptographically binds the refresh token to a certain client instance, e.g., by utilizing DPoP ([RFC 9449][RFC 9449]) or mTLS ([RFC 8705][RFC 8705]).
* **Refresh token rotation**: The authorization server issues a new refresh token with every access token refresh response. The previous refresh token is invalidated but information about the relationship is retained by the authorization server. If a refresh token is compromised and subsequently used by both the attacker and the legitimate client, one of them will present an invalidated refresh token, which will inform the authorization server of the breach. The authorization server cannot determine which party submitted the invalid refresh token, but it will revoke the active refresh token as well as the access authorization grant associated with it. This stops the attack at the cost of forcing the legitimate client to obtain a fresh authorization grant.

**NOTE**: The grant to which a refresh token belongs may be encoded into the refresh token itself. This can enable an authorization server to efficiently determine the grant to which a refresh token belongs, and by extension, all refresh tokens that need to be revoked. Authorization servers MUST ensure the integrity of the refresh token value in this case, for example, using signatures.

**NOTE**: For our implementation, we will use *refresh token rotation*, which is an OAuth 2.1 best practice.

## References

* [3.2 Token Theft][MCP Token Theft]
* [OAuth 2.1 Section 4.3.1 "Token Endpoint Extension"][OAuth 2.1 Section 4.3.1]

[OAuth 2.1 Section 4.3.1]: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-4.3.1
[OAuth 2.1 Section 3.2.2]: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#token-request
[RFC 9449]: https://www.rfc-editor.org/info/rfc9449
[RFC 8705]: https://www.rfc-editor.org/info/rfc8705
[MCP Token Theft]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#token-theft
