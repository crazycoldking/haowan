# 贡献指南 (Contributing Guide)

感谢您对本项目的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

如果您发现了 bug，请创建一个 Issue 并包含以下信息：

1. **Bug 描述**: 清晰简洁地描述问题
2. **重现步骤**: 详细列出重现步骤
3. **期望行为**: 描述您期望发生什么
4. **实际行为**: 描述实际发生了什么
5. **环境信息**:
   - 操作系统
   - Python 版本
   - 浏览器版本（如果是前端问题）

### 提出新功能

如果您有新功能建议，请创建一个 Issue 并包含：

1. **功能描述**: 详细描述建议的功能
2. **使用场景**: 说明为什么需要这个功能
3. **可能的实现**: 如果有想法，可以简单描述实现方式

### 提交代码

1. **Fork 仓库**
   ```bash
   # 点击 GitHub 页面上的 Fork 按钮
   ```

2. **克隆您的 Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/haowan.git
   cd haowan
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **进行修改**
   - 遵循现有的代码风格
   - 添加必要的注释
   - 更新相关文档

5. **测试您的修改**
   ```bash
   # 测试 Python 代码
   python src/main.py
   
   # 测试 Web 界面
   python -m http.server 8080
   # 访问 http://localhost:8080/web/
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "描述: 简短描述您的更改"
   ```

7. **推送到您的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 访问原仓库的 GitHub 页面
   - 点击 "New Pull Request"
   - 选择您的分支
   - 填写 PR 描述
   - 提交 PR

## 代码规范

### Python 代码

- 遵循 PEP 8 风格指南
- 使用 4 个空格缩进（不使用 Tab）
- 函数和类要有文档字符串（docstrings）
- 变量名使用 snake_case
- 类名使用 PascalCase
- 常量使用 UPPER_CASE

**示例:**
```python
class RepositoryRanker:
    """Ranks repositories based on multiple factors"""
    
    def __init__(self, config: Dict):
        """
        Initialize ranker with configuration
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
    
    def calculate_score(self, repo: Dict) -> float:
        """
        Calculate score for a repository
        
        Args:
            repo: Repository data dictionary
            
        Returns:
            Calculated score
        """
        # Implementation
        pass
```

### JavaScript 代码

- 使用 2 个空格缩进
- 使用 const/let，避免 var
- 使用箭头函数
- 添加注释说明复杂逻辑

**示例:**
```javascript
// 应用筛选
function applyFilters() {
  const language = document.getElementById('languageFilter').value;
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  
  filteredProjects = allProjects.filter(project => {
    // 语言筛选
    if (language !== 'all' && project.language !== language) {
      return false;
    }
    
    // 搜索筛选
    if (searchTerm) {
      const searchableText = `${project.full_name} ${project.description}`.toLowerCase();
      if (!searchableText.includes(searchTerm)) {
        return false;
      }
    }
    
    return true;
  });
  
  renderProjects();
}
```

### CSS 代码

- 使用有意义的类名
- 保持选择器简单
- 使用注释分隔不同部分
- 移动优先的响应式设计

## 项目结构

```
haowan/
├── src/              # Python 后端代码
│   ├── collector.py  # GitHub API 采集
│   ├── ranker.py     # 评分排序
│   ├── storage.py    # 数据存储
│   └── main.py       # 主程序
├── web/              # 前端代码
│   ├── index.html    # HTML 结构
│   ├── style.css     # 样式
│   └── app.js        # JavaScript 逻辑
├── data/             # 数据文件
└── .github/          # GitHub Actions
```

## 测试指南

### 后端测试

1. **基础功能测试**
   ```bash
   cd src
   python collector.py  # 测试采集器
   python ranker.py     # 测试排序器
   python storage.py    # 测试存储
   ```

2. **完整流程测试**
   ```bash
   python src/main.py
   # 检查 data/ 目录是否生成了数据文件
   ```

### 前端测试

1. **启动本地服务器**
   ```bash
   python -m http.server 8080
   ```

2. **测试功能**
   - 页面加载
   - 语言筛选
   - 搜索功能
   - 日期切换
   - 响应式布局（调整浏览器窗口大小）

3. **浏览器兼容性**
   - Chrome/Edge（最新版）
   - Firefox（最新版）
   - Safari（最新版）

## 提交信息规范

使用清晰的提交信息：

```
类型: 简短描述（不超过 50 字符）

详细描述（可选，72 字符换行）

相关 Issue: #123
```

**类型:**
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式（不影响代码运行）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具

**示例:**
```
feat: 添加 RSS 订阅功能

- 新增 RSS feed 生成器
- 支持订阅最新项目
- 添加 RSS 链接到首页

相关 Issue: #42
```

## 添加新功能的建议

### 1. RSS 订阅功能

**文件:** `src/rss_generator.py`

```python
def generate_rss_feed(repositories: List[Dict]) -> str:
    """Generate RSS feed from repositories"""
    # 实现 RSS XML 生成
    pass
```

### 2. 数据库支持

**文件:** `src/database.py`

```python
class DatabaseStorage:
    """Store data in SQLite/PostgreSQL"""
    
    def __init__(self, db_url: str):
        # 初始化数据库连接
        pass
```

### 3. 邮件通知

**文件:** `src/notification.py`

```python
def send_daily_digest(repositories: List[Dict], email: str):
    """Send daily project digest via email"""
    # 实现邮件发送
    pass
```

### 4. 趋势分析图表

**文件:** `web/charts.js`

```javascript
function renderTrendChart(historicalData) {
  // 使用 Chart.js 或其他库绘制趋势图
}
```

## 文档贡献

文档和代码同样重要！贡献文档的方式：

1. **修正错误**: 发现文档中的错别字或错误
2. **改进说明**: 让说明更清晰易懂
3. **添加示例**: 提供更多使用示例
4. **翻译**: 帮助翻译文档

## 代码审查流程

所有 Pull Request 都会经过以下审查：

1. **代码质量**
   - 遵循代码规范
   - 有适当的注释
   - 代码清晰易懂

2. **功能完整性**
   - 功能按预期工作
   - 没有破坏现有功能
   - 有必要的错误处理

3. **测试**
   - 已经测试过修改
   - 没有引入新的 bug

4. **文档**
   - 更新了相关文档
   - 添加了必要的说明

## 获取帮助

如果您在贡献过程中遇到问题：

1. 查看现有的 Issues 和 Pull Requests
2. 阅读项目文档（README, USAGE, DEPLOYMENT）
3. 创建新的 Issue 提问

## 行为准则

我们致力于提供一个友好、包容的环境：

- 尊重所有贡献者
- 接受建设性批评
- 关注对项目最有利的方面
- 对其他社区成员表现同理心

## 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。

## 感谢

感谢所有贡献者的付出！每一个贡献，无论大小，都很重要。

---

如有任何问题，请随时创建 Issue 或联系维护者。

Happy Coding! 🚀
