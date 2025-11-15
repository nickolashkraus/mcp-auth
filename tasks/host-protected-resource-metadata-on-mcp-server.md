# Host Protected Resource Metadata on MCP Server

## Overview

To allow ChatGPT to discover how to authenticate, the resource (i.e., MCP server) must provide Protected Resource Metadata ([RFC 9728][RFC 9728]).

This involves defining a metadata endpoint (`/.well-known/oauth-protected-resource`), which returns a JSON document with information on the resource's associated authorization servers.

**NOTE**: MCP servers **MUST** implement the OAuth 2.0 Protected Resource Metadata ([RFC 9728](https://datatracker.ietf.org/doc/html/rfc9728)) specification to indicate the locations of authorization servers.

**Example**

```json
{
  "resource": "https://api.example.com",
  "authorization_servers": [
    "https://auth.example.com"
  ],
  "scopes_supported": [
    "read:data",
    "write:data",
    "admin"
  ],
  "resource_documentation": "https://docs.example.com/api"
}
```

* `resource` [REQUIRED]: The canonical identifier of the resource server.
* `authorization_servers` [REQUIRED]: Array of authorization server URLs that can issue tokens for this resource.
* `scopes_supported` [OPTIONAL]: OAuth scopes your resource server recognizes. **NOTE**: These are TBD and are declared on the tool.
* `resource_documentation` [OPTIONAL]: Link to documentation.

## Acceptance Criteria

* A metadata endpoint is defined in the MCP server ([Function-Health/ai-chat](https://github.com/Function-Health/ai-chat)), which returns the Protected Resource Metadata for the resource.
* The MCP server returns a `401 Unauthorized` for unauthenticated requests that includes the `WWW-Authenticate` header.

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://api.example.com/.well-known/oauth-protected-resource"
```

**NOTE**: ChatGPT expects the above response when its request is blocked.

## Resources

* [2.3 Authorization Server Discovery](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#authorization-server-discovery)
* [Custom auth with OAuth 2.1](https://developers.openai.com/apps-sdk/build/auth#custom-auth-with-oauth-21)

[RFC 9728]: https://datatracker.ietf.org/doc/html/rfc9728
