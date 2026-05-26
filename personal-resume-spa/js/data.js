export const resumeData = {
  profile: {
    name: "韩梦蝶",
    tagline: "热衷于Agent的应届研究生",
    avatar: "assets/profile.png",
    contacts: [
      { type: "email", label: "邮箱", value: "hanmengdie814@gmail.com", href: "mailto:hanmengdie814@gmail.com" },
      { type: "github", label: "GitHub", value: "github.com/shanyiiiiii", href: "https://github.com/shanyiiiiii" },
      { type: "wechat", label: "微信", value: "扫一扫添加好友", qr: "assets/wechat-qr.png" },
      { type: "phone", label: "电话", value: "+86 187-3292-4814", href: "tel:+8618732924814" },
    ],
  },

  about: {
    content: `一名计算机视觉方向硕士研究生，关注多模态理解、视觉语言模型与 AI Agent 系统，致力于构建具备感知、推理与自主交互能力的智能应用。`,
  },

  education: [
    {
      school: "河北大学",
      degree: "人工智能 · 学士",
      period: "2020.09 — 2024.06",
      honors: "两次校级学业奖学金二等奖，一次校级学业奖学金三等奖",
      courses: "数据结构与算法、操作系统、计算机网络、计算机组成原理，计算机网络，计算机图形学，离散数学",
    },
    {
      school: "河北大学",
      degree: "计算机科学与技术 · 硕士",
      period: "2024.09 — 2027.06",
      honors: "校级学业奖学金三等奖，发表计算机视觉论文一篇",
      courses: "机器学习，机器视觉，文字识别工程，人工智能",
    },
  ],

  skills: [
    {
      category: "计算机视觉",
      description:
        "熟悉 **Transformer**、**ResNet** 等视觉骨干网络，具备图像预处理、**场景文本识别**与**开放集识别**等方向的实践与科研经验。",
      keywords: ["Transformer", "ResNet", "图像预处理", "场景文本识别", "开放集识别"],
    },
    {
      category: "AI产品经理",
      description:
        "具备 **需求分析**、**产品规划** 与 **PRD 撰写** 能力，关注 **AI 产品策略** 与竞品分析，能通过原型设计与数据驱动方法推进 AI 产品落地。",
      keywords: ["需求分析", "产品规划", "PRD 撰写", "AI 产品策略", "竞品分析"],
    },
    {
      category: "Agent开发",
      description:
        "掌握 **LangChain**、**RAG**、**LLM Agent** 与 **Tool Calling** 等技术，了解 Multi-Agent 协作、**Prompt Engineering** 及 **智谱 AI** 等大模型接入与工作流编排。",
      keywords: ["LangChain", "RAG", "LLM Agent", "Tool Calling", "智谱 AI"],
    },
    {
      category: "工程能力",
      description:
        "熟悉 **Docker**、**Linux**、**Git** 与 **CI/CD** 等工程化工具，能使用 Webpack / Vite 构建前端项目，并借助 vibe coding 提升开发效率。",
      keywords: ["Docker", "Linux", "Git", "CI/CD", "vibe coding"],
    },
    {
      category: "研究能力",
      description:
        "具备论文阅读、**实验设计**、**消融实验** 与模型评估能力，能撰写学术文稿并复现 SOTA 方法，支撑科研与工程验证。",
      keywords: ["论文阅读", "实验设计", "消融实验", "学术写作"],
    },
    {
      category: "其他技能",
      description:
        "扎实的 **数据结构** 与 **C++**、**Java** 基础，**英语 CET-6**，能阅读英文技术文档，具备良好的团队协作能力。",
      keywords: ["数据结构", "C++", "Java", "英语 CET-6", "团队协作"],
    },
  ],

  projects: [
    {
      name: "企业级数据中台可视化系统",
      role: "前端技术负责人",
      period: "2023.01 — 2024.06",
      techStack: ["React", "TypeScript", "ECharts", "Ant Design"],
      description:
        "面向大型制造企业的实时数据监控与报表平台，支持多租户、权限管理与自定义仪表盘配置。",
      achievements: [
        "主导前端架构设计，将首屏加载时间从 4.2s 优化至 1.1s",
        "设计可复用图表组件库，覆盖 20+ 业务场景，复用率达 78%",
        "推动 TypeScript 全面迁移，运行时错误率下降 40%",
      ],
    },
    {
      name: "移动端 H5 营销活动引擎",
      role: "核心开发",
      period: "2022.03 — 2022.12",
      techStack: ["Vue 3", "Vite", "Canvas", "Node.js"],
      description:
        "低代码配置的 H5 活动页面生成平台，运营人员可通过拖拽快速搭建抽奖、签到等活动页。",
      achievements: [
        "实现可视化编辑器，活动上线周期从 3 天缩短至 4 小时",
        "支持百万级并发访问，活动期间零故障",
        "沉淀 15 个活动模板，累计服务 200+ 次营销活动",
      ],
    },
    {
      name: "个人知识管理 Web App",
      role: "独立开发者",
      period: "2021.06 — 2021.12",
      techStack: ["React", "IndexedDB", "PWA"],
      description:
        "离线优先的笔记与知识图谱应用，支持 Markdown 编辑、双向链接与全文搜索。",
      achievements: [
        "GitHub 获得 500+ Stars，被收录于多个开源精选列表",
        "实现 Service Worker 离线缓存，弱网环境下可用性达 99%",
      ],
    },
  ],

  experience: [
    {
      company: "某互联网科技公司",
      position: "高级前端工程师",
      period: "2021.07 — 至今",
      responsibilities: [
        "负责核心产品前端架构演进，制定组件规范与代码审查标准",
        "带领 4 人前端小组完成数据中台、运营后台等关键项目交付",
        "推动性能监控体系建设，Core Web Vitals 指标全面达标",
        "参与技术招聘与新人培养，累计辅导 3 名 junior 工程师独立负责模块",
      ],
    },
    {
      company: "某软件外包公司",
      position: "前端开发工程师",
      period: "2019.07 — 2021.06",
      responsibilities: [
        "参与多个 B 端 SaaS 产品的前端开发与维护",
        "负责从 jQuery 到 Vue 2 的技术栈迁移工作",
        "编写单元测试与 E2E 测试，测试覆盖率提升至 75%",
        "与客户直接沟通需求，独立完成 3 个定制化模块的设计与实现",
      ],
    },
  ],
};

export const tabs = [
  { id: "about", label: "个人浏览" },
  { id: "education", label: "教育背景" },
  { id: "skills", label: "技能特长" },
  { id: "projects", label: "项目经历" },
  { id: "experience", label: "工作经历" },
];
