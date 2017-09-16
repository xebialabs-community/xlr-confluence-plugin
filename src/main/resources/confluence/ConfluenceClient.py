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
      print "Executing __init__() in ConfluenceClient\n"
      self.httpConnection = httpConnection
      self.httpRequest = HttpRequestPlus(httpConnection, username, password)

    @staticmethod
    def createClient(httpConnection, username=None, password=None):
      print "Executing createClient() in ConfluenceClient\n"
      return ConfluenceClient(httpConnection, username, password)

    def addComment(self, pageId, comment):
      print "Executing addComment() in ConfluenceClient\n"
      contentType = "application/json"
      headers = {'Accept' : 'application/json'}
      addCommentUrl = '/rest/api/content'
      payload = json.loads('{"body":{"storage":{"value":"","representation":"storage"}},"container":{"type":"page","id":""},"type":"comment"}')
      payload['body']['storage']['value'] = comment
      payload['container']['id'] = pageId
      response = self.httpRequest.post(addCommentUrl, json.dumps(payload), contentType=contentType, headers=headers)
      if response.getStatus() not in HTTP_SUCCESS:
        self.throw_error(response)
      print "Success.  The comment has been added to page %s.\n" % pageId

    def addPage(self, spaceKey, parentPageId, pageTitle, pageText):
      print "Executing addPage() in ConfluenceClient\n"
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
      print "Success.  The page %s has been added.\n" % pageTitle


    def getPage(self, pageId):
      print "Executing getPage() in ConfluenceClient\n"
      contentType = "application/json"
      headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
      getPageUrl = '/rest/api/content/%s' % pageId
      response = self.httpRequest.get(getPageUrl, contentType=contentType, headers=headers)
      if response.getStatus() not in HTTP_SUCCESS:
        self.throw_error(response)
      return json.loads(response.response)

    def getPageNumbersByTitle(self, spaceKey, pageTitles):
      print "Executing getPageNumbersByTitle() in ConfluenceClient\n"
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

    def updatePage(self, spaceKey, pageId, pageTitle, pageText):
      print "Executing updatePage() in ConfluenceClient\n"
      contentType = "application/json"
      headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
      newVersionNumber = self.getPage(pageId)['version']['number'] + 1
      updatePageUrl = '/rest/api/content/%s' % pageId
      payload = json.loads('{"type":"page", "title":"", "space":{"key":""}, "version":{"number":0}, "body":{"storage":{"representation":"storage","value":""}}}')
      payload['title'] = pageTitle
      payload['space']['key'] = spaceKey
      payload['version']['number'] = newVersionNumber
      payload['body']['storage']['value'] = pageText
      response = self.httpRequest.put(updatePageUrl, json.dumps(payload), contentType=contentType, headers=headers)
      if response.getStatus() not in HTTP_SUCCESS:
        self.throw_error(response)
      print "Success.  Page %s has been updated.\n" % pageId

    def throw_error(self, response):
      print "Error from Confluence, HTTP Return: %s\n" % (response.getStatus())
      print response.response
      sys.exit(1)
