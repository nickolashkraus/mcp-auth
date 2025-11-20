locals {
  api_gateway_openapi = templatefile("${path.module}/openapi.yaml", {
    cloud_run_uri = google_cloud_run_v2_service.app.uri
  })
}

resource "google_api_gateway_api" "api" {
  provider = google-beta
  api_id   = "mcp-auth-api"
}

resource "google_api_gateway_api_config" "config" {
  provider      = google-beta
  api           = google_api_gateway_api.api.api_id
  api_config_id = "mcp-auth-api-config"

  openapi_documents {
    document {
      path     = "spec.yaml"
      contents = base64encode(local.api_gateway_openapi)
    }
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "google_api_gateway_gateway" "gateway" {
  provider   = google-beta
  api_config = google_api_gateway_api_config.config.id
  gateway_id = "mcp-auth-api-gateway"
}
