# Authorization Flow

```mermaid
sequenceDiagram
    autonumber
    participant UA as User-Agent (Browser)
    participant Client as Client
    participant MCP as MCP Server (Resource Server)
    participant AS as Authorization Server

    Client->>MCP: MCP request without token
    MCP-->>Client: HTTP 401 Unauthorized with WWW-Authenticate header
    Note right of Client: Extract resource_metadata URL from WWW-Authenticate

    Client->>MCP: Request Protected Resource Metadata
    MCP-->>Client: Return metadata
    Note right of Client: Parse metadata and extract authorization server(s)\nClient determines AS to use

    Client->>AS: GET /.well-known/oauth-authorization-server
    AS-->>Client: Authorization server metadata response

    rect rgba(255,255,255,0)
    note over Client,AS: Dynamic client registration
    Client->>AS: POST /register
    AS-->>Client: Client Credentials
    end

    Note right of Client: Generate PKCE parameters\nInclude resource parameter
    Client->>UA: Open browser with authorization URL + code_challenge + resource
    UA->>AS: Authorization request with resource parameter
    Note right of AS: User authorizes
    AS-->>UA: Redirect to callback with authorization code
    UA->>Client: Authorization code callback

    Client->>AS: Token request + code_verifier + resource
    AS-->>Client: Access token (+ refresh token)

    Client->>MCP: MCP request with access token
    MCP-->>Client: MCP response

    Note over Client,MCP,AS: MCP communication continues with valid token
```

A very simplified OAuth 2.1 authorization flow for ChatGPT is as follows:

1. ChatGPT queries the MCP server for Protected Resource Metadata.
2. ChatGPT registers itself via Dynamic Client Registration with the
   authorization server using the `registration_endpoint` and obtains a client
   ID (`client_id`).
3. When the user first invokes a tool, the ChatGPT client launches the OAuth
   authorization code + PKCE flow. The user authenticates and consents to the
   requested scopes.
4. ChatGPT exchanges the authorization code for an access token and attaches it
   to subsequent MCP requests (`Authorization: Bearer <token>`).
5. The MCP server verifies the token on each request (issuer, audience,
   expiration, scopes, etc.) before executing the tool.
