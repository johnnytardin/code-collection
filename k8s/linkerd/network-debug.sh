#!/bin/bash

pods=$(kubectl get po -A -l linkerd.io/control-plane-ns -ojsonpath="{range .items[*]}{.metadata.name} {.metadata.namespace}{'\n'}{end}")

IFS=" "

while read name namespace; do
  tcp=$(kubectl debug -n $namespace $name --image=cr.l5d.io/linkerd/debug:stable-2.12.0 -it -- cat /proc/net/tcp)
  close_wait=$(echo $tcp | awk 'BEGIN {cnt=0} $4==08 {cnt++} END {print cnt}')
  fin_wait_2=$(echo $tcp | awk 'BEGIN {cnt=0} $4==05 {cnt++} END {print cnt}')
  if [ "$close_wait" -gt "0" -o "$fin_wait_2" -gt "0" ]; then
        echo "$name.$namespace has $close_wait sockets in CLOSE_WAIT and $fin_wait_2 sockets in FIN_WAIT_2"
        if [[ $namespace =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$ ]]; then
            kubectl delete pod -n $namespace $name
        fi
  else
        echo "$name.$namespace is okay"
  fi
done <<< "$pods"
