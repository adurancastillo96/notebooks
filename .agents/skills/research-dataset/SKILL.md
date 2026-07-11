---
name: research-dataset
description: >
  Investigates and documents open-access datasets from NASA, ESA, GCP, and other catalogs
  suitable for training and educational purposes.
tools: [Read, Glob, Grep, WebSearch]
---

# Skill: Research Dataset

Search for, evaluate, and select public datasets for a specific workshop notebook topic.

## Steps

1. **Define Criteria**
   - Identify the technical needs of the notebook (e.g., image classification, time series, tabular regression).
   - Establish constraints: must be publicly accessible, open-licensed (CC-BY, Public Domain), and have a manageable file size (< 50MB) for quick downloads during workshops.

2. **Search Catalogs**
   - Search NASA Earthdata, ESA Copernicus Hub, BigQuery public datasets, and general repositories (Kaggle, UCI, etc.).
   - Verify dataset download paths and authentication requirements.

3. **Evaluate Alternatives**
   - Compare at least 2 candidate datasets on size, access complexity, licensing, and pedagogical value.

4. **Document Findings**
   - Write a research report detailing:
     - Dataset name, source, and license.
     - Storage location (e.g., `gs://cloud-samples-data/...` or public HTTP URL).
     - Format (CSV, Parquet, netCDF, GeoTIFF).
     - Sample Python code cells showing how to download and parse the dataset.

5. **Recommend**
   - Recommend the best dataset and write the text blocks to be added to the Dataset subsection of the notebook spec.
