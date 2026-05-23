"""Interactive widget renderers for each activity type.

Each widget is a self-contained HTML/JS component embedded via
streamlit.components.v1.html. Widgets handle their own state in JavaScript
so they update smoothly without forcing Streamlit reruns.
"""

from __future__ import annotations

import html
import json
from typing import Any

import streamlit.components.v1 as components

from activities import Activity

# Shared styles + a font import. Each widget inlines its own scoped CSS to keep
# components self-contained inside the iframe.
_BASE_STYLE = """
<link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --pale-blue: #ebf9ff;
    --pastel-blue: #a5daff;
    --komodo-blue: #55b5f2;
    --vibrant-blue: #3d92e6;
    --komodo-navy: #064471;
    --light-green: #77eed6;
    --pastel-green: #d2ffe6;
    --white: #ffffff;
    --black-blue: #001f34;
    --score-red: #e53b19;
    --score-good-green: #3d8f70;
  }
  * { box-sizing: border-box; }
  body {
    font-family: 'Epilogue', 'Inter', sans-serif;
    color: var(--black-blue);
    margin: 0;
    padding: 0;
    background: transparent;
  }
  .panel {
    background: var(--white);
    border: 2px solid var(--black-blue);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 10px rgba(0,31,52,0.08);
  }
  .btn {
    background: var(--vibrant-blue);
    color: var(--white);
    border: 3px solid var(--black-blue);
    border-radius: 30px;
    font-weight: 700;
    font-family: 'Epilogue', sans-serif;
    font-size: 1rem;
    padding: 10px 22px;
    cursor: pointer;
    transition: background 0.15s ease;
    margin: 4px;
  }
  .btn:hover { background: var(--light-green); color: var(--black-blue); }
  .btn.secondary { background: var(--pastel-blue); color: var(--black-blue); }
  .btn.secondary:hover { background: var(--light-green); }
  .btn.ghost { background: var(--white); color: var(--black-blue); }
  .btn.ghost:hover { background: var(--pale-blue); }
  .btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .label { font-weight: 700; color: var(--komodo-navy); }
  .muted { color: #2a4458; }
</style>
"""


def render(activity: Activity) -> None:
    """Render the interactive widget for an activity."""
    t = activity.interactive_type
    if t == "breathe":
        _five_finger_breathing(activity)
    elif t == "bilateral":
        _bilateral_taps(activity)
    elif t == "stepped":
        _stepped_flow(activity)
    elif t == "list_prompts":
        _list_prompts(activity)
    elif t == "timer_simple":
        _timer_simple(activity)
    elif t == "weather_pick":
        _weather_pick(activity)
    elif t == "colour_breath":
        _colour_breath(activity)
    elif t == "motion_picker":
        _motion_picker(activity)
    elif t == "canvas":
        _canvas(activity)
    else:
        _fallback(activity)


# ---------- Widget: simple countdown timer with animated motion ----------
def _timer_simple(activity: Activity) -> None:
    cfg = activity.widget_config
    seconds = cfg.get("seconds", activity.duration_minutes * 60)
    prompt = cfg.get("prompt", "Move freely")
    finish_prompt = cfg.get("finish_prompt", "Take a deep breath in… and out.")
    # Activity-specific animation: "stomp_shake" | "squeeze" | None.
    animation = cfg.get("animation", "")

    # Per-animation HTML/CSS — chosen from a small library so each timer-based
    # activity gets visual feedback matching its physical action.
    anim_blocks = {
        "stomp_shake": """
            <div class="anim-stage" id="stage">
              <div class="arms-row">
                <div class="arm" id="armL">🙌</div>
                <div class="arm" id="armR">🙌</div>
              </div>
              <div class="feet-row">
                <div class="foot" id="footL">👟</div>
                <div class="foot" id="footR">👟</div>
              </div>
            </div>
            <style>
              .anim-stage { display:flex; flex-direction:column; gap: 14px; align-items:center; margin: 10px 0 18px; }
              .arms-row, .feet-row { display:flex; gap: 36px; }
              .arm, .foot { font-size: 3.4rem; line-height: 1; padding: 6px; }
              .running .arm   { animation: shake 0.25s ease-in-out infinite; }
              .running .arm:nth-child(2)  { animation-delay: 0.12s; }
              .running .foot  { animation: stomp 0.45s ease-in-out infinite; }
              .running .foot:nth-child(2) { animation-delay: 0.22s; }
              @keyframes shake { 0%,100% { transform: rotate(0deg); } 50% { transform: rotate(-15deg); } }
              @keyframes stomp { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-18px) rotate(-6deg); } }
            </style>
        """,
        "squeeze": """
            <div class="anim-stage" id="stage">
              <div class="squeeze-block" id="squeezer">🧻</div>
              <div class="hands-row">
                <div class="hand-emoji" id="handL">🤜</div>
                <div class="hand-emoji" id="handR">🤛</div>
              </div>
            </div>
            <style>
              .anim-stage { display:flex; flex-direction:column; align-items:center; gap: 8px; margin: 10px 0 18px; }
              .squeeze-block { font-size: 4rem; line-height: 1; padding: 8px; transition: transform 0.4s ease; }
              .hands-row { display:flex; gap: 60px; }
              .hand-emoji { font-size: 3rem; line-height: 1; padding: 6px; transition: transform 0.4s ease; }
              .running .squeeze-block { animation: squish 0.9s ease-in-out infinite; }
              .running #handL { animation: pushR 0.9s ease-in-out infinite; }
              .running #handR { animation: pushL 0.9s ease-in-out infinite; }
              @keyframes squish { 0%,100% { transform: scaleX(1) scaleY(1); } 50% { transform: scaleX(0.7) scaleY(1.15); } }
              @keyframes pushR  { 0%,100% { transform: translateX(0); }       50% { transform: translateX(22px); } }
              @keyframes pushL  { 0%,100% { transform: translateX(0); }       50% { transform: translateX(-22px); } }
            </style>
        """,
    }
    anim_html = anim_blocks.get(animation, "")

    components.html(
        f"""
{_BASE_STYLE}
<div class="panel" style="text-align:center;">
  <div style="font-size:1.1rem; font-weight:700; color:var(--komodo-navy); margin-bottom:8px;">
    DO THIS NOW
  </div>
  <div id="prompt" style="font-size:1.3rem; margin:14px 0 14px; min-height:48px; padding: 6px 0;">
    {html.escape(prompt)}
  </div>
  {anim_html}
  <div id="time" style="font-size:5.5rem; font-weight:700; color:var(--komodo-navy); line-height:1;">
    {seconds:02d}
  </div>
  <div style="margin-top:14px;">
    <button id="start" class="btn">▶ Start</button>
    <button id="pause" class="btn secondary">⏸ Pause</button>
    <button id="reset" class="btn ghost">↺ Reset</button>
  </div>
</div>
<script>
(function() {{
  const total = {seconds};
  let remaining = total;
  let running = false;
  let interval = null;
  const tEl = document.getElementById('time');
  const pEl = document.getElementById('prompt');
  const stage = document.getElementById('stage');
  const finish = {json.dumps(finish_prompt)};
  const startPrompt = {json.dumps(prompt)};

  function setRunning(v) {{
    running = v;
    if (stage) stage.classList.toggle('running', v);
  }}
  function fmt(s) {{
    if (s >= 60) {{
      const m = Math.floor(s/60);
      const ss = (s % 60).toString().padStart(2, '0');
      return m + ':' + ss;
    }}
    return s.toString().padStart(2, '0');
  }}
  function render() {{
    tEl.textContent = fmt(remaining);
    if (remaining === 0) {{
      tEl.style.color = 'var(--score-good-green)';
      pEl.innerHTML = '<strong>✅ ' + finish + '</strong>';
      setRunning(false);
    }} else if (remaining <= 5) {{
      tEl.style.color = 'var(--score-red)';
    }} else {{
      tEl.style.color = 'var(--komodo-navy)';
    }}
  }}
  document.getElementById('start').onclick = () => {{
    if (running) return;
    setRunning(true);
    pEl.textContent = startPrompt;
    interval = setInterval(() => {{
      if (remaining > 0) {{ remaining--; render(); }}
      else {{ clearInterval(interval); setRunning(false); }}
    }}, 1000);
  }};
  document.getElementById('pause').onclick = () => {{
    setRunning(false);
    if (interval) clearInterval(interval);
  }};
  document.getElementById('reset').onclick = () => {{
    setRunning(false);
    if (interval) clearInterval(interval);
    remaining = total;
    pEl.textContent = startPrompt;
    render();
  }};
  render();
}})();
</script>
""",
        height=540 if anim_html else 360,
    )


