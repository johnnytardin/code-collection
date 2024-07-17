# cordon todos os nos para nao permitir q sejam agendados
# nodes_to_cordon=$(kubectl get nodes --show-labels -o wide | grep -v management | grep spot | grep 5.10.165-143.735 | grep -v Disabled | awk '{print $1}');
# for node in ${nodes_to_cordon};
# do
#   echo "     Cordon: ${node}"
#   kubectl cordon ${node} 
# done

nodes_to_drain=$(kubectl get nodes --show-labels -o wide | awk '{print $1}');

for node in ${nodes_to_drain};
do
  echo "     Node Name: ${node}"
  kubectl drain ${node} --ignore-daemonsets --delete-emptydir-data --force
  sleep 2
done


