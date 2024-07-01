# Stop/Start Script Documentation

## Start Script

The start script is used to initiate server operations upon boot.

### Directory Path

The startup script should be placed in the following directory:

    /var/lib/cloud/scripts/per-boot

### Script Name

Ensure your startup script is named:

    startup.sh

This bash script is customized to start the SAP Service as required during server boot.

## Stop Script

The stop script is executed prior to server shutdown.

### Script Name

The script responsible for server shutdown operations is:

    StopServer.py

This script is designed for Lambda functions.

## Lambda Role

To use the Lambda function with the provided IAM policy, ensure you have the following JSON policy:

    IAMPolicy.json

This policy grants necessary permissions for the Lambda function to execute.

## Logs

Specify the location for storing script logs. These logs capture the output of the shutdown script, indicating successful script execution, and can also log startup script activities.

---

<p align="center">
    <strong style="color:green">Physics is theoretical, but the fun is real</strong>
</p>

<p align="center">
    😁 ENJOY 😁
</p>
