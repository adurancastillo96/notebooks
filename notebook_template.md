```python
# Antony Duran
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

# [TODO] Add your H1 title heading here

**_NOTE_**: This notebook has been tested in the following environment:

* Python version = 3.10.13

## Overview

{TODO: Include a paragraph or two explaining what this example demonstrates, who should be interested in it, and what you need to know before you get started.}

Learn more about [web-doc-title](linkback-to-webdoc-page). {TODO: if more than one primary feature, add tag/linkback for each one}

### Objective

In this tutorial, you learn how to {TODO: Complete the sentence explaining briefly what you will learn from the notebook, such as
training, hyperparameter tuning, or serving}:

This tutorial uses the following Google Cloud ML services and resources:

- *{TODO: Add high level bullets for the services/resources demonstrated; e.g., Vertex AI Training}*


The steps performed include:

- *{TODO: Add high level bullets for the steps of performed in the notebook}*

### Dataset

{TODO: Include a paragraph with Dataset information and where to obtain it.} 

{TODO: Make sure the dataset is accessible to the public. **Googlers**: Add your dataset to the [public samples bucket](http://goto/cloudsamples#sample-storage-bucket) within gs://cloud-samples-data/vertex-ai, if it doesn't already exist there.}

### Costs 

{TODO: Update the list of billable products that your tutorial uses.}

This tutorial uses billable components of Google Cloud:

* Vertex AI
* {TODO: BigQuery}
* Cloud Storage

{TODO: Include links to pricing documentation for each product you listed above.
 NOTE: If you use BigQuery or Dataflow, you need to add this to the pricing.
}

Learn about [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing),
{ TODO: [BigQuery pricing](https://cloud.google.com/bigquery/pricing), }
and [Cloud Storage pricing](https://cloud.google.com/storage/pricing), 
and use the [Pricing Calculator](https://cloud.google.com/products/calculator/)
to generate a cost estimate based on your projected usage.

## Installation

Install the following packages required to execute this notebook. 

{TODO: Suggest using the latest major GA version of each package; i.e., --upgrade}


```python
! pip3 install --upgrade --quiet google-cloud-aiplatform
```

## Before you begin

### Set up your Google Cloud project

**The following steps are required, regardless of your notebook environment.**

1. [Select or create a Google Cloud project](https://console.cloud.google.com/cloud-resource-manager). When you first create an account, you get a $300 free credit towards your compute/storage costs.

2. [Make sure that billing is enabled for your project](https://cloud.google.com/billing/docs/how-to/modify-project).

3. [Enable the Vertex AI API](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com). {TODO: Update the APIs needed for your tutorial. Edit the API names, and update the link to append the API IDs, separating each one with a comma. For example, container.googleapis.com,cloudbuild.googleapis.com}

4. If you are running this notebook locally, you need to install the [Cloud SDK](https://cloud.google.com/sdk).

#### Set your project ID

**If you don't know your project ID**, try the following:
* Run `gcloud config list`.
* Run `gcloud projects list`.
* See the support page: [Locate the project ID](https://support.google.com/googleapi/answer/7014113)


```python
PROJECT_ID = "[your-project-id]"  # @param {type:"string"}

# Set the project id
! gcloud config set project {PROJECT_ID}
```

#### Region

You can also change the `REGION` variable used by Vertex AI. Learn more about [Vertex AI regions](https://cloud.google.com/vertex-ai/docs/general/locations).


```python
REGION = "us-central1"  # @param {type: "string"}
```

### Authenticate your Google Cloud account

The Cloud SDK, code and other libraries currently run as the service account identity of the Workbench Instance running this notebook.

**- Authenticate the Cloud SDK with your credentials :**


```python
# ! gcloud auth login
```

**- Authenticate code and libraries with your credentials :**


```python
# ! gcloud auth application-default
```

**- Service account or other**
* See how to grant Cloud Storage permissions to your service account at https://cloud.google.com/storage/docs/gsutil/commands/iam#ch-examples.

### Create a Cloud Storage bucket

Create a storage bucket to store intermediate artifacts such as datasets.

- *{Note to notebook author: For any user-provided strings that need to be unique (like bucket names or model ID's), append "-unique" to the end so proper testing can occur}*


```python
BUCKET_URI = f"gs://your-bucket-name-{PROJECT_ID}-unique"  # @param {type:"string"}
```

**Only if your bucket doesn't already exist**: Run the following cell to create your Cloud Storage bucket.


```python
! gsutil mb -l {REGION} -p {PROJECT_ID} {BUCKET_URI}
```

### Import libraries


```python
from google.cloud import aiplatform
```

### Initialize Vertex AI SDK for Python

Initialize the Vertex AI SDK for Python for your project.


```python
aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)
```

## Cleaning up

To clean up all Google Cloud resources used in this project, you can [delete the Google Cloud
project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects) you used for the tutorial.

Otherwise, you can delete the individual resources you created in this tutorial:

{TODO: Include commands to delete individual resources below}


```python
import os

# Delete endpoint resource
# e.g. `endpoint.delete()`

# Delete model resource
# e.g. `model.delete()`

# Delete Cloud Storage objects that were created
delete_bucket = False
if delete_bucket or os.getenv("IS_TESTING"):
    ! gsutil -m rm -r $BUCKET_URI
```
