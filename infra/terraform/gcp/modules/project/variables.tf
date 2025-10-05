variable "project_id" {
  description = "Unique project ID (must be globally unique)."
  type        = string
}

variable "project_name" {
  description = "Display name for the project."
  type        = string
}

variable "folder_id" {
  description = "GCP folder ID (optional) under which the project will live."
  type        = string
  default     = null
}

variable "org_id" {
  description = "GCP organization ID (optional) under which the project will live."
  type        = string
  default     = null
}

variable "billing_account" {
  description = "Billing account ID to attach to the project."
  type        = string
}

variable "enabled_apis" {
  description = "List of APIs/services to enable for the project."
  type        = list(string)
  default     = []
}
