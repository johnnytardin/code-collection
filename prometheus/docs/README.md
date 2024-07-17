
# Listar workers com pouco volume de rede

```
(quantile(0.9,
   rate(
      container_network_transmit_bytes_total{}[5m]
   ) 
   +
   rate(
      container_network_receive_bytes_total{}[5m]
   )
) by (deployment, application, team)
+ on(deployment) group_left(type)
sum(
   label_replace
   (
      applications_info{}, "deployment", "$1", "uuid", "(.*)"
   ) * 0
) by (deployment, type)
)
< 1
```

# Listar webapps com pouco volume

```
(sum(
   increase(
      request_total{direction="inbound"}[5m]
   ) 
) by (deployment, alias, namespace)
+ on(deployment) group_left(type)
sum(
   label_replace
   (
      applications_info{type="webapp"}, "deployment", "$1", "uuid", "(.*)"
   ) * 0
) by (deployment, type)
) < 100
```



#####
(avg(
   increase(
      request_total{direction="inbound"}[$__range]
   ) 
) by (deployment, alias, namespace)
+ on(deployment) group_left(type)
sum(
   label_replace
   (
      applications_info{type="webapp"}, "deployment", "$1", "uuid", "(.*)"
   ) * 0
) by (deployment, type)
) 




sum(
   rate(
      container_network_transmit_bytes_total{}[$__range]
   ) 
   +
   rate(
      container_network_receive_bytes_total{}[$__range]
   )
) by (deployment, application, team)
+ on(deployment) group_left(type)
sum(
   label_replace
   (
      applications_info{type="webapp"}, "deployment", "$1", "uuid", "(.*)"
   ) * 0
) by (deployment, type)
< 1000

quantile(0.95,
   rate(
      container_network_transmit_bytes_total{}[$__interval]
   ) 
   +
   rate(
      container_network_receive_bytes_total{}[$__interval]
   )
) by (deployment, application, team)
+ on(deployment) group_left(type)
sum(
   label_replace
   (
      applications_info{type="webapp"}, "deployment", "$1", "uuid", "(.*)"
   ) * 0
) by (deployment, type)
# < 1000
