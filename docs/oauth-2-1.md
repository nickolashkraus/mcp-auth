# OAuth 2.1

The OAuth 2.1 implementation for the OpenAI Apps SDK has the following
features:
* OAuth 2.1 authentication flow that conforms to the [MCP authorization spec][MCP authorization spec].
* Client registration using Dynamic Client Registration (DCR) (required by OpenAI)
* Authorization code protection using Proof Key for Code Exchange (PKCE) (required by OpenAI)

## Authorization Flow

See [authorization-flow.md](docs/authorization-flow.md).

## Dynamic Client Registration (DCR)

See [dynamic-client-registration.md](docs/dynamic-client-registration.md).

## Proof Key for Code Exchange (PKCE)

See [proof-key-for-code-exchange.md](docs/proof-key-for-code-exchange.md).

[MCP authorization spec]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
