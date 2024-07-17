#!/bin/bash

# Obtém a lista de interfaces de rede
interfaces=$(ls /sys/class/net)

for interface in $interfaces; do
  # Verifica se o nome da interface começa com "vpn"
  if [[ $interface == vpn* ]]; then
    # Desativa a interface de rede
    sudo ip link set $interface down
    
    # Remove a interface de rede
    sudo ip link delete $interface
    
    echo "Interface $interface foi removida."
  fi
done

# Obtém a lista de rotas
rotas=$(ip route show)

while IFS= read -r linha; do
  # Verifica se a linha começa com "br-"
  if [[ $linha == *"br-"* ]]; then
    prefixo=$(echo $linha | awk '{print $1}')
    sudo ip route del $prefixo
    echo "Rota deletada: $prefixo"
  fi
done <<< "$rotas"