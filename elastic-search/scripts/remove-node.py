import urllib3
import logging

from decouple import config
from elasticsearch import Elasticsearch

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("elasticsearch").setLevel(logging.ERROR)

cluster_host = config("ELASTIC_HOST")
username = config("ELASTIC_USERNAME")
password = config("ELASTIC_PASSWORD")

es = Elasticsearch(cluster_host, verify_certs=False, http_auth=(username, password))

cluster_health = es.cluster.health()
if cluster_health["status"] != "green":
    print(
        "O cluster não está em estado saudável. Verifique o status antes de remover um nó."
    )
    exit(1)

nodes = es.nodes.stats()["nodes"]

print("Lista de nós no cluster:")
for i, (node_id, node_info) in enumerate(nodes.items(), start=1):
    hostname = node_info["name"]
    host = node_info["host"]
    print(f"{i}. ID: {node_id}, Hostname: {hostname}, Host: {host}")

# Solicitar ao usuário que escolha um nó para remover
selected_node = input("Digite o número do nó que deseja remover: ")

if (
    not selected_node.isdigit()
    or int(selected_node) < 1
    or int(selected_node) > len(nodes)
):
    print("Opção inválida.")
    exit(1)

node_to_remove = list(nodes.keys())[int(selected_node) - 1]

print(f"Removendo o nó {node_to_remove} do cluster...")
response = es.nodes.remove(node_id=node_to_remove)

if "acknowledged" in response and response["acknowledged"]:
    print(f"O nó {node_to_remove} foi removido com sucesso.")
else:
    print(f"A remoção do nó {node_to_remove} falhou.")

cluster_health = es.cluster.health()
if cluster_health["status"] != "green":
    print("O cluster não está em estado saudável após a remoção do nó.")
    print(f"Status atual do cluster: {cluster_health['status']}")
else:
    print("O cluster está em estado saudável após a remoção do nó.")
