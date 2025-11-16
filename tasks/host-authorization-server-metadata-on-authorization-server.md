# Host Authorization Server Metadata on Authorization Server

## Overview

Once ChatGPT has obtained the Protected Resource Metadata from the MCP server, it retrieves the Authorization Server Metadata ([RFC 8414][RFC 8414]) from the Authorization Server.

This involves defining a metadata endpoint (`/.well-known/openid-configuration`), which returns a JSON document with information needed to interact with the authorization server.

**NOTE**: You may also see `/.well-known/oauth-authorization-server`. OAuth 2.0 is the authorization framework. OpenID Connect is an authentication layer built on top of OAuth 2.0. Since we plan to use the claims on the OIDC token when making calls to the MCP server, we should use OIDC tokens instead of standard OAuth tokens.

**NOTE**: Authorization servers **MUST** provide OAuth 2.0 Authorization Server Metadata ([RFC 8414][RFC 8414]) (or OpenID Provider Metadata).

**Example**

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/oauth2/v1/authorize",
  "token_endpoint": "https://auth.example.com/oauth2/v1/token",
  "registration_endpoint": "https://auth.example.com/oauth2/v1/register",
  "jwks_uri": "https://auth.example.com/oauth2/v1/keys",
  "code_challenge_methods_supported": ["S256"],
  "scopes_supported": ["files:read", "files:write"]
}
```

* `authorization_endpoint`, `token_endpoint`, `jwks_uri` [REQUIRED]: The endpoints used by the client (ChatGPT) to execute the OAuth 2.1 (with PKCE) flow end-to-end.
* `registration_endpoint` [REQUIRED]: Enables dynamic client registration (DCR), so ChatGPT can use a dedicated `client_id` per connector.
* `code_challenge_methods_supported` [REQUIRED]: Must include `S256`, otherwise ChatGPT will refuse to proceed because PKCE appears unsupported.

A full list of available metadata is defined in [RFC 8414][RFC 8414]/[OpenID Connect Discovery][OpenID Connect Discovery]:
- [Authorization Server Metadata][Authorization Server Metadata]
- [OpenID Provider Metadata][OpenID Provider Metadata]

## Acceptance Criteria

* A metadata endpoint is defined in the authorization server ([Function-Health/member-app-middleware][Function-Health/member-app-middleware]), which returns the Authorization Server Metadata.

## Resources

* [2.3 Authorization Server Discovery](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#authorization-server-discovery)
* [Custom auth with OAuth 2.1](https://developers.openai.com/apps-sdk/build/auth#custom-auth-with-oauth-21)

[RFC 8414]: https://datatracker.ietf.org/doc/html/rfc8414
[OpenID Connect Discovery]: https://openid.net/specs/openid-connect-discovery-1_0.html
[Authorization Server Metadata]: https://datatracker.ietf.org/doc/html/rfc8414#section-2
[OpenID Provider Metadata]: https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata
[Function-Health/member-app-middleware]: https://github.com/Function-Health/member-app-middleware
