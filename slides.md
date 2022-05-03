# Cloud Native Data Pipelines 

---

## Aims

Showcase Portworx PDS (database-as-a-service on Kubernetes) via some simple cloud native data pipelines

---

## Technology Stack

- Portworx Data Services (underpinned by Portworx Enterprise)

- S3

- Python

- Twitter Tweepy V2 API

- Argo Workflows using the container WorkflowTemplate

- Kubernetes

---

<img src="images/07.png">

---

## Why Use Argo Workflows ?

- Cloud native from day one

- No dependencies on non-Kubernetes objects

- Simple to install and use

- Flexibility: container, resource, script, suspend and DAG templates

- Git / GitHub friendly

--

## Prerequisites

- A twitter bearer token, requires a twitter developer account

- Python 3 for local testing

- Docker for local testing

- An S3 bucket

- s5cmd

- Argo Workflows deployed to a Kubernetes cluster

- The Argo Workflows CLI

- Portworx Data Services 

## Getting Started

1. Deploy either Postgres or Cassandra via Portworx Data Services

2. Build the docker images using the Dockerfiles in the docker_images folder

3. Create a YAML file containing the workflow parameter values

4. Submit the pipeline YAML manifest using the Argo Workflows CLI:

```argo submit <YAML file> -n <Kubernetes namespace> -parameter-file <YAML file>
