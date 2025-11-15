# Handle Resource Indicators Provided by ChatGPT

## Overview

ChatGPT appends the identity of the protected resource(s) (e.g., MCP server) to requests to the authorization server, specifically the authorization and token requests.

**NOTE**: MCP clients **MUST** implement Resource Indicators for OAuth 2.0 as defined in [RFC 8707][RFC 8707] to explicitly specify the target resource for which the token is being requested.

**Example**

```
&resource=https%3A%2F%2Fmcp.example.com
```

**NOTE**: MCP servers **MUST** validate that tokens presented to them were specifically issued for their use. Therefore, any access token issued by the authorization server must include the resource indicator in its claims (`aud`).

## Acceptance Criteria

* The authorization server should be configured to copy the resource indicator into the access token (commonly the `aud` claim), so the MCP server can verify the token was minted for it and nobody else.
* If a token arrives without the expected audience or scopes, reject it and rely on the `WWW-Authenticate` challenge to prompt ChatGPT to re-authorize with the correct parameters.

## Resources

* [2.5.1 Resource Parameter Implementation](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#resource-parameter-implementation)
* [Custom auth with OAuth 2.1](https://developers.openai.com/apps-sdk/build/auth#custom-auth-with-oauth-21)

[RFC 8707]: https://www.rfc-editor.org/rfc/rfc8707.html
