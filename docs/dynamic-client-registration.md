# Dynamic Client Registration (DCR)

Dynamic Client Registration (DCR) is an OAuth 2.0 extension ([RFC 7591][RFC 7591])
that allows clients to programmatically register with an authorization server
at runtime instead of requiring manual pre-registration. MCP relies on DCR so
ChatGPT can use a dedicated `client_id` for each app and/or connector
installation. It allows clients like ChatGPT to self-register with the
authorization server without manual intervention.

In practice, DCR is a short HTTP exchange between the MCP client (ChatGPT) and
the authorization server. It should be noted that DCR is required by both
ChatGPT and the MCP authorization spec.

1. The MCP client discovers the `registration_endpoint` via the Authorization
   Server Metadata ([RFC 8414][RFC 8414]):

    ```json
    {
      "registration_endpoint": "https://auth.example.com/oauth2/v1/register"
    }
    ```

2. The MCP client prepares a registration request. ChatGPT always registers as
   a public client (no client secret) that uses `authorization_code` + PKCE.

    ```json
    {
      "client_name": "ChatGPT Connector",
      "redirect_uris": ["https://chat.openai.com/aip/callback"],
      "grant_types": ["authorization_code", "refresh_token"],
      "response_types": ["code"],
      "token_endpoint_auth_method": "none",
      "scope": "files:read files:write"
    }
    ```

   **NOTE**: If the authorization server requires an Initial Access Token
   ([RFC 7591 Section 3.1][RFC 7591 Section 3.1]), ChatGPT sends it in the
   `Authorization: Bearer <token>` header.

3. The authorization server validates the payload:

    ```
    VALIDATE redirect_uris ⊆ AllowedUris
    VALIDATE grant_types includes "authorization_code"
    VALIDATE token_endpoint_auth_method == "none"
    ```

4. The authorization server persists the client metadata (see **Storage**).

5. The authorization server returns a registration response:

    ```json
    {
      "client_id": "e3d3879e-a3d2-4b86-9d7f-9f1c354ad8a1",
      "client_id_issued_at": 1730000000,
      "redirect_uris": ["https://chat.openai.com/aip/callback"],
      "grant_types": ["authorization_code", "refresh_token"],
      "response_types": ["code"],
      "token_endpoint_auth_method": "none",
      "registration_client_uri": "https://auth.example.com/oauth2/v1/register/e3d3879e-a3d2-4b86-9d7f-9f1c354ad8a1",
      "registration_access_token": "<REDACTED>"
    }
    ```

   **NOTE**: Public clients do not need a `client_secret`. If your server
   always generates one, set `client_secret_expires_at` to `0` and ignore the
   secret.

## Storage

Since every app and/or connector installation gets its own OAuth client, the
authorization server must store the registration metadata. A relational schema
could look like:

```
CREATE TABLE oauth_clients (
    client_id TEXT PRIMARY KEY,
    client_name TEXT NOT NULL,
    redirect_uris JSONB NOT NULL,
    grant_types JSONB NOT NULL,
    response_types JSONB NOT NULL,
    token_endpoint_auth_method TEXT NOT NULL,
    scope TEXT,
    registration_client_uri TEXT,
    registration_access_token TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

This allows the server to look up the connector during `/token` and
`/introspect` calls, revoke access, or rotate redirect URIs safely.

## References

* [RFC 7591: OAuth 2.0 Dynamic Client Registration Protocol][RFC 7591]
* [RFC 8414: OAuth 2.0 Authorization Server Metadata][RFC 8414]
* [Model Context Protocol — Dynamic Client Registration][MCP DCR]

[RFC 7591]: https://datatracker.ietf.org/doc/html/rfc7591
[RFC 8414]: https://datatracker.ietf.org/doc/html/rfc8414
[MCP DCR]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#dynamic-client-registration
[RFC 7591 Section 3.1]: https://datatracker.ietf.org/doc/html/rfc7591#section-3.1
