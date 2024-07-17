from elasticsearch import Elasticsearch

# Configurações do cluster Elasticsearch
es_source = Elasticsearch(["source_node_host:9200"])
es_destination = Elasticsearch(["destination_node_host:9200"])

# Obtenha a lista de shards alocados no nó de origem
shards_to_migrate = es_source.cat.shards(format="json")

# Desabilite a realocação automática de shards no cluster Elasticsearch
es_destination.cluster.put_settings(
    body={"persistent": {"cluster.routing.allocation.enable": "none"}}
)

# Mova manualmente os shards dos índices do nó de origem para o nó de destino
for shard in shards_to_migrate:
    index = shard["index"]
    shard_id = shard["shard"]
    source_node = shard["node"]

    # Mova o shard para o nó de destino
    es_destination.cluster.reroute(
        body={
            "commands": [
                {
                    "move": {
                        "index": index,
                        "shard": shard_id,
                        "from_node": source_node,
                        "to_node": "destination_node_name",
                    }
                }
            ]
        }
    )

# Verifique o progresso da realocação de shards
while True:
    shards_status = es_destination.cat.shards(format="json")

    # Verifique se todos os shards foram realocados com sucesso
    if all(shard["node"] != source_node for shard in shards_status):
        break

# Desligue ou remova o nó de origem com segurança
