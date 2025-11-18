# mcp-authorization

A custom authorization implementation that conforms to the [Model Context
Protocol (MCP) authorization specification][MCP authorization spec].

This implementation is tailored to the OAuth 2.1 authentication flow for the
[OpenAI Apps SDK][OpenAI Apps SDK]. It implements both the [resource
server][OAuth 2.1 Roles] (MCP server) and [authorization server][OAuth 2.1
Roles].

## Resources
* [Understanding Authorization in MCP][Understanding Authorization in MCP]

[MCP authorization spec]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
[OpenAI Apps SDK]: https://developers.openai.com/apps-sdk/build/auth
[OAuth 2.1 Roles]: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#name-roles
[Understanding Authorization in MCP]: https://modelcontextprotocol.io/docs/tutorials/security/authorization
