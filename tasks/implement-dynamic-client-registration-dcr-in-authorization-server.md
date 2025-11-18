# Implement Dynamic Client Registration (DCR) in Authorization Server

## Overview

ChatGPT acting on behalf of the user supports Dynamic Client Registration (DCR). [Dynamic Client Registration][Dynamic Client Registration] is part of the MCP authorization specification:

> MCP clients and authorization servers **SHOULD** support the OAuth 2.0 Dynamic Client Registration Protocol [RFC 7591][RFC 7591] to allow MCP clients to obtain OAuth client IDs without user interaction.

Client registration is a fundamental security mechanism in OAuth 2.0. The authorization server needs to know which clients it can trust before allowing them to participate in the authorization flow. Dynamic Client Registration (DCR) allows clients to automatically register themselves with an authorization server at runtime, without requiring manual pre-registration by an administrator.

In ChatGPT, this looks like the following:

1. A user adds an app or connector in ChatGPT.
2. ChatGPT initiates the MCP authentication flow and retrieves the `registration_endpoint` from Authorization Server Metadata.
3. ChatGPT sends a registration request to the authorization server's `registration_endpoint`. The request is authenticated with an Initial Access Token if the server requires one (RFC 7591 §3.1).
4. The authorization server creates a client by generating a unique `client_id` for the specific user/connector. The client information is persisted (e.g., in a database).
5. The authorization server returns the registration response (client metadata, optional registration management URI/token), and ChatGPT stores the `client_id` to complete the authentication flow.

**Example Request**

```
POST /oauth2/v1/register HTTP/1.1
Host: auth.example.com
Content-Type: application/json

{
  "client_name": "ChatGPT Connector for User",
  "redirect_uris": ["https://chat.openai.com/aip/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "scope": "files:read files:write"
}
```

**Example Response**

```
{
  "client_id": "abc123xyz789",
  "client_id_issued_at": 1234567890,
  "redirect_uris": ["https://chat.openai.com/aip/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "registration_client_uri": "https://auth.example.com/oauth2/v1/register/abc123xyz789",
  "registration_access_token": "redacted",
  "client_secret_expires_at": 0
}
```

**NOTE**: Public PKCE clients (like ChatGPT) do not require a `client_secret`. If your implementation always creates one, set `client_secret_expires_at` to `0` and ignore the secret on the client.

## Acceptance Criteria

* A metadata-driven registration endpoint (e.g., `/register`) exists in the authorization server ([Function-Health/member-app-middleware][Function-Health/member-app-middleware]) to facilitate DCR.
* The authorization server validates the request payload (redirect URIs, grant types, token endpoint auth method) and enforces any Initial Access Token requirements.
* The registration response includes the fields required by RFC 7591 (client metadata plus `registration_client_uri` and `registration_access_token` for management).
* The client metadata is persisted (e.g., in a database) for later token issuance and administration:
 
  ```
  CREATE TABLE oauth_clients (
      client_id VARCHAR(255) PRIMARY KEY,
      client_name VARCHAR(255) NOT NULL,
      redirect_uris JSON NOT NULL,
      grant_types JSON NOT NULL,
      response_types JSON NOT NULL,
      token_endpoint_auth_method VARCHAR(64) NOT NULL,
      scope TEXT,
      registration_client_uri TEXT,
      registration_access_token TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

**NOTE**: At minimum, persist `client_id` and `redirect_uris`, but storing the full metadata simplifies rotations and revocations.

## Resources

* [Model Context Protocol — Dynamic Client Registration][Dynamic Client Registration]
* [Custom Auth with OAuth 2.1][Custom Auth with OAuth 2.1]

[Dynamic Client Registration]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#dynamic-client-registration
[RFC 7591]: https://datatracker.ietf.org/doc/html/rfc7591
[Function-Health/member-app-middleware]: https://github.com/Function-Health/member-app-middleware
[Custom Auth with OAuth 2.1]: https://developers.openai.com/apps-sdk/build/auth#custom-auth-with-oauth-21
