variable "credentials_file" {
  description = "Path to the service account JSON used by Terraform (leave empty to use ADC)."
  type        = string
  default     = ""
}

variable "project_id" {
  description = "Globally unique project ID for the dev environment."
  type        = string
}

variable "project_name" {
  description = "Display name for the dev project."
  type        = string
}

variable "org_id" {
  description = "Optional organization ID to own the project."
  type        = string
  default     = null
}

variable "folder_id" {
  description = "Optional folder ID where the project should live."
  type        = string
  default     = null
}

variable "billing_account" {
  description = "Billing account ID to associate with the project."
  type        = string
}

variable "enabled_apis" {
  description = "List of APIs to enable for the project (e.g. serviceusage.googleapis.com)."
  type        = list(string)
  default     = []
}