# ---------- Widget: stepped flow (auto-advance optional) ----------
def _stepped_flow(activity: Activity) -> None:
    steps = list(activity.steps)
    auto_secs = activity.widget_config.get("auto_advance_seconds", 0)

    payload_steps = [
        {
            "icon": s.get("icon", "•"),
            "label": s.get("label", ""),
            "body": s.get("body", ""),
        }
        for s in steps
    ]

    components.html(
        f"""
{_BASE_STYLE}
<style>
  .progress-row {{ display:flex; gap:6px; margin-bottom:18px; }}
  .progress-cell {{
    flex:1; height:8px; border-radius:6px;
    background: var(--pale-blue); border: 1.5px solid var(--black-blue);
    transition: background 0.3s;
  }}
  .progress-cell.done {{ background: var(--light-green); }}
  .progress-cell.current {{ background: var(--vibrant-blue); }}
  .step-icon {{
    font-size: 4rem;
    line-height: 1.2;
    display: block;
    margin: 18px 0 14px;
    padding: 8px 0;
  }}
  .step-label {{ font-size: 1.6rem; font-weight:700; color: var(--komodo-navy); margin: 16px 0 12px; line-height: 1.25; }}
  .step-body  {{ font-size: 1.15rem; line-height:1.55; white-space: pre-line; color: var(--black-blue); margin-top: 10px; padding: 0 6px; }}
  .step-counter {{ color: var(--komodo-blue); font-weight:700; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; }}
  .timer-pill {{
    display:inline-block; padding: 4px 12px; border-radius: 999px;
    background: var(--pastel-blue); border: 2px solid var(--black-blue);
    font-weight:700; font-size: 0.85rem; margin-left:8px;
  }}
</style>
<div class="panel">
  <div class="progress-row" id="progress"></div>
  <div style="text-align:center; padding: 12px 8px 18px;">
    <div class="step-counter">
      <span id="step-num"></span>
      <span class="timer-pill" id="auto-pill" style="display:none;">▶ auto-advance: <span id="auto-secs"></span>s</span>
    </div>
    <div class="step-icon" id="step-icon"></div>
    <div class="step-label" id="step-label"></div>
    <div class="step-body" id="step-body"></div>
  </div>
  <div style="text-align:center; margin-top:8px;">
    <button id="prev" class="btn ghost">◀ Previous</button>
    <button id="auto" class="btn secondary">▶ Auto-play</button>
    <button id="next" class="btn">Next ▶</button>
  </div>
</div>
<script>
(function() {{
  const steps = {json.dumps(payload_steps)};
  const autoSecs = {auto_secs};
  let idx = 0;
  let autoInterval = null;
  let autoRemaining = autoSecs;

  const prog = document.getElementById('progress');
  const stepNum = document.getElementById('step-num');
  const stepIcon = document.getElementById('step-icon');
  const stepLabel = document.getElementById('step-label');
  const stepBody = document.getElementById('step-body');
  const autoPill = document.getElementById('auto-pill');
  const autoSecsEl = document.getElementById('auto-secs');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const autoBtn = document.getElementById('auto');

  function buildProgress() {{
    prog.innerHTML = '';
    steps.forEach((_, i) => {{
      const cell = document.createElement('div');
      cell.className = 'progress-cell';
      prog.appendChild(cell);
    }});
  }}
  function stopAuto() {{
    if (autoInterval) clearInterval(autoInterval);
    autoInterval = null;
    autoPill.style.display = 'none';
    autoBtn.textContent = '▶ Auto-play';
  }}
  function startAuto() {{
    if (!autoSecs) return;
    autoRemaining = autoSecs;
    autoSecsEl.textContent = autoRemaining;
    autoPill.style.display = 'inline-block';
    autoBtn.textContent = '⏸ Stop auto';
    autoInterval = setInterval(() => {{
      autoRemaining--;
      autoSecsEl.textContent = autoRemaining;
      if (autoRemaining <= 0) {{
        if (idx < steps.length - 1) {{
          idx++; render(); autoRemaining = autoSecs; autoSecsEl.textContent = autoRemaining;
        }} else {{
          stopAuto();
        }}
      }}
    }}, 1000);
  }}
  function render() {{
    const s = steps[idx];
    stepNum.textContent = `Step ${{idx + 1}} of ${{steps.length}}`;
    stepIcon.textContent = s.icon;
    stepLabel.textContent = s.label;
    stepBody.textContent = s.body;
    Array.from(prog.children).forEach((c, i) => {{
      c.classList.remove('done', 'current');
      if (i < idx) c.classList.add('done');
      if (i === idx) c.classList.add('current');
    }});
    prev.disabled = (idx === 0);
    next.disabled = (idx === steps.length - 1);
  }}
  prev.onclick = () => {{ if (idx > 0) {{ idx--; render(); }} stopAuto(); }};
  next.onclick = () => {{ if (idx < steps.length - 1) {{ idx++; render(); }} stopAuto(); }};
  autoBtn.onclick = () => {{
    if (autoInterval) {{ stopAuto(); }} else {{ startAuto(); }}
  }};
  if (!autoSecs) {{ autoBtn.style.display = 'none'; }}

  buildProgress();
  render();
}})();
</script>
""",
        height=520,
    )


