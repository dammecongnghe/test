from flask import Flask, jsonify, request, Response
import time

# from freeGPT import AsyncClient
from asyncio import run
from flask_cors import CORS
import sys

sys.path.append("c:/python37/lib/site-packages")
import random
import requests
import json
import html
from pathlib import Path
from typing import Dict, Any, List, Tuple
import string

app = Flask(__name__)
CORS(app)


@app.route("/recommend", methods=["POST"])
async def main():

    # data = request.get_json()
    data = request.get_json()
    prompt = data["searchTerm"]
    print(prompt)

    url = "https://www.aimoviefinder.com/api/demo/gen-text"

    # Define the user's movie description
    user_description = prompt

    # Build the full prompt using f-string
    full_prompt = f"""# YOUR ROLE
    You are "CineSage", a world-class movie expert and detective. You have an encyclopedic knowledge of films from all eras, genres, and countries. Your specialty is identifying a movie from even the most obscure, vague, or partially incorrect descriptions. You are logical, analytical, and precise.
    
    # YOUR TASK
    Your task is to identify a movie based on the user's description. To do this, you must follow a strict two-step process.
    
    ## Step 1: Internal Analysis (Your Thought Process)
    First, you will internally analyze the user's description. You will not show this step in the final output. This is your private thought process.
    1.  **Extract Key Elements:** Identify all potential keywords, actors, plot points, genres, settings, time periods, and emotional tones from the user's description.
    2.  **Formulate Hypotheses:** Based on the extracted elements, generate a list of possible movie candidates. Consider potential user errors (e.g., misremembering an actor).
    3.  **Evaluate Hypotheses:** Assess each hypothesis against the user's description, weighing the evidence.
    4.  **Rank Candidates:** Rank the top 3 most likely candidates based on your evaluation.
    
    ## Step 2: Final JSON Output
    After completing your internal analysis, you will generate the final output. Your output MUST be ONLY a single, valid JSON block, containing the top 3 candidates you identified. Do not include any other text, explanation, or introductions like "Here is the JSON output:".
    
    # USER'S DESCRIPTION
    {user_description}
    
    # REQUIRED JSON OUTPUT FORMAT
    {{
      "candidates": [
        {{
          "title": "Movie Title",
          "year": YYYY,
          "plot_summary": "A brief, one-sentence summary of the plot to help the user confirm.",
          "confidence_score": 0.95,
          "reasoning": "Briefly explain why you think this is the movie, based on the user's description."
        }}
      ]
    }}"""

    # ---- Build the payload (send as JSON, not form-encoded) ----
    payload = {
        "provider": "openrouter",
        ""model": "mistralai/devstral-2512:free",
        "prompt": full_prompt,
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://www.aimoviefinder.com",
        "referer": "https://www.aimoviefinder.com/",
        "user-agent": "Mozilla/5.0",
    }

    # ---- Call API with error handling ----
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
    except requests.RequestException as e:
        # If the request fails, write an error page and exit
        error_html = f"<html><body><pre>Request failed: {html.escape(str(e))}</pre></body></html>"
        Path("results.html").write_text(error_html, encoding="utf-8")
        print("❌ Request failed. Wrote results.html with error.")
        raise SystemExit(1)

    # Parse outer JSON (safely)
    try:
        api_json = response.json()
    except ValueError:
        # Not valid JSON, show raw text in the output page
        raw = response.text[:2000]
        error_html = f"<html><body><pre>Non-JSON response:\n{html.escape(raw)}</pre></body></html>"
        Path("results.html").write_text(error_html, encoding="utf-8")
        print("❌ Non-JSON response. Wrote results.html with raw body.")
        raise SystemExit(1)

    # ---------- helpers ----------
    def esc(s: Any) -> str:
        """HTML-escape text safely."""
        return html.escape("" if s is None else str(s), quote=True)

    def get_fallback_css() -> str:
        # Styles apply when Tailwind isn’t loaded; harmless if it is.
        return """
    <style>
      /* --- icon sizing (works whether or not Tailwind is present) --- */
      svg.lucide { width: 14px; height: 14px; stroke-width: 1.6; }
    
      /* slightly larger in card thumbnail only */
      .card-icon svg.lucide { width: 16px; height: 16px; }
    
      /* badges */
      .pill { font-size: 12px; padding: 2px 8px; border-radius: 9999px;
              border: 1px solid rgba(0,0,0,0.08); }
    
      /* tabs look/feel */
      .tabbase {
        display:flex; flex-direction:column; align-items:center; gap:6px;
        padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(0,0,0,.08);
        background: #fff; transition: background .2s, border-color .2s, color .2s;
      }
      .tabbase:hover { background: rgba(0,0,0,0.03); }
      .tabon   { background: #2563eb; color: #fff; border-color: #2563eb; }
      .taboff  { color: #334155; }
      .tabrank { display:flex; align-items:center; gap:6px; font-size:11px; font-weight:600; }
      .tabtitle{ font-size:12px; font-weight:600; max-width: 120px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
      .tabyear { font-size:11px; color:#6b7280; }
    
      /* card + section */
      .soft-card {
        border: 1px solid rgba(0,0,0,.08);
        background: linear-gradient(135deg, rgba(2,6,23,.04), rgba(2,6,23,.02));
        border-radius: 12px; padding: 16px;
      }
      .soft-panel {
        border: 1px solid rgba(0,0,0,.08);
        background: #fff; border-radius: 12px; padding: 16px;
      }
    
      /* header layout polish */
      .container { max-width: 960px; margin: 24px auto; }
      .muted { color:#6b7280; }
      .headline { font-weight:700; font-size: 20px; margin:6px 0 4px; }
      .section-sub { font-size:12px; color:#6b7280; }
    
      /* small dot pager */
      .dots { display:flex; gap:8px; justify-content:center; margin: 6px 0 14px; }
      .dot { width:8px; height:8px; border-radius:9999px; background:#cbd5e1; }
      .dot.on { background:#64748b; }
    </style>
    """

    def parse_candidates(api_json: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        API returns:
          {"code": 0, "message": "ok", "data": {"text": "<JSON STRING>"}}
        Where data.text is a JSON string containing {"candidates": [...]}
        """
        if not isinstance(api_json, dict) or api_json.get("code") != 0:
            return []
        data = api_json.get("data") or {}
        inner_text = data.get("text")
        if not isinstance(inner_text, str):
            return []
        try:
            inner = json.loads(inner_text)
        except Exception:
            # try to recover a JSON block between braces if provider added extra text
            a, b = inner_text.find("{"), inner_text.rfind("}")
            if a != -1 and b != -1 and b > a:
                try:
                    inner = json.loads(inner_text[a : b + 1])
                except Exception:
                    return []
            else:
                return []
        cands = inner.get("candidates", [])
        return cands if isinstance(cands, list) else []

    def conf_badge(score: Any) -> Tuple[int, str]:
        """Return (percent_int, css_class) for confidence badge."""
        try:
            pct = round(float(score) * 100)
        except Exception:
            pct = 0
        if pct >= 80:
            cls = "bg-green-100 text-green-700 border-green-300 dark:bg-green-900/40 dark:text-green-300 dark:border-green-700"
        elif pct >= 60:
            cls = "bg-orange-100 text-orange-700 border-orange-300 dark:bg-orange-900/30 dark:text-orange-300 dark:border-orange-800/30"
        else:
            cls = "bg-red-100 text-red-700 border-red-200 dark:bg-red-900/30 dark:text-red-400 dark:border-red-800/30"
        return pct, cls

    def build_tabs(cands: List[Dict[str, Any]]) -> str:
        parts = []
        for i, c in enumerate(cands[:3]):
            pct, cls = conf_badge(c.get("confidence_score"))
            if "green" in cls:
                badge = "pill"
            elif "orange" in cls:
                badge = "pill"
            else:
                badge = "pill"

            active = i == 0
            rank_icon = (
                '<svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-trophy"><path d="M10 14.66v1.626a2 2 0 0 1-.976 1.696A5 5 0 0 0 7 21.978"/><path d="M14 14.66v1.626a2 2 0 0 0 .976 1.696A5 5 0 0 1 17 21.978"/><path d="M18 9h1.5a1 1 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M6 9a6 6 0 0 0 12 0V3a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1z"/><path d="M6 9H4.5a1 1 0 0 1 0-5H6"/></svg>'
                if i == 0
                else (
                    '<svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-medal"><path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15"/><path d="M11 12 5.12 2.2"/><path d="m13 12 5.88-9.8"/><path d="M8 7h8"/><circle cx="12" cy="17" r="5"/><path d="M12 18v-2h-.5"/></svg>'
                    if i == 1
                    else '<svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-award"><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/></svg>'
                )
            )

            parts.append(
                f"""
    <button type="button" role="tab" aria-selected="{str(active).lower()}" aria-controls="tab-content-{i}"
            data-state="{ 'active' if active else 'inactive' }" id="tab-trigger-{i}"
            class="tabbase {'tabon' if active else 'taboff'}"
            data-tab-index="{i}">
      <div class="tabrank">{rank_icon}<span>#${i+1}</span></div>
      <div class="text-center" style="line-height:1.15;">
        <div class="tabtitle">{esc(c.get('title'))}</div>
        <div class="tabyear">{esc(c.get('year'))}</div>
      </div>
      <div class="{badge}">{pct}%</div>
    </button>"""
            )
        return "\n".join(parts)

    def build_panel(c: Dict[str, Any], i: int) -> str:
        pct, _cls = conf_badge(c.get("confidence_score"))
        active = i == 0
        return f"""
    <div data-state="{ 'active' if active else 'inactive' }" role="tabpanel"
            aria-labelledby="tab-trigger-{i}" id="tab-content-{i}"
            {'hidden=""' if not active else ''} tabindex="0">
    
        <div class="soft-card" style="margin-bottom:12px;">
        <div style="display:flex; align-items:flex-start; gap:12px;">
            <div class="card-icon" style="width:56px; height:80px; border-radius:10px; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg, rgba(99,102,241,.12), rgba(236,72,153,.10), rgba(249,115,22,.10)); border:1px solid rgba(0,0,0,.06);">
            <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-film"><rect width="18" height="18" x="3" y="3" rx="2"></rect><path d="M7 3v18"></path><path d="M3 7.5h4"></path><path d="M3 12h18"></path><path d="M3 16.5h4"></path><path d="M17 3v18"></path><path d="M17 7.5h4"></path><path d="M17 16.5h4"></path></svg>
            </div>
            <div style="flex:1; min-width:0;">
            <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:10px; margin-bottom:4px;">
                <h4 style="font-size:16px; font-weight:700; margin:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{esc(c.get('title'))}</h4>
                <div class="pill" style="background:#f0fdf4; color:#166534; border-color:#bbf7d0;">{pct}%</div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <div class="pill" style="display:inline-flex; align-items:center; gap:6px;">
                <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-clock"><path d="M12 6v6l4 2"></path><circle cx="12" cy="12" r="10"></circle></svg>
                {esc(c.get('year'))}
                </div>
            </div>
            </div>
        </div>
        </div>
    
        <div class="soft-panel">
        <h5 style="font-size:13px; font-weight:600; display:flex; align-items:center; gap:6px; margin:0 0 8px;">
            <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-align-left"><line x1="3" x2="21" y1="6" y2="6"></line><line x1="3" x2="15" y1="12" y2="12"></line><line x1="3" x2="17" y1="18" y2="18"></line></svg>
            Plot Summary
        </h5>
        <div style="font-size:13.5px; color:#475569; line-height:1.7;">
            <p style="margin:0;">{esc(c.get('plot_summary'))}</p>
        </div>
        </div>
    </div>"""

    # ensure this is imported

    def generate_html(api_json: Dict[str, Any], search_text: str = "") -> str:
        cands = parse_candidates(api_json)[:3]
        n = len(cands)
        tabs_html = build_tabs(cands)
        panels_html = "\n".join(build_panel(c, i) for i, c in enumerate(cands))
        header_search = (
            f'<p class="muted">Search: <span>{esc(search_text)}</span></p>'
            if search_text
            else ""
        )

        tpl = string.Template(
            """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Movie Results</title>
    $fallback_css
    </head>
    <body>
    <div class="container">
        <div class="soft-panel" style="height: 720px; display:flex; flex-direction:column;">
        <div style="padding:14px 16px 12px; border-bottom:1px solid rgba(0,0,0,.06); background:rgba(2,6,23,.03);">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <div style="width:10px; height:10px; background:#22c55e; border-radius:9999px;"></div>
                <span style="font-size:14px; font-weight:600;">$n Perfect Matches Found</span>
            </div>
            <div class="pill" style="display:inline-flex; align-items:center; gap:6px; background:rgba(37,99,235,.1); color:#2563eb; border-color:rgba(37,99,235,.2);">
                <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-zap"><path d="M13 2L3 14h7l-1 8 11-12h-7l1-8z"/></svg>
                AI Powered
            </div>
            </div>
            <div class="headline">🎬 Movie Results</div>
            $header_search
            <div class="section-sub">Click a tab to view details</div>
        </div>
    
        <div style="flex:1; display:flex; flex-direction:column;">
            <div style="padding:14px 16px 8px;">
            <div style="text-align:center; margin-bottom:8px;">
                <div style="font-size:13px; font-weight:600;">🏆 Top 3 AI Matches</div>
                <div class="section-sub">Compact, readable, and balanced</div>
            </div>
    
            <div role="tablist" style="display:grid; grid-template-columns: repeat($grid_cols, minmax(0,1fr)); gap:12px;">
                $tabs_html
            </div>
            </div>
    
            <div style="padding: 10px 16px 16px; flex:1; overflow:auto;">
            $panels_html
            </div>
        </div>
        </div>
    </div>
    
    <script>
        (function(){
        const triggers = document.querySelectorAll('[role="tab"]');
        const panels   = document.querySelectorAll('[role="tabpanel"]');
        triggers.forEach((btn) => {
            btn.addEventListener('click', () => {
            const idx = Number(btn.getAttribute('data-tab-index'));
            triggers.forEach((b, j) => {
                const on = j === idx;
                b.setAttribute('aria-selected', on ? 'true' : 'false');
                b.dataset.state = on ? 'active' : 'inactive';
                b.classList.toggle('tabon', on);
                b.classList.toggle('taboff', !on);
            });
            panels.forEach((p, j) => {
                const on = j === idx;
                p.dataset.state = on ? 'active' : 'inactive';
                if (on) p.removeAttribute('hidden'); else p.setAttribute('hidden', '');
            });
            });
        });
        })();
    </script>
    </body>
    </html>"""
        )

        return tpl.substitute(
            n=n,
            header_search=header_search,
            grid_cols=max(1, n),
            tabs_html=tabs_html,
            panels_html=panels_html,
            fallback_css=get_fallback_css(),
        )

    # ---- Build and write the HTML using the REAL API JSON ----
    html_str = generate_html(api_json, f"“{user_description}”")
    Path("results.html").write_text(html_str, encoding="utf-8")
    print("✅ Wrote results.html")

    # Return raw HTML content directly
    return Response(html_str, status=200, content_type="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
