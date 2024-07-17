#!/bin/bash
for filename in *.yaml; do
    echo $filename
    new_name=${filename/.yaml/""}
    k2tf -f $filename -o $new_name.tf
done