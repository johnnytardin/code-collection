import boto3
import re
import json
import csv


mathed_records = {}


session = boto3.Session(region_name="us-east-1")

client = session.client("route53")


def get_matching_records(zone_id, pattern, record_types):
    response = client.list_resource_record_sets(
        HostedZoneId=zone_id,
    )

    matching_records = []

    for record_set in response["ResourceRecordSets"]:
        if any(record_type in record_set["Type"] for record_type in record_types):
            for record in record_set.get("ResourceRecords", []):
                if "Value" in record and re.match(pattern, record["Value"]):
                    matching_records.append(record_set)

    return matching_records


def main():
    zones = client.list_hosted_zones()

    for zone in zones["HostedZones"]:
        zone_id = zone["Id"]
        zone_name = zone["Name"]

        pattern_to_search_cloudflare = r".*\.cdn\.cloudflare\.net$"
        record_types = ["A", "CNAME"]

        cloudflare_records = [
            "app.xxx.com.cdn.cloudflare.net",
            "app.xxx.com.cdn.cloudflare.net.",
        ]

        matching_records = get_matching_records(
            zone_id, pattern_to_search_cloudflare, record_types
        )

        if matching_records:
            for record in matching_records:
                name = record["Name"]
                type = record["Type"]
                records = [r["Value"] for r in record["ResourceRecords"]]

                if zone_name not in mathed_records:
                    mathed_records[zone_name] = {}
                mathed_records[zone_name][name] = {"type": type, "names": records}

    output_filename_external = "/tmp/registros_dns_cloudflare.csv"
    with open(output_filename_external, "w", newline="") as csvfile:
        fieldnames = ["zone", "name", "record", "type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for zone, records in mathed_records.items():
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
    # print("Internal Records")
    # print(json.dumps(internal_records, indent=4))


if __name__ == "__main__":
    main()
