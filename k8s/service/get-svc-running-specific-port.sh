#! /bin/bash

IFS=$'\n'$'\r'

for i in $(seq 0 1024); do
    echo "Verificando a porta $i"

    services=$(kubectl get svc -A -o=custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,PORT:.spec.ports[*].targetPort' | egrep " ${i}$")
    for service in ${services}; do
        status_pod=""
        status_user=""
        echo "-------------------------------------------------------------"

        name=$(echo $service | cut -d " " -f4-4 | sed "s/svc-//g" | tr '\n' ' ' | xargs)
        namespace=$(echo $service | cut -d " " -f1-1 | tr '\n' ' ' | xargs)

        pods=$(kubectl get pods -n ${namespace} -l app=${name})

        if [[ $pods != *"Running"* || $pods == *"1/2"* ]]; then
            status_pod="NOK"
        fi

        echo $pods

        id_pod=$(kubectl get pod -n ${namespace} | grep ${name} | awk 'END {print $1}' | tr '\n' ' ' | xargs echo)
        container_name=$(kubectl get pod -n ${namespace} $id_pod -o=custom-columns=':.metadata.labels.alias' | tr '\n' ' ' | xargs)
        user_pod=$(kubectl exec -it -n ${namespace} $id_pod -c ${container_name} -- id)

        if [[ $user_pod != *"uid=0(root)"* && $user_pod == *"uid"* ]]; then
            status_user="NOK"
        elif [[ $user_pod == *"uid=0(root)"* ]]; then
            status_user="OK"
        fi

        echo $user_pod

        if [[ $status_user != "OK" ]]; then
            if [[ $status_pod == "NOK" || $status_user == "NOK" ]]; then
                team=$(kubectl get pod -n ${namespace} $id_pod -o=custom-columns=':.metadata.labels.namespace' | tr '\n' ' ' | xargs)
                echo -e "${team};${container_name};${name}" >> apps.csv
            fi
        fi  
    done
done
