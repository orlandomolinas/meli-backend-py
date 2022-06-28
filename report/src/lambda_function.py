import json

def lambda_handler(event, context):

    import boto3
    dynamodb = boto3.client('dynamodb')
    pag = dynamodb.get_paginator('scan')
    iterator = pag.paginate(TableName='mutants')
    genx = 0
    gen = 0


    
    for page in iterator:
        for item in page['Items']:
            obj = json.dumps(item)
            print('obj', obj)
            
            print('data', item['state']['S'] != "false")
            value = item['state']['S']
            print('value', value)
            if value == "true":
                genx = genx + 1
            else:
                gen = gen + 1
    
    total = genx + gen
    ratio = gen / total
    return {
        'statusCode': ratio,
        'humans': gen,
        'mutants': genx
        
    }
