#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS 
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import com.xhaus.jyson.JysonCodec as json
from confluence.HttpRequestPlus import HttpRequestPlus

print "Executing addCommentToPages.py\n"

pageIdList = []
#payload = '{"body":{"storage":{"value":"<p>This Plugin comment is going to Production</p>","representation":"storage"}},"container":{"type":"page","id":"103843895"},"type":"comment"}}'
payload = json.loads('{"body":{"storage":{"value":"","representation":"storage"}},"container":{"type":"page","id":""},"type":"comment"}')
payload['body']['storage']['value'] = comment

if confluenceServer is None:
  print "No server provided\n"
  sys.exit(1)

contentType = "application/json"
headers = {'Accept' : 'application/json'}

for pageTitle in pageTitles:
  request = HttpRequestPlus(confluenceServer)
  response = request.get('/rest/api/content?spaceKey=%s&title=%s' % (spaceKey, pageTitle), contentType=contentType, headers=headers, quotePlus=True)
  result = json.loads(response.response)
  for page in result['results']:
    pageIdList.append(page['id'])

for pageNumber in pageNumbers:
  pageIdList.append(pageNumber)

for pageId in pageIdList:
  payload['container']['id'] = pageId
  request = HttpRequestPlus(confluenceServer)
  response = request.post('/rest/api/content', json.dumps(payload), contentType=contentType, headers=headers)

