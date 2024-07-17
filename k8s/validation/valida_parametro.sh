#! /bin/bash
clear

K8S_COMPONENTS=("deployment")
KUBECTL_PARAMS=("-o=custom-columns=NAME:.metadata.name --no-headers=true")


kubernetes_webapp () {
    echo "Checking webapp"
    namespace=$1

    if [ -z ${namespace} ]; then
        namespaces=$(kubectl ${KUBECTL_PARAMS[@]} get namespaces -l alias)
    else
        namespaces=$(kubectl ${KUBECTL_PARAMS[@]} get namespaces $1)
        echo "Check if namespace exist"
    fi

    for namespace in ${namespaces}; do
        for component in ${K8S_COMPONENTS[@]} ; do
            resources=$(kubectl ${KUBECTL_PARAMS[@]} -n ${namespace} get ${component} -l type=webapp)
            for resource in ${resources}; do
                status=$(kubectl -n ${namespace} get ${component} ${resource} -o json | jq '.spec.template.spec.affinity' | wc -c);
                if [[ "${status}" -le "423" ]]; then
                    echo -e "WEBAPP::Resource: \033[01;34m${resource}\033[0m"
                fi
            done
        done
    done
}

kubernetes_worker () {
    echo "Checking worker"
    namespace=$1

    if [ -z ${namespace} ]; then
        namespaces=$(kubectl ${KUBECTL_PARAMS[@]} get namespaces -l alias)
    else
        namespaces=$(kubectl ${KUBECTL_PARAMS[@]} get namespaces $1)
        echo "Check if namespace exist"
    fi

    for namespace in ${namespaces}; do
        for component in ${K8S_COMPONENTS[@]} ; do
            resources=$(kubectl ${KUBECTL_PARAMS[@]} -n ${namespace} get ${component} -l type=worker)
            for resource in ${resources}; do
                status=$(kubectl -n ${namespace} get ${component} ${resource} -o json | jq '.spec.template.spec.affinity' | wc -c);
                if [[ "${status}" -gt "5" ]]; then
                    echo -e "WORKER::Resource: \033[01;34m${resource}\033[0m"
                fi
            done
        done
    done
}

kubernetes_webapp $1
kubernetes_worker $1