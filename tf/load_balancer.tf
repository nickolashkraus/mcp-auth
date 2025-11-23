# Creates an Application Load Balancer (ALB) that proxies traffic from the
# Internet to backend services (Cloud Run) while still restricting network
# ingress.
#
# NOTE: The ALB as a whole is the combination of the forwarding rule, target
# proxy, URL map, and backend services working together.
#
#   1. A client makes a request to a public domain name (ex. mcp.example.com).
#   2. The domain name maps to the IPv4 address of the ALB
#      (mcp.example.com → A/AAAA).
#   3. The ALB routes the request to the appropriate backend service using
#      a URL map.
#   4. A serverless network endpoint group facilitates the connection between
#      the ALB and Cloud Run services.
#
#      Client → DNS → ALB → Backend Service(s) → Serverless NEG(s) → Cloud Run
# 
# This allows Cloud Run services to only be reachable from Cloud Load Balancing
# and other allowed internal Google producer traffic (Cloud Run, Cloud
# Functions, etc.), but not directly from the public internet.
#
# The following associations are used to link Terraform resources:
#
#   1. google_compute_global_address: Defines a global static IPv4 address.
#      This represents the IP address of the ALB and is bound to the global
#      forwarding rule in order to connect a public IP address with the load
#      balancer configuration.
#   2. google_compute_global_forwarding_rule: Routes traffic by IP address,
#      port, and protocol to a target proxy, which together with the URL map
#      and backend services forms the load balancing configuration.
#   3. google_compute_target_http_proxy: Uses the URL map to determine how to
#      route traffic to backend services.
#   4. google_compute_url_map: Matching patterns for URL-based routing of
#      requests to the appropriate backend services.
#   5. google_compute_backend_service: Defines how traffic is distributed to
#      backends (for example, a serverless network endpoint group that targets
#      a Cloud Run service). This backend service is referenced by the URL map
#      and is part of the chain back to the global static IPv4 address.
#   6. google_compute_region_network_endpoint_group: Provides a way for the
#      backend service to reference a serverless endpoint (i.e., Cloud Run).
#      When combined with the "Internal and Cloud Load Balancing" setting for
#      Cloud Run ingress, it allows requests from an external Application Load
#      Balancer to reach the Cloud Run service.
#
#      Forwarding Rule → Target HTTP(S) Proxy → URL Map → Backend Service(s) →
#      Serverless NEG(s) → Cloud Run

# Backend services can be configured dynamically by adding a mapping containing
# a host name and Cloud Run service. Each backend service has an associated
# network endpoint group and routing rules.
locals {
  services = {
    mcp-auth = {
      host              = "mcp-auth.example.com"
      cloud_run_service = google_cloud_run_v2_service.app.name
    }
  }
}

# Allocates a global static IPv4 address. The address is bound to the ALB using
# a global forwarding rule. 
resource "google_compute_global_address" "alb_ip" {
  name = "mcp-auth-alb-ip"
}

# Global forwarding rules route traffic by IP address, port, and protocol to
# a load balancing configuration consisting of a target proxy, URL map, and one
# or more backend services.
#
# See: https://docs.cloud.google.com/load-balancing/docs/https#forwarding-rule
#
# NOTE: To support HTTPS, set port_range to 443, use the
# google_compute_target_https_proxy, resource, and configure TLS certificates.         
resource "google_compute_global_forwarding_rule" "alb" {
  name                  = "mcp-auth-http-forwarding-rule"
  target                = google_compute_target_http_proxy.alb.id
  ip_address            = google_compute_global_address.alb_ip.address
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "80"
  ip_protocol           = "TCP"
}

# A target proxy terminates incoming connections from clients and create new
# connections from the load balancer to the backends.
#
# See: https://docs.cloud.google.com/load-balancing/docs/https#target-proxies
resource "google_compute_target_http_proxy" "alb" {
  name    = "mcp-auth-http-proxy"
  url_map = google_compute_url_map.alb.id
}

# Configures routing for the Application Load Balancer:
#
#   mcp.example.com  → ALB → MCP backend
#   auth.example.com → ALB → Auth backend
#
# The dynamic blocks below can be uncommented to enable this pattern.
#
# This configuration uses host-based routing. When a request arrives at the
# load balancer, the load balancer routes the request to a particular backend
# service using the host_rule and path_matcher arguments.
#
# See: https://cloud.google.com/load-balancing/docs/url-map-concepts
resource "google_compute_url_map" "alb" {
  name = "mcp-auth-url-map"

  # Fallback backend service to use when none of the given rules match.
  default_service = google_compute_backend_service.services["mcp-auth"].id

  # NOTE: Uncomment the following to configure host-based routing for multiple
  # hosts.
  #
  # dynamic "host_rule" {
  #   for_each = local.services
  #   content {
  #     hosts        = [host_rule.value.host]
  #     path_matcher = "${host_rule.key}-matcher"
  #   }
  # }
  #
  # dynamic "path_matcher" {
  #   for_each = local.services
  #   content {
  #     name            = "${path_matcher.key}-matcher"
  #     default_service = google_compute_backend_service.services[path_matcher.key].id
  #   }
  # }
}

# Global external Application Load Balancer. Defines how traffic is distributed
# to backend endpoints (Cloud Run services). For serverless backends, this
# routes traffic through serverless NEGs rather than traditional VM-based
# backends. Different backend services support various backend *types*. For
# a global external Application Load Balancer (designated by the
# EXTERNAL_MANAGED load balancing scheme), all serverless NEGs with one or more
# Cloud Run resources are supported.
#
# See: https://cloud.google.com/load-balancing/docs/backend-service
resource "google_compute_backend_service" "services" {
  for_each = local.services

  name                  = "${each.key}-backend"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  protocol              = "HTTP"
  timeout_sec           = 30

  backend {
    group = google_compute_region_network_endpoint_group.services[each.key].id
  }

  # Configure Cloud Armor policy.
  # security_policy = google_compute_security_policy.armor_policy.id
}

# To enable HTTPS, create a TLS certificate which includes a Subject
# Alternative Name (SAN) for the desired subdomains:
#
#   mcp.example.com  
#   auth.example.com 
#   
# resource "google_compute_managed_ssl_certificate" "tls" {
#   name = "tls-cert"
# 
#   managed {
#     domains = [
#       "mcp.example.com",
#       "auth.example.com"
#     ]
#   }
# }

# Specifies a group of backend endpoints for the Application Load Balancer.
#
# See: https://cloud.google.com/load-balancing/docs/negs/serverless-neg-concepts
resource "google_compute_region_network_endpoint_group" "services" {
  for_each = local.services

  name   = "${each.key}-neg"
  region = var.region

  # For Cloud Run behind an ALB, use a serverless network endpoint group (NEG).
  network_endpoint_type = "SERVERLESS"

  cloud_run {
    service = each.value.cloud_run_service
  }
}
