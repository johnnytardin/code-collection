# delete os pods por status em todos os ns
status_to_delete="CrashLoopBackOff|Error"

for ns in $(kubectl get ns -oname | awk -F "/" '{print $2}'); do
  for pod in $(kubectl get po --field-selector=status.phase=Running -n $ns -o wide | egrep $status_to_delete | awk -F " " '{print $1}'); do
    kubectl delete pod $pod -n $ns
  done;
done