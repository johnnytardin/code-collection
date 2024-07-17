# aws ec2 describe-network-interfaces --filters Name=vpc-id,Values=vpc-aaaaaa | grep GroupName | sort | uniq -c | sort -n 

aws ec2 describe-network-interfaces --filters Name=subnet-id,Values=subnet-aaaaaa | grep GroupName | sort | uniq -c | sort -n 