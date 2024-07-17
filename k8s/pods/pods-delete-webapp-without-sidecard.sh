# delete os pods sem sidecard

for ns in $(kubectl get ns -oname | awk -F "/" '{print $2}'); do
  for pod in $(kubectl get po -l type=webapp --field-selector=status.phase=Running -n $ns -o wide | grep /1 | awk -F " " '{print $1}'); do
    kubectl delete pod $pod -n $ns
    # sleep 5
  done;
done