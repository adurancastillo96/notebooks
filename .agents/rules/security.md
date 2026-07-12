# Security Rules

Mandatory security rules for GCP credentials and secret handling in workshop notebooks.

## Credential Handling (CRITICAL)
- **NEVER** write or commit GCP service account keys, API keys, passwords, or personal credentials inside notebook files.
- The `gcloud auth login` and `gcloud auth application-default` authentication cells in the "Before you begin" section must be commented out by default. When the notebook runs in Workbench, it uses the Workbench instance service account automatically without needing explicit login cells active.
- Explain the Workbench authentication workflow in markdown cells so users understand how billing and identities are resolved.

## Project & Resource Configuration
- Always use parameterized variables (`GOOGLE_CLOUD_PROJECT = "[your-google-cloud-project]"  # @param {type:"string"}`) for GCP projects.
- Always parameterize `GOOGLE_CLOUD_LOCATION = "us-central1"  # @param {type:"string"}` and `BUCKET_URI = f"gs://your-bucket-name-{GOOGLE_CLOUD_PROJECT}-unique"  # @param {type:"string"}`.
- Use unique suffixes for resource names (endpoints, models, buckets) by appending the project ID or google-cloud-location to avoid naming collisions and resource leaks.
- Ensure that the Cleaning up section has comprehensive resource deletion logic to prevent users from incurring unexpected GCP costs.

## CI/CD and Secrets
- GitHub Actions must never run notebook cells (no GCP authentication inside CI).
- Do not commit `.env` or configurations with valid GCP project details.
- Flag any security deviations or credential exposure as **Critical** blocking issues during reviews.
