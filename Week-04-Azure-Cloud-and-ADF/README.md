# Week 4: Azure Cloud Fundamentals and Data Pipeline Implementation using Azure Data Factory (ADF)

## 📌 Project Overview

The objective of this week's assignment was to understand Azure cloud fundamentals and build an end-to-end data pipeline using Azure Storage Account and Azure Data Factory (ADF).

The project demonstrates how Azure Data Factory can securely connect to Azure Blob Storage, validate source files using the **Get Metadata** activity, and copy data from a source blob to a destination blob using the **Copy Data** activity.

---

# 🏗️ Architecture

```text
Sample - Superstore.csv
         │
         ▼
Azure Blob Storage (Source)
         │
         ▼
Azure Data Factory (ADF)
         │
 ┌───────┴────────┐
 │                │
 ▼                ▼
Get Metadata   Copy Data
 │                │
 └───────┬────────┘
         │
         ▼
Copied-Superstore.csv
Azure Blob Storage (Destination)
```

---

# ☁️ Azure Services Used

- Azure Resource Group
- Azure Storage Account
- Azure Blob Container
- Azure Data Factory (V2)
- Linked Service
- Source & Destination Datasets
- Get Metadata Activity
- Copy Data Activity
- Azure IAM (RBAC)

---

# 🚀 Implementation Steps

## Step 1: Resource Group

A Resource Group was created to organize all Azure resources used in this project.

- **Resource Group:** `celebal-rg`
- **Region:** Central India

![Resource Group](./screenshots/01-resource-group.png)

---

## Step 2: Storage Account & Blob Container

An Azure Storage Account was created to store the source dataset.

- **Storage Account:** `celebalstorage82715`
- **Container:** `superstore-data`
- **Dataset:** `Sample - Superstore.csv`

### Storage Account

![Storage Account](./screenshots/02-storage-account.png)

### Blob Container

![Blob Container](./screenshots/03-blob-container.png)

---

## Step 3: Azure Data Factory

An Azure Data Factory instance was created to orchestrate the data movement process.

- **ADF Name:** `celebal-adf82715`

### Azure Data Factory

![ADF Overview](./screenshots/04-adf-overview.png)

### ADF Studio

![ADF Studio](./screenshots/05-adf-studio.png)

---

## Step 4: Linked Service & Datasets

A Linked Service was configured to connect Azure Data Factory with Azure Blob Storage.

Two datasets were created:

- **DS_Source**
- **DS_Destination**

### Linked Service

![Linked Service](./screenshots/06-linked-service.png)

### Datasets

![Datasets](./screenshots/07-datasets.png)

---

## Step 5: Get Metadata Activity

The **Get Metadata** activity was configured to validate the source file before copying.

The following metadata fields were retrieved:

- Exists
- Size
- Last Modified

![Get Metadata](./screenshots/08-get-metadata.png)

---

## Step 6: Pipeline Development

A pipeline was developed using two activities:

- Get Metadata
- Copy Data

Pipeline Flow:

```text
Get Metadata
      │
      ▼
Copy Data
```

![Pipeline Design](./screenshots/09-pipeline-design.png)

---

## Step 7: Pipeline Execution

The pipeline was executed successfully using the **Debug** option in Azure Data Factory.

Pipeline Status:

- **Succeeded**

![Pipeline Success](./screenshots/10-pipeline-success.png)

---

## Step 8: Output Verification

After successful execution, the destination file was created in Azure Blob Storage.

![Output Blob](./screenshots/11-output-blob.png)

---

## Step 9: Identity and Access Management (IAM)

Azure Role-Based Access Control (RBAC) was configured to allow Azure Data Factory to access the Storage Account.

Assigned Roles:

- Reader
- Storage Blob Data Contributor

![IAM Roles](./screenshots/12-iam-roles.png)

---

# 📊 Project Outcome

Successfully implemented an end-to-end Azure data pipeline that:

- Created Azure cloud resources.
- Stored data in Azure Blob Storage.
- Connected Azure Data Factory with Blob Storage.
- Retrieved file metadata.
- Copied data from source to destination.
- Executed and monitored the pipeline successfully.
- Configured IAM roles for secure access.

---

# 📚 Key Learnings

- Understanding Azure Resource Groups and Storage Accounts.
- Working with Azure Blob Storage.
- Creating Linked Services and Datasets.
- Building pipelines using Azure Data Factory.
- Using Get Metadata and Copy Data activities.
- Monitoring pipeline execution.
- Implementing secure access using Azure IAM.

---

## 📂 Repository Structure

```text
Week-04-Azure-Cloud-and-ADF/
│
├── README.md
└── screenshots/
    ├── 01-resource-group.png
    ├── 02-storage-account.png
    ├── 03-blob-container.png
    ├── 04-adf-overview.png
    ├── 05-adf-studio.png
    ├── 06-linked-service.png
    ├── 07-datasets.png
    ├── 08-get-metadata.png
    ├── 09-pipeline-design.png
    ├── 10-pipeline-success.png
    ├── 11-output-blob.png
    └── 12-iam-roles.png
```

---

## ✅ Technologies Used

- Microsoft Azure
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory (ADF)
- Azure IAM (RBAC)