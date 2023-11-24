import boto3

def lambda_handler(event, context):
    # TODO implement
    ec2_client = boto3.client('ec2')
    
    # Get list of all the regions
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]
    
    # Iterate over each region
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        print("Region:", region)
        
        # Get only running instances
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        
        for instance in instances:
            instance.stop()
            print("Stopped Instance:", instance.id)
