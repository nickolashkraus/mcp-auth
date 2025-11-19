variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region"
  type        = string
  default     = "us-central1"
}

variable "container_image" {
  description = "Container image for the Cloud Run service"
  type        = string
  default     = "us-central1-docker.pkg.dev/personal-478717/mcp-auth/app:latest"
}
