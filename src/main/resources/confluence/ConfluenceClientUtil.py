#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from confluence.ConfluenceClient import ConfluenceClient

class ConfluenceClientUtil(object):

    @staticmethod
    def createConfluenceClient(container, username, password):
        return ConfluenceClient.createClient(container, username, password)

