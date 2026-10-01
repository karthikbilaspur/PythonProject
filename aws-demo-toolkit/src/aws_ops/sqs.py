"""Thin, stateless SQS service. No mocking and no shared mutable state here;
mocking belongs in the tests. Errors propagate as ClientError."""
import boto3


class SQSService:
    def __init__(self, region_name: str = "us-east-1", client=None):
        self.sqs = client or boto3.client("sqs", region_name=region_name)

    def create_queue(self, queue_name: str) -> str:
        return self.sqs.create_queue(QueueName=queue_name)["QueueUrl"]

    def get_queue_url(self, queue_name: str) -> str:
        return self.sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]

    def send_message(self, queue_name: str, body: str) -> str:
        return self.sqs.send_message(QueueUrl=self.get_queue_url(queue_name), MessageBody=body)["MessageId"]

    def receive_message(self, queue_name: str) -> str | None:
        """Receive one message, delete it, and return its body (None if empty)."""
        url = self.get_queue_url(queue_name)
        resp = self.sqs.receive_message(QueueUrl=url, MaxNumberOfMessages=1, WaitTimeSeconds=1)
        messages = resp.get("Messages")
        if not messages:
            return None
        msg = messages[0]
        self.sqs.delete_message(QueueUrl=url, ReceiptHandle=msg["ReceiptHandle"])
        return msg["Body"]

    def delete_queue(self, queue_name: str) -> None:
        self.sqs.delete_queue(QueueUrl=self.get_queue_url(queue_name))
