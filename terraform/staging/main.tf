terraform {
  required_version = "1.5.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
  backend "gcs" {
    bucket      = "la-famiglia-jst2324-tf-state"
    prefix      = "terraform/state/staging/mining/affinity"
    credentials = "../.secrets/la-famiglia-parma-ai.json"
  }
}

locals {
  project = "la-famiglia-parma-ai"
  region  = "europe-west1"
}

provider "google" {
  credentials = file("../.secrets/la-famiglia-parma-ai.json")
  project     = local.project
  region      = local.region
}

module "main" {
  source           = "../module"
  env              = "staging"
  project          = local.project
  region           = local.region
  AFFINITY_API_KEY = var.AFFINITY_API_KEY
  AFFINITY_BASE_URL = var.AFFINITY_BASE_URL
  ANALYTICS_BASE_URL = var.ANALYTICS_BASE_URL

  PARMA_SHARED_SECRET_KEY = var.PARMA_SHARED_SECRET_KEY
}
