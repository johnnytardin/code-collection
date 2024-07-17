kubectl get pods --all-namespaces -o=json | jq -r '.items[] | select(.spec.containers[].securityContext.privileged or .spec.securityContext.privileged) | "\(.metadata.namespace)/\(.metadata.name) has privileged container"'