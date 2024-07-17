import boto3
from datetime import datetime, timedelta
import csv

cw = boto3.client("cloudwatch")
elb = boto3.client("elb")

period_in_hours = 24 * 7
now = datetime.utcnow()
start_time = now - timedelta(hours=period_in_hours)

response = elb.describe_load_balancers()
load_balancers = response["LoadBalancerDescriptions"]

no_request_lb = []
no_instance_lb = []
low_request_lb = []
no_health_instances_lb = []

for lb in load_balancers:
    lb_name = lb["LoadBalancerName"]

    tags = elb.describe_tags(LoadBalancerNames=[lb_name])
    tag_descriptions = tags["TagDescriptions"]

    tag_svc_name = ""
    for tag_description in tag_descriptions:
        for tag in tag_description["Tags"]:
            if tag["Key"] == "kubernetes.io/service-name":
                tag_svc_name = tag["Value"]
                if "svc-" in tag_svc_name:
                    tag_svc_name = tag_svc_name.split("/")[1][4:]

    health = elb.describe_instance_health(LoadBalancerName=lb_name)
    instances = health["InstanceStates"]

    instances_outofservice = list(
        filter(lambda x: x["State"] == "OutOfService", instances)
    )

    all_unhealthy = False
    if instances and (
        sum(len(i) for i in instances) == sum(len(i) for i in instances_outofservice)
    ):
        all_unhealthy = True

    try:
        response = cw.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": "m1",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": "AWS/ELB",
                            "MetricName": "RequestCount",
                            "Dimensions": [
                                {"Name": "LoadBalancerName", "Value": lb_name},
                            ],
                        },
                        "Period": 60 * period_in_hours,
                        "Stat": "Sum",
                    },
                    "ReturnData": True,
                },
            ],
            StartTime=start_time,
            EndTime=now,
        )

        if not response["MetricDataResults"][0]["Values"]:
            request_count = 0
        else:
            request_count = sum(response["MetricDataResults"][0]["Values"])

    except Exception as e:
        print(f"Error getting data for load balancer {lb_name}: {e}")
    else:
        if not instances:
            no_instance_lb.append(
                {
                    "Load Balancer": lb_name,
                    "kubernetes.io/service-name": tag_svc_name,
                    "requests": request_count,
                }
            )
        elif all_unhealthy:
            no_health_instances_lb.append(
                {
                    "Load Balancer": lb_name,
                    "kubernetes.io/service-name": tag_svc_name,
                    "requests": request_count,
                }
            )
        elif request_count == 0:
            no_request_lb.append(
                {
                    "Load Balancer": lb_name,
                    "kubernetes.io/service-name": tag_svc_name,
                    "requests": request_count,
                }
            )
        elif request_count < 20:
            low_request_lb.append(
                {
                    "Load Balancer": lb_name,
                    "kubernetes.io/service-name": tag_svc_name,
                    "requests": request_count,
                }
            )


fieldnames = ["Load Balancer", "kubernetes.io/service-name", "requests"]
with open("/tmp/no_instance_lb.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for lb in no_instance_lb:
        writer.writerow(lb)

with open("/tmp/no_request_lb.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for lb in no_request_lb:
        writer.writerow(lb)

with open("/tmp/low_request_lb.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for lb in low_request_lb:
        writer.writerow(lb)

with open("/tmp/no_health_instances_lb.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for lb in no_health_instances_lb:
        writer.writerow(lb)
