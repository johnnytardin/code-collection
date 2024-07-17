function count-pods(){
    if [[ $1 == -h ]]; then
        echo 'Usage: $0 OPTIONS
        -h: Show this help
        --ns namespaceName: Count pods per Namespace
        --host nodeName: Count pods per specific nodes'
    else
        allPods=$(kubectl get pods -A -o wide --no-headers | sed 's/(.*)//g'| awk '{ printf $1","$2","$3","$4","$5","$6","$7","$8 "\n"}')
        if [[ $1 == --host ]] ; then
            if [[ ${2}X = "X" ]] ; then
                echo -e "Missing nodeName. "
            else
                echo "$2: $(echo $allPods | grep -c $2)"
            fi
        elif [[ $1 == --ns ]]; then
            if [[ ${2}X = "X" ]] ; then
                echo $allPods | awk -F"," '{ print $1 }' | sort | uniq -c | sort -rn
            else
                echo "$2: $(echo $allPods | grep -c $2)"
            fi
        else
            echo -e "Total Pods: \n$(echo "$allPods" | grep -v Completed | awk -F"," '/ip-/{ print $8 }' | sort | uniq -c | sort -nr -k1 -t " " | column -t)\n"
            echo -e "Pods by Status: \n$(echo "$allPods" | awk -F"," '{ print $4 }' | sort | uniq -c | sort -nr -k1 -t " " | column -t)\n"
        fi
    fi
}

count-pods