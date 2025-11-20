"""Protected Resource Metadata model as defined in RFC 9728.

See: https://datatracker.ietf.org/doc/html/rfc9728
"""

from pydantic import BaseModel, Field, HttpUrl


class ProtectedResourceMetadata(BaseModel):
    """OAuth 2.0 Protected Resource Metadata (RFC 9728).

    This model represents the metadata for a protected resource as specified
    in RFC 9728 Section 2 (Protected Resource Metadata). It contains only the
    metadata necessary to facilitate the MCP authorization spec.

    See: https://datatracker.ietf.org/doc/html/rfc9728#name-protected-resource-metadata
    """

    resource: HttpUrl = Field(
        ...,
        description=(
            "The protected resource's resource identifier, as defined in "
            "Section 1.2 of RFC 9728."
        ),
    )

    authorization_servers: list[str] | None = Field(
        default=None,
        description=(
            "List of OAuth authorization server issuer identifiers, as defined "
            "in RFC 8414, for authorization servers that can be used with this "
            "protected resource."
        ),
    )

    scopes_supported: list[str] | None = Field(
        default=None,
        description=(
            "List of scope values, as defined in OAuth 2.0 [RFC 6749], that are "
            "used in authorization requests to request access to this protected "
            "resource."
        ),
    )

    bearer_methods_supported: list[str] | None = Field(
        default=["header"],
        description=(
            "List of the supported methods of sending an OAuth 2.0 bearer token "
            "[RFC 6750] to the protected resource. Defined values are "
            "['header', 'body', 'query'], corresponding to Sections 2.1, 2.2, "
            "and 2.3 of [RFC 6750]."
        ),
    )

    resource_signing_alg_values_supported: list[str] | None = Field(
        default=["RS256"],
        description=(
            "JSON array containing a list of the JWS [JWS] signing algorithms "
            "(alg values) [JWA] supported by the protected resource for signing "
            "resource responses."
        ),
    )

    resource_name: str | None = Field(
        default=None,
        description=(
            "Human-readable name of the protected resource intended for display "
            "to the end user."
        ),
    )

    resource_documentation: HttpUrl | None = Field(
        default=None,
        description=(
            "URL of a page containing human-readable information that "
            "developers might want or need to know when using the protected "
            "resource."
        ),
    )


class AuthorizationServerMetadata(BaseModel):
    """OAuth 2.0 Authorization Server Metadata (RFC 8414)."""

    pass
