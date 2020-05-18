import requests
import base64
import io
import sys
import json

from PIL import Image


api_url = 'https://1o0lu10wzk.execute-api.us-east-1.amazonaws.com/Initial/ocr'


if __name__ == '__main__':
	operation = sys.argv[1]

	if operation == 'image-ocr':
		try:
			image_name = sys.argv[2]

		except:
			print ('You need to specify the name of the image file')
			exit(0)

		with open(image_name, 'rb') as f:
			image_bytes = f.read()

		res = requests.get(api_url, json={'operation': operation,
										 'image64': base64.b85encode(image_bytes).decode('utf-8')})
		
		print(res.json()['body'])


	elif operation == 'Fetch':
		try:
			unity_id = sys.argv[2]

		except:
			print ('You need to specify the unityid of the person whose records need to be fetched')
			exit(0)

		res = requests.get(api_url, json={'operation': operation,
										'unity_id': unity_id})

		data = res.json()['body']

		try:
			data = json.loads(data[1:len(data)-1])
			for (key, value) in data.items():
				print (key + ': ' + value)

		except:
			print ('Seemns like UnityID is incorrect')