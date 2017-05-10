#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from confluence.ConfluenceClientUtil import ConfluenceClientUtil

print "Executing addWikiPages.py\n"

if confluenceServer is None:
  print "No server provided\n"
  sys.exit(1)

credentials = CredentialsFallback(confluenceServer, username, password).getCredentials()

confluenceClient = ConfluenceClientUtil.createConfluenceClient(confluenceServer, credentials['username'], credentials['password'])

parentPageIdList = confluenceClient.getPageNumbersByTitle(spaceKey, parentPageTitles)

for parentPageNumber in parentPageNumbers:
  parentPageIdList.append(parentPageNumber)

for parentPageId in parentPageIdList:
  confluenceClient.addPage(spaceKey, parentPageId, pageTitle, pageText)
