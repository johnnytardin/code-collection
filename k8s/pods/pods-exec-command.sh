# executa comandos em todos os pods
for ns in $(kubectl get ns -oname | awk -F "/" '{print $2}'); do
  for pod in $(kubectl get po --field-selector=status.phase=Running -n $ns -oname | awk -F "/" '{print $2}'); do
    echo $pod, $ns  
    kubectl exec $pod -n $ns -- sh -c "echo $pod; find / -name *log4j* | grep -v cve-2021" foo; 
  done; 
done
