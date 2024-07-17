# delete todos os pods
for ns in $(kubectl get ns -oname | awk -F "/" '{print $2}'); do
  for pod in $(kubectl get po -n $ns -o wide | egrep -v (kube-system|linkerd) | awk -F " " '{print $1}'); do
    kubectl delete pod $pod -n $ns
  done;
done