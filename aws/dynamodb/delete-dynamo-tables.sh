tables=$(aws dynamodb list-tables | jq -r '.TableNames[]')
for table in ${tables}; do
    if [[ "${table}" == *"cortex"* ]]; then
        echo ${table} 
        aws dynamodb delete-table --table-name ${table}
    fi
done
