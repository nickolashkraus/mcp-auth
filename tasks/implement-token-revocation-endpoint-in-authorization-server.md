# Implement Token Revocation Endpoint in Authorization Server (`/revoke`)

## Overview

The token revocation endpoint (`/revoke`) is used to invalidate a client's access and refresh tokens, thereby preventing further token issuance until the client has re-authenticated.

This may be done for the following reasons (in the context of ChatGPT apps):
* The user explicitly wishes to revoke the client's access, such as when disconnecting the app (**Settings** > **Apps & Connectors** > *Disconnect*).
* The developer/app owner wants to revoke one or more users' access to the app.
* The developer/app owner wants to delete the app entirely.
* The user is malicious or the app has been compromised.

Since access and refresh tokens are stored in a database (PostgreSQL), we can delete tokens or mark them are revoked by querying based on the ID of the client. After token revocation and given the resource server (MCP server) validates access tokens by looking them up in the database, the next time the client attempts to make an authenticated request using the revoked token, the validation will fail.

**NOTE**: As a security measure, it is important to only issue short-lived access tokens.

## Implementation Details

We can perform token revocation at the client-level (i.e., revoking the client's currently valid access and refresh tokens) or at the token level using the JWT ID (`jti`), which is provided via the claims of the token.

**NOTE**: We will also need to invalidate the client's refresh tokens that were issued along with the access token. Revoking the refresh token means the next time the client attempts to refresh the access token, the request for a new access token will be denied.

## Acceptance Criteria
* The token revocation endpoint (`/revoke`) is implemented in the authorization server that is responsible for revoking the access and refresh tokens of a client.

## Resources

* [13.1 Revoking Access][13.1 Revoking Access]

[13.1 Revoking Access]: https://www.oauth.com/oauth2-servers/listing-authorizations/revoking-access/
