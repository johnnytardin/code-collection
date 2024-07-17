from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth

# Configurações do Elasticsearch
es = Elasticsearch(["localhost:9200"], http_auth=HTTPBasicAuth("username", "password"))

# 1. Criar uma política de ILM
policy_name = "7day-retention-policy"
policy_config = {
    "policy": {"phases": {"delete": {"min_age": "7d", "actions": {"delete": {}}}}}
}

es.ilm.put_lifecycle(policy_name, body=policy_config)

# 2. Atribuir a política de ILM ao template de índice
template_name = "my-template"
index_pattern = "my-data-stream-*"
template_config = {
    "index_patterns": [index_pattern],
    "template": {
        "settings": {
            "index.lifecycle.name": policy_name,
            "index.lifecycle.rollover_alias": "my-data-stream",
        }
    },
}

es.indices.put_index_template(name=template_name, body=template_config)

print("Index Lifecycle Management configuration completed.")