# ---------- Widget: list of prompts with input boxes + submit/celebrate ----------
def _list_prompts(activity: Activity) -> None:
    steps = list(activity.steps)
    examples = activity.widget_config.get("examples", [])

    items = []
    for s in steps:
        items.append({
            "icon": s.get("icon", "•"),
            "label": s.get("label", ""),
            "placeholder": s.get("placeholder", ""),
            "count": int(s.get("count", 1)),
            "multiline": bool(s.get("multiline", False)),
        })

    examples_html = ""
    if examples:
        items_html = "".join(f"<li>{html.escape(e)}</li>" for e in examples)
        examples_html = (
            f"<details style='margin-bottom:16px;'><summary style='cursor:pointer; font-weight:700; color:var(--komodo-navy);'>"
            f"💡 Sentence starters (click to open)</summary>"
            f"<ul style='margin:8px 0 0 18px; line-height:1.7;'>{items_html}</ul></details>"
        )

    components.html(
        f"""
{_BASE_STYLE}
<style>
  .prompt-row {{
    margin-bottom: 16px; padding: 14px 16px;
    background: var(--pale-blue); border: 2px solid var(--black-blue); border-radius: 12px;
  }}
  .prompt-row .head {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
  .prompt-row .head .icon {{ font-size:1.6rem; padding: 4px 0; }}
  .prompt-row .head .text {{ font-weight:700; font-size:1.05rem; color: var(--komodo-navy); }}
  .input-row {{ display:flex; gap:8px; margin-top:6px; }}
  .input-row input, .input-row textarea {{
    flex:1; padding: 10px 12px; border:2px solid var(--black-blue);
    border-radius: 8px; font-family: 'Epilogue', sans-serif; font-size: 1rem;
    background: var(--white); color: var(--black-blue);
  }}
  .input-row input:focus, .input-row textarea:focus {{
    outline: none; border-color: var(--vibrant-blue);
    box-shadow: 0 0 0 3px rgba(61,146,230,0.25);
  }}
  .check-num {{
    background: var(--white); border: 2px solid var(--black-blue); border-radius: 999px;
    min-width: 30px; height: 30px; display:flex; align-items:center; justify-content:center;
    font-weight: 700; color: var(--komodo-navy);
  }}
  .check-num.filled {{ background: var(--light-green); }}
  textarea {{ min-height: 60px; resize: vertical; }}
  .actions-row {{
    display: flex; gap: 8px; justify-content: flex-end; align-items: center;
    margin-top: 14px; flex-wrap: wrap;
  }}
  .progress-text {{ margin-right: auto; color: var(--komodo-navy); font-weight: 700; font-size: 0.92rem; }}

  /* ---- Celebration overlay ---- */
  .panel {{ position: relative; overflow: hidden; }}
  .celebrate {{
    display: none;
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(180deg, var(--pastel-green) 0%, var(--white) 100%);
    border: 2px solid var(--black-blue);
    border-radius: 16px;
    position: relative;
  }}
  .celebrate.show {{ display: block; animation: pop 0.45s ease-out; }}
  .celebrate .big-emoji {{
    font-size: 5rem;
    line-height: 1;
    margin-bottom: 12px;
    animation: bounce 0.6s ease-out 0.1s 2;
  }}
  .celebrate .msg {{
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--komodo-navy);
    margin-bottom: 6px;
  }}
  .celebrate .sub {{ color: var(--komodo-navy); margin-bottom: 18px; }}
  @keyframes pop {{
    0%   {{ transform: scale(0.7); opacity: 0; }}
    70%  {{ transform: scale(1.05); opacity: 1; }}
    100% {{ transform: scale(1); }}
  }}
  @keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50%      {{ transform: translateY(-12px); }}
  }}

  /* ---- Confetti ---- */
  .confetti-stage {{
    position: absolute; inset: 0; pointer-events: none; overflow: hidden; z-index: 5;
  }}
  .confetti-piece {{
    position: absolute; top: -20px;
    width: 10px; height: 18px;
    border-radius: 2px;
    animation: confetti-fall 2.4s cubic-bezier(.22,.61,.36,1) forwards;
  }}
  @keyframes confetti-fall {{
    0%   {{ transform: translateY(-30px) rotate(0deg); opacity: 1; }}
    100% {{ transform: translateY(700px) rotate(720deg); opacity: 0; }}
  }}
</style>
<div class="panel">
  <div class="confetti-stage" id="confetti"></div>
  <div id="form-view">
    {examples_html}
    <div id="rows"></div>
    <div class="actions-row">
      <div class="progress-text" id="prog"></div>
      <button id="reset" class="btn ghost">↺ Clear</button>
      <button id="submit" class="btn">✨ Submit</button>
    </div>
  </div>
  <div id="celebrate" class="celebrate">
    <div class="big-emoji">🎉</div>
    <div class="msg" id="celebrate-msg">Nice work!</div>
    <div class="sub" id="celebrate-sub">You've completed this activity.</div>
    <button id="again" class="btn">↺ Try again</button>
  </div>
</div>
<script>
(function() {{
  const items = {json.dumps(items)};
  const rows = document.getElementById('rows');
  const formView = document.getElementById('form-view');
  const celebrate = document.getElementById('celebrate');
  const progEl = document.getElementById('prog');
  const confetti = document.getElementById('confetti');
  let totalInputs = 0;

  function buildRow(item, rowIdx) {{
    const row = document.createElement('div');
    row.className = 'prompt-row';
    row.innerHTML = `
      <div class="head">
        <div class="icon">${{item.icon}}</div>
        <div class="text">${{item.label}}</div>
      </div>
    `;
    for (let i = 0; i < item.count; i++) {{
      const ir = document.createElement('div');
      ir.className = 'input-row';
      const num = document.createElement('div');
      num.className = 'check-num';
      num.textContent = item.count > 1 ? (i+1) : '✎';
      const inp = item.multiline ? document.createElement('textarea') : document.createElement('input');
      inp.placeholder = item.placeholder;
      if (!item.multiline) inp.type = 'text';
      inp.addEventListener('input', () => {{
        if (inp.value.trim().length > 0) num.classList.add('filled');
        else num.classList.remove('filled');
        updateProgress();
      }});
      ir.appendChild(num);
      ir.appendChild(inp);
      row.appendChild(ir);
      totalInputs++;
    }}
    rows.appendChild(row);
  }}
  function updateProgress() {{
    const filled = rows.querySelectorAll('.check-num.filled').length;
    progEl.textContent = filled > 0 ? `${{filled}} of ${{totalInputs}} filled in` : '';
  }}

  function spawnConfetti() {{
    const colors = ['#55b5f2','#77eed6','#ffc30f','#f5a6c0','#3d92e6','#2cdd9c','#ffb37a'];
    for (let i = 0; i < 40; i++) {{
      const p = document.createElement('div');
      p.className = 'confetti-piece';
      p.style.left = (Math.random() * 100) + '%';
      p.style.background = colors[Math.floor(Math.random() * colors.length)];
      p.style.animationDuration = (1.6 + Math.random() * 1.4) + 's';
      p.style.animationDelay = (Math.random() * 0.4) + 's';
      confetti.appendChild(p);
    }}
    setTimeout(() => {{ confetti.innerHTML = ''; }}, 3500);
  }}

  items.forEach((it, i) => buildRow(it, i));
  updateProgress();

  document.getElementById('reset').onclick = () => {{
    rows.querySelectorAll('input, textarea').forEach(el => el.value = '');
    rows.querySelectorAll('.check-num').forEach(el => el.classList.remove('filled'));
    updateProgress();
  }};

  document.getElementById('submit').onclick = () => {{
    const filled = rows.querySelectorAll('.check-num.filled').length;
    formView.style.display = 'none';
    celebrate.classList.add('show');
    document.getElementById('celebrate-sub').textContent =
      filled > 0
        ? `You shared ${{filled}} thing${{filled === 1 ? '' : 's'}}. Well done!`
        : "You completed this activity. Well done!";
    spawnConfetti();
  }};

  document.getElementById('again').onclick = () => {{
    celebrate.classList.remove('show');
    formView.style.display = '';
    rows.querySelectorAll('input, textarea').forEach(el => el.value = '');
    rows.querySelectorAll('.check-num').forEach(el => el.classList.remove('filled'));
    updateProgress();
  }};
}})();
</script>
""",
        height=_estimate_list_height(items),
    )


def _estimate_list_height(items: list[dict[str, Any]]) -> int:
    """Roughly size the iframe based on number of inputs.
    Add a healthy floor so Submit/celebrate always have room."""
    h = 200  # base (examples + actions + celebrate fits)
    for it in items:
        h += 90  # row header + spacing (was 80, increase for new padding)
        per_input = 100 if it.get("multiline") else 64
        h += per_input * max(1, int(it.get("count", 1)))
    # Cap raised so Five senses (5+4+3+2+1 inputs) fits comfortably
    return min(h, 1600)


