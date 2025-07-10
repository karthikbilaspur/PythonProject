from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import awstesting.sqsTester as sqs_testing

app = Flask(__name__)

# run_with_ngrok(app)

# Create an instance of the SQSTest class
sqs_test = sqs_testing.SQSTest()

@app.route("/", methods=['GET'])
def welcome():
    message = "Welcome to the SQS testing API. Use the following endpoints to test SQS operations."
    return message

@app.route("/create_queue", methods=['POST'])
def create_queue():
    queue_name = request.json['queue_name']
    sqs_test.create_sqs_queue(queue_name)
    return jsonify({'message': f"Queue {queue_name} created"})

@app.route("/send_message", methods=['POST'])
def send_message():
    queue_name = request.json['queue_name']
    message_body = request.json['message_body']
    sqs_test.queue_url = sqs_test.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    sqs_test.send_message(message_body)
    return jsonify({'message': f"Message sent to queue {queue_name}"})

@app.route("/receive_message", methods=['POST'])
def receive_message():
    queue_name = request.json['queue_name']
    sqs_test.queue_url = sqs_test.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    message = sqs_test.receive_message()
    return jsonify({'message': message})

@app.route("/delete_queue", methods=['POST'])
def delete_queue():
    queue_name = request.json['queue_name']
    sqs_test.queue_url = sqs_test.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    sqs_test.delete_queue()
    return jsonify({'message': f"Queue {queue_name} deleted"})

if __name__ == '__main__':
    app.run()