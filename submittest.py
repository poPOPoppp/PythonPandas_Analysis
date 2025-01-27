import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# GitHub API 参数
REPO = "pandas-dev/pandas"
TOKEN = "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"
PER_PAGE = 100  # 每页提交数
MAX_PAGES = 10  # 最大页数

def get_commits(repo, token, per_page=100, page=1):
    """获取仓库的提交历史"""
    url = f"https://api.github.com/repos/{repo}/commits"
    params = {
        'per_page': per_page,
        'page': page
    }
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

# 获取提交数据
all_commits = []
for page in range(1, MAX_PAGES + 1):
    commits = get_commits(REPO, TOKEN, PER_PAGE, page)
    all_commits.extend(commits)
    if len(commits) < PER_PAGE:
        break  # 如果最后一页的提交数少于每页提交数，则停止

# 转换为 DataFrame
data = []
for commit in all_commits:
    author = commit['author']['login'] if commit['author'] else 'Unknown'
    date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
    data.append({
        'author': author,
        'date': date
    })
df = pd.DataFrame(data)


# 将日期字符串转换为 datetime 对象
df['date'] = pd.to_datetime(df['date'])

# 提取日期和小时
df['day'] = df['date'].dt.date
df['hour'] = df['date'].dt.hour

# 分析提交频率
total_commits = len(df)
average_commits_per_day = total_commits / df['day'].nunique()

# 分析贡献者活跃度
contributor_activity = df['author'].value_counts().head(25)

# 分析提交时间分布
hourly_distribution = df['hour'].value_counts().sort_index()

# 分析每日提交数
daily_commits = df['day'].value_counts().sort_index()

# 提交频率图
plt.figure(figsize=(8, 4))
plt.text(0.5, 0.5, f'Total Commits: {total_commits}\nAverage per Day: {average_commits_per_day:.2f}', horizontalalignment='center', verticalalignment='center')
plt.title('Commit Frequency')
plt.axis('off')
#plt.savefig('C://Users\ZHAOYAN\Desktop\commit_frequency.png')
plt.show()

# 贡献者活跃度图
plt.figure(figsize=(12, 6))
sns.barplot(x=contributor_activity.values, y=contributor_activity.index)
plt.title('Top 25 Contributor Activity')
plt.xlabel('Number of Commits')
plt.ylabel('Contributor')
#plt.savefig('C://Users\ZHAOYAN\Desktop\Top 25 Contributor Activity.png')
plt.show()

# 提交时间分布图
plt.figure(figsize=(8, 4))
sns.barplot(x=hourly_distribution.index, y=hourly_distribution.values)
plt.title('Hourly Commit Distribution')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Commits')
#plt.savefig('C://Users\ZHAOYAN\Desktop\Hourly Commit Distribution.png')
plt.show()

# 每日提交数图  
plt.figure(figsize=(12, 6))
sns.lineplot(x=daily_commits.index, y=daily_commits.values)
plt.title('Daily Commit Count')
plt.xlabel('Date')
plt.ylabel('Number of Commits')
plt.xticks(rotation=45)
plt.tight_layout()
#plt.savefig('C://Users\ZHAOYAN\Desktop\Daily Commit Count.png')
plt.show()
