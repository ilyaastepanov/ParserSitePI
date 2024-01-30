import os
import pathlib
import shutil
import zipfile
from glob import glob
from pathlib import Path
import requests
from bs4 import BeautifulSoup



def get_html():
	url = 'https://sfr.gov.ru/employers/general_information/software/software/'
	r = requests.get(url)
	return r.text


def get_version(html, sp):
	soup = BeautifulSoup(html, 'lxml')
	links = sp.find('section').find_all('h3')[0]

	try:
		txt = open('version_app.txt', 'r+', encoding='utf-8')
	except IOError:
		txt = open('version_app.txt', 'w+', encoding='utf-8')

	txt = open('version_app.txt', 'r', encoding='utf-8')
	url_txt = txt.read().rstrip()
	dir = './dist'

	if dir == pathlib.Path('dist'):
		shutil.rmtree('dist')  # Удаление папки со всеми файлами

	if links.text != url_txt:
		txt_w = open('version_app.txt', 'w', encoding='utf-8')
		txt_w.write(links.text)
		files_z = glob('*.zip')
		for z in files_z:
			os.remove(z)
		return True
	else:
		return False
	

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('section').find_all('a')[1].get('href')
    url = f'https://sfr.gov.ru{links}'
    r = requests.get(url)

    with open(os.path.basename(url), 'wb') as f:
        f.write(r.content)

    for path in Path().rglob('*.zip'):
        with zipfile.ZipFile(path, mode="r") as archive:
            archive.extractall('dist')

    for path in Path().rglob('Запуск_ПОПД.bat'):
        path_link = str(path)[:-15]
        os.chdir(path_link)
        return os.system('Запуск_ПОПД.bat')


def get_bat():
    for path in Path().rglob('Запуск_ПОПД.bat'):
        path_link = str(path)[:-15]
        os.chdir(path_link)
        return os.system('Запуск_ПОПД.bat')


def main():
	soup = BeautifulSoup(get_html(), 'lxml')
	print(get_version(html=get_html(), sp=soup))
	print(get_url(html=get_html(), sp=soup))


if __name__ == '__main__':
	main()
