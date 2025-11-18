"""Metadata endpoints.

Defines the metadata endpoints specified in the following:
  * OAuth 2.0 Protected Resource Metadata (RFC 9728)
  * OAuth 2.0 Authorization Server Metadata (RFC 8414)

See:
  * https://datatracker.ietf.org/doc/html/rfc9728
  * https://datatracker.ietf.org/doc/html/rfc8414
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core import config
from app.schemas import metadata as metadata_schemas

router = APIRouter()

PROTECTED_RESOURCE_METADATA_URI = "/.well-known/oauth-protected-resource"
AUTHORIZATION_SERVER_METADATA_URI = "/.well-known/openid-configuration"


@router.get(PROTECTED_RESOURCE_METADATA_URI)
async def protected_resource_metadata(
    config: config.Settings = Depends(config.get_settings),
):
    """
    MCP servers MUST implement OAuth 2.0 Protected Resource Metadata (RFC9728).
    MCP clients MUST use OAuth 2.0 Protected Resource Metadata for
    authorization server discovery.

    See: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#authorization-server-location
    """
    return JSONResponse(
        metadata_schemas.ProtectedResourceMetadata(
            resource=config.protected_resource_metadata.resource,
            authorization_servers=config.protected_resource_metadata.authorization_servers,
            scopes_supported=config.protected_resource_metadata.scopes_supported,
            bearer_methods_supported=config.protected_resource_metadata.bearer_methods_supported,
            resource_signing_alg_values_supported=config.protected_resource_metadata.resource_signing_alg_values_supported,
            resource_name=config.protected_resource_metadata.resource_name,
            resource_documentation=config.protected_resource_metadata.resource_documentation,
        ).model_dump(mode="json")
    )


@router.get(AUTHORIZATION_SERVER_METADATA_URI)
async def authorization_server_metadata():
    """
    Authorization servers MUST provide OAuth 2.0 Authorization Server Metadata
    (RFC8414). MCP clients MUST use the OAuth 2.0 Authorization Server
    Metadata.

    See: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#server-metadata-discovery
    """