# ---------- Widget: five-finger breathing (animated hand SVG) ----------
def _five_finger_breathing(activity: Activity) -> None:
    cfg = activity.widget_config
    in_s = cfg.get("in_seconds", 4)
    out_s = cfg.get("out_seconds", 4)
    cycles = cfg.get("cycles", 10)

    components.html(
        f"""
{_BASE_STYLE}
<style>
  .breath-row {{
    display:flex; align-items:center; gap:36px;
    justify-content:center; flex-wrap:wrap;
  }}
  svg.hand {{ width: 260px; height: 300px; flex-shrink: 0; }}
  /* Realistic-ish hand: rounded fingertips, gradient skin tone, soft shadows */
  .finger {{
    fill: #ffe0c4;
    stroke: var(--black-blue); stroke-width: 2.5;
    transition: fill 0.5s ease;
  }}
  .finger.active {{ fill: var(--vibrant-blue); }}
  .finger.tracing {{ fill: var(--light-green); }}
  .palm {{ fill: #ffe0c4; stroke: var(--black-blue); stroke-width: 2.5; }}
  .knuckle {{ fill: none; stroke: rgba(0,31,52,0.25); stroke-width: 1.5; }}

  /* Side-by-side: hand on left, fixed-size pulse stage on right with text below
     so the expanded circle never overlaps the text. */
  .info-col {{
    display:flex; flex-direction:column; align-items:center;
    flex: 1; min-width: 240px; max-width: 320px;
  }}
  .pulse-stage {{
    width: 220px; height: 220px;
    display:flex; align-items:center; justify-content:center;
    flex-shrink: 0;
  }}
  .breath-circle {{
    width: 130px; height: 130px; border-radius:50%;
    background: var(--pastel-blue); border: 4px solid var(--black-blue);
    transition: transform 4s ease, background 0.8s ease;
  }}
  .breath-circle.in {{ transform: scale(1.55); background: var(--light-green); }}
  .breath-circle.out {{ transform: scale(0.65); background: var(--pastel-blue); }}
  .info {{ text-align:center; }}
  .info .phase {{
    font-size: 2.2rem; font-weight: 700; color: var(--komodo-navy);
    margin: 6px 0 4px;
  }}
  .info .instruction {{ font-size: 1.0rem; color: var(--komodo-navy); margin-bottom: 8px; }}
  .info .cycle {{ color: var(--vibrant-blue); font-weight:700; }}
</style>
<div class="panel">
  <div class="breath-row">
    <svg class="hand" viewBox="0 0 220 240">
      <!-- Soft drop shadow for depth -->
      <defs>
        <filter id="handshadow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
          <feOffset dx="0" dy="2"/>
          <feComponentTransfer><feFuncA type="linear" slope="0.25"/></feComponentTransfer>
          <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <g filter="url(#handshadow)">
        <!-- Palm with thumb pad — wide enough for 4 fingers + pinky on right -->
        <path class="palm" d="
          M 38 160
          Q 32 130 44 110
          L 56 105
          L 56 200
          Q 60 220 80 226
          L 140 226
          Q 168 224 180 208
          L 180 130
          Q 198 132 196 160
          Q 192 200 178 222
          Q 152 240 100 240
          Q 58 240 42 222
          Q 32 200 38 160 Z" />

        <!-- Thumb -->
        <path class="finger" id="f0" d="
          M 30 145
          Q 16 152 16 175
          Q 16 198 30 210
          Q 44 218 56 208
          L 56 158
          Q 50 142 30 145 Z" />

        <!-- Index finger -->
        <path class="finger" id="f1" d="
          M 56 110
          Q 56 50 70 38
          Q 80 32 88 38
          Q 96 50 96 110 Z" />

        <!-- Middle finger -->
        <path class="finger" id="f2" d="
          M 96 110
          Q 96 30 110 18
          Q 122 12 132 18
          Q 142 30 142 110 Z" />

        <!-- Ring finger -->
        <path class="finger" id="f3" d="
          M 138 110
          Q 138 56 150 46
          Q 158 40 166 46
          Q 174 56 174 110 Z" />

        <!-- Pinky -->
        <path class="finger" id="f4" d="
          M 174 122
          Q 174 80 184 72
          Q 191 68 197 72
          Q 204 80 204 122 Z" />

        <!-- Subtle knuckle lines -->
        <path class="knuckle" d="M 60 105 L 92 105"/>
        <path class="knuckle" d="M 100 105 L 134 105"/>
        <path class="knuckle" d="M 142 105 L 170 105"/>
        <path class="knuckle" d="M 178 120 L 200 120"/>
      </g>
    </svg>
    <div class="info-col">
      <div class="pulse-stage">
        <div class="breath-circle" id="circle"></div>
      </div>
      <div class="info">
        <div class="phase" id="phase">Ready</div>
        <div class="instruction" id="instr">Press start, then trace each finger in time with the breath.</div>
        <div class="cycle"><span id="cycle">0</span> / {cycles} cycles</div>
        <div style="margin-top:14px;">
          <button id="start" class="btn">▶ Start</button>
          <button id="stop"  class="btn ghost">⏹ Stop</button>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
(function() {{
  const inMs = {in_s * 1000};
  const outMs = {out_s * 1000};
  const totalCycles = {cycles};
  const phase = document.getElementById('phase');
  const instr = document.getElementById('instr');
  const circle = document.getElementById('circle');
  const cycleEl = document.getElementById('cycle');
  const fingers = [0,1,2,3,4].map(i => document.getElementById('f' + i));
  let timer = null;
  let cycle = 0;
  let phaseIdx = 0; // alternates IN (0) and OUT (1) per finger trace

  circle.style.transitionDuration = (inMs/1000) + 's';

  function clearFingers() {{ fingers.forEach(f => f.classList.remove('active','tracing')); }}
  function tick() {{
    const fingerIdx = cycle % 5;
    if (phaseIdx === 0) {{
      clearFingers();
      fingers[fingerIdx].classList.add('tracing');
      phase.textContent = 'Breathe IN';
      instr.textContent = 'Trace UP this finger';
      circle.classList.remove('out'); circle.classList.add('in');
      circle.style.transitionDuration = (inMs/1000) + 's';
      phaseIdx = 1;
      timer = setTimeout(tick, inMs);
    }} else {{
      fingers[fingerIdx].classList.remove('tracing');
      fingers[fingerIdx].classList.add('active');
      phase.textContent = 'Breathe OUT';
      instr.textContent = 'Trace DOWN this finger';
      circle.classList.remove('in'); circle.classList.add('out');
      circle.style.transitionDuration = (outMs/1000) + 's';
      phaseIdx = 0;
      cycle++;
      cycleEl.textContent = cycle;
      if (cycle >= totalCycles) {{
        timer = setTimeout(() => {{
          phase.textContent = '✅ Done';
          instr.textContent = 'Notice how you feel now.';
          clearFingers();
        }}, outMs);
        return;
      }}
      timer = setTimeout(tick, outMs);
    }}
  }}
  document.getElementById('start').onclick = () => {{
    if (timer) clearTimeout(timer);
    cycle = 0; phaseIdx = 0; cycleEl.textContent = 0;
    clearFingers();
    tick();
  }};
  document.getElementById('stop').onclick = () => {{
    if (timer) clearTimeout(timer);
    clearFingers();
    phase.textContent = 'Stopped';
    instr.textContent = 'Press start to begin again.';
    circle.classList.remove('in','out');
  }};
}})();
</script>
""",
        height=420,
    )


# ---------- Widget: colour breathing (pulse + colour picker) ----------
def _colour_breath(activity: Activity) -> None:
    cfg = activity.widget_config
    in_s = cfg.get("in_seconds", 4)
    out_s = cfg.get("out_seconds", 6)
    cycles = cfg.get("cycles", 8)
    default_colour = cfg.get("default_colour", "#55b5f2")
    palette = cfg.get("palette", [])

    swatches = "".join(
        f"<button class='swatch' data-hex='{p['hex']}' style='background:{p['hex']};' "
        f"title='{html.escape(p['name'])}'></button>"
        for p in palette
    )

    components.html(
        f"""
{_BASE_STYLE}
<style>
  .swatch {{
    width: 44px; height: 44px; border-radius: 50%;
    border: 3px solid var(--black-blue); cursor: pointer; margin: 4px;
    transition: transform 0.15s ease;
  }}
  .swatch:hover {{ transform: scale(1.1); }}
  .swatch.selected {{ box-shadow: 0 0 0 4px var(--light-green); }}
  .palette {{ text-align:center; margin-bottom: 18px; }}
  .palette .lbl {{ font-weight:700; color: var(--komodo-navy); margin-bottom: 6px; }}

  /* Side-by-side layout: pulse stage on left, text on right.
     A fixed-size stage prevents the expanding circle from overlapping the text. */
  .pulse-row {{
    display: flex; align-items: center; gap: 28px; flex-wrap: wrap;
    justify-content: center;
  }}
  .pulse-stage {{
    width: 280px; height: 280px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }}
  .pulse {{
    width: 160px; height: 160px; border-radius: 50%;
    transition: transform 4s ease, background 0.6s ease;
    border: 4px solid var(--black-blue);
  }}
  .pulse.in  {{ transform: scale(1.5); }}
  .pulse.out {{ transform: scale(0.6); }}

  .text-col {{ flex: 1; min-width: 240px; max-width: 320px; }}
  .phase {{ font-size: 2.2rem; font-weight: 700; color: var(--komodo-navy); margin: 0 0 6px; }}
  .instruction {{ color: var(--komodo-navy); font-size: 1.05rem; margin-bottom: 12px; }}
  .cycle {{ color: var(--vibrant-blue); font-weight:700; margin-bottom: 14px; }}
  .controls {{ margin-top: 8px; }}
</style>
<div class="panel">
  <div class="palette">
    <div class="lbl">Pick a soothing colour</div>
    {swatches}
  </div>
  <div class="pulse-row">
    <div class="pulse-stage">
      <div class="pulse" id="pulse" style="background: {default_colour};"></div>
    </div>
    <div class="text-col">
      <div class="phase" id="phase">Ready</div>
      <div class="instruction" id="instr">Breathe IN through your nose, imagine the colour filling you. Breathe OUT slowly through your mouth.</div>
      <div class="cycle"><span id="cycle">0</span> / {cycles} cycles</div>
      <div class="controls">
        <button id="start" class="btn">▶ Start</button>
        <button id="stop"  class="btn ghost">⏹ Stop</button>
      </div>
    </div>
  </div>
</div>
<script>
(function() {{
  const inMs = {in_s * 1000};
  const outMs = {out_s * 1000};
  const totalCycles = {cycles};
  let chosen = {json.dumps(default_colour)};
  const pulse = document.getElementById('pulse');
  const phase = document.getElementById('phase');
  const instr = document.getElementById('instr');
  const cycleEl = document.getElementById('cycle');
  let timer = null, cycle = 0, phaseIdx = 0;

  // Swatch selection
  document.querySelectorAll('.swatch').forEach(sw => {{
    sw.addEventListener('click', () => {{
      document.querySelectorAll('.swatch').forEach(s => s.classList.remove('selected'));
      sw.classList.add('selected');
      chosen = sw.dataset.hex;
      pulse.style.background = chosen;
    }});
  }});
  // Pre-select default
  const defaultSw = Array.from(document.querySelectorAll('.swatch')).find(s => s.dataset.hex === chosen);
  if (defaultSw) defaultSw.classList.add('selected');

  function tick() {{
    if (cycle >= totalCycles) {{
      phase.textContent = '✅ Done';
      instr.textContent = 'Notice how your body feels now.';
      pulse.classList.remove('in','out');
      return;
    }}
    if (phaseIdx === 0) {{
      phase.textContent = 'Breathe IN';
      instr.textContent = 'Imagine the colour filling your body';
      pulse.style.transitionDuration = (inMs/1000) + 's';
      pulse.classList.remove('out'); pulse.classList.add('in');
      phaseIdx = 1;
      timer = setTimeout(tick, inMs);
    }} else {{
      phase.textContent = 'Breathe OUT';
      instr.textContent = 'Imagine the colour flowing softly away';
      pulse.style.transitionDuration = (outMs/1000) + 's';
      pulse.classList.remove('in'); pulse.classList.add('out');
      phaseIdx = 0;
      cycle++;
      cycleEl.textContent = cycle;
      timer = setTimeout(tick, outMs);
    }}
  }}
  document.getElementById('start').onclick = () => {{
    if (timer) clearTimeout(timer);
    cycle = 0; phaseIdx = 0; cycleEl.textContent = 0;
    tick();
  }};
  document.getElementById('stop').onclick = () => {{
    if (timer) clearTimeout(timer);
    pulse.classList.remove('in','out');
    phase.textContent = 'Stopped';
    instr.textContent = 'Press start to begin again.';
  }};
}})();
</script>
""",
        height=520,
    )


