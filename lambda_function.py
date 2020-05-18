import json
import pytesseract
import io
import boto3
import base64

from PIL import Image
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # TODO implement
    operation = event['operation']
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('ocr_table')
    
    
    if operation == 'image-ocr':
        image64 = base64.b85decode(event['image64'])
        res = pytesseract.image_to_string(Image.open(io.BytesIO(image64)))
        
        student_data = {}
        for line in res.split('\n'):
            field, value = line.split(':')
            student_data[field] = value.lstrip()
        
        
        with table.batch_writer() as batch:
            table.put_item(Item=student_data)
            
    elif operation == 'Fetch':
        unity_id = event['unity_id']
        res = table.query(KeyConditionExpression=Key('UnityID').eq(unity_id))['Items']
        
        
    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }
