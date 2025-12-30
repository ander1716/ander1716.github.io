---
layout: page
title: 关于我
permalink: /about
---

<div class="about-container">
  <!-- 个人简介 -->
  <section class="about-section profile-section">
    <div class="profile-header">
      <div class="profile-avatar">
        <span>👨‍💻</span>
      </div>
      <div class="profile-info">
        <h2>Hello, 我是 zyc</h2>
        <p class="profile-bio">全栈开发（偏前端） / 9年工作经验 </p>
        <p class="profile-desc">
          喜欢追逐新技术，开拓视野。目前正深入钻研 <strong>AI 大模型</strong>、<strong>智能体 (Agents)</strong> 及 <strong>RAG</strong> 等前沿领域。
        </p>
      </div>
    </div>
  </section>

  <div class="about-grid">
    <!-- 左侧：技能栈 -->
    <div class="about-col-main">
      <section class="about-section">
        <h3>🛠️ 技术栈</h3>
        
        <div class="skill-group">
          <div class="skill-label">前端开发</div>
          <div class="skill-tags">
            <span class="skill-tag vue">Vue</span>
            <span class="skill-tag react">React</span>
          </div>
        </div>

        <div class="skill-group">
          <div class="skill-label">后端开发</div>
          <div class="skill-tags">
            <span class="skill-tag node">Node.js</span>
            <span class="skill-tag nest">NestJS</span>
            <span class="skill-tag python">Python</span>
            <span class="skill-tag fast">FastAPI</span>
          </div>
        </div>

        <div class="skill-group">
          <div class="skill-label">AI & 大模型</div>
          <div class="skill-tags">
            <span class="skill-tag ai">RAG</span>
            <span class="skill-tag ai">LangChain</span>
            <span class="skill-tag ai">AI Agents</span>
          </div>
        </div>

        <div class="skill-group">
          <div class="skill-label">数据库</div>
          <div class="skill-tags">
            <span class="skill-tag db">MySQL</span>
            <span class="skill-tag db">Chroma</span>
          </div>
        </div>

        <div class="skill-group">
          <div class="skill-label">DevOps</div>
          <div class="skill-tags">
            <span class="skill-tag ops">Linux</span>
            <span class="skill-tag ops">Docker</span>
          </div>
        </div>
      </section>
    </div>

    <!-- 右侧：经历 -->
    <div class="about-col-side">
      <section class="about-section">
        <h3>🎓 经历</h3>
        <ul class="timeline">
          <li class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <div class="timeline-title">全栈开发</div>
              <div class="timeline-time">9 年经验</div>
              <div class="timeline-desc">专注于前端架构与全栈解决方案</div>
            </div>
          </li>
          <li class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <div class="timeline-title">本科</div>
              <div class="timeline-desc">计算机相关专业</div>
            </div>
          </li>
        </ul>
      </section>

      <section class="about-section">
        <h3>💡 关注方向</h3>
        <div class="interests-list">
          <div class="interest-item">🤖 AI 大模型应用</div>
          <div class="interest-item">🧠 智能体 (Agents)</div>
          <div class="interest-item">🔍 检索增强生成 (RAG)</div>
        </div>
      </section>
    </div>
  </div>
</div>

<style>
  .about-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px 0;
  }

  .about-section {
    background: var(--white);
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  }

  .about-section h3 {
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 1.4rem;
    border-left: 4px solid var(--primary-color);
    padding-left: 12px;
  }

  /* Profile Header */
  .profile-header {
    display: flex;
    align-items: center;
    gap: 30px;
  }

  .profile-avatar {
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    flex-shrink: 0;
  }

  .profile-info h2 {
    margin: 0 0 10px 0;
    font-size: 1.8rem;
  }

  .profile-bio {
    color: var(--text-gray);
    font-weight: 500;
    margin-bottom: 10px;
  }

  .profile-desc {
    line-height: 1.6;
    color: var(--text-dark);
  }

  /* Grid Layout */
  .about-grid {
    display: grid;
    grid-template-columns: 3fr 2fr;
    gap: 25px;
  }

  /* Skills */
  .skill-group {
    margin-bottom: 20px;
  }

  .skill-label {
    font-weight: 600;
    margin-bottom: 10px;
    color: var(--text-dark);
    font-size: 1rem;
  }

  .skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .skill-tag {
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 0.9rem;
    background: #f5f7fa;
    color: var(--text-gray);
    border: 1px solid transparent;
    transition: all 0.2s;
  }

  .skill-tag:hover {
    transform: translateY(-2px);
  }

  .skill-tag.vue { background: #eafff5; color: #42b883; border-color: #42b883; }
  .skill-tag.react { background: #f0fdff; color: #61dafb; border-color: #61dafb; }
  .skill-tag.node { background: #f0fff4; color: #68a063; border-color: #68a063; }
  .skill-tag.nest { background: #fff5f5; color: #e0234e; border-color: #e0234e; }
  .skill-tag.python { background: #f7f9ff; color: #306998; border-color: #306998; }
  .skill-tag.ai { background: #fbf5ff; color: #9d4edd; border-color: #9d4edd; }
  .skill-tag.db { background: #fffbe6; color: #faad14; border-color: #faad14; }
  .skill-tag.ops { background: #e6f7ff; color: #1890ff; border-color: #1890ff; }

  /* Timeline */
  .timeline {
    list-style: none;
    padding: 0;
    margin: 0;
    position: relative;
  }

  .timeline::before {
    content: '';
    position: absolute;
    left: 7px;
    top: 5px;
    bottom: 5px;
    width: 2px;
    background: #e5e6eb;
  }

  .timeline-item {
    position: relative;
    padding-left: 30px;
    margin-bottom: 25px;
  }

  .timeline-marker {
    position: absolute;
    left: 0;
    top: 6px;
    width: 16px;
    height: 16px;
    background: var(--white);
    border: 3px solid var(--primary-color);
    border-radius: 50%;
    z-index: 1;
  }

  .timeline-title {
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-dark);
  }

  .timeline-time {
    font-size: 0.85rem;
    color: var(--primary-color);
    margin: 4px 0;
  }

  .timeline-desc {
    font-size: 0.9rem;
    color: var(--text-gray);
    line-height: 1.5;
  }

  /* Interests */
  .interest-item {
    padding: 10px 15px;
    background: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 10px;
    font-size: 0.95rem;
    color: var(--text-dark);
    display: flex;
    align-items: center;
  }

  @media (max-width: 768px) {
    .about-grid {
      grid-template-columns: 1fr;
    }
    
    .profile-header {
      flex-direction: column;
      text-align: center;
    }
  }
</style>