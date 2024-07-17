# # Download and extract Vertical Pod Autoscaler
wget https://github.com/kubernetes/autoscaler/archive/refs/tags/vertical-pod-autoscaler-0.11.0.tar.gz -P /tmp/
tar -xvzf /tmp/vertical-pod-autoscaler-0.11.0.tar.gz -C /tmp/
/tmp/autoscaler-vertical-pod-autoscaler-0.11.0/vertical-pod-autoscaler/hack/vpa-up.sh

# # Apply node selector to VPA components
kubectl patch deployments -n kube-system vpa-admission-controller -p '{"spec": {"template": {"spec": {"nodeSelector": {"workload": "management"}}}}}'
kubectl patch deployments -n kube-system vpa-recommender -p '{"spec": {"template": {"spec": {"nodeSelector": {"workload": "management"}}}}}'
kubectl patch deployments -n kube-system vpa-updater  -p '{"spec": {"template": {"spec": {"nodeSelector": {"workload": "management"}}}}}'

# Configure VPA Recommender
kubectl patch deployments -n kube-system vpa-recommender -p '{"spec": {
    "template": {
        "spec": {
            "containers": [
                {
                    "name": "recommender",
                    "args": [
                        "--recommendation-margin-fraction=0.35",
                        "--pod-recommendation-min-cpu-millicores=50",
                        "--pod-recommendation-min-memory-mb=32",
                        "--storage=prometheus",
                        "--prometheus-address=http://metricsplat.local:9011/api/prom",
                        "--pod-namespace-label=namespace",
                        "--pod-name-label=pod",
                        "--container-namespace-label=namespace",
                        "--container-pod-name-label=pod",
                        "--container-name-label=name",
                        "--prometheus-query-timeout=15m",
                        "--history-resolution=8h",
                        "--history-length=5d",
                        "--memory-saver=true",
                        "-v=1"
                    ],
                    "resources": {
                        "limits": {
                            "cpu": "1500m",
                            "memory": "18000Mi"
                        },
                        "requests": {
                            "cpu": "500m",
                            "memory": "12000Mi"
                        }
                    }
                }
            ]
        }
    }
}}'

# VPA Updater
kubectl patch deployments -n kube-system vpa-updater -p '{"spec": {
    "template": {
        "spec": {
            "containers": [
                {
                    "name": "updater",
                    "args": [
                        "--min-replicas=1",
                        "-v=1"
                    ]
                }
            ]
        }
    }
}}'

# Apply node selector and set replicas for CoreDNS
kubectl patch deployments -n kube-system coredns -p '{"spec": {
    "template": {
        "spec": {
            "nodeSelector": {
                "workload": "management"
            }
        }
    }
}}'
kubectl patch deployments -n kube-system coredns -p '{"spec": {"replicas": 5}}'
