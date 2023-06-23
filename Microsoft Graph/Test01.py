#!/usr/bin/env python

# Needs
# pip install shareplum


from shareplum import Site
from shareplum import Office365
from shareplum.site import Version

import config
import siteinfo

# SharePoint Online credentials
username = config.USERNAME
password = config.PASSWORD
site_url = siteinfo.SHAREPOINT_SITE

# Connect to SharePoint site
authcookie = Office365(site_url, username=username, password=password).GetCookies()
site = Site(site_url, version=Version.v365, authcookie=authcookie)

# SharePoint document library and file information
document_library = siteinfo.SHAREPOINT_LIST_NAME
file_name = "About Pinnacle for Proposals.docx"

# Get document information
file = site.ListItem(file_name, document_library).GetItem()
created_by = file["Created_x0020_By"]
modified_by = file["Modified_x0020_By"]

# Get users' principal names
created_by_principal = site.GetUserLoginFromEmail(created_by)
modified_by_principal = site.GetUserLoginFromEmail(modified_by)

# Print the principal names
print("Created By:", created_by_principal)
print("Modified By:", modified_by_principal)
