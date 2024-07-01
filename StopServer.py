## Run Script And Stop Sever


import boto3
import time

def lambda_handler(event, context):
    
    instance_id = 'i-XXXXXXXXXXXX'  # Replace with your EC2 instance ID

    # Define the commands to be executed
    commands = [
        {
            'instance_id': instance_id,
            'user': 'ubuntu',
            'script_path': '/home/ubuntu/start.sh',
            'output_path': '/home/ubuntu/shutdownlog.txt'
        }
    ]

    # Initialize the SSM client for ap-south-1 region
    ssm_client = boto3.client('ssm', region_name='ap-south-1')


    # Execute each command asynchronously
    for command in commands:
        response = ssm_client.send_command(
            DocumentName="AWS-RunShellScript",
            InstanceIds=[command['instance_id']],
            Parameters={
                'commands': [
                    f'sudo su - {command["user"]} -c {command["script_path"]} >> {command["output_path"]} 2>&1'
                ]
            }
        )
        
        print(f"Command sent to instance {command['instance_id']}: {response['Command']['CommandId']}")

    
    print("let me sleep for 2 minutes")

    # it take seconds as input 120 seconds means 2 min
    time.sleep(120)
    
    print("I wake UP, Now going to run second command")
    

    # All commands have completed, send shutdown command
    shutdown_response = ssm_client.send_command(
        DocumentName="AWS-RunShellScript",
        InstanceIds=[instance_id],
        Parameters={
            'commands': [
                'sudo shutdown -h now'
            ]
        }
    )

    print(f"Shutdown command sent to instance {instance_id}: {shutdown_response['Command']['CommandId']}")

    # Return any relevant information
    return {
        'statusCode': 200,
        'body': 'Commands sent successfully'
    }
