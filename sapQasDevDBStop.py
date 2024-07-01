# Stop DB Server This Script Not Required....... Because When Stoping DB it takes fewer minutes 

import boto3
import time

def lambda_handler(event, context):
    instance_id = 'i-XXXXXXXXXXX'  # Replace with your EC2 instance ID

    # Define the commands to be executed
    commands = [
        {
            'instance_id': instance_id,
            'user': 'ubuntu',
            'script_path': '/usr/sap/DDB/HDB00/stopdb_DDB',
            'output_path': '/home/ssm-user/shutdownDevLogs.txt'
        },
        {
            'instance_id': instance_id,
            'user': 'ubuntu',
            'script_path': '/usr/sap/QDB/HDB02/start.sh',
            'output_path': '/home/ssm-user/shutdownQasLogs.txt'
        }
    ]

    # Initialize the SSM client for ap-south-1 region
    ssm_client = boto3.client('ssm', region_name='ap-south-1')

    # List to track command completion
    command_ids = []

    # Execute each command asynchronously
    for command in commands:
        response = ssm_client.send_command(
            DocumentName="AWS-RunShellScript",
            InstanceIds=[command['instance_id']],
            Parameters={
                'commands': [
                    f'sudo -u {command["user"]} {command["script_path"]} >> {command["output_path"]} 2>&1'
                ]
            }
        )
        
        command_ids.append(response['Command']['CommandId'])
        print(f"Command sent to instance {command['instance_id']}: {response['Command']['CommandId']}")

    # Function to check if all commands have completed successfully
    def check_commands_complete(command_ids):
        for command_id in command_ids:
            result = ssm_client.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id
            )
            status = result['Status']
            if status not in ['Success', 'Cancelled', 'Failed']:
                print(f"status of command {status}")
                return False
        print(f"status of command {status}")
        return True

    print(f"check command complete {check_commands_complete}")
    # Wait for commands to complete
    while not check_commands_complete(command_ids):
        print("Waiting for commands to complete...")
        time.sleep(5)  # Adjust sleep time as needed for your scenario

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
