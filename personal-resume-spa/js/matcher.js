export function initJobMatcher() {
  const form = document.getElementById("matcher-form");
  const textarea = document.getElementById("matcher-jd");
  const submitBtn = document.getElementById("matcher-submit");
  const modal = document.getElementById("matcher-modal");
  const backdrop = document.getElementById("matcher-backdrop");
  const closeBtn = document.getElementById("matcher-close");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const jd = textarea.value.trim();
    if (jd.length < 20) {
      alert("请粘贴完整的岗位描述（至少 20 字）");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "匹配中…";

    try {
      const res = await fetch("/api/match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jd }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "匹配失败");
      showResult(data);
    } catch (err) {
      alert(err.message || "网络错误，请确认已通过 server/app.py 启动服务");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = '开始匹配 <span aria-hidden="true">→</span>';
    }
  });

  closeBtn?.addEventListener("click", hideModal);
  backdrop?.addEventListener("click", hideModal);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal?.classList.contains("open")) hideModal();
  });

  function hideModal() {
    modal?.classList.remove("open");
    backdrop?.classList.remove("open");
    document.body.style.overflow = "";
  }

  function showResult(data) {
    const score = data.overallScore ?? 0;
    document.getElementById("result-score").textContent = `${score}/100`;
    document.getElementById("result-grade").textContent = data.grade ?? "-";
    document.getElementById("result-label").textContent = data.matchLabel ?? "匹配";

    document.getElementById("result-bars").innerHTML = (data.categories || [])
      .map(
        (c) => `
        <div class="match-bar-row">
          <div class="match-bar-head"><span>${escapeHtml(c.name)}</span><span>${c.score}%</span></div>
          <div class="match-bar-track"><div class="match-bar-fill" style="width:${c.score}%"></div></div>
        </div>
      `
      )
      .join("");

    document.getElementById("result-highlights").innerHTML = (data.highlights || [])
      .map(
        (h) => `
        <li>
          <strong>JD：</strong>${escapeHtml(h.jd)}<br/>
          <strong>候选人：</strong>${escapeHtml(h.candidate)}
        </li>
      `
      )
      .join("");

    document.getElementById("result-summary").textContent = data.summary ?? "";

    modal.classList.add("open");
    backdrop.classList.add("open");
    document.body.style.overflow = "hidden";
  }
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
