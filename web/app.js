// 全局状态
let allProjects = [];
let filteredProjects = [];
let currentPage = 1;
const projectsPerPage = 20;
let currentDate = '';

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
async function initializeApp() {
    setupEventListeners();
    await loadHistory();
    await loadLatestData();
}

// 设置事件监听
function setupEventListeners() {
    document.getElementById('dateSelect').addEventListener('change', handleDateChange);
    document.getElementById('languageFilter').addEventListener('change', applyFilters);
    document.getElementById('searchInput').addEventListener('input', debounce(applyFilters, 300));
    document.getElementById('refreshBtn').addEventListener('click', refreshData);
    document.getElementById('prevBtn').addEventListener('click', () => changePage(-1));
    document.getElementById('nextBtn').addEventListener('click', () => changePage(1));
}

// Load a data file: deployed site serves it at data/, local repo-root server at ../data/
async function fetchData(path) {
    const response = await fetch(`data/${path}`);
    if (response.ok) {
        return response;
    }
    return fetch(`../data/${path}`);
}

// 加载历史记录
async function loadHistory() {
    try {
        const response = await fetchData('history.json');
        if (!response.ok) {
            throw new Error('History file not found');
        }
        
        const history = await response.json();
        const dateSelect = document.getElementById('dateSelect');
        
        dateSelect.innerHTML = '';
        
        if (history.dates && history.dates.length > 0) {
            history.dates.forEach(entry => {
                const option = document.createElement('option');
                option.value = entry.date;
                option.textContent = formatDate(entry.date);
                dateSelect.appendChild(option);
            });
            
            currentDate = history.dates[0].date;
        }
    } catch (error) {
        console.log('No history file found, will create on first run');
        document.getElementById('dateSelect').innerHTML = '<option value="">no data</option>';
    }
}

// 加载最新数据
async function loadLatestData() {
    showLoading();
    
    try {
        const response = await fetchData('latest.json');
        if (!response.ok) {
            throw new Error('Latest data not found');
        }
        
        const data = await response.json();
        allProjects = data.repositories || [];
        currentDate = data.date;
        
        updateStats(data);
        populateLanguageFilter();
        applyFilters();
        
        document.getElementById('updateTime').textContent = 
            `last_update: ${formatDateTime(data.generated_at)}`;
    } catch (error) {
        console.error('Error loading data:', error);
        showNoResults('暂无数据', '请运行数据采集任务以生成项目列表');
    }
}

// 加载指定日期的数据
async function loadDateData(date) {
    showLoading();
    
    try {
        const response = await fetchData(`daily/${date}.json`);
        if (!response.ok) {
            throw new Error(`Data for ${date} not found`);
        }
        
        const data = await response.json();
        allProjects = data.repositories || [];
        currentDate = date;
        
        updateStats(data);
        populateLanguageFilter();
        applyFilters();
        
        document.getElementById('updateTime').textContent = 
            `last_update: ${formatDateTime(data.generated_at)}`;
    } catch (error) {
        console.error('Error loading date data:', error);
        showNoResults('加载失败', `无法加载 ${date} 的数据`);
    }
}

// 处理日期变更
async function handleDateChange(event) {
    const selectedDate = event.target.value;
    if (selectedDate) {
        await loadDateData(selectedDate);
    }
}

// 刷新数据
async function refreshData() {
    if (currentDate) {
        await loadDateData(currentDate);
    } else {
        await loadLatestData();
    }
}

// 更新统计信息
function updateStats(data) {
    document.getElementById('totalCount').textContent = data.total_count || 0;
    const langCounts = {};
    data.repositories.forEach(repo => {
        if (repo.language) {
            langCounts[repo.language] = (langCounts[repo.language] || 0) + 1;
        }
    });
    const topLang = Object.keys(langCounts).sort((a, b) => langCounts[b] - langCounts[a])[0];
    document.getElementById('topLanguage').textContent = topLang || '-';
    document.getElementById('totalStars').textContent = 
        formatNumber(data.repositories.reduce((sum, repo) => sum + repo.stars, 0));
    document.getElementById('avgStars').textContent = 
        formatNumber(Math.round(data.repositories.reduce((sum, repo) => sum + repo.stars, 0) / data.total_count));
}

