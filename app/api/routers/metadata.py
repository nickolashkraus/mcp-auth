"""Metadata endpoints.

Defines the metadata endpoints specified in the following:
  * OAuth 2.0 Protected Resource Metadata (RFC 9728)
  * OAuth 2.0 Authorization Server Metadata (RFC 8414)

See:
  * https://datatracker.ietf.org/doc/html/rfc9728
  * https://datatracker.ietf.org/doc/html/rfc8414
"""

from fastapi import APIRouter, Depends

from app.core import config
from app.schemas import metadata as metadata_schemas

router = APIRouter()

PROTECTED_RESOURCE_METADATA_URI = "/.well-known/oauth-protected-resource"
AUTHORIZATION_SERVER_METADATA_URI = "/.well-known/openid-configuration"


@router.get(
    PROTECTED_RESOURCE_METADATA_URI,
    response_model=metadata_schemas.ProtectedResourceMetadata,
)
async def protected_resource_metadata(
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
