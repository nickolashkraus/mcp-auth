output "cloud_run_uri" {
  description = "Canonical URL for the Cloud Run service"
  value       = google_cloud_run_v2_service.app.uri
}
