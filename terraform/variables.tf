variable "project" {
  description = "Project ID. Set default name in TF_VAR_project"
  type = string
}

variable "region" {
  description = "Region name"
  default     = "europe-central2"
}

variable "location" {
  description = "Project location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "Dataset for payments transaction. Set default name in TF_VAR_bq_dataset_name"
  type = string
}

variable "gcs_bucket_name" {
  description = "Bucket storage for payments transaction. Set default name in TF_VAR_gcs_bucket_name"
  type = string
}
