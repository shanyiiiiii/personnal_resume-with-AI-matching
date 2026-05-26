import { resumeData, tabs } from "./data.js";
import { initJobMatcher } from "./matcher.js";

const ICONS = {
  email: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>`,
  github: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>`,
  wechat: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8.5 7C5.46 7 3 9.13 3 11.75c0 1.45.78 2.73 2.05 3.58L4.5 18l2.55-1.28c.73.2 1.5.31 2.3.31 3.04 0 5.5-2.13 5.5-4.75S11.54 7 8.5 7zm-1.2 2.8h2.4v1.2H7.3v-1.2zm4.8 0h2.4v1.2h-2.4v-1.2zM20 5c-2.76 0-5 2.02-5 4.5 0 1.28.65 2.42 1.68 3.18L15.5 14l2.2-1.1c.58.1 1.18.16 1.8.16 2.76 0 5-2.02 5-4.5S22.76 5 20 5zm-2.5 2.5h2v1h-2v-1zm-4 0h2v1h-2v-1z"/></svg>`,
  phone: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>`,
  external: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>`,
};

const SKILL_ICONS = {
  vision: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`,
  product: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 13h6M9 17h4"/></svg>`,
  agent: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M6 20v-1a6 6 0 0112 0v1"/><path d="M17 11l2 2-2 2M7 11l-2 2 2 2"/></svg>`,
  deeplearning: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a4 4 0 014 4c0 1.95-1.4 3.58-3.25 3.93L12 22l-.75-12.07A4.001 4.001 0 0112 2z"/><path d="M8 6.5C5.5 7.5 4 9.5 4 12s1.5 4.5 4 5.5M16 6.5c2.5 1 4 3 4 5.5s-1.5 4.5-4 5.5"/></svg>`,
  backend: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>`,
  engineering: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>`,
  research: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3h6v7H9z"/><path d="M10 14h4v7h-4z"/><path d="M4 14h4v4H4zM16 14h4v4h-4z"/></svg>`,
  other: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`,
};

const PROJECT_ICONS = ["⚡", "🎯", "🚀", "💡", "📊", "✨"];

let currentTab = "about";

function parseBold(text) {
  return text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
}

function getPrimaryEmail() {
  return resumeData.profile.contacts.find((c) => c.type === "email")?.href || "#";
}

function getAllSkillNames() {
  return resumeData.skills.flatMap((cat) => cat.keywords || cat.tags || []);
}

function renderNav() {
  const navEl = document.getElementById("nav-tabs");
  navEl.innerHTML = tabs
    .map(
      (tab) => `
      <button
        type="button"
        class="nav-tab${tab.id === currentTab ? " active" : ""}"
        data-tab="${tab.id}"
        id="tab-${tab.id}"
        aria-selected="${tab.id === currentTab}"
      >
        ${tab.label}
      </button>
    `
    )
    .join("");

  navEl.querySelectorAll(".nav-tab").forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  document.getElementById("logo-link")?.addEventListener("click", (e) => {
    e.preventDefault();
    switchTab("about");
  });
}

function renderProjectCards(compact = false) {
  return resumeData.projects
    .map((p, i) => {
      if (compact) {
        const visualClass = `project-card-visual--${(i % 3) + 1}`;
        return `
          <article class="project-card">
            <div class="project-card-visual ${visualClass}" aria-hidden="true">${PROJECT_ICONS[i % PROJECT_ICONS.length]}</div>
            <div class="project-card-body">
              <h4 class="project-card-name">${p.name}</h4>
              <p class="project-card-desc">${p.description}</p>
              <a href="#" class="project-card-link" data-goto="projects" aria-label="查看 ${p.name} 详情">
                查看详情 ${ICONS.external}
              </a>
            </div>
          </article>
        `;
      }

      return `
        <article class="project-detail-card">
          <h3 class="project-card-name">${p.name}</h3>
          <p class="project-meta">${p.role} · ${p.period}</p>
          <div class="project-tech">
            ${p.techStack.map((t) => `<span class="tech-tag">${t}</span>`).join("")}
          </div>
          <p class="project-card-desc">${p.description}</p>
          <ul class="project-achievements">
            ${p.achievements.map((a) => `<li>${a}</li>`).join("")}
          </ul>
        </article>
      `;
    })
    .join("");
}

function bindProjectLinks(container) {
  container.querySelectorAll("[data-goto]").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      switchTab(link.dataset.goto);
    });
  });
}

function renderAbout() {
  const { profile, about } = resumeData;
  const paragraphs = about.content.trim().split(/\n\n+/);
  const emailHref = getPrimaryEmail();

  const contactsHtml = profile.contacts
    .map((c) => {
      if (c.type === "wechat") {
        return `
      <button type="button" class="contact-link contact-link--wechat" id="btn-wechat" title="${c.label}" aria-label="${c.label}：${c.value}">
        ${ICONS.wechat}
      </button>`;
      }
      return `
      <a class="contact-link" href="${c.href}" target="_blank" rel="noopener noreferrer" title="${c.label}" aria-label="${c.label}">
        ${ICONS[c.type] || ICONS.email}
      </a>`;
    })
    .join("");

  const el = document.getElementById("section-about");
  el.innerHTML = `
    <div class="hero">
      <div class="hero-content">
        <h1 class="hero-greeting">Hi，我是 ${profile.name}</h1>
        <p class="hero-role" id="hero-role">${profile.tagline}<span class="cursor" aria-hidden="true"></span></p>
        <div class="hero-intro">
          ${paragraphs.map((p) => `<p>${parseBold(p)}</p>`).join("")}
        </div>
        <div class="hero-actions">
          <button type="button" class="btn btn-outline" id="btn-print">下载简历</button>
          <a class="btn btn-mint" href="${emailHref}">联系我</a>
        </div>
        <nav class="hero-contacts" aria-label="联系方式">${contactsHtml}</nav>

        <section class="matcher-section" aria-labelledby="matcher-title">
          <p class="matcher-label" id="matcher-title">AI 岗位匹配器</p>
          <form class="matcher-box" id="matcher-form">
            <textarea
              id="matcher-jd"
              class="matcher-input"
              rows="3"
              placeholder="粘贴目标岗位的 Job Description（JD），AI 将对照本站全部简历内容进行匹配分析…"
              required
            ></textarea>
            <button type="submit" class="matcher-submit" id="matcher-submit">
              开始匹配 <span aria-hidden="true">→</span>
            </button>
          </form>
        </section>
      </div>
      <div class="hero-visual">
        <div class="avatar-frame">
          <img class="hero-avatar" src="${profile.avatar}" alt="${profile.name} 的头像" />
        </div>
      </div>
    </div>
  `;

  document.getElementById("btn-print")?.addEventListener("click", () => window.print());
  initWeChatModal(profile.contacts.find((c) => c.type === "wechat"));
  initJobMatcher();
}

function initWeChatModal(wechatContact) {
  const btn = document.getElementById("btn-wechat");
  const modal = document.getElementById("wechat-modal");
  const backdrop = document.getElementById("wechat-backdrop");
  const closeBtn = document.getElementById("wechat-close");
  const img = document.getElementById("wechat-qr-img");

  if (!btn || !modal || !wechatContact?.qr) return;

  img.src = wechatContact.qr;
  img.alt = `${wechatContact.label}二维码`;

  const open = () => {
    modal.classList.add("open");
    backdrop.classList.add("open");
    document.body.style.overflow = "hidden";
  };

  const close = () => {
    modal.classList.remove("open");
    backdrop.classList.remove("open");
    document.body.style.overflow = "";
  };

  btn.addEventListener("click", open);
  closeBtn?.addEventListener("click", close);
  backdrop?.addEventListener("click", close);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("open")) close();
  });
}

function renderEducation() {
  const el = document.getElementById("section-education");
  const items = resumeData.education
    .map(
      (edu) => `
      <article class="timeline-item">
        <h3 class="timeline-school">${edu.school}</h3>
        <p class="timeline-degree">${edu.degree}</p>
        <p class="timeline-period">${edu.period}</p>
        ${edu.honors ? `<p class="timeline-detail"><strong>荣誉：</strong>${edu.honors}</p>` : ""}
        ${edu.courses ? `<p class="timeline-detail"><strong>核心课程：</strong>${edu.courses}</p>` : ""}
      </article>
    `
    )
    .join("");

  el.innerHTML = `
    <h2 class="section-page-title">教育背景</h2>
    <div class="timeline-wrap"><div class="timeline">${items}</div></div>
  `;
}

function renderSkills() {
  const el = document.getElementById("section-skills");
  const categories = resumeData.skills
    .map(
      (cat) => `
      <article class="skills-category">
        <h3 class="skill-category-title">${cat.category}</h3>
        <p class="skill-description">${parseBold(cat.description)}</p>
      </article>
    `
    )
    .join("");

  el.innerHTML = `
    <h2 class="section-page-title">技能特长</h2>
    <div class="skills-wrap">${categories}</div>
  `;
}

function renderProjects() {
  const el = document.getElementById("section-projects");
  el.innerHTML = `
    <h2 class="section-page-title">项目经历</h2>
    <div class="projects-page-grid">${renderProjectCards(false)}</div>
  `;
}

function renderExperience() {
  const el = document.getElementById("section-experience");
  const skillTags = getAllSkillNames().slice(0, 8);

  const cards = resumeData.experience
    .map((exp, index) => {
      const tagsHtml = skillTags
        .slice(index * 4, index * 4 + 4)
        .map((t) => `<span class="experience-tag">${t}</span>`)
        .join("");

      const projectsBlock =
        index === 0
          ? `
          <div class="section-divider">项目经历</div>
          <div class="projects-grid">${renderProjectCards(true)}</div>
        `
          : "";

      return `
        <article class="experience-card">
          <header class="experience-card-header">
            <div>
              <h3 class="experience-card-title">${exp.company}</h3>
              <p class="experience-card-sub">${exp.position}</p>
            </div>
            <time class="experience-card-period">${exp.period}</time>
          </header>
          <div class="experience-card-body">
            <ul>
              ${exp.responsibilities.map((r) => `<li>${r}</li>`).join("")}
            </ul>
          </div>
          <div class="experience-tags">${tagsHtml}</div>
          ${projectsBlock}
        </article>
      `;
    })
    .join("");

  el.innerHTML = `
    <h2 class="section-page-title">工作经历</h2>
    <div class="experience-list">${cards}</div>
  `;

  bindProjectLinks(el);
}

function switchTab(tabId) {
  if (tabId === currentTab) return;

  const prevSection = document.getElementById(`section-${currentTab}`);
  const nextSection = document.getElementById(`section-${tabId}`);

  prevSection.classList.add("leaving");
  prevSection.classList.remove("active");

  setTimeout(() => {
    prevSection.classList.remove("leaving");
    prevSection.style.display = "none";

    nextSection.style.display = "block";
    nextSection.classList.add("active");

    currentTab = tabId;
    document.querySelectorAll(".nav-tab").forEach((btn) => {
      const isActive = btn.dataset.tab === tabId;
      btn.classList.toggle("active", isActive);
      btn.setAttribute("aria-selected", isActive);
    });

    window.scrollTo({ top: 0, behavior: "smooth" });

    if (tabId === "experience") {
      bindProjectLinks(nextSection);
    }
  }, 300);
}

function init() {
  document.title = `${resumeData.profile.name} · 个人动态简历`;
  renderNav();
  renderAbout();
  renderEducation();
  renderSkills();
  renderProjects();
  renderExperience();

  document.querySelectorAll(".content-section").forEach((section) => {
    if (!section.classList.contains("active")) {
      section.style.display = "none";
    }
  });
}

init();
