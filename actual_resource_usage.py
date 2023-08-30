from kubernetes import client, config
import datetime

# Load Kubernetes configuration (you should have a valid kubeconfig)
config.load_kube_config()

# Create a Kubernetes API client for Pods and Metrics
api = client.CoreV1Api()
metrics_api = client.CustomObjectsApi()

# Define the namespace
namespace = "your-namespace"

# List all pods in the namespace
try:
    pod_list = api.list_namespaced_pod(namespace=namespace)
except Exception as e:
    print(f"Error listing pods in namespace {namespace}: {e}")
    exit(1)

# Get current time for the timestamp
current_time = datetime.datetime.now()

# Display resource usage for each pod
for pod in pod_list.items:
    pod_name = pod.metadata.name

    # Fetch resource metrics for the pod
    try:
        metrics = metrics_api.get_namespaced_pod_metrics(name=pod_name, namespace=namespace)
        container_metrics = metrics["containers"]

        print(f"Pod: {pod_name}")
        print(f"Timestamp: {current_time}")
        for container_metric in container_metrics:
            container_name = container_metric["name"]
            cpu_usage = container_metric["usage"]["cpu"]
            memory_usage = container_metric["usage"]["memory"]

            print(f"Container: {container_name}")
            print(f"CPU Usage: {cpu_usage}")
            print(f"Memory Usage: {memory_usage}")
            print("---")
    except Exception as e:
        print(f"Error fetching metrics for pod {pod_name}: {e}")

    print("\n" + "=" * 40 + "\n")  # Separation between pods
