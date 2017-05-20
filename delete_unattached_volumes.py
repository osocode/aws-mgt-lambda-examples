import boto3
import logging

ec2 = boto3.resource('ec2', region_name='us-east-1')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    for vol in ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}]):
        can_delete = True
        for t in vol.tags:
            if t['Key'] == 'DoNotDelete':
                can_delete = False
        if can_delete:
            logger.info('Deleting volume id: {} with tags: {}'.format(vol.id, vol.tags))
            volume = ec2.Volume(vol.id)
            volume.delete()
            
