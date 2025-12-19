# 部署指南 (Deployment Guide)

## GitHub Pages 部署

### 步骤 1: 启用 GitHub Pages

1. 进入仓库页面 `https://github.com/crazycoldking/haowan`
2. 点击 **Settings** (设置)
3. 在左侧菜单中找到 **Pages**
4. 在 **Source** (来源) 部分:
   - 选择 **GitHub Actions** (不要选择 Branch)
5. 点击 **Save** (保存)

### 步骤 2: 触发工作流

#### 方式 1: 手动触发（推荐首次使用）

1. 进入仓库的 **Actions** 标签页
2. 在左侧选择 **"Daily GitHub Trending Projects"** 工作流
3. 点击右上角的 **"Run workflow"** 按钮
4. 选择分支（通常是 `main` 或 `master`）
5. 点击绿色的 **"Run workflow"** 按钮确认

#### 方式 2: 等待自动执行

- 工作流配置为每天 UTC 00:00 (北京时间 08:00) 自动运行
- 首次部署建议手动触发，之后会自动运行

### 步骤 3: 查看部署状态

1. 在 **Actions** 标签页可以看到工作流的运行状态
2. 点击具体的运行记录可以查看详细日志
3. 成功后会显示绿色的 ✓ 标记

### 步骤 4: 访问网站

部署成功后，访问:
```
https://crazycoldking.github.io/haowan/
```

**注意**: 首次部署可能需要等待几分钟才能访问。

## 本地开发和测试

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/crazycoldking/haowan.git
cd haowan

# 运行快速启动脚本
./run.sh
```

### 手动运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 GitHub Token (可选但推荐)
export GITHUB_TOKEN=your_github_token_here

# 3. 运行数据采集
cd src
python main.py
cd ..

# 4. 启动 Web 服务器
python -m http.server 8080

# 5. 在浏览器中访问
# http://localhost:8080/web/index.html
```

## GitHub Token 配置

### 为什么需要 Token？

- **未认证**: GitHub API 限制为 60 次/小时
- **已认证**: 5000 次/小时
- **搜索 API**: 未认证 10 次/分钟，已认证 30 次/分钟

### 如何获取 Token？

1. 访问 https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 设置描述，如 "haowan trending projects"
4. **不需要选择任何权限**（公开数据访问不需要权限）
5. 点击 **"Generate token"**
6. **立即复制 token**（之后无法再看到）

### 在 GitHub Actions 中配置

GitHub Actions 会自动使用 `secrets.GITHUB_TOKEN`，不需要手动配置。这是 GitHub 自动提供的。

### 在本地配置

```bash
# Linux/Mac
export GITHUB_TOKEN=your_token_here

# Windows (PowerShell)
$env:GITHUB_TOKEN="your_token_here"

# Windows (CMD)
set GITHUB_TOKEN=your_token_here
```

或者创建 `.env` 文件:
```
GITHUB_TOKEN=your_token_here
```

## 自定义配置

编辑 `config.json` 来自定义系统行为:

### 搜索配置

```json
{
  "github": {
    "search_days": 7,              // 搜索最近 N 天
    "min_stars": 10,               // 最小 star 数
    "max_results_per_language": 50,// 每种语言的最大结果
    "languages": [                 // 要搜索的语言
      "Python",
      "JavaScript",
      "TypeScript",
      "Go",
      "Rust"
    ]
  }
}
```

### 评分配置

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

**注意**: 所有权重相加应该等于 1.0

### 输出配置

```json
{
  "output": {
    "max_daily_projects": 100,   // 每日最多项目数
    "history_retention_days": 30  // 历史保留天数
  }
}
```

## 工作流配置

### 修改运行时间

编辑 `.github/workflows/daily-job.yml`:

```yaml
on:
  schedule:
    # 当前: 每天 UTC 00:00 (北京时间 08:00)
    - cron: '0 0 * * *'
    
    # 改为每天 UTC 12:00 (北京时间 20:00)
    # - cron: '0 12 * * *'
    
    # 改为每 6 小时一次
    # - cron: '0 */6 * * *'
```

### 禁用自动运行

如果只想手动触发，可以删除 `schedule` 部分，只保留 `workflow_dispatch`:

```yaml
on:
  workflow_dispatch: # 仅允许手动触发
```

## 故障排查

### 问题 1: 工作流失败

**可能原因:**
- API 速率限制
- 网络问题
- 配置错误

**解决方法:**
1. 查看 Actions 日志了解具体错误
2. 检查 API 速率限制
3. 验证 config.json 格式

### 问题 2: 网页无法访问

**可能原因:**
- GitHub Pages 未启用
- 工作流未成功运行
- 部署仍在进行中

**解决方法:**
1. 确认 GitHub Pages 已启用
2. 检查 Actions 是否成功完成
3. 等待几分钟后重试

### 问题 3: 没有找到项目

**可能原因:**
- 搜索条件太严格
- API 速率限制
- 最近没有符合条件的新项目

**解决方法:**
1. 降低 `min_stars` 阈值
2. 增加 `search_days` 范围
3. 配置 GitHub Token

### 问题 4: 数据文件为空

**可能原因:**
- 工作流权限不足
- Git 推送失败

**解决方法:**
1. 检查仓库的 Actions 权限设置
2. 确保工作流有写入权限
3. 查看 Actions 日志

## 进阶配置

### 添加自定义域名

1. 购买域名
2. 在域名提供商处配置 DNS:
   ```
   Type: CNAME
   Name: www (或其他子域名)
   Value: crazycoldking.github.io
   ```
3. 在 GitHub Pages 设置中添加自定义域名
4. 等待 DNS 传播（可能需要几小时）

### 配置 HTTPS

GitHub Pages 自动提供免费的 HTTPS（通过 Let's Encrypt）:
1. 在 Pages 设置中勾选 **"Enforce HTTPS"**
2. 等待证书签发（通常几分钟）

### 监控和通知

可以配置 GitHub Actions 在失败时发送通知:

```yaml
- name: Send notification on failure
  if: failure()
  run: |
    # 发送邮件、Slack 通知等
    echo "Workflow failed!"
```

## 性能优化

### 减少 API 调用

- 减少 `languages` 列表中的语言数量
- 降低 `max_results_per_language` 值
- 增加运行间隔（从每天改为每周）

### 加速数据加载

- 使用 CDN 加速 (GitHub Pages 自带)
- 优化 JSON 文件大小
- 实现数据分页

## 贡献

欢迎提交 Issue 和 Pull Request！

如有问题，请在 GitHub Issues 中提出:
https://github.com/crazycoldking/haowan/issues

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
