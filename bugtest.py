import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# GitHub API 配置
REPO = "pandas-dev/pandas"
TOKEN = "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"  # 替换为你的GitHub令牌
HEADERS = {"Authorization": f"token {TOKEN}"}

def get_one_year_ago_date():
    return (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

def get_issues(repo, since_date):
    issues = []
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/repos/{repo}/issues",
            headers=HEADERS,
            params={
                "state": "closed",
                "since": since_date,
                "labels": "bug",
                "per_page": 100,
                "page": page
            }
        )
        response.raise_for_status()  # 确保请求成功
        new_issues = response.json()
        if not new_issues:
            break  # 没有更多数据，退出循环
        issues.extend(new_issues)
        print(f"Fetched {len(new_issues)} bugs from page {page}.")
        page += 1
        # 为了避免速率限制，可以在这里添加一个小的延迟
        time.sleep(1)
    return issues

# 获取一年前的日期
since_date = get_one_year_ago_date()

# 获取最近一年的bug
recent_one_year_bugs = get_issues(REPO, since_date)

# 将bug数据转换为DataFrame
df_bug = pd.DataFrame(recent_one_year_bugs)

# 转换日期时间列
df_bug['created_at'] = pd.to_datetime(df_bug['created_at'])
df_bug['closed_at'] = pd.to_datetime(df_bug['closed_at'])

# 计算关闭时间
df_bug['time_to_close'] = df_bug['closed_at'] - df_bug['created_at']

# 添加一个新列来表示创建月份
df_bug['created_month'] = df_bug['created_at'].dt.to_period('M')

# 按月统计bug数量
bug_counts_by_month = df_bug.groupby('created_month').size().reset_index(name='bug_count')

# 绘制每个月的bug数量
plt.figure(figsize=(10, 5))
plt.bar(bug_counts_by_month['created_month'].astype(str), bug_counts_by_month['bug_count'])
plt.xlabel('Month')
plt.ylabel('Bug Count')
plt.title('Bugs Count by Month')
plt.xticks(rotation=45)
plt.tight_layout()
#plt.savefig('C://Users\ZHAOYAN\Desktop\Bugs Count by Month.png')
plt.show()


# 定义一个函数，将修复时间分类
def categorize_time(time_delta):
    if time_delta <= timedelta(days=3):
        return '0-3 days'
    elif time_delta <= timedelta(days=7):
        return '4-7 days'
    else:
        return '> 1 week'

# 应用函数，创建一个新的列来表示修复时间区间
df_bug['time_to_close_category'] = df_bug['time_to_close'].apply(categorize_time)

# 统计不同时间区间的bug数量
time_to_close_counts = df_bug['time_to_close_category'].value_counts()

# 绘制修复时间区间的图表
if not time_to_close_counts.empty:
    time_to_close_counts.plot(kind='bar')
    plt.xlabel('Time to Close Category')
    plt.ylabel('Count')
    plt.title('Bugs Count by Time to Close Category')
    plt.xticks(rotation=0)
    plt.tight_layout()
    #plt.savefig('C://Users\ZHAOYAN\Desktop\Bugs Count by Time to Close Category.png')
    plt.show()
else:
    print("No time to close data available for plotting.")



