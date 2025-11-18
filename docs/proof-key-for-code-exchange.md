# Proof Key for Code Exchange (PKCE)

Proof Key for Code Exchange (PKCE) (pronounced "pixy") is a security extension
for OAuth 2.0 that prevents authorization code interception attacks. It's
especially important for public clients like mobile apps and single-page
applications (SPAs) that can't securely store client secrets.

In traditional OAuth 2.0 authorization code flow, a malicious app could
intercept the authorization code and exchange it for tokens. PKCE prevents this
by cryptographically binding the authorization request to the token request.

PKCE occurs *after* the client has registered with the authorization server
during the steps involved with obtaining the authorization code and access
token.

**NOTE**: PKCE is required for OAuth 2.1 (no longer optional) and recommended
for OAuth 2.0.

1. The client generates a code verifier. This is simply a string of random
   characters from the [RFC 7636][RFC 7636] allowed alphabet (`A-Z`, `a-z`,
   `0-9`, `-._~`) with a length between 43 and 128 characters:

    ```
    code_verifier = RANDOM_STRING(43-128 characters, alphabet="A-Za-z0-9-._~")
    ```

    **NOTE**: The code verifier never leaves the client until token exchange
    (`POST /token`). See [RFC 7636 Section 4.1][RFC 7636 Section 4.1] for
    code verifier constraints.

2. The client generates a code challenge. This is a hash of the code verifier
   encoded using base64url *without* padding:

    ```
    code_challenge = BASE64URL(SHA256(code_verifier))
    ```

    See: [Appendix A. Notes on Implementing Base64url Encoding without
    Padding][Appendix A. Notes on Implementing Base64url Encoding without
    Padding]

3. The client includes the code challenge in the authorization request
   (`GET /authorize`):

   **NOTE**: OpenAI (and ChatGPT acting as the MCP client) only supports the
   `S256` code challenge method. Therefore, the hash of the code verifier must
   use the SHA-256 hash function.

    ```
    GET /authorize?
      response_type=code
      &client_id=CLIENT_ID
      &redirect_uri=REDIRECT_URI
      &code_challenge=CHALLENGE
      &code_challenge_method=S256
    ```

4. The client includes the original code verifier in the token request:

    ```
    POST /token
      grant_type=authorization_code
      &code=AUTH_CODE
      &code_verifier=ORIGINAL_VERIFIER
    ```

    **NOTE**: The code verifier is included in the body of the request, which,
    over HTTPS, is cryptographically secure.

5. The authorization server verifies the token request by recomputing the hash
   of the code verifier. If the hash of the code verifier matches the original
   code challenge, the authorization server issues the access token:

    ```
    BASE64URL(SHA256(code_verifier)) == code_challenge
    ```

## Storage

Since the code challenge needs to be used to verify the token request, it must
be stored temporarily. The most common approach is ephemeral storage using
Redis or Memcached:

```
SET auth:code:HXaz4hNg... '{"code_challenge":"eCe/nK...","client_id":"..."}' EX 600
```

This allows for fast, simple lookups with automatic expiration.

[RFC 7636]: https://datatracker.ietf.org/doc/html/rfc7636
[RFC 7636 Section 4.1]: https://datatracker.ietf.org/doc/html/rfc7636#section-4.1
[Appendix A. Notes on Implementing Base64url Encoding without Padding]: https://datatracker.ietf.org/doc/html/rfc7636#appendix-A
