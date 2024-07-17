import json
import subprocess

instances = json.loads(
    subprocess.check_output(
        [
            "aws",
            "ec2",
            "describe-instances",
            "--filters",
            "Name=tag:product,Values=product_name",
            "Name=instance-state-name,Values=running",
        ]
    )
)

for reservation in instances["Reservations"]:
    for instance in reservation["Instances"]:
        instance_id = instance["InstanceId"]
        try:
            subprocess.check_call(
                ["aws", "ec2", "unmonitor-instances", "--instance-ids", instance_id]
            )
        except Exception as e:
            print(e)
            pass