# ---------- Widget: bilateral taps (Butterfly hugs) ----------
def _bilateral_taps(activity: Activity) -> None:
    cfg = activity.widget_config
    interval = cfg.get("tap_interval_ms", 900)
    total = cfg.get("total_seconds", 120)

    components.html(
        f"""
{_BASE_STYLE}
<style>
  .stage {{
    position: relative; height: 220px; margin: 8px 0 16px;
    display:flex; align-items:center; justify-content: center; gap: 100px;
  }}
  .arm {{
    width: 120px; height: 160px; border-radius: 70px;
    background: var(--pastel-blue); border: 3px solid var(--black-blue);
    display:flex; align-items:center; justify-content:center;
    font-size: 3rem; transition: transform 0.18s ease, background 0.18s ease;
  }}
  .arm.tap {{ background: var(--light-green); transform: scale(1.15); }}
  .heart {{
    position: absolute; left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    font-size: 3.5rem;
  }}
  .phase {{ text-align:center; font-size: 1.5rem; font-weight: 700; color: var(--komodo-navy); margin: 4px 0 6px; }}
  .instruction {{ text-align:center; color: var(--komodo-navy); margin-bottom: 8px; }}
  .timeline {{ text-align:center; color: var(--vibrant-blue); font-weight:700; margin-top: 6px; }}
  .controls {{ text-align:center; margin-top: 12px; }}
</style>
<div class="panel">
  <div class="phase" id="phase">Cross your arms over your chest</div>
  <div class="instruction">Rest a hand on each upper arm. Tap one side at a time, in rhythm with the pulse below.</div>
  <div class="stage">
    <div class="arm" id="left">🫲</div>
    <div class="heart">💛</div>
    <div class="arm" id="right">🫱</div>
  </div>
  <div class="timeline" id="time">0:00 / {total // 60}:{total % 60:02d}</div>
  <div class="controls">
    <button id="start" class="btn">▶ Start</button>
    <button id="stop"  class="btn ghost">⏹ Stop</button>
  </div>
</div>
<script>
(function() {{
  const intervalMs = {interval};
  const totalMs = {total * 1000};
  const leftEl = document.getElementById('left');
  const rightEl = document.getElementById('right');
  const phase = document.getElementById('phase');
  const timeEl = document.getElementById('time');
  let tapInt = null, tickInt = null, side = 0, elapsed = 0;

  function fmt(s) {{
    const m = Math.floor(s/60);
    const ss = (s % 60).toString().padStart(2,'0');
    return m + ':' + ss;
  }}
  function clearTaps() {{ leftEl.classList.remove('tap'); rightEl.classList.remove('tap'); }}
  document.getElementById('start').onclick = () => {{
    if (tapInt) clearInterval(tapInt);
    if (tickInt) clearInterval(tickInt);
    elapsed = 0; side = 0;
    phase.textContent = 'Tap… Tap… Tap…';
    tapInt = setInterval(() => {{
      clearTaps();
      if (side === 0) leftEl.classList.add('tap');
      else rightEl.classList.add('tap');
      side = 1 - side;
    }}, intervalMs);
    tickInt = setInterval(() => {{
      elapsed++;
      timeEl.textContent = fmt(elapsed) + ' / {total // 60}:{total % 60:02d}';
      if (elapsed * 1000 >= totalMs) {{
        clearInterval(tapInt); clearInterval(tickInt); clearTaps();
        phase.textContent = '✅ Done — notice how you feel';
      }}
    }}, 1000);
  }};
  document.getElementById('stop').onclick = () => {{
    if (tapInt) clearInterval(tapInt);
    if (tickInt) clearInterval(tickInt);
    clearTaps();
    phase.textContent = 'Paused';
  }};
}})();
</script>
""",
        height=460,
    )


