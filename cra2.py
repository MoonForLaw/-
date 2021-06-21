import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from github import Github, Issue
import datetime
from pytz import timezone
from dateutil.parser import parse
import os

KST = timezone('Asia/Seoul')
today = datetime.datetime.now(KST)

def isDateInRange(created_at):
    suffix_KST = '.000001+09:00'
    created_at = parse(created_at + suffix_KST)
    yesterday = today - datetime.timedelta(1)
    return today > created_at and created_at > yesterday

url = 'https://law.cnu.ac.kr/law/index.do'

response = requests.get(url)

html = response.text
soup = BeautifulSoup(html, 'html.parser')

listTitle = []
for x in range(24):
	temp = soup.select(".articleTitle")[x].get_text()
	temp = temp.replace('\t', '').replace('\n', '')
	listTitle.append(temp)

GITHUB_TOKEN = os.environ['GitTo']
REPO_NAME = "MFL"
repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)

if issue_body != '' and REPO_NAME == repo.name:
	issue_title = "CLS공지(%s)" % today.strftime("%y.%m.%d")
	print(issue_title)
	print('----------------------------------\n')
	for x in range(24):
		if x == 0:
			print('[공지사항]')
		if x == 6:
			print('[취업정보]')
		if x == 12:
			print('[장학 및 학생복지]')
		if x == 18:
			print('[실무수습 및 봉사활동]')
		print(listTitle[x])
		if x%6 == 5:
			print('----------------------------------\n')
	print('https://law.cnu.ac.kr/law/index.do')
