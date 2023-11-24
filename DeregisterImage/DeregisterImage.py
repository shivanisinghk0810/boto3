import boto3
import datetime
from dateutil.parser import parse

def days_old(date):
    parsed = parse(date).replace(tzinfo=None)
    diff = datetime.datetime.now() - parsed
    return diff.days
    
def lambda_handler(event , context):
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        print("Region",region)
        
        amis = ec2.describe_images(Owners=['self']['Images'])
        
        for ami in amis:
            creationdate = ami['CreationDate']
            age_days = days_old(creationdate)
            image_id = ami['ImageId']
            print("creation date {} days old {} imageId {}", creationdate, age_days, image_id )
            
            if age_days >= 2:
                print("Deleting imageId {}", image_id)
                
                ec2.deregister_image(ImageId=image_id)
