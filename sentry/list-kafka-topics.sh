#!/bin/bash

# Lista todos os grupos de consumidores
groups=$(docker-compose exec -T kafka kafka-consumer-groups --list --bootstrap-server kafka:9092)

# Loop sobre cada grupo e executa o comando describe
for group in $groups; do
    if [ -n "$group" ]; then
        echo "Descrevendo o grupo: $group"
        docker-compose exec -T kafka kafka-consumer-groups --bootstrap-server kafka:9092 --group "$group" --describe
    fi
done
