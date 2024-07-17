# deleta pods por idade
for ns in $(kubectl get ns -oname | awk -F "/" '{print $2}'); do
  kubectl get pods -n $ns -l type=webapp -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{"\n"}}{{end}}' | awk '$2 <= "'$(date -d'now-7 hours' -Ins --utc | sed 's/+0000/Z/')'" { print $1 }' | xargs --no-run-if-empty kubectl delete pod -n $ns
done


