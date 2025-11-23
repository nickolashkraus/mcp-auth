terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.12.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 7.12.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# Uncomment to retrieve information about the current Google Cloud project.
# data "google_project" "project" {}
