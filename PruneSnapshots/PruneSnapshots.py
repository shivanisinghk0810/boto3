import boto3


def lambda_handler(event, context):
    # TODO implement
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec2 = boto3.client ('ec2')
    regions = [region[RegionName]
               for region in ec2.describe_regions()['Regions']]
    
    for region in regions:
        print(region)
        ec2 = boto3.client('ec2', region_name=region)
        
        response = ec2.describe_snapshots(OwnerIds=[account_id])
        snapshots.sort(key=lambda x: x["StartTime"])
        snapshots = snapshots[:-3]
        
        for snapshot in snapshots:
            id = snapshot['SnapshotId']
            try:
                print("Deleting Snapshots:",id)
                ec2.delete_snapshot(SnapshotId=id)
            except Exception as e:
                if 'InvalidSnapshot.InUse' in e.message:
                    print("Snapshot {} in use, skipping".format(id))
