from kubernetes import client, config

# Load Kubernetes configuration (you should have a valid kubeconfig)
config.load_kube_config()

# Create a Kubernetes API client for Pods and Metrics
api = client.CoreV1Api()
metrics_api = client.CustomObjectsApi()

# Define the namespace
namespace = "default"

# List all pods in the namespace
try:
    pod_list = api.list_namespaced_pod(namespace=namespace)
except Exception as e:
    print(f"Error listing pods in namespace {namespace}: {e}")
    exit(1)

# Display resource usage for each pod
for pod in pod_list.items:
    pod_name = pod.metadata.name

    # Fetch resource metrics for the pod
    try:
        metrics = metrics_api.get_namespaced_pod_metrics(name=pod_name, namespace=namespace)
        for container_metric in metrics.containers:
            container_name = container_metric.name
            cpu_usage = container_metric.usage["cpu"]
            memory_usage = container_metric.usage["memory"]

            print(f"Pod: {pod_name}")
            print(f"Container: {container_name}")
            print(f"CPU Usage: {cpu_usage}")
            print(f"Memory Usage: {memory_usage}")
            print("---")
    except Exception as e:
        print(f"Error fetching metrics for pod {pod_name}: {e}")

    print("\n" + "=" * 40 + "\n")  # Separation between pods