# ---------- Widget: weather picker (Inner weather report) ----------
def _weather_pick(activity: Activity) -> None:
    options = activity.widget_config.get("options", [])
    opts_html = "".join(
        f"""
<button class='weather-opt' data-key='{html.escape(o["label"])}'>
  <div class='emoji'>{o["emoji"]}</div>
  <div class='lbl'>{html.escape(o["label"])}</div>
  <div class='feel'>{html.escape(o["feel"])}</div>
</button>
"""
        for o in options
    )

    components.html(
        f"""
{_BASE_STYLE}
<style>
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; }}
  .weather-opt {{
    background: var(--white); border: 2px solid var(--black-blue); border-radius: 12px;
    padding: 14px 10px; cursor: pointer; text-align: center;
    font-family: 'Epilogue', sans-serif; transition: transform 0.15s ease, background 0.15s ease;
  }}
  .weather-opt:hover {{ background: var(--pale-blue); transform: translateY(-2px); }}
  .weather-opt.selected {{ background: var(--light-green); }}
  .weather-opt .emoji {{ font-size: 2.6rem; line-height:1; margin-bottom:4px; padding: 6px 0; }}
  .weather-opt .lbl {{ font-weight:700; color: var(--komodo-navy); }}
  .weather-opt .feel {{ font-size: 0.82rem; color: #2a4458; margin-top: 4px; }}
  .forecast-row {{
    margin-top: 18px; padding: 14px 16px;
    background: var(--pale-blue); border: 2px solid var(--black-blue); border-radius: 12px;
  }}
  .forecast-row .label {{ font-weight: 700; color: var(--komodo-navy); margin-bottom: 6px; }}
  .forecast-row textarea {{
    width: 100%; min-height: 60px; padding: 10px 12px;
    border: 2px solid var(--black-blue); border-radius: 8px;
    font-family: 'Epilogue', sans-serif; font-size: 1rem;
    background: var(--white); color: var(--black-blue);
  }}

  /* ----- Weather animation stage ----- */
  .weather-stage {{
    display: none;
    position: relative;
    height: 220px;
    margin: 18px 0;
    border: 2px solid var(--black-blue);
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(180deg, #e1f3ff 0%, #ffffff 100%);
  }}
  .weather-stage.show {{ display: block; }}
  .stage-hero {{
    position: absolute; left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    font-size: 5rem; line-height: 1; z-index: 2;
  }}
  .stage-hero.spin {{ animation: spin 4s linear infinite; }}
  .stage-hero.bob   {{ animation: bob 2.5s ease-in-out infinite; }}
  .stage-hero.shake {{ animation: shake 0.4s linear infinite; }}
  @keyframes spin {{ to {{ transform: translate(-50%, -50%) rotate(360deg); }} }}
  @keyframes bob {{
    0%,100% {{ transform: translate(-50%, -50%); }}
    50% {{ transform: translate(-50%, -60%); }}
  }}
  @keyframes shake {{
    0%,100% {{ transform: translate(-50%, -50%); }}
    25% {{ transform: translate(-48%, -50%); }}
    75% {{ transform: translate(-52%, -50%); }}
  }}

  /* Falling element template for rain / snow */
  .drop {{
    position: absolute; top: -20px;
    animation: fall linear infinite;
    font-size: 1.4rem;
  }}
  @keyframes fall {{
    to {{ transform: translateY(260px); opacity: 0; }}
  }}

  /* Lightning flash overlay for thunderstorm */
  .flash {{
    position: absolute; inset: 0;
    background: #fff;
    opacity: 0;
    animation: flash 4s infinite;
    z-index: 1;
  }}
  @keyframes flash {{
    0%, 92%, 100% {{ opacity: 0; }}
    93% {{ opacity: 0.9; }}
    95% {{ opacity: 0; }}
    96% {{ opacity: 0.7; }}
    97% {{ opacity: 0; }}
  }}

  /* Sun rays */
  .rays {{
    position: absolute; left: 50%; top: 50%; width: 200px; height: 200px;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle, rgba(255,195,15,0.6) 0%, transparent 70%);
    animation: pulse-glow 3s ease-in-out infinite;
  }}
  @keyframes pulse-glow {{
    0%, 100% {{ opacity: 0.6; transform: translate(-50%, -50%) scale(1); }}
    50%      {{ opacity: 0.9; transform: translate(-50%, -50%) scale(1.15); }}
  }}

  /* Drifting fog wisps */
  .fog {{
    position: absolute; top: 50%; left: -120px;
    width: 140px; height: 30px; border-radius: 20px;
    background: rgba(200, 210, 220, 0.6);
    animation: drift 6s linear infinite;
  }}
  @keyframes drift {{
    to {{ left: 100%; }}
  }}

  .summary {{
    display:none; padding: 14px 16px; background: var(--pastel-green);
    border:2px solid var(--black-blue); border-radius:12px; margin-top: 14px;
    font-size: 1.05rem;
  }}
</style>
<div class="panel">
  <div class="label" style="margin-bottom: 8px;">If your mood was weather right now, what would it be?</div>
  <div class="grid">
    {opts_html}
  </div>
  <div class="forecast-row">
    <div class="label">📅 Your forecast for the rest of the day:</div>
    <textarea id="forecast" placeholder="e.g. Brightening up by afternoon, with a chance of homework storms…"></textarea>
  </div>
  <div class="forecast-row">
    <div class="label">🧥 One thing you'll do to prepare for that weather:</div>
    <textarea id="prepare" placeholder="e.g. It's stormy — I'll find a quiet corner before the meeting."></textarea>
  </div>
  <div style="text-align:center; margin-top:14px;">
    <button id="show" class="btn">📰 Show my report</button>
    <button id="reset" class="btn ghost">↺ Clear</button>
  </div>
  <div class="weather-stage" id="stage"></div>
  <div class="summary" id="summary"></div>
</div>
<script>
(function() {{
  let chosen = null;
  let chosenEmoji = null;
  document.querySelectorAll('.weather-opt').forEach(b => {{
    b.addEventListener('click', () => {{
      document.querySelectorAll('.weather-opt').forEach(x => x.classList.remove('selected'));
      b.classList.add('selected');
      chosen = b.dataset.key;
      chosenEmoji = b.querySelector('.emoji').textContent.trim();
    }});
  }});

  function animateWeather(stage, label, emoji) {{
    stage.innerHTML = '';
    stage.classList.add('show');
    const map = {{
      'Sunny':         {{ bg: 'linear-gradient(180deg, #ffe9b3 0%, #fff8e7 100%)', cls: 'spin', extras: 'rays' }},
      'Partly cloudy': {{ bg: 'linear-gradient(180deg, #d8edff 0%, #ffffff 100%)', cls: 'bob',  extras: 'fog' }},
      'Overcast':      {{ bg: 'linear-gradient(180deg, #cdd6df 0%, #e9eef3 100%)', cls: 'bob',  extras: 'fog2' }},
      'Foggy':         {{ bg: 'linear-gradient(180deg, #d4dade 0%, #e7ebef 100%)', cls: 'bob',  extras: 'fog3' }},
      'Light drizzle': {{ bg: 'linear-gradient(180deg, #cee2ef 0%, #e7eff5 100%)', cls: 'bob',  extras: 'drizzle' }},
      'Thunderstorm':  {{ bg: 'linear-gradient(180deg, #6c7886 0%, #99a5b3 100%)', cls: 'shake', extras: 'storm' }},
      'Tornado':       {{ bg: 'linear-gradient(180deg, #a6acb3 0%, #d2d6db 100%)', cls: 'spin',  extras: 'wind' }},
      'Snowy':         {{ bg: 'linear-gradient(180deg, #e9f3fb 0%, #ffffff 100%)', cls: 'bob',   extras: 'snow' }},
    }};
    const cfg = map[label] || {{ bg: 'linear-gradient(180deg, #e1f3ff 0%, #ffffff 100%)', cls: '', extras: '' }};
    stage.style.background = cfg.bg;

    // Hero emoji
    const hero = document.createElement('div');
    hero.className = 'stage-hero ' + cfg.cls;
    hero.textContent = emoji;
    stage.appendChild(hero);

    // Extras layer
    if (cfg.extras === 'rays') {{
      const r = document.createElement('div'); r.className = 'rays'; stage.appendChild(r);
    }}
    if (cfg.extras === 'fog' || cfg.extras === 'fog2' || cfg.extras === 'fog3') {{
      for (let i = 0; i < 3; i++) {{
        const f = document.createElement('div');
        f.className = 'fog';
        f.style.top = (30 + i * 60) + 'px';
        f.style.animationDelay = (i * 1.5) + 's';
        f.style.animationDuration = (5 + i) + 's';
        if (cfg.extras === 'fog3') {{ f.style.background = 'rgba(180,190,200,0.7)'; f.style.height = '40px'; }}
        if (cfg.extras === 'fog2') {{ f.style.background = 'rgba(160,170,180,0.6)'; }}
        stage.appendChild(f);
      }}
    }}
    if (cfg.extras === 'drizzle' || cfg.extras === 'storm') {{
      const count = cfg.extras === 'storm' ? 20 : 12;
      for (let i = 0; i < count; i++) {{
        const d = document.createElement('div');
        d.className = 'drop';
        d.textContent = '💧';
        d.style.left = (Math.random() * 100) + '%';
        d.style.animationDuration = (0.8 + Math.random() * 0.8) + 's';
        d.style.animationDelay = (Math.random() * 1.5) + 's';
        d.style.fontSize = cfg.extras === 'storm' ? '1.6rem' : '1.2rem';
        stage.appendChild(d);
      }}
      if (cfg.extras === 'storm') {{
        const fl = document.createElement('div'); fl.className = 'flash'; stage.appendChild(fl);
      }}
    }}
    if (cfg.extras === 'snow') {{
      for (let i = 0; i < 18; i++) {{
        const s = document.createElement('div');
        s.className = 'drop';
        s.textContent = '❄️';
        s.style.left = (Math.random() * 100) + '%';
        s.style.animationDuration = (3 + Math.random() * 2) + 's';
        s.style.animationDelay = (Math.random() * 3) + 's';
        s.style.fontSize = '1.1rem';
        stage.appendChild(s);
      }}
    }}
    if (cfg.extras === 'wind') {{
      for (let i = 0; i < 6; i++) {{
        const w = document.createElement('div');
        w.className = 'fog';
        w.style.top = (20 + i * 30) + 'px';
        w.style.animationDuration = (1 + Math.random()) + 's';
        w.style.animationDelay = (i * 0.2) + 's';
        w.style.background = 'rgba(180,180,180,0.5)';
        stage.appendChild(w);
      }}
    }}
  }}

  document.getElementById('show').onclick = () => {{
    const f = document.getElementById('forecast').value.trim();
    const p = document.getElementById('prepare').value.trim();
    const sum = document.getElementById('summary');
    const stage = document.getElementById('stage');
    if (chosen) animateWeather(stage, chosen, chosenEmoji);
    sum.style.display = 'block';
    sum.innerHTML = '<strong>Inner weather report:</strong> ' +
      (chosen ? chosen : '(no weather picked)') +
      (f ? '<br><strong>Forecast:</strong> ' + f : '') +
      (p ? '<br><strong>Preparation:</strong> ' + p : '');
  }};
  document.getElementById('reset').onclick = () => {{
    document.querySelectorAll('.weather-opt').forEach(x => x.classList.remove('selected'));
    document.getElementById('forecast').value = '';
    document.getElementById('prepare').value = '';
    document.getElementById('summary').style.display = 'none';
    const stage = document.getElementById('stage');
    stage.classList.remove('show');
    stage.innerHTML = '';
    chosen = null;
    chosenEmoji = null;
  }};
}})();
</script>
""",
        height=860,
    )


