import boto3

elb = boto3.client("elb")

load_balancers_to_delete = ["lb1", "lb2"]

for lb_name in load_balancers_to_delete:
    try:
        elb.delete_load_balancer(LoadBalancerName=lb_name)
        print(f"Deleted load balancer: {lb_name}")
    except Exception as e:
        print(f"Error deleting load balancer {lb_name}: {e}")
