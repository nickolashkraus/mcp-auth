# Validate Access Token in Requests to MCP Server

## Overview

Per the MCP authorization specification,

1. MCP clients **MUST** use the `Authorization` request header field:

```
Authorization: Bearer <access-token>
```

2. MCP servers **MUST** validate access tokens as described in [OAuth 2.1 Section 5.2][OAuth 2.1 Section 5.2].

Access token validation comprises the following:

1. The access token is not yet expired.
2. The access token is authorized to access the requested resource (i.e., the access token was issued specifically for them as the intended audience, according to [RFC 8707 Section 2][RFC 8707 Section 2]).
3. The access token was issued with the appropriate scope.

Access tokens generally fall into two categories: *reference tokens* or *self-encoded tokens*. Reference tokens can be validated by querying the authorization server or looking up the token in a token database, whereas self-encoded tokens contain the authorization information in an encrypted and/or signed string which can be extracted by the resource server.

Since we will be using OIDC, the information used to validate the token can be taken from the token's claims.

**NOTE**: MCP servers **MUST** validate that tokens presented to them were specifically issued for their use. Therefore, any access token issued by the authorization server must include the resource indicator in its claims (`aud`).

Once a request reaches the MCP server the token should be considered untrusted and the MCP server must perform the full set of resource-server checks: signature validation, issuer and audience matching, expiry, replay considerations, and scope enforcement.

In practice this comprises the following:
1. Fetch the signing keys published by the authorization server (via JWKS) and verify the token’s signature and `iss`.
2. Reject tokens that have expired or have not yet become valid (`exp`/`nbf`).
3. Confirm the token was minted for the MCP server (`aud` or the resource claim) and contains the scopes marked as required.
4. Run any app-specific policy checks, then either attach the resolved identity to the request context or return a `401` with a `WWW-Authenticate` challenge.

**NOTE**: If verification fails, respond with `401 Unauthorized` and a `WWW-Authenticate` header that points back to the protected-resource metadata. This tells the client to run the OAuth flow again.

## Acceptance Criteria

* The MCP server ([Function-Health/ai-chat][Function-Health/ai-chat]) validates the access token it receives in requests as described in [OAuth 2.1 Section 5.2][OAuth 2.1 Section 5.2].
* The server verifies the token on each request (issuer, audience, expiration, scopes) before executing the tool.
* If validation fails, servers **MUST** respond according to [OAuth 2.1 Section 5.3][OAuth 2.1 Section 5.3] error handling requirements. Invalid or expired tokens **MUST** receive an HTTP 401 response.

| **Status Code** | **Description** | **Usage**                                  |
| --------------- | --------------- | ------------------------------------------ |
| `401`           | `Unauthorized`  | Authorization required or token invalid    |
| `403`           | `Forbidden`     | Invalid scopes or insufficient permissions |
| `400`           | `Bad Request`   | Malformed authorization request            |

## Resources

* [2.6 Access Token Usage](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#access-token-usage)

[OAuth 2.1 Section 5.2]: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-5.2
[OAuth 2.1 Section 5.3]: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-5.3
[RFC 8707 Section 2]: https://www.rfc-editor.org/rfc/rfc8707.html#section-2
[Function-Health/ai-chat]: https://github.com/Function-Health/ai-chat
