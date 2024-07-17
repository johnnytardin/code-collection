export ENDPOINT="https://cluster.gr7.us-east-1.eks.amazonaws.com"
export TOKEN=$(kubectl get secret admin -o=jsonpath="{.data.token}" | base64 -d)

curl -H "Authorization: Bearer $TOKEN" $ENDPOINT/api/v1/pods -k
curl -H "Authorization: Bearer $TOKEN" $ENDPOINT/apis/metrics.k8s.io/v1beta1/nodes -k