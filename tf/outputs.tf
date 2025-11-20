output "cloud_run_uri" {
  description = "Canonical URL for the Cloud Run service"
  value       = google_cloud_run_v2_service.app.uri
}

output "api_gateway_default_hostname" {
  description = "Default API Gateway hostname"
  value       = google_api_gateway_gateway.gateway.default_hostname
}
