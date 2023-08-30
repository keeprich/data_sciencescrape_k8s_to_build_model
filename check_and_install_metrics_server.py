import subprocess

def check_metrics_server():
    try:
        # Check if Metrics Server pods are running in the kube-system namespace
        result = subprocess.run(['kubectl', 'get', 'pods', '-n', 'kube-system', '-l', 'k8s-app=metrics-server', '--field-selector=status.phase=Running'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print("Metrics Server is already installed and running.")
        else:
            print("Metrics Server is not installed.")
    except Exception as e:
        print(f"Error checking Metrics Server status: {e}")

def install_metrics_server():
    try:
        # Install Metrics Server using kubectl apply
        subprocess.run(['kubectl', 'apply', '-f', 'https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml'], check=True)
        print("Metrics Server has been installed successfully.")
    except Exception as e:
        print(f"Error installing Metrics Server: {e}")

# Check if Metrics Server is installed
check_metrics_server()

# If not installed, install it
install_metrics_server()
