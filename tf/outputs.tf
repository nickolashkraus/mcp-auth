output "cloud_run_uri" {
  description = "Canonical URL for the Cloud Run service"
  value       = google_cloud_run_v2_service.app.uri
}

output "api_gateway_default_hostname" {
  description = "Default API Gateway hostname"
  value       = google_api_gateway_gateway.gateway.default_hostname
}

output "load_balancer_ip" {
  description = "Global IP address of the external Application Load Balancer (ALB)"
  value       = google_compute_global_address.alb_ip.address
}
