
for ns in $(kubectl get ns -oname | awk -F "/" '{print $2}'); do
  for deploy in $(kubectl get deploy -n $ns -l type=worker| grep -v NAME | awk -F " " '{print $1}'); do
    kubectl get deploy $deploy -n $ns -o yaml > /tmp/deploy/$deploy
  done;
done