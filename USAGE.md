# 使用指南 (Usage Guide)

## 快速开始

### 1. 本地运行

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 配置 GitHub Token (可选但推荐)
为了避免 GitHub API 速率限制，建议配置 GitHub Token：

1. 访问 https://github.com/settings/tokens
2. 生成一个新的 Personal Access Token
3. 设置环境变量：
```bash
export GITHUB_TOKEN=your_github_token_here
```

#### 运行数据采集
```bash
cd src
python main.py
```

运行成功后，数据会保存到 `data/` 目录：
- `data/latest.json` - 最新数据
- `data/daily/YYYY-MM-DD.json` - 每日存档
- `data/history.json` - 历史索引

#### 启动 Web 服务
```bash
# 从项目根目录启动
python -m http.server 8080

# 访问 http://localhost:8080/web/index.html
```

### 2. GitHub Actions 自动化

#### 启用 GitHub Pages

1. 进入仓库的 **Settings** → **Pages**
2. 在 **Source** 下选择 **GitHub Actions**
3. 保存设置

#### 配置工作流

工作流已配置在 `.github/workflows/daily-job.yml`，会：
- 每天 UTC 00:00 (北京时间 08:00) 自动运行
- 收集和排名 GitHub 项目
- 提交数据到仓库
- 部署 Web 界面到 GitHub Pages

#### 手动触发

1. 进入仓库的 **Actions** 标签
2. 选择 "Daily GitHub Trending Projects" 工作流
3. 点击 **Run workflow**

### 3. 自定义配置

编辑 `config.json` 来自定义系统行为：

```json
{
  "github": {
    "search_days": 7,              // 搜索最近 N 天的仓库
    "min_stars": 10,               // 最小 star 数阈值
    "max_results_per_language": 50, // 每种语言的最大结果数
    "languages": [...],            // 要搜索的编程语言列表
    "topics": [...]                // 关注的主题标签
  },
  "ranking": {
    "star_weight": 0.4,            // Star 总数权重
    "growth_rate_weight": 0.3,     // 增长速度权重
    "freshness_weight": 0.2,       // 新鲜度权重
    "topic_relevance_weight": 0.1  // 主题相关性权重
  },
  "output": {
    "max_daily_projects": 100,     // 每日最多展示项目数
    "history_retention_days": 30   // 历史数据保留天数
  }
}
```

## 模块说明

### collector.py - 数据采集模块

负责从 GitHub API 获取仓库数据。

**主要功能：**
- 搜索最近创建的仓库
- 按语言筛选
- 获取仓库详细信息
- 检查 API 速率限制

**示例用法：**
```python
from collector import GitHubCollector

collector = GitHubCollector(token='your_token')
repos = collector.search_repositories(
    created_days_ago=7,
    min_stars=10,
    language='Python',
    max_results=100
)
```

### ranker.py - 排序算法模块

实现多维度评分和排序算法。

**主要功能：**
- 计算项目综合得分
- 多维度评分（star 数、增长率、新鲜度、主题相关性）
- 排序和过滤

**示例用法：**
```python
from ranker import RepositoryRanker

config = {
    'star_weight': 0.4,
    'growth_rate_weight': 0.3,
    'freshness_weight': 0.2,
    'topic_relevance_weight': 0.1
}

ranker = RepositoryRanker(config)
ranked_repos = ranker.rank_repositories(
    repositories,
    trending_topics=['ai', 'machine-learning']
)
```

### storage.py - 数据持久化模块

处理数据的保存和加载。

**主要功能：**
- 保存每日数据
- 加载历史数据
- 管理历史索引
- 清理过期数据

**示例用法：**
```python
from storage import DataStorage

storage = DataStorage()
storage.save_daily_data(repositories, '2025-12-19')
storage.save_latest(repositories)
storage.update_history('2025-12-19', summary)
```

### main.py - 主协调脚本

协调整个系统的运行。

**主要功能：**
- 加载配置
- 协调数据采集、排序、存储
- 生成统计报告
- 清理过期数据

## Web 界面功能

### 主要特性

1. **日期选择**：浏览历史榜单
2. **语言筛选**：按编程语言过滤项目
3. **搜索功能**：搜索项目名称或描述
4. **统计概览**：显示项目总数、热门语言、总 Star 数等
5. **项目详情**：显示完整的项目信息，包括：
   - 项目名称和链接
   - Star 数和增长率
   - 编程语言
   - 描述
   - Topics 标签
   - 许可证信息

### 交互操作

- **点击项目名称**：跳转到 GitHub 仓库
- **点击主题标签**：查看 GitHub 上的相关主题
- **搜索框**：实时搜索（带防抖）
- **语言筛选**：即时过滤结果

## API 速率限制

GitHub API 有以下速率限制：

- **未认证**: 60 次/小时
- **已认证**: 5000 次/小时
- **搜索 API**: 10 次/分钟（未认证），30 次/分钟（已认证）

**建议：**
- 总是使用 GitHub Token
- 合理设置 `max_results_per_language` 以控制 API 调用次数
- 监控 API 速率限制（系统会自动显示剩余配额）

## 数据文件格式

### latest.json / daily/YYYY-MM-DD.json

```json
{
  "date": "2025-12-19",
  "generated_at": "2025-12-19T10:00:00Z",
  "total_count": 100,
  "repositories": [
    {
      "id": 123456789,
      "name": "repo-name",
      "full_name": "user/repo-name",
      "owner": "user",
      "html_url": "https://github.com/user/repo-name",
      "description": "Project description",
      "language": "Python",
      "stars": 1000,
      "forks": 100,
      "watchers": 1000,
      "open_issues": 10,
      "topics": ["ai", "machine-learning"],
      "created_at": "2025-12-15T08:30:00Z",
      "updated_at": "2025-12-19T09:45:00Z",
      "pushed_at": "2025-12-19T09:30:00Z",
      "homepage": "https://example.com",
      "license": "MIT",
      "days_since_creation": 4,
      "stars_per_day": 250.0,
      "score": 92.5,
      "rank": 1
    }
  ]
}
```

### history.json

```json
{
  "dates": [
    {
      "date": "2025-12-19",
      "total_count": 100,
      "top_language": "Python",
      "language_distribution": {
        "Python": 30,
        "JavaScript": 25,
        "TypeScript": 20
      },
      "top_repo": {
        "name": "user/repo",
        "stars": 5000,
        "score": 95.0
      },
      "average_stars": 500.0,
      "total_stars": 50000
    }
  ]
}
```

## 常见问题

### Q: 为什么没有找到任何项目？

A: 可能的原因：
1. API 速率限制已用完 - 配置 GitHub Token
2. 搜索条件太严格 - 降低 `min_stars` 阈值
3. 最近几天没有符合条件的新项目

### Q: 如何增加搜索的项目数量？

A: 编辑 `config.json`：
- 增加 `search_days`（搜索更多天）
- 降低 `min_stars`（降低门槛）
- 增加 `max_results_per_language`

### Q: Web 界面显示"暂无数据"？

A: 确保已运行 `python src/main.py` 生成数据，并且从正确的目录启动 Web 服务器。

### Q: 如何修改评分算法？

A: 编辑 `config.json` 中的 `ranking` 部分，调整各个权重。权重总和应该为 1.0。

### Q: 数据多久更新一次？

A: 
- **GitHub Actions**: 每天自动运行一次
- **本地**: 手动运行 `python src/main.py`

## 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 开启 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
