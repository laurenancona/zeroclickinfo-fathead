###############################################################
#
# Description: Import all fetched html files in the
# /download directory, parse out info for output.txt
# file for fathead - relating to all listed R packages
# on the CRAN site
#
##############################################################
from os import listdir
import re
from bs4 import BeautifulSoup
# parse each of the different articles for the output.txt file

# "1. Full Article Title\n",
# "2. Type of Entry: A - article, D - Disambiguation Pages (list of articles), R - Redirects\n",
# "3. Alias - (only applies to redirects)\n",
# "4. Empty field (put requires place holder)\n",
# "5. Categories - article can belong to multiple categories\n",
# "6. Empty field (requires place holder)\n",
# "7. Related Topics - list of links to be displayed\n",
# "8. Empty field\n",
# "9. External Links\n",
# "10. Content of disambiguation page (only applies to disambiguation pages)\n",
# "11. Image - link to image url\n",
# "12. Abstract - contains all content you wish to display\n",
# "13. URL - source domain\n"

file_ext = '.html'
package_list = listdir('download')
base_url = "https://cran.r-project.org/package="

for package in package_list:
    # initialize output dict
    output = dict(title = '\t',
                  entry_type = '\t',
                  alias = '\t',
                  category = '\t',
                  related_topics = '\t',
                  ex_links = '\t',
                  disam_page = '\t',
                  image = '\t',
                  abstract = '\t',
                  url = '\t')
    # get all 'required fields'
    # may want to add in protections?

    # title and entry type
    output['title'] = package[:-len(file_ext)] + '\t'
    output['entry_type'] = 'A\t'
    output['url'] = base_url + package[:-len(file_ext)] + '\t'

    # ABSTRACT
    fin = open('download/' + package, "r")
    r = fin.read()
    fin.close()
    soup = BeautifulSoup(r, 'html.parser')
    output['abstract'] = soup.find('body').find_all('p')[0].get_text() + '\t'

    # look for vignettes entries - if present add them to external
    # links
    try:
        ex_links = soup.find_all(href = re.compile("vignette"))
        for e in ex_links:
            print(base_url +  package[:-len(file_ext)] + '/' + e.get('href'))
    except:
        pass

    # for key,value in output.items():
    #     print(key,': ', value)
