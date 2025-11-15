# Implement Dynamic Client Registration (DCR) in Authorization Server

## Overview

ChatGPT acting on behalf of the user supports dynamic client registration (DCR). [Dynamic Client Registration][Dynamic Client Registration] is part of the MCP authorization specification:

> MCP clients and authorization servers **SHOULD** support the OAuth 2.0 Dynamic Client Registration Protocol [RFC 7591](https://datatracker.ietf.org/doc/html/rfc7591) to allow MCP clients to obtain OAuth client IDs without user interaction.

Client registration is a fundamental security mechanism in OAuth 2.0. The authorization server needs to know which clients it can trust before allowing them to participate in the authorization flow. Dynamic Client Registration (DCR) allows clients to automatically register themselves with an authorization server at runtime, without requiring manual pre-registration by an administrator.

In ChatGPT, this looks like the following:

1. A user adds an app or connector in ChatGPT.
2. ChatGPT initiates the MCP authentication flow in which the endpoint (`registration_endpoint`) for Dynamic Client Registration (DCR) is retrieved.
3. ChatGPT sends a registration request to the authorization server's `registration_endpoint`.
4. The authorization server creates a client by generating a unique `client_id` for the specific user/connector. The client information is persisted (e.g., in a database).
5. The authorization server returns the credentials and ChatGPT stores the `client_id`, which is then used to complete the authentication flow.

**Example Request**

```
POST /register HTTP/1.1
Host: auth.example.com
Content-Type: application/json

{
  "client_name": "ChatGPT Connector for User",
  "redirect_uris": ["https://chat.openai.com/aip/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "token_endpoint_auth_method": "none",
  "scope": "files:read files:write"
}
```

**Example Response**

```
{
  "client_id": "abc123xyz789",
  "client_id_issued_at": 1234567890,
  "client_secret": "secret",
  "client_secret_expires_at": 0,
  "redirect_uris": ["https://chat.openai.com/aip/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "token_endpoint_auth_method": "none"
}
```

**NOTE**: `client_secret` is optional for public clients using PKCE. This includes web/mobile apps like ChatGPT.

## Acceptance Criteria

* An endpoint (`/register`) exists in the authorization server ([Function-Health/member-app-middleware][Function-Health/member-app-middleware]) to facilitate Dynamic Client Registration (DCR).
* The client ID is persisted (e.g., in a database):
 
  ```
  CREATE TABLE oauth_clients (
      client_id VARCHAR(255) PRIMARY KEY,
      redirect_uris JSON NOT NULL,
      grant_types JSON DEFAULT '["authorization_code", "refresh_token"]',
      response_types JSON DEFAULT '["code"]',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

**NOTE**: The absolute minimum information to store is `client_id` and `redirect_uris`.

## Resources

* [2.4 Dynamic Client Registration](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#dynamic-client-registration)
* [Custom auth with OAuth 2.1](https://developers.openai.com/apps-sdk/build/auth#custom-auth-with-oauth-21)

[Dynamic Client Registration]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#dynamic-client-registration
[Function-Health/member-app-middleware]: https://github.com/Function-Health/member-app-middleware
