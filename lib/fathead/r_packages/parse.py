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

def clean_text(text):
    text = re.sub('\t', '    ', text)
    return re.sub('\n|\r\n|\r', r'\\n',  text )

def format_abstract(abstract_body, abstract_subtitle):
    clean_body = clean_text(abstract_body)
    clean_subtitle = clean_text(abstract_subtitle)
    return('<section class="prog__container"></section>' +
           '<span class="prog__sub">' + clean_subtitle + '</span>' +
            '<p>' + clean_body + '</p>')
#######################################################
# What has to be surrounded with code?
# abstract:
    # Make sure to wrap the entire abstract in a <section class="prog__container"></section> tag
    # All subtitles should be wrapped in a <span class="prog__sub"></span> element
    # Code snippets should be wrapped in <pre><code></code></pre> tags
    # Descriptions should go inside <p></p> tags, before the code snippets

########################################################
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
fout = 'output.txt'


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

    # add try/except in case these elements are not present
    abstract_subtitle = soup.find('body').find_all('h2')[0].get_text()
    abstract_body     = soup.find('body').find_all('p')[0].get_text()
    # print(abstract_subtitle)
    output['abstract'] = format_abstract(abstract_body, abstract_subtitle)

    # print('%r' % output['abstract'])

    # look for vignettes entries - if present add them to external
    # links
    ex_links = soup.find_all(href = re.compile("vignette"))
    if ex_links:
        external_links = 'Vignettes:'+ r'\n'
        for e in ex_links:
            # append urls together
            external_links += (base_url +  package[:-len(file_ext)] + '/' +
             e.get('href') + r'\n')
        output["ex_links"] = external_links

    # 
    # for key,value in output.items():
    #     print(key,': ', value)
