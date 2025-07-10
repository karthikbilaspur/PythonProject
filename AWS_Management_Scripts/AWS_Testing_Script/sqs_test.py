import boto3
from moto import mock_sqs
import json

class SQSTest:
    def __init__(self):
        self.sqs = None
        self.queue_url = None

    @mock_sqs
    def create_sqs_queue(self, queue_name):
        try:
            self.sqs = boto3.client('sqs', region_name='us-east-1')
            response = self.sqs.create_queue(QueueName=queue_name)
            self.queue_url = response['QueueUrl']
            print(f"Queue created: {self.queue_url}")
        except Exception as e:
            print(f"Error creating queue: {str(e)}")

    @mock_sqs
    def send_message(self, message_body):
        try:
            response = self.sqs.send_message(QueueUrl=self.queue_url, MessageBody=message_body)
            print(f"Message sent: {response['MessageId']}")
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    @mock_sqs
    def receive_message(self):
        try:
            response = self.sqs.receive_message(QueueUrl=self.queue_url)
            if 'Messages' in response:
                message = response['Messages'][0]
                print(f"Received message: {message['Body']}")
                self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])
            else:
                print("No messages in queue")
        except Exception as e:
            print(f"Error receiving message: {str(e)}")

    @mock_sqs
    def delete_queue(self):
        try:
            self.sqs.delete_queue(QueueUrl=self.queue_url)
            print(f"Queue deleted: {self.queue_url}")
        except Exception as e:
            print(f"Error deleting queue: {str(e)}")

if __name__ == "__main__":
    sqs_test = SQSTest()
    queue_name = 'my-queue'
    sqs_test.create_sqs_queue(queue_name)
    message_body = json.dumps({'message': 'Hello, world!'})
    sqs_test.send_message(message_body)
    sqs_test.receive_message()
    sqs_test.delete_queue()