# ---------- Widget: motion picker (Tension tamers) ----------
def _motion_picker(activity: Activity) -> None:
    """User picks one of several physical motions; a matching emoji-based
    animation plays alongside a countdown timer."""
    cfg = activity.widget_config
    seconds = cfg.get("seconds", 30)
    finish_prompt = cfg.get("finish_prompt", "Big breath in… and out.")
    motions = cfg.get(
        "motions",
        [
            {"key": "rock",   "emoji": "🪨", "label": "Rock",       "anim": "rock"},
            {"key": "crawl",  "emoji": "🐛", "label": "Crawl",      "anim": "crawl"},
            {"key": "stomp",  "emoji": "👣", "label": "Stomp",      "anim": "stomp"},
            {"key": "twist",  "emoji": "🌀", "label": "Twist",      "anim": "twist"},
            {"key": "spin",   "emoji": "💫", "label": "Spin",       "anim": "spin"},
            {"key": "tap",    "emoji": "👏", "label": "Tap",        "anim": "tap"},
            {"key": "push",   "emoji": "🧱", "label": "Push wall",  "anim": "push"},
        ],
    )

    opts_html = "".join(
        f"<button class='motion-opt' data-key='{m['key']}' data-anim='{m['anim']}' "
        f"data-emoji='{m['emoji']}' data-label='{html.escape(m['label'])}'>"
        f"<div class='m-emoji'>{m['emoji']}</div>"
        f"<div class='m-label'>{html.escape(m['label'])}</div>"
        "</button>"
        for m in motions
    )

    components.html(
        f"""
{_BASE_STYLE}
<style>
  .pick-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px;
    margin-bottom: 14px;
  }}
  .motion-opt {{
    background: var(--white); border: 2px solid var(--black-blue); border-radius: 12px;
    padding: 14px 10px; cursor: pointer; text-align: center;
    font-family: 'Epilogue', sans-serif;
    transition: transform 0.15s ease, background 0.15s ease;
  }}
  .motion-opt:hover {{ background: var(--pale-blue); transform: translateY(-2px); }}
  .motion-opt.selected {{ background: var(--light-green); }}
  .m-emoji {{ font-size: 2.2rem; line-height:1; margin-bottom: 4px; padding: 4px 0; }}
  .m-label {{ font-weight: 700; color: var(--komodo-navy); font-size: 0.9rem; }}

  .stage {{
    text-align: center; padding: 18px 0;
    background: var(--pale-blue);
    border: 2px solid var(--black-blue); border-radius: 14px;
    margin: 14px 0; min-height: 130px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
  }}
  .stage-emoji {{ font-size: 4.5rem; line-height: 1; padding: 8px; }}
  .stage-label {{ color: var(--komodo-navy); font-weight: 700; margin-top: 4px; }}

  /* Per-motion animations */
  .running .stage-emoji.rock   {{ animation: rock 1.2s ease-in-out infinite; }}
  .running .stage-emoji.crawl  {{ animation: crawl 1.4s ease-in-out infinite; }}
  .running .stage-emoji.stomp  {{ animation: stomp 0.5s ease-in-out infinite; }}
  .running .stage-emoji.twist  {{ animation: twist 1.2s ease-in-out infinite; }}
  .running .stage-emoji.spin   {{ animation: spin 1.6s linear infinite; }}
  .running .stage-emoji.tap    {{ animation: tap 0.4s ease-in-out infinite; }}
  .running .stage-emoji.push   {{ animation: push 1.2s ease-in-out infinite; }}

  @keyframes rock  {{ 0%,100% {{ transform: rotate(-12deg); }} 50% {{ transform: rotate(12deg); }} }}
  @keyframes crawl {{ 0%,100% {{ transform: translateX(-30px); }} 50% {{ transform: translateX(30px); }} }}
  @keyframes stomp {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-22px); }} }}
  @keyframes twist {{ 0%,100% {{ transform: rotate(0deg) scaleX(1); }} 50% {{ transform: rotate(180deg) scaleX(-1); }} }}
  @keyframes spin  {{ to {{ transform: rotate(360deg); }} }}
  @keyframes tap   {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.25); }} }}
  @keyframes push  {{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(28px); }} }}

  .time {{ font-size: 4rem; font-weight: 700; color: var(--komodo-navy); line-height: 1; }}
  .controls {{ text-align: center; margin-top: 12px; }}
</style>
<div class="panel">
  <div style="font-weight:700; color: var(--komodo-navy); margin-bottom: 8px;">
    1. Pick a motion to try
  </div>
  <div class="pick-grid">{opts_html}</div>
  <div style="font-weight:700; color: var(--komodo-navy); margin: 10px 0 6px;">
    2. Press start
  </div>
  <div class="stage" id="stage">
    <div class="stage-emoji" id="stage-emoji">🎯</div>
    <div class="stage-label" id="stage-label">Pick a motion above</div>
  </div>
  <div class="time" id="time" style="text-align:center;">{seconds:02d}</div>
  <div class="controls">
    <button id="start" class="btn">▶ Start</button>
    <button id="pause" class="btn secondary">⏸ Pause</button>
    <button id="reset" class="btn ghost">↺ Reset</button>
  </div>
</div>
<script>
(function() {{
  const total = {seconds};
  let remaining = total, running = false, interval = null;
  let chosen = null;

  const stage = document.getElementById('stage');
  const sEmoji = document.getElementById('stage-emoji');
  const sLabel = document.getElementById('stage-label');
  const tEl = document.getElementById('time');
  const finish = {json.dumps(finish_prompt)};

  function fmt(s) {{
    if (s >= 60) {{ return Math.floor(s/60) + ':' + (s%60).toString().padStart(2,'0'); }}
    return s.toString().padStart(2,'0');
  }}
  function setRunning(v) {{
    running = v;
    stage.classList.toggle('running', v);
  }}
  function render() {{
    tEl.textContent = fmt(remaining);
    if (remaining === 0) {{
      tEl.style.color = 'var(--score-good-green)';
      sLabel.innerHTML = '<strong>✅ ' + finish + '</strong>';
      setRunning(false);
    }} else if (remaining <= 5) {{
      tEl.style.color = 'var(--score-red)';
    }} else {{
      tEl.style.color = 'var(--komodo-navy)';
    }}
  }}

  document.querySelectorAll('.motion-opt').forEach(b => {{
    b.onclick = () => {{
      document.querySelectorAll('.motion-opt').forEach(x => x.classList.remove('selected'));
      b.classList.add('selected');
      chosen = {{
        anim: b.dataset.anim,
        emoji: b.dataset.emoji,
        label: b.dataset.label,
      }};
      sEmoji.className = 'stage-emoji ' + chosen.anim;
      sEmoji.textContent = chosen.emoji;
      sLabel.textContent = chosen.label;
    }};
  }});

  document.getElementById('start').onclick = () => {{
    if (running) return;
    if (!chosen) {{ sLabel.textContent = 'Pick a motion above first!'; return; }}
    setRunning(true);
    interval = setInterval(() => {{
      if (remaining > 0) {{ remaining--; render(); }}
      else {{ clearInterval(interval); setRunning(false); }}
    }}, 1000);
  }};
  document.getElementById('pause').onclick = () => {{
    setRunning(false);
    if (interval) clearInterval(interval);
  }};
  document.getElementById('reset').onclick = () => {{
    setRunning(false);
    if (interval) clearInterval(interval);
    remaining = total;
    render();
  }};
  render();
}})();
</script>
""",
        height=700,
    )


