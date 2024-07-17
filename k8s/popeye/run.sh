docker run --rm -it \
  -v $HOME/.kube:/root/.kube \
  -e POPEYE_REPORT_DIR=/tmp/popeye \
  -v /tmp:/tmp \
  derailed/popeye --context foo -n bar --save --output-file report.txt
