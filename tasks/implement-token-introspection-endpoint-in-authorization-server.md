# Implement Token Introspection Endpoint in Authorization Server (`/introspect`)

## Overview

The OAuth 2.0 Token Introspection extension ([RFC 7662][RFC 7662]) defines a protocol that returns information about an access token, intended to be used by resource servers or other internal servers.

An alternative to token introspection is to use a structured token format that is recognized by both the authorization server and resource server. The JWT Profile for OAuth 2.0 Access Tokens ([RFC 9068][RFC 9068]) is a recent RFC that describes a standardized format for access tokens using JWTs. This enables a resource server to validate access tokens without a network call, by validating the signature and parsing the claims within the structured token itself.

Since we plan to use OIDC tokens for access tokens, implementing the token introspection endpoint (`/introspect`) is optional. The token can be verified locally by checking its signature, then decoding it to retrieve the claims. Further assertions using the token's claims can then be made in order to validate the token.

## Resources

* [RFC 7662][RFC 7662]
* [18 Token Introspection Endpoint][18 Token Introspection Endpoint]

[RFC 7662]: https://datatracker.ietf.org/doc/html/rfc7662
[RFC 9068]: https://datatracker.ietf.org/doc/html/rfc9068
[18 Token Introspection Endpoint]: https://www.oauth.com/oauth2-servers/token-introspection-endpoint/
