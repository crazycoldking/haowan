# 🚀 GitHub 好玩项目 - 每日发现

一个自动化系统，用于每日发现 GitHub 上 star 增长较快、具有趣味性或潜力的新项目，并通过 Web 页面进行集中展示。

## ✨ 核心功能

- 🤖 **自动化采集**: 通过 GitHub Actions 每日定时运行
- 📊 **智能排序**: 基于 star 增长速度、新鲜度等多维度评分
- 🔍 **灵活筛选**: 支持按编程语言、主题、关键词筛选
- 📅 **历史数据**: 保留历史榜单，支持按日期浏览
- 🌐 **Web 展示**: 简洁美观的 Web 界面

## 🏗️ 系统架构

```
haowan/
├── .github/workflows/
│   └── daily-job.yml       # GitHub Actions 工作流
├── src/
│   ├── collector.py        # GitHub API 数据采集模块
│   ├── ranker.py           # 评分与排序算法模块
│   ├── storage.py          # 数据持久化模块
│   └── main.py             # 主协调脚本
├── data/
│   ├── daily/              # 每日数据存档
│   ├── latest.json         # 最新榜单数据
│   └── history.json        # 历史记录索引
├── web/
│   ├── index.html          # Web 界面
│   ├── style.css           # 样式文件
│   └── app.js              # 前端逻辑
├── config.json             # 配置文件
└── requirements.txt        # Python 依赖
```

## 🚀 快速开始

### 前置要求

- Python 3.11+
- GitHub Token (可选，用于提高 API 速率限制)

### 本地运行

1. **克隆仓库**
```bash
git clone https://github.com/crazycoldking/haowan.git
cd haowan
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 (可选)**

编辑 `config.json` 自定义配置：
- 搜索天数范围
- 最小 star 数阈值
- 支持的编程语言
- 评分权重等

4. **运行数据采集**
```bash
export GITHUB_TOKEN=your_github_token  # 可选
cd src
python main.py
```

5. **查看 Web 界面**

在浏览器中打开 `web/index.html` 或启动本地服务器：
```bash
cd web
python -m http.server 8000
# 访问 http://localhost:8000
```

### GitHub Pages 部署

1. **启用 GitHub Pages**
   - 进入仓库的 Settings → Pages
   - Source 选择 "GitHub Actions"

2. **触发工作流**
   - 工作流将每天自动运行
   - 也可以在 Actions 标签页手动触发

3. **访问网站**
   - 部署完成后，访问 `https://crazycoldking.github.io/haowan/`

## 📊 评分算法

项目采用多维度评分系统：

| 维度 | 权重 | 说明 |
|------|------|------|
| Star 总数 | 40% | 使用对数归一化，避免大项目垄断 |
| 增长速度 | 30% | Stars per day，反映项目热度 |
| 新鲜度 | 20% | 新创建的项目获得加分 |
| 主题相关性 | 10% | 匹配流行主题的项目加分 |

总分 = (star_score × 0.4 + growth_score × 0.3 + freshness_score × 0.2 + topic_score × 0.1) × 100

## 🎨 Web 界面特性

- 📱 **响应式设计**: 适配桌面和移动设备
- 🔍 **实时搜索**: 快速查找感兴趣的项目
- 🏷️ **多维度筛选**: 按语言、日期筛选
- 📊 **统计概览**: 直观展示数据概况
- 🎯 **分页浏览**: 高效浏览大量项目

## ⚙️ 配置说明

### GitHub API 配置

```json
{
  "github": {
    "search_days": 7,           // 搜索最近几天创建的仓库
    "min_stars": 10,            // 最小 star 数阈值
    "max_results_per_language": 50,  // 每种语言最多返回结果数
    "languages": ["Python", "JavaScript", ...],  // 支持的语言
    "topics": ["ai", "web-development", ...]     // 关注的主题
  }
}
```

### 排序权重配置

```json
{
  "ranking": {
    "star_weight": 0.4,          // Star 总数权重
    "growth_rate_weight": 0.3,   // 增长速度权重
    "freshness_weight": 0.2,     // 新鲜度权重
    "topic_relevance_weight": 0.1 // 主题相关性权重
  }
}
```

### 输出配置

```json
{
  "output": {
    "max_daily_projects": 100,   // 每日最多展示项目数
    "history_retention_days": 30  // 历史数据保留天数
  }
}
```

## 🔧 API 使用

### 数据文件

- `data/latest.json` - 最新榜单
- `data/daily/YYYY-MM-DD.json` - 历史榜单
- `data/history.json` - 历史索引

### 数据格式

```json
{
  "date": "2025-12-19",
  "generated_at": "2025-12-19T00:00:00Z",
  "total_count": 100,
  "repositories": [
    {
      "rank": 1,
      "full_name": "user/repo",
      "html_url": "https://github.com/user/repo",
      "description": "项目描述",
      "language": "Python",
      "stars": 1000,
      "stars_per_day": 50,
      "score": 85.5,
      "topics": ["ai", "machine-learning"],
      ...
    }
  ]
}
```

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 待办事项

- [ ] 添加更多评分维度（如贡献者数量、Issue 活跃度）
- [ ] 支持多种数据持久化方案（SQLite、PostgreSQL）
- [ ] 添加趋势分析和可视化图表
- [ ] 支持自定义主题和样式
- [ ] 添加 RSS 订阅功能
- [ ] 支持多语言界面（英文、中文）
- [ ] 集成更多数据源（GitLab、Gitee）
- [ ] 添加邮件/Webhook 通知功能

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

- **WilliamChen** - *Initial work* - [crazycoldking](https://github.com/crazycoldking)

## 🙏 致谢

- GitHub API - 提供强大的数据接口
- 开源社区 - 持续的灵感来源

## 📮 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue: [GitHub Issues](https://github.com/crazycoldking/haowan/issues)
- Pull Request: [GitHub PRs](https://github.com/crazycoldking/haowan/pulls)

---

⭐ 如果这个项目对你有帮助，请给它一个 Star！