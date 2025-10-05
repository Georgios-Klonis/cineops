resource "google_project" "this" {
  project_id      = var.project_id
  name            = var.project_name
  folder_id       = var.folder_id         # (optional)
  org_id          = var.org_id            # (optional)
  billing_account = var.billing_account   
}

resource "google_project_service" "enabled_apis" {
  for_each           = toset(var.enabled_apis)
  project            = google_project.this.project_id
  service            = each.value
  disable_on_destroy = false
}
