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

issue_title = "CLS공지(%s)" % today.strftime("%y.%m.%d")
issue_body = ''
for x in range(24):
	if x == 0:
		issue_body = issue_body + '[공지사항]\n'
	if x == 6:
		issue_body = issue_body + '[취업정보]\n'
	if x == 12:
		issue_body = issue_body + '[장학 및 학생복지]\n'
	if x == 18:
		issue_body = issue_body + '[실무수습 및 봉사활동]\n'
	issue_body = issue_body + listTitle[x] + '\n'
	if x%6 == 5:
		issue_body = issue_body + '----------------------------------\n\n'
issue_body + 'https://law.cnu.ac.kr/law/index.do'

GITHUB_TOKEN = os.environ['GITTO']
REPO_NAME = "MFL"
repo = Github(GITHUB_TOKEN).get_user().get_repo(REPO_NAME)
res = repo.create_issue(title=issue_title, body='')

print(issue_title)
print('----------------------------------\n')
print(issue_body)


