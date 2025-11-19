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

    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }

  }

  # NOTE: To only allow internal traffic, set to `INGRESS_TRAFFIC_INTERNAL_ONLY`.
  ingress = "INGRESS_TRAFFIC_ALL"

  labels = {
    managed-by = "terraform"
  }
}

resource "google_cloud_run_v2_service_iam_binding" "app" {
  name = google_cloud_run_v2_service.app.name
  role = "roles/run.invoker"

  # NOTE: "allUsers" is a special identifier that represents anyone who is on
  # the internet; with or without a Google account.
  members = ["allUsers"]
}
