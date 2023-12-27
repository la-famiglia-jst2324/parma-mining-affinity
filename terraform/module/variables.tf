variable "env" {
  description = "staging or prod environment"
  type        = string
}

variable "project" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
}


variable "AFFINITY_API_KEY" {
  description = "value"
  type        = string
  sensitive   = true
}

variable "AFFINITY_BASE_URL" {
  description = "value"
  type        = string
}

variable "ANALYTICS_BASE_URL" {
  description = "value"
  type        = string
}
