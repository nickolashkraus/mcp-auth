# Implement UserInfo Endpoint in Authorization Server (`/userinfo`)

## Overview

The `/userinfo` endpoint is defined in the [OpenID Connect Core][OpenID Connect Core] specification. It returns the claims for the authenticated user when provided an access token. The `/userinfo` endpoint is discovered via the `userinfo_endpoint` field in the Authorization Server Metadata (i.e., `/.well-known/openid-configuration`).

**NOTE**:
- The `/userinfo` endpoint MUST utilize TLS.
- The `/userinfo` endpoint MUST support the use of the HTTP `GET` and HTTP `POST` methods.
- The `/userinfo` endpoint MUST accept an access tokens as a bearer token.
- The `/userinfo` endpoint SHOULD support the use of Cross-Origin Resource Sharing (CORS).

## Resources

* [OpenID Connect Section 5.3 — UserInfo Endpoint][OpenID Connect Core Section 5.3]

[OpenID Connect Core]: https://openid.net/specs/openid-connect-core-1_0.html
[OpenID Connect Core Section 5.3]: https://openid.net/specs/openid-connect-core-1_0.html#UserInfo
