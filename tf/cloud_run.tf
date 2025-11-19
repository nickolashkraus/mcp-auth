resource "google_cloud_run_v2_service" "app" {
  name     = "mcp-auth"
  location = var.region

  template {
    containers {
      image = var.container_image

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }

  # NOTE: To only allow internal traffic, set to `INGRESS_TRAFFIC_INTERNAL_ONLY`.
  ingress = "INGRESS_TRAFFIC_ALL"

  labels = {
    managed-by = "terraform"
  }
}
