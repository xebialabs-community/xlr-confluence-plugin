#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import re
import urllib

from java.lang import String

from org.apache.commons.codec.binary import Base64
from org.apache.http import HttpHost
from org.apache.http.client.config import RequestConfig
from org.apache.http.client.methods import HttpGet, HttpHead, HttpPost, HttpPut, HttpDelete, HttpPatch
from org.apache.http.util import EntityUtils
from org.apache.http.entity import StringEntity
from org.apache.http.impl.client import HttpClients

from com.xebialabs.xlrelease.domain.configuration import HttpConnection
from xlrelease.HttpResponse import HttpResponse


class HttpRequestPlus:
    def __init__(self, params, username = None, password = None):
        """
        Builds an HttpRequest

        :param params: an <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a>
        :param username: the username
            (optional, it will override the credentials defined on the <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> object)
        :param password: an password
            (optional, it will override the credentials defined on the <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> object)
        """
        self.params = HttpConnection(params)
        self.username = username
        self.password = password

    def doRequest(self, **options):
        """
        Performs an HTTP Request

        :param options: A keyword arguments object with the following properties :
            method: the HTTP method : 'GET', 'PUT', 'POST', 'DELETE', 'PATCH'
                (optional: GET will be used if empty)
            context: the context url
                (optional: the url on <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> will be used if empty)
            body: the body of the HTTP request for PUT & POST calls
                (optional: an empty body will be used if empty)
            contentType: the content type to use
                (optional, no content type will be used if empty)
            headers: a dictionary of headers key/values
                (optional, no headers will be used if empty)
            quotePlus:  boolean to control quoting with urllib.quote_plus() versus urllib.quote()
                (optional, urllib.quote() will be used if empty or false)
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        request = self.buildRequest(
            options.get('method', 'GET'),
            options.get('context', ''),
            options.get('body', ''),
            options.get('contentType', None),
            options.get('headers', None),
            options.get('quotePlus', False))
        return self.executeRequest(request)


    def get(self, context, **options):
        """
        Performs an HTTP GET Request

        :param context: the context url
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'GET'
        options['context'] = context
        return self.doRequest(**options)


    def head(self, context, **options):
        """
        Performs an HTTP HEAD Request

        :param context: the context url
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'HEAD'
        options['context'] = context
        return self.doRequest(**options)


    def put(self, context, body, **options):
        """
        Performs an HTTP PUT Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'PUT'
        options['context'] = context
        options['body'] = body
        return self.doRequest(**options)


    def post(self, context, body, **options):
        """
        Performs an HTTP POST Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'POST'
        options['context'] = context
        options['body'] = body
        return self.doRequest(**options)


    def delete(self, context, **options):
        """
        Performs an HTTP DELETE Request

        :param context: the context url
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'DELETE'
        options['context'] = context
        return self.doRequest(**options)

    def patch(self, context, body, **options):
        """
        Performs an HTTP PATCH Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'PATCH'
        options['context'] = context
        options['body'] = body
        return self.doRequest(**options)

    def buildRequest(self, method, context, body, contentType, headers, quotePlus):
        url = self.quote(self.createPath(self.params.getUrl(), context), quotePlus)

        method = method.upper()

        if method == 'GET':
            request = HttpGet(url)
        elif method == 'HEAD':
            request = HttpHead(url)
        elif method == 'POST':
            request = HttpPost(url)
            request.setEntity(StringEntity(body))
        elif method == 'PUT':
            request = HttpPut(url)
            request.setEntity(StringEntity(body))
        elif method == 'DELETE':
            request = HttpDelete(url)
        elif method == 'PATCH':
            request = HttpPatch(url)
            request.setEntity(StringEntity(body))
        else:
            raise Exception('Unsupported method: ' + method)

        request.addHeader('Content-Type', contentType)
        request.addHeader('Accept', contentType)
        self.setCredentials(request)
        self.setProxy(request)
        self.setHeaders(request, headers)

        return request


    def createPath(self, url, context):
        url = re.sub('/*$', '', url)
        if context is None:
            return url
        elif context.startswith('/'):
            return url + context
        else:
            return url + '/' + context

    def quote(self, url, quotePlus):
        if quotePlus:
          return urllib.quote_plus(url, ':/?&=%')
        else:
          return urllib.quote(url, ':/?&=%')


    def setCredentials(self, request):
        if self.username:
            username = self.username
            password = self.password
        elif self.params.getUsername():
            username = self.params.getUsername()
            password = self.params.getPassword()
        else:
            return

        encoding = Base64.encodeBase64String(String(username + ':' + password).getBytes('ISO-8859-1'))
        request.addHeader('Authorization', 'Basic ' + encoding)


    def setProxy(self, request):
        if not self.params.getProxyHost():
            return

        proxy = HttpHost(self.params.getProxyHost(), int(self.params.getProxyPort()))
        config = RequestConfig.custom().setProxy(proxy).build()
        request.setConfig(config)


    def setHeaders(self, request, headers):
        if headers:
            for key in headers:
                request.setHeader(key, headers[key])


    def executeRequest(self, request):
        client = None
        response = None
        try:
            client = HttpClients.createDefault()
            response = client.execute(request)
            status = response.getStatusLine().getStatusCode()
            entity = response.getEntity()
            result = EntityUtils.toString(entity, "UTF-8") if entity else None
            headers = response.getAllHeaders()
            EntityUtils.consume(entity)

            return HttpResponse(status, result, headers)
        finally:
            if response:
                response.close()
            if client:
                client.close()
