import datetime
import logging
import time
import json
from urllib.parse import urlencode
import urllib3

import requests
from decouple import config
from kubernetes import client
from kubernetes.client.rest import ApiException


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_error_logs():
    minutes_backward = config("LOGS_ERROR_MINUTES_COUNT_BACKWARD", default=2, cast=int)
    loki_url = config("LOKI_URL", default="http://localhost:3100", cast=str)

    query = r'sum by(pod) (rate({container="keda-operator"} |= `error finding offset block` [1m]))'

    params = {}
    params["query"] = query
    params["end"] = int(datetime.datetime.now().timestamp() * 10**9)
    params["start"] = int(
        (
            datetime.datetime.fromtimestamp(params["end"] / 10**9)
            - datetime.timedelta(minutes=minutes_backward)
        ).timestamp()
        * 10**9
    )
    params["limit"] = 10
    params["direction"] = "backward"

    enc_query = urlencode(params)
    target_url = f"{loki_url}/loki/api/v1/query_range?{enc_query}"

    response = requests.get(url=target_url, verify=False).json()
    if response.get("data").get("result"):
        return True
    return False


def delete_pods():
    clusters = json.loads(config("KUBERNETES_CLUSTERS", default=[]))
    if not clusters:
        logging.info("No cluster declared in variable KUBERNETES_CLUSTERS")

    for cluster in clusters:
        logging.info("Deleting keda pods on cluster {}".format(cluster.get("name")))

        configuration = client.Configuration()
        configuration.api_key["authorization"] = cluster.get("auth_token")
        configuration.api_key_prefix["authorization"] = "Bearer"
        configuration.host = cluster.get("host")
        configuration.verify_ssl = False

        with client.ApiClient(configuration) as api_client:
            api_instance = client.CoreV1Api(api_client)
            namespace = "keda"
            pod_list = api_instance.list_namespaced_pod(namespace)
            for pod in pod_list.items:
                start_time = pod.status.start_time
                if (
                    datetime.datetime.now(datetime.timezone.utc) - start_time
                ).seconds < config(
                    "POD_MIN_AGE_SECONDS_TO_DELETE", default=60 * 5, cast=int
                ):
                    logging.info(
                        f"Pod {pod.metadata.name} is too new, ignoring. Start time: {start_time}"
                    )
                else:
                    try:
                        logging.info(
                            f"Pod {pod.metadata.name} found in namespace {namespace}. Removing the pod. Start time: {start_time}"
                        )
                        api_instance.delete_namespaced_pod(pod.metadata.name, namespace)
                    except ApiException as e:
                        logging.exception(
                            f"Exception when deleting pod {pod.metadata.name}: {e}"
                        )


if __name__ == "__main__":
    time_to_sleep = config("TIME_TO_SLEEP", default=60 * 3, cast=int)
    while True:
        has_errors = get_error_logs()
        if has_errors:
            delete_pods()
        logging.info(f"No errors in keda. Sleeping for {time_to_sleep} seconds")
        time.sleep(time_to_sleep)
