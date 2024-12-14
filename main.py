import requests
from bs4 import BeautifulSoup
from tkinter import *


class Window:
    def __init__(self, links):
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title("Погода")
        self.check = []
        self.label = Label(self.root, wraplength=800, font=('Arial', 11))
        self.label.grid(row=0, column=0, columnspan=2)
        self.set_text(links)

        self.entry = Entry(self.root, width=50)
        self.entry.grid(row=1, column=0, sticky="E")
        self.btn = Button(self.root, text='myau', command=lambda x=links: self.check_input(links))
        self.btn.grid(row=1, column=1, sticky='W')
        self.label2 = Label(self.root, wraplength=800, font=('Arial', 11))
        self.label2.grid(row=2, column=0, columnspan=2)

    def check_input(self, links):
        choice = self.entry.get()
        if choice not in self.check:
            return
        self.parse_weather(links[choice])

    def parse_weather(self, link):
        weather2 = Weather(link)
        data1 = weather2.soup.find("div", {'id': 'archiveString'})
        temp = data1.find('span', {'class': "t_0"}).text
        text = data1.find('a', {'class': 'ArchiveStrLink'})
        if text is None:
            text = data1.find('div', {'class': 'ArchiveInfo'})
        text = text.text.replace('Архив погоды на метеостанции', "myau")
        self.label2.configure(text=temp + '\n' + text)

    def set_text(self, links):
        text = ''
        for city in links:
            self.check.append(city)
            text += city + ", "
        text = text[:-2]
        self.label.configure(text=text)


class Weather:
    def __init__(self, link):
        self.link = link
        r = requests.get(self.link).text
        self.soup = BeautifulSoup(r, "html.parser")

    def get_cities(self):
        info = self.soup.find_all("a")
        links = {}
        useless_various = ['Главная', '', 'Новости', 'Мобильная версия', "О сайте", "Частые вопросы (FAQ)", 'Контакты',
                           "Беларусь", "Литва", "Россия", "Украина", "Все страны", " 21 сент. 2023", '>>>',
                           "Посмотреть"]
        for block in info:
            text = block.__str__()
            name = block.get_text()
            text = text[text.find('href="'):][6:]
            last = text.find('"')
            text = text[:last]
            if name not in useless_various:
                links[name] = "https://rp5.ru" + text
        sorted_links = {k: v for k, v in sorted(links.items())}
        return sorted_links


w = Weather("https://rp5.ru/Погода_в_России")
data = w.get_cities()
print(data)
win = Window(data)
win.root.mainloop()
