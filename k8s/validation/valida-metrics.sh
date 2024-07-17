# metrics-server
kubectl describe apiservice v1beta1.metrics.k8s.io
kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes


export ENDPOINT="https://cluster.gr7.us-east-1.eks.amazonaws.com"
export TOKEN=$(kubectl get secret -n kube-system admin -o=jsonpath="{.data.token}" | base64 -d)
curl -H "Authorization: Bearer $TOKEN" $ENDPOINT/api/v1/pods -k
curl -H "Authorization: Bearer $TOKEN" $ENDPOINT/apis/metrics.k8s.io/v1beta1/nodes -k