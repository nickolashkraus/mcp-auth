# Protected MCP Endpoints Should Return `401 Unauthorized` for Unauthorized Requests

## Overview

MCP servers **MUST** use the HTTP header `WWW-Authenticate` when returning a `401 Unauthorized` to indicate the location of the resource server metadata URL as described in [RFC 9728 Section 5.1 "WWW-Authenticate Response"][RFC 9728 Section 5.1].

## Acceptance Criteria

* Any protected endpoints on the MCP server should return a `401 Unauthorized` for unauthorized requests.
* The response should include a `WWW-Authenticate` header with the location of the resource server metadata:

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://your-mcp.example.com/.well-known/oauth-protected-resource",scope="files:read"
```

[RFC 9728 Section 5.1]: https://datatracker.ietf.org/doc/html/rfc9728#name-www-authenticate-response
