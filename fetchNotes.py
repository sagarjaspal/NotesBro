import requests
import os
import bs4
import threading
import queue


class FetchNotes(threading.Thread):
    def __init__(self, link, address):
        threading.Thread.__init__(self)
        self.link = link
        self.address = address
        self.queue = queue.Queue()
        print(self.link, '\n', self.address.get())

    def run(self):
        print('Running now!')
        self.fetch_notes(self.link, self.address)

    def fetch_notes(self, link, address):
        site = 'https://lecturenotes.in'
        url = link

        # TODO: Print no. of pages in gui

        os.makedirs('NotesBro', exist_ok=True)
        os.chdir(address.get())

        i = 1
        while not url.endswith('#'):

            res = requests.get(url)
            res.raise_for_status()

            page = bs4.BeautifulSoup(res.text, 'html5lib')
            notesList = page.select('#pic{}'.format(i))

            if not notesList:
                print('Couldn\'t find notes :(')
            else:
                try:
                    notesUrl = notesList[0].get('style')
                    notesUrl = site + notesUrl[22:-39]

                    print('Downloading Page-{}...'.format(i))

                    res = requests.get(notesUrl)
                    res.raise_for_status()

                except requests.exceptions.MissingSchema:
                    prevLink = page.select('#right')[0]
                    url = site + prevLink.get('href')
                    continue

                imageFile = open(os.path.join('{}.jpeg'.format(i)), 'wb')

                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()

                page_no_list = page.find_all('span', {'class': 'total_page'})
                page_val = page_no_list[0].text
                page_val = [int(n) for n in page_val.strip().split() if n.isdigit()]
                pageNo = page_val[0]
                global cur
                cur = (i/pageNo)*100

                self.queue.put(cur)

                # set_progress(cur)

                prevLink = page.select('#right')[0]
                url = site + prevLink.get('href')
            i += 1
        print('Done!')

    def return_queue(self):
        return self.queue
