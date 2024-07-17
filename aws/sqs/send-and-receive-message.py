import click
import boto3

sqs = boto3.client("sqs")

queue_name = "naner-test-johnny"

try:
    response = sqs.create_queue(QueueName=queue_name)
except sqs.exceptions.QueueNameExists:
    response = sqs.get_queue_url(QueueName=queue_name)

queue_url = response["QueueUrl"]


def send_message(message):
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
    message_id = response["MessageId"]
    print(f"Message sent with ID {message_id}")


def receive_message():
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)

    messages = response.get("Messages", [])

    if not messages:
        print("There are no messages in the queue.")
    else:
        message = messages[0]
        receipt_handle = message["ReceiptHandle"]
        body = message["Body"]

        print(f"Message received: {body}")

        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

        print("Message deleted from the queue.")


@click.command()
@click.option("--send", "-s", help="Send a message to the queue")
@click.option("--receive", "-r", is_flag=True, help="Receive a message from the queue")
def main(send, receive):
    if send:
        send_message(send)
    elif receive:
        receive_message()
    else:
        print(
            "No option was selected. Please use '--send' to send a message or '--receive' to receive a message."
        )


if __name__ == "__main__":
    main()
