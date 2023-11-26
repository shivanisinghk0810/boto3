import boto3
import time
import string
import random
import base64

def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def encode_message_body(message_body):
    encoded_body = base64.b64encode(message_body.encode()).decode()
    return encoded_body

def decode_message_body(encoded_message_body):
    # Decode the Base64-encoded message body
    decoded_body = base64.b64decode(encoded_message_body).decode()
    return decoded_body

# Replace 'YOUR_REGION_NAME' and 'YOUR_QUEUE_NAME' with the desired region and queue name
region_name = 'eu-west-2'
queue_name = 'my_first_queue'

# Create SQS client
sqs = boto3.client('sqs', region_name=region_name)

# Create SQS queue
response = sqs.create_queue(
    QueueName=queue_name,
    Attributes={'VisibilityTimeout': '60'}
)

queue_url = response['QueueUrl']
print("Queue URL:", queue_url)

def push_msgs_to_sqs(queue_url, num_messages=10):
    # Create SQS client
    sqs_client = boto3.client('sqs', region_name=region_name)
    
    for i in range(1, num_messages + 1):
        random_string = generate_random_string()
        message_body = f"shivani+ {random_string}"

        encoded_message_body = encode_message_body(message_body)

        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=encoded_message_body
        )
        
        print(f"Sent Message {i}, MessageId: {response['MessageId']}")
        time.sleep(1)

push_msgs_to_sqs(queue_url)

def read_msgs_from_sqs(queue_url):
    # Create SQS client
    sqs = boto3.client('sqs', region_name=region_name)
    
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=0,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']

            # Decode msg body
            decoded_message_body = decode_message_body(message['Body'])
            print(f"Received Message: {decoded_message_body}")

            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

# Push messages to the SQS queue
push_msgs_to_sqs(queue_url)

# Read and print messages from the SQS queue
read_msgs_from_sqs(queue_url)

