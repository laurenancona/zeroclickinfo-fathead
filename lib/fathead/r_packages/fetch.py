from bs4 import BeautifulSoup
import urllib.request
import logging
import time
from socket import timeout

# base_url = "https://cran.r-project.org/"
# cannonical base url for a given package
base_url = "https://cran.r-project.org/package="
# lists all packages
home_url = "https://cran.r-project.org/web/packages/available_packages_by_name.html"
# make request to webpage
timeout = 10
response = urllib.request.urlopen(home_url)
r = response.read()
# make the soup (parse the page)

soup = BeautifulSoup(r, 'html.parser')
package_table = soup.find('table', summary="Available CRAN packages by name.").find_all('a')

# write each page to file
# add in delay
for package in package_table[0:3]:
    package_url = base_url + package.get_text()
    print(package_url)
    try:
        response = urllib.request.urlopen(package_url, timeout = timeout)
        r = response.read()
        f = open('download/' + package.get_text() + '.html', 'wb')
        f.write(r)
        f.close()
    except (HTTPError, URLError) as error:
        logging.error('Data of %s not retrieved because %s\nURL: %s', name, error, package_url)
    except timeout:
        logging.error('socket timed out - URL %s', url)
    else:
        logging.info('Access successful.')
    time.sleep(1)
