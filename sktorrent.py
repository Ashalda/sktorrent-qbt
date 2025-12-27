#MADE BY ASHALDA
#https://github.com/Ashalda
# VERSION: 1.1

import re
from helpers import retrieve_url
from novaprinter import prettyPrinter
from datetime import datetime

class sktorrent():

    url = 'https://sktorrent.eu'
    name = 'SkTorrent'
    supported_categories = {'all': ''}


    pattern = re.compile(
        r'id=(?P<id>[a-f0-9]+)".*?<br>(?P<name>.*?)</A>\s*'
        r'<br>Velkost (?P<size>[^|]+)\| Pridany (?P<date>\d{2}/\d{2}/\d{4})<br>\s*'
        r'Odosielaju : (?P<seeders>\d+)<br>\s*'
        r'Stahuju : (?P<leechers>\d+)',
        re.S
    )

    def is_empty_page(self, html):
        return "Nenasli ste co ste hladali" in html

    def search(self, what, cat='all'):
        turn = 0
        while True:
            html = retrieve_url(f"https://sktorrent.eu/torrent/torrents_v2.php?search={what}&category=0&zaner=&jazyk=&active=0&page={turn}")

            if self.is_empty_page(html):
                break

            for m in self.pattern.finditer(html):

                id = m.group("id")
                date = m.group("date")
                dt = datetime.strptime(date, "%d/%m/%Y")

                dict = {
                    "link": (f"magnet:?xt=urn:btih:{id}&tr=https%3A%2F%2Fannounce1.sktorrent.eu%2Ftorrent%2Fannounce.php%3Fpid%3D1968a215113a4d87936336557ba8e800&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Fipv4announce.sktorrent.eu%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce"),
                    "name": m.group("name"),
                    "size": m.group("size").strip(),
                    "seeds": m.group("seeders"),
                    "leech": m.group("leechers"),
                    "engine_url": sktorrent.url,
                    "desc_link": (f"https://sktorrent.eu/torrent/details.php?id={id}"),
                    "pub_date": int(dt.timestamp())
                }
            
                prettyPrinter(dict)

            turn += 1

