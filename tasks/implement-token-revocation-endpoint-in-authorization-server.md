# Implement Token Revocation Endpoint in Authorization Server (`/revoke`)

## Overview

The token revocation endpoint (`/revoke`), as defined in [RFC 7009][RFC 7009], is used to invalidate a client's access and refresh tokens, thereby preventing further token issuance until the client has re-authenticated.

This may be done for the following reasons (in the context of ChatGPT apps):
* The user explicitly wishes to revoke the client's access, such as when disconnecting the app (**Settings** > **Apps & Connectors** > *Disconnect*).
* The developer/app owner wants to revoke one or more users' access to the app.
* The developer/app owner wants to delete the app entirely.
* The user is malicious or the app has been compromised.

Since access and refresh tokens are stored in a database (PostgreSQL), we can delete tokens or mark them as revoked by querying based on the ID of the client. After token revocation and given the resource server (MCP server) validates access tokens by looking them up in the database, the next time the client attempts to make an authenticated request using the revoked token, the validation will fail.

**NOTE**: As a security measure, it is important to only issue short-lived access tokens.

## Implementation Details

We can perform token revocation at the client-level (i.e., revoking the client's currently valid access and refresh tokens) or at the token level using the JWT ID (`jti`), which is provided via the claims of the token.

**NOTE**: We will also need to invalidate the client's refresh tokens that were issued along with the access token. Revoking the refresh token means the next time the client attempts to refresh the access token, the request for a new access token will be denied.

The `/revoke` endpoint MUST follow [RFC 7009][RFC 7009].

**Example**

```
POST /revoke HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW

token=45ghiukldjahdnhzdauz&token_type_hint=refresh_token
```

* HTTP method: `POST`
* Content type: `application/x-www-form-urlencoded`
* Request parameters:
  * `token` [REQUIRED]: The access or refresh token to revoke.
  * `token_type_hint` [OPTIONAL]: `access_token` or `refresh_token` to help locate the token.
* Response: Respond with an HTTP 200 on success, even if the token was already invalid. Error responses should follow [RFC 7009 Section 2.2.1][RFC 7009 Section 2.2.1].

**NOTE**: It is important to note that the client MUST first be authenticated to ensure the token belongs to it before revoking it. We can also implement a mechanism whereby an admin can revoke a client's token.

**NOTE**: Refresh-token revocation should remove/rotate the stored refresh token so that subsequent `/token` calls fail. Access token revocation should ensure the MCP server's validation logic checks revocation status (e.g., via database lookup or introspection).

## Acceptance Criteria
* The token revocation endpoint (`/revoke`) is implemented in the authorization server following [RFC 7009][RFC 7009].
* The endpoint revokes both access and refresh tokens tied to the authenticated client.
* Revoked refresh tokens cannot be used to mint new access tokens.
* Revoked access tokens are rejected by the MCP server's validation logic.

## Resources

* [RFC 7009][RFC 7009]
* [13.1 Revoking Access][13.1 Revoking Access]

[RFC 7009]: https://datatracker.ietf.org/doc/html/rfc7009
[RFC 7009 Section 2.2.1]: https://datatracker.ietf.org/doc/html/rfc7009#section-2.2.1 
[13.1 Revoking Access]: https://www.oauth.com/oauth2-servers/listing-authorizations/revoking-access/
