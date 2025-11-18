# Tasks

The following provides a list of tasks in sequential order for implementing
a custom authorization implementation that conforms to the [Model Context
Protocol (MCP) authorization specification][MCP authorization spec].

1. [Host Protected Resource Metadata on MCP Server](./host-protected-resource-metadata-on-mcp-server.md)
2. [Host Authorization Server Metadata on Authorization Server](./host-authorization-server-metadata-on-authorization-server.md)
3. [Implement Dynamic Client Registration (DCR) in Authorization Server](./implement-dynamic-client-registration-dcr-in-authorization-server.md)
4. [Handle Resource Indicators Provided by ChatGPT](./handle-resource-indicators-provided-by-chatgpt.md)
5. [Implement Authorization Code Protection (PKCE)](./implement-authorization-code-protection.md)
6. [Implement Authorization Endpoint in Authorization Server (`/authorize`)](./implement-authorization-endpoint-in-authorization-server.md)
7. [Implement Authorization Callback Endpoint in Authorization Server (`/authorize/callback`)](./implement-authorization-callback-endpoint-in-authorization-server.md)
8. [Implement Token Endpoint in Authorization Server (`/token`)](./implement-token-endpoint-in-authorization-server.md)
9. [Validate Access Token in Requests to MCP Server](./validate-access-token-in-requests-to-mcp-server.md)
10. [Generate JSON Web Key Sets (JWKS)](./generate-json-web-key-sets.md)
11. [Implement Token Refresh in Authorization Server (`/token`)](./implement-token-refresh-in-authorization-server.md)
12. [Protected MCP Endpoints Should Return 401 Unauthorized for Unauthorized Requests](./protected-mcp-endpoints-should-return-401-unauthorized-for-unauthorized-requests.md)
13. [Implement UserInfo Endpoint in Authorization Server (`/userinfo`)](./implement-userinfo-endpoint-in-authorization-server.md)
14. [Implement Token Revocation Endpoint in Authorization Server (`/revoke`)](./implement-token-revocation-endpoint-in-authorization-server.md)
15. [Implement Token Introspection Endpoint in Authorization Server (`/introspect`)](./implement-token-introspection-endpoint-in-authorization-server.md)

[MCP authorization spec]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
