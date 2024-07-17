#! /bin/bash

K8S_COMPONENTS=("deployment")
KUBECTL_PARAMS=("-o=custom-columns=NAME:.metadata.name --no-headers=true")

kubernetes_deployment () {
    echo "Checking deployment"
    namespace=$1

    if [ -z ${namespace} ]; then
        namespaces=$(kubectl ${KUBECTL_PARAMS[@]} get namespaces -l alias)
    else
        namespaces=$(kubectl ${KUBECTL_PARAMS[@]} get namespaces $1)
        echo "Check if namespace exist"
    fi

    for namespace in ${namespaces}; do
        for component in ${K8S_COMPONENTS[@]} ; do
            resources=$(kubectl ${KUBECTL_PARAMS[@]} -n ${namespace} get ${component})
            for resource in ${resources}; do
                status=$(kubectl -n ${namespace} get ${component} ${resource} -o json | egrep -i '(1433|191.185.112.172)' | wc -c);
                if [[ "${status}" -gt "0" ]]; then
                    echo -e "DEPLOYMENT::Resource: \033[01;34m${resource}\033[0m"
                fi
            done
        done
    done
}

clusters="arn:aws:eks:us-east-1:xxxxx:cluster/cluster-name"
for cluster in ${clusters}; do
    kubectx ${cluster}
    kubernetes_deployment $1
done
