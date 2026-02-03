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
        <span>🤖</span>
      </div>
      <div class="profile-info">
        <h2>你好，我是 zyc</h2>
        <p class="profile-bio">LLM 应用工程 / 软件工程背景</p>
        <p class="profile-desc">
          具备扎实的软件工程背景，专注于大模型（LLM）应用工程化落地，关注 Agent、RAG、企业级 AI 系统设计与性能优化。
        </p>
        <p class="profile-desc">
          熟悉从需求分析、系统架构设计到开发部署的完整流程，能够将大模型能力稳定地集成到传统业务系统中。
        </p>
        <p class="profile-desc">
          对 LLM、Agent、RAG 等方向有强烈兴趣和自驱力，注重工程质量、可扩展性与真实业务价值。
        </p>
      </div>
    </div>
  </section>

  <div class="about-grid">
    <!-- 左侧：技能栈 -->
    <div class="about-col-main">
      <section class="about-section">
        <h3>🧠 核心技能</h3>

        <div class="skill-group">
          <div class="skill-label">大模型 / AI 应用</div>
          <div class="skill-tags">
            <span class="skill-tag llm">LLM 应用开发流程</span>
            <span class="skill-tag llm">OpenAI / LLaMA 集成</span>
            <span class="skill-tag llm">RAG 技术栈</span>
            <span class="skill-tag llm">向量检索设计与调优</span>
            <span class="skill-tag llm">Agent / Workflow</span>
            <span class="skill-tag llm">多步骤任务拆解</span>
            <span class="skill-tag llm">Prompt Engineering</span>
            <span class="skill-tag llm">模型评估与迭代</span>
          </div>
        </div>

        <div class="skill-group">
          <div class="skill-label">工程与后端</div>
          <div class="skill-tags">
            <span class="skill-tag backend">Python 后端开发</span>
            <span class="skill-tag backend">可维护代码结构</span>
            <span class="skill-tag backend">FastAPI API 服务</span>
            <span class="skill-tag backend">PostgreSQL</span>
            <span class="skill-tag backend">MySQL</span>
            <span class="skill-tag backend">Redis 缓存</span>
            <span class="skill-tag backend">Git 版本管理</span>
            <span class="skill-tag backend">Docker 容器化</span>
          </div>
        </div>

        <div class="skill-group">
          <div class="skill-label">基础设施</div>
          <div class="skill-tags">
            <span class="skill-tag infra">向量数据库 Qdrant</span>
            <span class="skill-tag infra">Milvus</span>
            <span class="skill-tag infra">FAISS</span>
            <span class="skill-tag infra">分布式系统概念</span>
            <span class="skill-tag infra">性能优化思路</span>
            <span class="skill-tag infra">模型部署</span>
            <span class="skill-tag infra">vLLM 推理加速</span>
            <span class="skill-tag infra">ONNX Runtime</span>
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
    border: 1px solid #eef0f3;
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
    background: linear-gradient(135deg, #dbeafe 0%, #f5d0fe 100%);
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
    margin-bottom: 12px;
  }

  .profile-desc {
    line-height: 1.6;
    color: var(--text-dark);
    margin: 0;
  }

  .profile-desc + .profile-desc {
    margin-top: 10px;
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
    gap: 8px;
  }

  .skill-tag {
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    background: #ffffff;
    color: var(--text-dark);
    border: 1px solid #e5e7eb;
    transition: all 0.2s ease;
  }

  .skill-tag:hover {
    transform: translateY(-2px);
  }

  .skill-tag.llm { background: #eef2ff; color: #4338ca; border-color: #c7d2fe; }
  .skill-tag.backend { background: #ecfeff; color: #0e7490; border-color: #a5f3fc; }
  .skill-tag.infra { background: #fdf2f8; color: #be185d; border-color: #fbcfe8; }

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
