export ANSIBLE_HOST_KEY_CHECKING=False

ansible-playbook -i inventory --private-key=~key.pem run_command.yml