// 填充语言筛选器
function populateLanguageFilter() {
    const languages = new Set();
    allProjects.forEach(project => {
        if (project.language) {
            languages.add(project.language);
        }
    });
    
    const languageFilter = document.getElementById('languageFilter');
    const currentValue = languageFilter.value;
    
    languageFilter.innerHTML = '<option value="all">all</option>';
    
    Array.from(languages).sort().forEach(lang => {
        const option = document.createElement('option');
        option.value = lang;
        option.textContent = lang;
        languageFilter.appendChild(option);
    });
    
    languageFilter.value = currentValue;
}

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
    
    currentPage = 1;
    renderProjects();
}

// 渲染项目列表
function renderProjects() {
    const projectsContainer = document.getElementById('projects');
    
    if (filteredProjects.length === 0) {
        showNoResults('未找到匹配的项目', '请尝试调整筛选条件');
        return;
    }
    
    const startIndex = (currentPage - 1) * projectsPerPage;
    const endIndex = startIndex + projectsPerPage;
    const pageProjects = filteredProjects.slice(startIndex, endIndex);
    
    projectsContainer.innerHTML = pageProjects.map(project => createProjectCard(project)).join('');
    
    updatePagination();
}

// 创建项目卡片
function createProjectCard(project) {
    const topics = project.topics && project.topics.length > 0
        ? `<div class="project-topics">
            ${project.topics.slice(0, 5).map(topic =>
                `<a href="https://github.com/topics/${encodeURIComponent(topic)}" target="_blank" rel="noopener" class="topic-tag">#${escapeHtml(topic)}</a>`
            ).join('')}
           </div>`
        : '';

    const homepage = project.homepage && /^https?:\/\//i.test(project.homepage)
        ? `<div class="meta-item">&rarr; <a href="${escapeHtml(project.homepage)}" target="_blank" rel="noopener">homepage</a></div>`
        : '';

    const rank = String(project.rank).padStart(2, '0');

    return `
        <div class="project-card">
            <div class="project-header">
                <div class="project-rank">${rank}</div>
                <div class="project-title">
                    <h2><a href="${escapeHtml(project.html_url)}" target="_blank" rel="noopener">${escapeHtml(project.full_name)}</a></h2>
                    <div class="project-meta">
                        <span class="badge badge-language">${escapeHtml(project.language || 'Unknown')}</span>
                        <span class="badge badge-score">score=${project.score}</span>
                        <div class="meta-item">created: ${formatRelativeTime(project.created_at)}</div>
                        ${homepage}
                    </div>
                </div>
            </div>
            <p class="project-description">${escapeHtml(project.description || '暂无描述')}</p>
            <div class="project-stats">
                <div class="stat-item">stars <b>${formatNumber(project.stars)}</b></div>
                <div class="stat-item hot">stars/day <b>${project.stars_per_day}</b></div>
                <div class="stat-item">forks <b>${formatNumber(project.forks)}</b></div>
                <div class="stat-item">watchers <b>${formatNumber(project.watchers)}</b></div>
                <div class="stat-item">license <b>${escapeHtml(project.license || 'N/A')}</b></div>
            </div>
            ${topics}
        </div>
    `;
}

// 更新分页
function updatePagination() {
    const totalPages = Math.ceil(filteredProjects.length / projectsPerPage);
    
    document.getElementById('pageInfo').textContent = `page ${currentPage}/${totalPages}`;
    document.getElementById('prevBtn').disabled = currentPage === 1;
    document.getElementById('nextBtn').disabled = currentPage === totalPages;
    
    document.getElementById('pagination').style.display = 
        filteredProjects.length > projectsPerPage ? 'flex' : 'none';
}

// 切换页面
function changePage(delta) {
    currentPage += delta;
    renderProjects();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 显示加载状态
function showLoading() {
    document.getElementById('projects').innerHTML = '<div class="loading">fetching data</div>';
}

// 显示无结果
function showNoResults(title, message) {
    document.getElementById('projects').innerHTML = `
        <div class="no-results">
            <h3>${title}</h3>
            <p>${message}</p>
        </div>
    `;
}

// 工具函数：防抖
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 工具函数：格式化数字
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// 工具函数：格式化日期
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 工具函数：格式化日期时间
function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    return date.toLocaleString('zh-CN');
}

// 工具函数：格式化相对时间
function formatRelativeTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    const now = new Date();
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
        return 'today';
    } else if (diffDays === 1) {
        return 'yesterday';
    } else if (diffDays < 7) {
        return `${diffDays}d ago`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks}w ago`;
    } else {
        return formatDate(dateTimeStr);
    }
}

// 工具函数：转义HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
