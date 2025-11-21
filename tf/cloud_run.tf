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

  # Allow internal traffic and traffic from a Google Cloud Load Balancer.
  ingress = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  labels = {
    managed-by = "terraform"
  }
}

resource "google_cloud_run_v2_service_iam_binding" "app" {
  name = google_cloud_run_v2_service.app.name
  role = "roles/run.invoker"

  members = ["allUsers"]
  # To only allow requests from the API Gateway, uncomment the following and
  # set "ingress" to INGRESS_TRAFFIC_ALL.
  # members = [
  #   "serviceAccount:service-${data.google_project.project.number}@gcp-sa-apigateway.iam.gserviceaccount.com",
  # ]
}
