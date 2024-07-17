kubectl apply -f cluster-role-binding-admin.yaml
kubectl create token admin
kubectl describe secret admin

kubectl get secret -n kube-system admin -o=jsonpath="{.data.token}" | base64 -d