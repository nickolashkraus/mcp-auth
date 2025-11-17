# Implement Authorization Endpoint in Authorization Server (`/authorize`)

## Overview

The authorization endpoint (`/authorize`) handles the authorization request in the OAuth 2.1 authentication flow.

After ChatGPT registers (`/register`) itself with the authorization server via Dynamic Client Registration (DCR), if the user invokes a tool that makes a request to a protected MCP server, the OAuth 2.1 flow is initiated. This begins with user authorization, in which the client makes a `GET` request to the authorization server's authorization endpoint (`/authorize`). Required information is added to the request's URL parameters (e.g., `client_id`, `code_challenge`, `code_challenge_method`, `resource`). A full list of the request parameters can be found below.

It should be noted that the `/authorize` endpoint does not actually authorize the user; it is simply an endpoint that facilitates the authorization step by performing request verification and returning the login prompt. Actual authorization is done using the authorization callback endpoint (`/authorize/callback`).

**NOTE**: Additionally, the authorization endpoint is responsible for handling the authorization code flow with PKCE by passing the `code_challenge` to the user via an HTML form and subsequently to the authorization request callback endpoint.

**A note on redirection...**
Redirection (via `redirect_uri`) in the OAuth flow is a little confusing. Recall that the OAuth authorization flow consists of a user, OAuth client, and authorization server. When the OAuth client initiates the authorization request, it makes a call to the authorization server's authorization endpoint (`/authorize`). This endpoint is responsible for returning the login page to the user. However, since the OAuth client needs to be *read-in* to the authorization flow without handling the user's credentials, the authorization server *redirects* the request from the user's browser back to the OAuth client after successful login. This is a key aspect of OAuth: a user authorizes with an entity (authorization server) that can in turn delegate authorization to another entity (OAuth client) without that entity (OAuth client) knowing the credentials of the user.

**Authorization Request**
* **URL**: The authorization endpoint is responsible for authorizing the user (e.g., via a login page). The URL of the endpoint is published to the authorization server's Authorization Server Metadata using the `authorization_endpoint` field. 

**Parameters**
* `client_id`: Unique identifier for the client. The client ID is created during registration (DCR).
* `code_challenge`[^1]: SHA-256 hash of the client's `code_verifier`. Used for authorization code flow with PKCE.
* `code_challenge_method`: Hashing function for client's `code_verifier`. Default: `S256`. **NOTE**: `S256` is required by ChatGPT.
* `redirect_uri`: URI to redirect the user back to the client (ChatGPT). `USER → AS → USER → Client`.
* `resource`: Target resource (MCP server) the client is requesting access to. See [RFC 8707][RFC 8707].
* `response_type`: Specifies the type of credential the client wants to receive back from the authorization server. Default: `code`.
* `scope`: Permissions/access the client is requesting from the resource owner. This is shown to the user on the consent screen.
* `state`: Security mechanism to prevent CSRF attacks and maintain client state. Ensures the authorization response matches the original request. The `state` originates from the client and can be checked in the authorization request callback endpoint. This should be returned back to the client, since the client verifies the returned state matches what it sent.

**Authorization Response**
Returns HTML with a form element for user log in.

**Form Element**
```html
<form method="POST" action="/authorize/callback">
  <!-- Hidden inputs. -->
  <input type="hidden" name="client_id" value="..."/>
  <input type="hidden" name="code_challenge" value="..."/>
  <input type="hidden" name="code_challenge_method" value="..."/>
  <input type="hidden" name="redirect_uri" value="..."/>
  <input type="hidden" name="resource" value="..."/>
  <input type="hidden" name="response_type" value="...">
  <input type="hidden" name="scope" value="..."/>
  <input type="hidden" name="state" value="..."/>
  <!-- User inputs. -->
  <input type="email" name="email" placeholder="Email" required/>
  <input type="password" name="password" placeholder="Password" required/>
  <button type="submit">Log in</button>
</form>
```

**NOTE**: The form element makes a `POST` request to the authorization server's authorization request callback endpoint (`/authorize/callback`).

## Acceptance Criteria
* The endpoint should return HTML with an HTML form element that allows the user to log in. See above form element.
* The HTML form element must contain the following inputs:
    * **Hidden**
        * `client_id`
        * `code_challenge`
        * `code_challenge_method`
        * `redirect_uri`
        * `resource`
        * `response_type`
        * `scope`
        * `state`
    * **User**
        * `email`
        * `password`
* The HTML form element makes a `POST` request to the authorization server's authorization request callback endpoint (`/authorize/callback`).
* The endpoint should complete the following validation:
    * Validate client ID (`client_id`).
    * Validate code challenge and code challenge method (`code_challenge` and `code_challenge_method`).
    * Validate redirect URI (`redirect_uri`).
    * Validate resource (`resource`).
    * Validate state (`state`).
* The endpoint should return a `400` if any validation fails. See the [Error Handling][Error Handling] section of the MCP authorization spec.

[^1]: MCP clients and authorization servers create a secret verifier-challenge pair, ensuring that only the original requester can exchange an authorization code for tokens. See PKCE.

[RFC 8707]: https://www.rfc-editor.org/rfc/rfc8707.html
[Error Handling]: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#error-handling
