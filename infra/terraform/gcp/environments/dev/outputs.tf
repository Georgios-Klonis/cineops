output "project_id" {
  description = "ID of the created dev project."
  value       = module.project.project_id
}

output "project_number" {
  description = "Numeric project identifier."
  value       = module.project.project_number
}
