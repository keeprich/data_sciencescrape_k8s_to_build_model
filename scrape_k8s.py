import os
import csv
from kubernetes import client, config

# Load Kubernetes configuration (you should have a valid kubeconfig)
config.load_kube_config()

# Define the namespace
namespace = "your-namespace"

# Create a Kubernetes API client
api = client.CoreV1Api()

# List all pods in the namespace
try:
    pod_list = api.list_namespaced_pod(namespace=namespace)
except Exception as e:
    print(f"Error listing pods in namespace {namespace}: {e}")
    exit(1)

# Define the path to save the CSV file
output_dir = "/path/to/output/dir"
csv_file_name = "logs.csv"

# Create a CSV file and save the logs for each pod
with open(os.path.join(output_dir, csv_file_name), "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Pod Name", "Log Content"])  # Write header row

    for pod in pod_list.items:
        pod_name = pod.metadata.name
        try:
            logs = api.read_namespaced_pod_log(name=pod_name, namespace=namespace)
            csv_writer.writerow([pod_name, logs])
        except Exception as e:
            print(f"Error reading logs from pod {pod_name}: {e}")

print(f"Logs from all pods in namespace {namespace} saved in {os.path.join(output_dir, csv_file_name)}")
