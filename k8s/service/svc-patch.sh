for namespace in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
  echo "Namespace: $namespace"
  kubectl get services -n $namespace
done
