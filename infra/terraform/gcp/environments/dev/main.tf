provider "google" {
  credentials = var.credentials_file != "" ? file(var.credentials_file) : null
  project     = var.project_id
}

provider "google-beta" {
  credentials = var.credentials_file != "" ? file(var.credentials_file) : null
  project     = var.project_id
}

module "project" {
  source = "../../modules/project"

  project_id       = var.project_id
  project_name     = var.project_name
  org_id           = var.org_id
  folder_id        = var.folder_id
  billing_account  = var.billing_account
  enabled_apis     = var.enabled_apis
}
