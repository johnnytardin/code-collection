aws ec2 describe-instances --filters "Name=tag:product,Values=product_name" --query "Reservations[].Instances[].NetworkInterfaces[].Association.PublicDnsName"

