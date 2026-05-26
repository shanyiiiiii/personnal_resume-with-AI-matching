#!/usr/bin/env python3
"""统一服务：静态站点 + AI 岗位匹配 API（无需数据库）"""

import json
import os
import re
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

app = Flask(__name__, static_folder=str(ROOT), static_url_path="")

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = os.getenv("ZHIPU_MODEL", "glm-4-flash")

RESUME_PATH = Path(__file__).resolve().parent / "resume.json"


def load_resume() -> dict:
    with open(RESUME_PATH, encoding="utf-8") as f:
        return json.load(f)


def resume_to_text(data: dict) -> str:
    lines = [
        f"姓名：{data['profile']['name']}",
        f"标语：{data['profile']['tagline']}",
        f"\n【个人简介】\n{data['about']['content']}",
        "\n【教育背景】",
    ]
    for edu in data["education"]:
        lines.append(
            f"- {edu['school']} | {edu['degree']} | {edu['period']}"
            + (f" | 荣誉：{edu.get('honors', '')}" if edu.get("honors") else "")
        )
    lines.append("\n【技能特长】")
    for cat in data["skills"]:
        if "tags" in cat:
            tags = ", ".join(cat["tags"])
            lines.append(f"- {cat['category']}：{tags}")
        elif "description" in cat:
            lines.append(f"- {cat['category']}：{cat['description']}")
        else:
            items = ", ".join(f"{i['name']}({i['level']}%)" for i in cat.get("items", []))
            lines.append(f"- {cat['category']}：{items}")
    lines.append("\n【项目经历】")
    for p in data["projects"]:
        lines.append(f"- {p['name']} | {p['role']} | {p['period']}")
        lines.append(f"  技术栈：{', '.join(p['techStack'])}")
        lines.append(f"  描述：{p['description']}")
        for a in p["achievements"]:
            lines.append(f"  · {a}")
    lines.append("\n【工作经历】")
    for exp in data["experience"]:
        lines.append(f"- {exp['company']} | {exp['position']} | {exp['period']}")
        for r in exp["responsibilities"]:
            lines.append(f"  · {r}")
    return "\n".join(lines)


def score_to_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 85:
        return "A-"
    if score >= 80:
        return "B+"
    if score >= 75:
        return "B"
    if score >= 70:
        return "B-"
    if score >= 60:
        return "C"
    return "D"


def call_zhipu(jd: str, resume_text: str) -> dict:
    system_prompt = """你是专业的 HR 与技术招聘顾问。根据候选人完整简历与岗位 JD，输出 JSON 匹配报告。
必须只返回合法 JSON，不要 markdown 代码块，格式如下：
{
  "overallScore": 0-100 的整数,
  "categories": [
    {"name": "学历", "score": 0-100},
    {"name": "工作经验", "score": 0-100},
    {"name": "技能特长", "score": 0-100},
    {"name": "软技能", "score": 0-100}
  ],
  "highlights": [
    {"jd": "JD 中的要求摘要", "candidate": "候选人对应优势或差距"}
  ],
  "summary": "200字以内的综合总结"
}
评分需客观，highlights 至少 3 条最多 6 条。"""

    user_prompt = f"【岗位 JD】\n{jd}\n\n【候选人简历】\n{resume_text}"

    resp = requests.post(
        ZHIPU_API_URL,
        headers={
            "Authorization": f"Bearer {ZHIPU_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        },
        timeout=90,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
    return json.loads(content)


@app.route("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.route("/api/health")
def health():
    return jsonify({"ok": True, "hasApiKey": bool(ZHIPU_API_KEY)})


@app.route("/api/match", methods=["POST"])
def match():
    if not ZHIPU_API_KEY:
        return jsonify({"error": "服务端未配置 ZHIPU_API_KEY"}), 500

    body = request.get_json(silent=True) or {}
    jd = (body.get("jd") or "").strip()
    if len(jd) < 20:
        return jsonify({"error": "请粘贴完整的岗位描述（至少 20 字）"}), 400

    try:
        resume = load_resume()
        resume_text = resume_to_text(resume)
        result = call_zhipu(jd, resume_text)
        score = int(result.get("overallScore", 0))
        result["grade"] = score_to_grade(score)
        result["matchLabel"] = "高度匹配" if score >= 85 else "良好匹配" if score >= 70 else "部分匹配"
        return jsonify(result)
    except requests.HTTPError as e:
        msg = e.response.text if e.response is not None else str(e)
        return jsonify({"error": f"AI 接口调用失败：{msg}"}), 502
    except (json.JSONDecodeError, KeyError) as e:
        return jsonify({"error": f"AI 返回格式异常：{e}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"Resume site running at http://{host}:{port}")
    app.run(host=host, port=port, debug=False)
