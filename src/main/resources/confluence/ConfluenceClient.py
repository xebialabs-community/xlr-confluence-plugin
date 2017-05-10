#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sets
import sys
import com.xhaus.jyson.JysonCodec as json
from confluence.HttpRequestPlus import HttpRequestPlus

HTTP_SUCCESS = sets.Set([200])

class ConfluenceClient(object):

    def __init__(self, httpConnection, username=None, password=None):
      self.httpConnection = httpConnection
      self.httpRequest = HttpRequestPlus(httpConnection, username, password)

    @staticmethod
    def createClient(httpConnection, username=None, password=None):
      return ConfluenceClient(httpConnection, username, password)

    def addComment(self, pageId, comment):
      contentType = "application/json"
      headers = {'Accept' : 'application/json'}
      addCommentUrl = '/rest/api/content'
      payload = json.loads('{"body":{"storage":{"value":"","representation":"storage"}},"container":{"type":"page","id":""},"type":"comment"}')
      payload['body']['storage']['value'] = comment
      payload['container']['id'] = pageId
      response = self.httpRequest.post(addCommentUrl, json.dumps(payload), contentType=contentType, headers=headers)
      if response.getStatus() not in HTTP_SUCCESS:
        self.throw_error(response)

    def addPage(self, spaceKey, parentPageId, pageTitle, pageText):
      contentType = "application/json"
      headers = {'Accept' : 'application/json'}
      addPageUrl = '/rest/api/content'
      payload = json.loads('{"type":"page", "title":"", "ancestors":[{"id":0}], "space":{"key":""}, "body":{"storage":{"representation":"storage","value":""}}}')
      payload['space']['key'] = spaceKey
      payload['ancestors'][0]['id'] = parentPageId
      payload['title'] = pageTitle
      payload['body']['storage']['value'] = pageText
      response = self.httpRequest.post(addPageUrl, json.dumps(payload), contentType=contentType, headers=headers)
      if response.getStatus() not in HTTP_SUCCESS:
        self.throw_error(response)

    def getPageNumbersByTitle(self, spaceKey, pageTitles):
      contentType = "application/json"
      headers = {'Accept' : 'application/json'}
      pageIdList = []
      for pageTitle in pageTitles:
      	searchByPageTitleUrl = '/rest/api/content?spaceKey=%s&title=%s' % (spaceKey, pageTitle)
        response = self.httpRequest.get(searchByPageTitleUrl, contentType=contentType, headers=headers, quotePlus=True)
        if response.getStatus() not in HTTP_SUCCESS:
          self.throw_error(response)
        result = json.loads(response.response)
        for page in result['results']:
          pageIdList.append(page['id'])
      return pageIdList

