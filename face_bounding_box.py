import httplib, urllib, base64, json,requests,mimetypes,time
from PIL import Image, ImageDraw


subscription_key = ''

uri_base = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
image_uri = raw_input("Enter publically avaiable image to detect faces in: \n")
response = requests.get(image_uri)
content_type = response.headers['content-type']
extension = mimetypes.guess_extension(content_type)
urllib.urlretrieve(image_uri,'wololo_image'+extension)
headers = {
    		'Content-Type': 'application/json',
    		'Ocp-Apim-Subscription-Key': subscription_key,
	  }

params = urllib.urlencode(
	{
		'returnFaceId': 'true',
    		'returnFaceLandmarks': 'false',
    		'returnFaceAttributes': 'age,gender,occlusion,accessories,blur,exposure,noise',
	})

body = "{\"" + 'url\":'+"\""+image_uri+"\""'}'
print "\n\n\n#########################     Request     #########################\n",body

try:
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    print "\n\n\n####################     Response     ####################\n"
    print (json.dumps(parsed[0], sort_keys=True, indent=2))
    top_left_coords = [ parsed[0]['faceRectangle']['left'], parsed[0]['faceRectangle']['top'] ]
    im = Image.open('wololo_image'+extension)
    img_drawer = ImageDraw.Draw(im)
    img_drawer.rectangle([top_left_coords[0],top_left_coords[1],top_left_coords[0]+parsed[0]['faceRectangle']['width'],top_left_coords[1]+parsed[0]['faceRectangle']['width']],outline='red')
    time.sleep(1)
    im.show()

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
