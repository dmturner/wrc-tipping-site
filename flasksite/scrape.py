import requests
from bs4 import BeautifulSoup

events = {
    'monte': '42870-rallye-automobile-de-monte-carlo-2018',
    'sweden': '42875-rally-sweden-2018',
    'mexico': '44257-rally-guanajuato-mexico-2018',
    'corsica': '44258-corsica-linea-tour-de-corse-2018',
    'argentina': '44259-ypf-rally-argentina-2018',
    'portugal': '44260-vodafone-rally-de-portugal-2018',
    'sardinia': '44261-rally-italia-sardegna-2018',
    'finland': '44262-neste-rally-finland-2018',
    'germany': '44263-adac-rallye-deutschland-2018',
    'turkey': '44264-marmaris-rally-turkey-2018',
    'gb': '43469-dayinsure-wales-rally-gb-2018',
    'spain': '44265-rallyracc-catalunya-costa-daurada-2018',
    'australia': '44266-kennards-hire-rally-australia-2018'
}

select_box_count = 1

rally_name = 'germany'

entries_list = ['entries']

entries_url = 'https://www.ewrc-results.com/entries/' + events[rally_name] + '/'

response = requests.get(entries_url)
entries = BeautifulSoup(response.text, 'html.parser')

group = entries.select('.startlist tr td:nth-of-type(3) a')

for item in group:
    item = item.get_text().partition(' ')[0]
    entries_list.append(item)

entries_list = entries_list[1::2]
