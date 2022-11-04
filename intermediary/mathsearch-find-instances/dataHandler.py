from constants import *
import os
import boto3
import time

class DataHandler():
    def __init__(self):
        self.clients = [boto3.client('sqs'), boto3.client('s3')]
    
    def enqueue(self, message):
        self.clients[client_indices['sqs']].send_message(QueueUrl = queue_url, MessageBody = message)
    
    def dequeue(self):
        return self.clients[client_indices['sqs']].receive_message(QueueUrl = queue_url)['Messages']
    
    def invoke_model(self):
        pass

    def process_input(self, input):
        pass
    
    def format_output(self, output):
        pass

    def download_file_from_s3(self, s3_bucket, s3_object, directory="/tmp"):
        # s3 = boto3.resource('s3')
        # object = s3.Object('mathsearch-intermediary', 'mathsearch_test_pdf.png')
        # body = object.get()['Body'].read()
        # print(body)
        
        self.clients[client_indices['s3']].download_file(s3_bucket, s3_object, f'{directory}/mathsearch_{s3_object}')
        # with open("/tmp/tmpa.txt", "w") as f:
            # f.write('this is some content')
        
        print(os.listdir('/tmp'))
    
    def upload_file_to_s3(self, s3_bucket, s3_object, directory="/tmp"):
        self.clients[client_indices['s3']].upload_file(f'{directory}/mathsearch_{s3_object}', s3_bucket, f'{s3_object}_UPLOADED')
        
    def delete_expired_files(self, s3_bucket, s3_object, directory="/tmp"):
        kwargs = {"Bucket": s3_bucket, "Prefix": directory}
        
        while True:
            response = self.clients[client_indices['s3']].list_objects_v2(**kwargs)
            for obj in response["Contents"]:
                if "." in obj["Key"]:
                    key_date = time.time()
                    
            
        return 0
        
    def get_key_info(self, s3_bucket, directory="/tmp"):
        key_names = []
        file_timestamps = []
        file_sizes = []
        kwargs = {"Bucket": s3_bucket, "Prefix": directory}
        
        while True:
            response = self.clients[client_indices['s3']].list_objects_v2(**kwargs)
            for obj in response["Contents"]:
                # excludes deleting directories, which should not be in the bucket    
                if "." in obj["Key"]:
                    key_names.append(obj["Key"])
                    file_timestamps.append(obj["LastModified"].timestamp())
                    file_sizes.append(obj["Size"])
                
            try:
                kwargs["ContinuationToken"] = response["NextContinuationToken"]
            except KeyError:
                break
            
        key_info = {
            "key_path": key_names,
            "timestamp": file_timestamps,
            "size": file_sizes
        }
        
        return key_info
    
    def check_expiration(limit=_expire_limit):
        key_date = time.time()
        expiration_limit = key_date - constants.duration
        
        return key_date < limit
        
    def delete_s3_file(self, s3_bucket, s3_object):
        self.clients[client_indices['s3']].delete_object(Bucket=s3_bucket, Key=s3_object)
        return True

    def run(self):
        # Get new input
        message = self.dequeue()

        # Process the input
        self.process_input(message)

        # Invoke the model
        model_output = self.invoke_model()

        # Format the output
        output = self.format_output(model_output)
        
        # Return the output to the frontend
        return {'result': output}