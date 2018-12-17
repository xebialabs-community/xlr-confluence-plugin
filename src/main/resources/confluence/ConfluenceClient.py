#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sets
import sys
import com.xhaus.jyson.JysonCodec as json
from confluence.HttpRequestPlus import HttpRequestPlus

HTTP_SUCCESS = sets.Set([200, 204])

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

    def deletePage(self, spaceKey, pageId):
      print "Executing deletePage() in ConfluenceClient\n"
      contentType = "application/json"
      headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
      deletePageUrl = '/rest/api/content/%s' % pageId
      response = self.httpRequest.delete(deletePageUrl, contentType=contentType, headers=headers)
      if response.getStatus() not in HTTP_SUCCESS:
        self.throw_error(response)
      print "Success.  Page %s has been deleted.\n" % pageId

    def getPage(self, pageId):
      print "Executing getPage() in ConfluenceClient\n"
      contentType = "application/json"
      headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
      getPageUrl = '/rest/api/content/%s' % pageId
      response = self.httpRequest.get(getPageUrl, contentType=contentType, headers=headers)
      if response.getStatus() not in HTTP_SUCCESS:
        self.throw_error(response)
      return json.loads(response.response)

    def getPageIdsByTitle(self, spaceKey, pageTitles):
      print "Executing getPageIdsByTitle() in ConfluenceClient\n"
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

    def getPageHtmlByTitle(self, spaceKey, pageTitles):
      print "Executing getPageHtmlByTitle() in ConfluenceClient\n"
      pageID = self.getPageIdsByTitle(spaceKey, pageTitles)[0]
      contentType = "application/json"
      headers = {'Accept' : 'application/json'}
      pageList = []
      pageStr = ''
      for pageTitle in pageTitles:
        searchByPageTitleUrl = '/rest/api/content/' + pageID + '?expand=body.storage'
        response = self.httpRequest.get(searchByPageTitleUrl, contentType=contentType, headers=headers, quotePlus=True)
        if response.getStatus() not in HTTP_SUCCESS:
          self.throw_error(response)
        result = json.loads(response.response)
        for page in result['body']['storage']['value']:
          pageStr = pageStr + page

      pageList.append(pageStr)
      return pageList

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

    def updateEnvironmentPage(self, spaceKey, pageTitles, environment, version, application):
      print "Executing updateEnvironmentPage() in ConfluenceClient\n"
      pageID = self.getPageIdsByTitle(spaceKey, pageTitles)[0]
      contentType = "application/json"
      headers = {'Accept' : 'application/json'}
      pageStr = ''
      tmpPageStr = ''
      bappend = True
      bfound = False
      for pageTitle in pageTitles:
        searchByPageTitleUrl = '/rest/api/content/' + pageID + '?expand=body.storage'
        response = self.httpRequest.get(searchByPageTitleUrl, contentType=contentType, headers=headers, quotePlus=True)
        if response.getStatus() not in HTTP_SUCCESS:
          self.throw_error(response)
        result = json.loads(response.response)
        
        for page in result['body']['storage']['value']:
          if bappend:
            pageStr = pageStr + page
            if environment in pageStr and not bfound:
              pageStr = pageStr + '</td><td>'+application+'</td><td>'+version+'</td>' 
              appendbool = False
              bfound = True

          if not bappend and "</tr>" in tmpPageStr:
            pageStr = pageStr + "</tr>"
            appendbool = True
          
          if bfound:
              tmpPageStr = tmpPageStr + page            
      print "********* HTML PAGE > " + pageStr
      self.updatePage(spaceKey, pageID, pageTitles[0], pageStr)


    def throw_error(self, response):
      print "Error from Confluence, HTTP Return: %s\n" % (response.getStatus())
      print response.response
      sys.exit(1)
