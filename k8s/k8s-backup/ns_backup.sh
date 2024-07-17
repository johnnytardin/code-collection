#! /bin/bash
clear

# Change if you need
K8S_BACKUP_COMPONENTS=("deployment" "service" "hpa" "serviceaccount" "rolebinding")

# Do not change
START_TIME=$(date +%Y%m%d%H%M)
KUBECTL_PARAMS=("-o=custom-columns=NAME:.metadata.name --no-headers=true")

status () {
    if [ $? -eq 0 ]; then
        echo -e "$1 [\033[01;32mOK\033[0m]"
    else
        echo -e "[\033[01;31mERROR\033[0m]"
        echo ""
        exit 1;
    fi
}

kubernetes_backup () {
    namespace=$1
    cluster_name=$(kubectl config current-context)

    if [ -z ${namespace} ]; then
        namespaces=$(kubectl ${KUBECTL_PARAMS[@]} get namespaces)
    else
        namespaces=$(kubectl ${KUBECTL_PARAMS[@]} get namespaces $1)
        status "Check if namespace exist"
    fi

    for namespace in ${namespaces}; do
        full_destination_dir=${DESTINATION_DIR}/${cluster_name}/${START_TIME}/${namespace}
        echo ""
        echo "[ ---------- Backuping namespace \"${namespace}\" ---------- ]"
        for component in ${K8S_BACKUP_COMPONENTS[@]} ; do
            echo ""
            echo -e "::Component: \033[01;34m${component}\033[0m"
            mkdir -p ${full_destination_dir}/${component}
            status "Dest dir: \"${full_destination_dir}/${component}\""
            resources=$(kubectl ${KUBECTL_PARAMS[@]} -n ${namespace} get ${component})
            for resource in ${resources}; do
                kubectl -n ${namespace} get ${component} ${resource} -o yaml > ${full_destination_dir}/${component}/${resource}.yaml;
                status "Dump \"${resource}\" from \"${namespace}\"";
            done
        done
    done

}

kubernetes_backup $1