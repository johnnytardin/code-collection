FILTER="string-to-find"

# for ns in $(kubectl get ns -oname | awk -F "/" '{print $2}'); do
#   for deploy in $(kubectl get deploy -n $ns | grep -v NAME | awk -F " " '{print $1}'); do
#     filtered=$(kubectl get deploy $deploy -n $ns -o yaml | grep $FILTER)
    
#     if [ $(echo $filtered | wc -c) -gt "1" ]; then
#         echo "$deploy;$filtered"
#         echo "$deploy;$filtered" >> id.txt
#     fi

#   done;
# done

# cronjob
for ns in $(kubectl get ns -oname | awk -F "/" '{print $2}'); do
  for cronjob in $(kubectl get cronjob -n $ns | grep -v NAME | awk -F " " '{print $1}'); do
    filtered=$(kubectl get cronjob $cronjob -n $ns -o yaml | grep $FILTER)
    
    if [ $(echo $filtered | wc -c) -gt "1" ]; then
        echo "$cronjob;$filtered"
        echo "$cronjob;$filtered" >> cronjob.txt
    fi

  done;
done