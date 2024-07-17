curl -g -X POST 'http://metricsplat.local:9090/api/v1/admin/tsdb/delete_series?match[]=kube_node_labels{exporter_node!=""}&start=1669945322&end=1669945322' -H 'x-scope-orgid: 1'
