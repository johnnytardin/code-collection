import boto3
import re
import json
import csv

internal_records = {}
external_records = {}


session = boto3.Session(region_name="us-east-1")

client = session.client("route53")


def get_matching_records(zone_id, pattern, record_types):
    matching_records = []

    response = client.list_resource_record_sets(
        HostedZoneId=zone_id,
    )

    while True:
        for record_set in response["ResourceRecordSets"]:
            if any(record_type in record_set["Type"] for record_type in record_types):
                for record in record_set.get("ResourceRecords", []):
                    if "Value" in record and re.match(pattern, record["Value"]):
                        matching_records.append(record_set)

        if response["IsTruncated"]:
            response = client.list_resource_record_sets(
                HostedZoneId=zone_id,
                StartRecordName=response["NextRecordName"],
                StartRecordType=response["NextRecordType"],
            )
        else:
            break

    return matching_records


def main():
    zones = client.list_hosted_zones()

    for zone in zones["HostedZones"]:
        zone_id = zone["Id"]
        zone_name = zone["Name"]

        pattern_to_search_app = r"(gateway|app-[0-9a-f-]+)\.domain\.io"
        record_types = ["A", "CNAME"]

        edge_records = [
            "app.example.com.",
        ]

        matching_records = get_matching_records(
            zone_id, pattern_to_search_app, record_types
        )

        if matching_records:
            for record in matching_records:
                name = record["Name"]
                type = record["Type"]
                records = [r["Value"] for r in record["ResourceRecords"]]

                is_edge = any(edge_record in records for edge_record in edge_records)

                if is_edge:
                    if zone_name not in external_records:
                        external_records[zone_name] = {}
                    external_records[zone_name][name] = {"type": type, "names": records}
                else:
                    if zone_name not in internal_records:
                        internal_records[zone_name] = {}
                    internal_records[zone_name][name] = {"type": type, "names": records}

    output_filename_external = "/tmp/registros_dns_external.csv"
    with open(output_filename_external, "w", newline="") as csvfile:
        fieldnames = ["zone", "name", "record", "type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for zone, records in external_records.items():
            for domain, record in records.items():
                writer.writerow(
                    {
                        "zone": zone,
                        "name": domain,
                        "record": record["names"][0],
                        "type": record["type"],
                    }
                )

    output_filename_external = "/tmp/registros_dns_internal.csv"
    with open(output_filename_external, "w", newline="") as csvfile:
        fieldnames = ["zone", "name", "record", "type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for zone, records in internal_records.items():
            for domain, record in records.items():
                writer.writerow(
                    {
                        "zone": zone,
                        "name": domain,
                        "record": record["names"][0],
                        "type": record["type"],
                    }
                )

    # print("---" * 30)
    # print("Edge Records")
    # print(json.dumps(external_records, indent=4))

    # print("---" * 30)
    # print("Internal Records")
    # print(json.dumps(internal_records, indent=4))


if __name__ == "__main__":
    main()
