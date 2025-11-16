# Implement Authorization Endpoint in Authorization Server (`/authorize`)

## Overview

The authorization endpoint (`/authorize`) handles the authorization request in the OAuth 2.1 authentication flow.

After ChatGPT registers (`/register`) itself with the authorization server via Dynamic Client Registration (DCR), if the user invokes a tool that makes a request to a protected MCP server, the OAuth 2.1 flow is initiated. This begins with user authorization using three values: the authorization URL, `code_challenge` (plus `code_challenge_method`), and `resource`:

* **Authorization URL**: Authorization endpoint responsible for authorizing the user (e.g., login). This URL is published to the authorization server's Authorization Server Metadata using the `authorization_endpoint` field. Additionally, the authorization endpoint is responsible for handling the authorization code flow with PKCE.
* **code_challenge**: MCP clients and authorization servers create a secret verifier-challenge pair, ensuring that only the original requester can exchange an authorization code for tokens.
* **resource**: Target resource for which the token is being requested.

It should be noted that the `/authorize` endpoint does not actually authorize the user; it is simply an endpoint that facilitates the authorization step by performing request verification and returning the login prompt. Actual authorization is done using the authorization callback endpoint (`/authorize/callback`).
