"""Metadata endpoints.

Defines the metadata endpoints specified in the following:
  * OAuth 2.0 Protected Resource Metadata (RFC 9728)
  * OAuth 2.0 Authorization Server Metadata (RFC 8414)

See:
  * https://datatracker.ietf.org/doc/html/rfc9728
  * https://datatracker.ietf.org/doc/html/rfc8414
"""

import http

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.core import config
from app.schemas import metadata as metadata_schemas

router = APIRouter(tags=["metadata"])

PROTECTED_RESOURCE_METADATA_URI = "/.well-known/oauth-protected-resource"
AUTHORIZATION_SERVER_METADATA_URI = "/.well-known/oauth-authorization-server"


@router.options(PROTECTED_RESOURCE_METADATA_URI, include_in_schema=False)
async def protected_resource_metadata_options() -> Response:
    """Handle OPTIONS for Protected Resource Metadata endpoint."""
    return Response(
        status_code=http.HTTPStatus.NO_CONTENT,
        headers={
            "Allow": ", ".join(
                method.value
                for method in (http.HTTPMethod.GET, http.HTTPMethod.OPTIONS)
            ),
        },
    )


@router.get(
    PROTECTED_RESOURCE_METADATA_URI,
    response_model=metadata_schemas.ProtectedResourceMetadata,
)
async def protected_resource_metadata_get(
    settings: config.Settings = Depends(config.get_settings),
) -> metadata_schemas.ProtectedResourceMetadata:
    """Returns the OAuth 2.0 Protected Resource Metadata (RFC 9728).

    See: https://datatracker.ietf.org/doc/html/rfc9728
    """
    return metadata_schemas.ProtectedResourceMetadata(
        resource=settings.protected_resource_metadata.resource,
        authorization_servers=settings.protected_resource_metadata.authorization_servers,
        scopes_supported=settings.protected_resource_metadata.scopes_supported,
        bearer_methods_supported=settings.protected_resource_metadata.bearer_methods_supported,
        resource_signing_alg_values_supported=settings.protected_resource_metadata.resource_signing_alg_values_supported,
        resource_name=settings.protected_resource_metadata.resource_name,
        resource_documentation=settings.protected_resource_metadata.resource_documentation,
    )


@router.get(
    AUTHORIZATION_SERVER_METADATA_URI,
    response_model=metadata_schemas.AuthorizationServerMetadata,
)
async def authorization_server_metadata() -> (
    metadata_schemas.AuthorizationServerMetadata
):
    """Returns the OAuth 2.0 Authorization Server Metadata (RFC 8414).

    See: https://datatracker.ietf.org/doc/html/rfc8414
    """
    return metadata_schemas.AuthorizationServerMetadata()