# ---------- Widget: drawing canvas (Draw it out) ----------
def _canvas(activity: Activity) -> None:
    """Simple HTML5 drawing canvas with colour palette, brush sizes, and clear."""
    cfg = activity.widget_config
    width = cfg.get("width", 600)
    height = cfg.get("height", 360)
    palette = cfg.get(
        "palette",
        ["#001f34", "#3d92e6", "#55b5f2", "#77eed6", "#2cdd9c", "#ffc30f", "#e53b19", "#f5a6c0", "#ffffff"],
    )
    sizes = cfg.get("sizes", [3, 6, 12, 24])

    palette_html = "".join(
        f"<button class='c-swatch' data-c='{c}' style='background:{c};'></button>" for c in palette
    )
    sizes_html = "".join(
        f"<button class='c-size' data-s='{s}'>"
        f"<div style='width:{s+2}px; height:{s+2}px; background: var(--black-blue); border-radius: 50%;'></div>"
        f"</button>"
        for s in sizes
    )

    components.html(
        f"""
{_BASE_STYLE}
<style>
  .tools {{
    display: flex; gap: 18px; align-items: center; flex-wrap: wrap;
    margin-bottom: 10px;
  }}
  .tools .group {{ display:flex; gap: 4px; align-items: center; }}
  .tools .lbl {{ font-weight: 700; color: var(--komodo-navy); font-size: 0.85rem; margin-right: 4px; }}
  .c-swatch {{
    width: 30px; height: 30px; border-radius: 50%;
    border: 2.5px solid var(--black-blue); cursor: pointer;
    padding: 0;
  }}
  .c-swatch.selected {{ box-shadow: 0 0 0 3px var(--light-green); }}
  .c-size {{
    width: 36px; height: 36px; border: 2px solid var(--black-blue);
    background: var(--white); border-radius: 8px; cursor: pointer;
    display:flex; align-items:center; justify-content:center;
  }}
  .c-size.selected {{ background: var(--light-green); }}
  canvas#pad {{
    background: #ffffff;
    border: 2px solid var(--black-blue); border-radius: 12px;
    touch-action: none; cursor: crosshair;
    display: block; max-width: 100%;
  }}
  .canvas-actions {{ display:flex; gap: 8px; margin-top: 10px; justify-content:flex-end; }}

  /* Celebration on save */
  .panel {{ position: relative; overflow: hidden; }}
  .confetti-stage {{
    position: absolute; inset: 0; pointer-events: none; overflow: hidden; z-index: 5;
  }}
  .confetti-piece {{
    position: absolute; top: -20px; width: 10px; height: 18px; border-radius: 2px;
    animation: fall 2.4s cubic-bezier(.22,.61,.36,1) forwards;
  }}
  @keyframes fall {{
    0% {{ transform: translateY(-30px) rotate(0deg); opacity: 1; }}
    100% {{ transform: translateY(700px) rotate(720deg); opacity: 0; }}
  }}
  .save-msg {{
    display: none; margin-top: 10px; padding: 10px 14px;
    background: var(--pastel-green); border: 2px solid var(--black-blue); border-radius: 10px;
    font-weight: 700; color: var(--komodo-navy); text-align: center;
  }}
  .save-msg.show {{ display: block; animation: pop 0.4s ease-out; }}
  @keyframes pop {{
    0%   {{ transform: scale(0.7); opacity: 0; }}
    70%  {{ transform: scale(1.05); opacity: 1; }}
    100% {{ transform: scale(1); }}
  }}
</style>
<div class="panel">
  <div class="confetti-stage" id="confetti"></div>
  <div class="tools">
    <div class="group">
      <div class="lbl">Colour</div>
      {palette_html}
    </div>
    <div class="group">
      <div class="lbl">Brush</div>
      {sizes_html}
    </div>
  </div>
  <canvas id="pad" width="{width}" height="{height}"></canvas>
  <div class="canvas-actions">
    <button id="clear" class="btn ghost">🗑️ Clear</button>
    <button id="save"  class="btn">✨ Done</button>
  </div>
  <div class="save-msg" id="save-msg">🎨 Beautiful — your feeling is on the page, not inside you any more.</div>
</div>
<script>
(function() {{
  const canvas = document.getElementById('pad');
  const ctx = canvas.getContext('2d');
  let drawing = false;
  let last = null;
  let colour = {json.dumps(palette[0])};
  let size = {sizes[1]};

  // White background so saved drawings aren't transparent
  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, canvas.width, canvas.height);

  function pos(ev) {{
    const r = canvas.getBoundingClientRect();
    const sx = canvas.width / r.width, sy = canvas.height / r.height;
    const t = ev.touches ? ev.touches[0] : ev;
    return {{ x: (t.clientX - r.left) * sx, y: (t.clientY - r.top) * sy }};
  }}
  function draw(p) {{
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = colour; ctx.lineWidth = size;
    ctx.beginPath();
    if (last) ctx.moveTo(last.x, last.y);
    else ctx.moveTo(p.x, p.y);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
    last = p;
  }}
  canvas.addEventListener('mousedown', e => {{ drawing = true; last = null; draw(pos(e)); }});
  canvas.addEventListener('mousemove', e => {{ if (drawing) draw(pos(e)); }});
  canvas.addEventListener('mouseup',   () => {{ drawing = false; last = null; }});
  canvas.addEventListener('mouseleave',() => {{ drawing = false; last = null; }});
  canvas.addEventListener('touchstart', e => {{ e.preventDefault(); drawing = true; last = null; draw(pos(e)); }});
  canvas.addEventListener('touchmove',  e => {{ e.preventDefault(); if (drawing) draw(pos(e)); }});
  canvas.addEventListener('touchend',   () => {{ drawing = false; last = null; }});

  // Swatches
  document.querySelectorAll('.c-swatch').forEach(sw => {{
    sw.onclick = () => {{
      document.querySelectorAll('.c-swatch').forEach(x => x.classList.remove('selected'));
      sw.classList.add('selected');
      colour = sw.dataset.c;
    }};
  }});
  document.querySelector('.c-swatch').classList.add('selected');

  // Sizes
  document.querySelectorAll('.c-size').forEach(s => {{
    s.onclick = () => {{
      document.querySelectorAll('.c-size').forEach(x => x.classList.remove('selected'));
      s.classList.add('selected');
      size = parseInt(s.dataset.s, 10);
    }};
  }});
  document.querySelectorAll('.c-size')[1].classList.add('selected');

  // Clear
  document.getElementById('clear').onclick = () => {{
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    document.getElementById('save-msg').classList.remove('show');
  }};

  // Done → celebration
  document.getElementById('save').onclick = () => {{
    const msg = document.getElementById('save-msg');
    msg.classList.add('show');
    const stage = document.getElementById('confetti');
    const colors = ['#55b5f2','#77eed6','#ffc30f','#f5a6c0','#3d92e6','#2cdd9c','#ffb37a'];
    for (let i = 0; i < 30; i++) {{
      const p = document.createElement('div');
      p.className = 'confetti-piece';
      p.style.left = (Math.random() * 100) + '%';
      p.style.background = colors[Math.floor(Math.random() * colors.length)];
      p.style.animationDuration = (1.6 + Math.random() * 1.4) + 's';
      p.style.animationDelay = (Math.random() * 0.4) + 's';
      stage.appendChild(p);
    }}
    setTimeout(() => {{ stage.innerHTML = ''; }}, 3500);
  }};
}})();
</script>
""",
        height=height + 200,
    )


# ---------- Widget: fallback ----------
def _fallback(activity: Activity) -> None:
    components.html(
        f"""
{_BASE_STYLE}
<div class="panel">
  <div style="font-size:1.05rem; line-height:1.6; white-space: pre-line;">
    {html.escape(activity.instructions)}
  </div>
</div>
""",
        height=240,
    )
