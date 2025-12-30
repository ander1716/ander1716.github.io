---
layout: default
title: 文章标签
permalink: /tags.html
---

<div class="wrapper" style="margin-top: 40px">
  <!-- 顶部：标签标题 -->
  <div class="category-header" style="margin-bottom: 30px">
    <h1
      id="tag-title"
      class="section-title"
      style="
        font-size: 1.8rem;
        margin-bottom: 20px;
        border-left: 5px solid var(--primary-color);
        padding-left: 15px;
      "
    >
      文章标签
    </h1>
  </div>
  <div class="main-container">
    <!-- 左侧：标签内容 -->
    <div class="content-column">
      <!-- 文章列表容器 -->
      <div id="tag-posts-container">
        <div
          class="loading"
          style="text-align: center; padding: 40px; color: var(--text-light)"
        >
          加载中...
        </div>
      </div>
    </div>
    <!-- 右侧：侧边栏 -->
    <aside class="sidebar-column">
      <!-- Tag Cloud Widget -->
      {% include sidebar-tags.html %}
    </aside>
  </div>
</div>

<style>
  /* 列表为空时的提示 */
  .empty-state {
    text-align: center;
    padding: 60px;
    background: var(--white);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    color: var(--text-gray);
  }
</style>

<!-- 引入文章卡片渲染函数 -->
{% include post-card-renderer.html %}

<script>
  // 1. 生成所有文章的 JSON 数据
  const allPosts = [
      {% for post in site.posts %}
      {
          title: {{ post.title | jsonify }},
          url: "{{ post.url | relative_url }}",
          date: "{{ post.date | date: '%Y-%m-%d' }}",
          excerpt: {{ post.excerpt | strip_html | truncate: 120 | jsonify }},
          categories: {{ post.categories | jsonify }},
          tags: {{ post.tags | jsonify }}
      }{% unless forloop.last %},{% endunless %}
      {% endfor %}
  ];

  // 2. 渲染文章列表函数
  function renderPosts(tag) {
      const container = document.getElementById('tag-posts-container');
      const titleElement = document.getElementById('tag-title');

      // 处理默认情况
      const targetTag = (tag && tag !== 'all') ? tag : null;

      // 筛选文章
      let filteredPosts = allPosts;
      let displayTitle = '全部标签';

      if (targetTag) {
          // 筛选包含该标签的文章
          filteredPosts = allPosts.filter(post => post.tags && post.tags.includes(targetTag));
          displayTitle = `#${targetTag}`;
  }

      // 更新标题
      titleElement.textContent = displayTitle;

      // 生成 HTML
      if (filteredPosts.length === 0) {
          container.innerHTML = '<div class="empty-state">该标签下暂无文章</div>';
          return;
  }

      const html = filteredPosts.map(post => {
          // 简化的文章列表渲染
          const tagsHtml = post.tags && post.tags.length > 0
              ? `<div class="simple-tags-list">
                  ${post.tags.map(tag => `<span class="simple-tag-pill">${tag}</span>`).join('')}
                 </div>`
              : '';
              
          return `
          <article class="simple-post-card">
              <div class="simple-card-header">
                  <h3 class="simple-post-title"><a href="${post.url}">${post.title}</a></h3>
                  ${tagsHtml}
              </div>
              <p class="simple-post-excerpt">${post.excerpt}</p>
          </article>
          `;
      }).join('');

      container.innerHTML = html;
  }

  // 3. 监听 Hash 变化
  function handleHashChange() {
      // 获取 hash，去掉 # 并解码 (处理中文)
      const hash = decodeURIComponent(window.location.hash.substring(1));
      // 如果没有 hash，或者 hash 为空，显示全部
      renderPosts(hash || 'all');
  }

  // 初始化
  window.addEventListener('hashchange', handleHashChange);
  document.addEventListener('DOMContentLoaded', handleHashChange);
</script>
