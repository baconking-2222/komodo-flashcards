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
    else:
        _fallback(activity)


# ---------- Widget: simple countdown timer with movement prompt ----------
def _timer_simple(activity: Activity) -> None:
    cfg = activity.widget_config
    seconds = cfg.get("seconds", activity.duration_minutes * 60)
    prompt = cfg.get("prompt", "Move freely")
    finish_prompt = cfg.get("finish_prompt", "Take a deep breath in… and out.")

    components.html(
        f"""
{_BASE_STYLE}
<div class="panel" style="text-align:center;">
  <div style="font-size:1.1rem; font-weight:700; color:var(--komodo-navy); margin-bottom:8px;">
    DO THIS NOW
  </div>
  <div id="prompt" style="font-size:1.4rem; margin:14px 0 24px; min-height:60px;">
    {html.escape(prompt)}
  </div>
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
  const finish = {json.dumps(finish_prompt)};
  const startPrompt = {json.dumps(prompt)};

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
    }} else if (remaining <= 5) {{
      tEl.style.color = 'var(--score-red)';
    }} else {{
      tEl.style.color = 'var(--komodo-navy)';
    }}
  }}
  document.getElementById('start').onclick = () => {{
    if (running) return;
    running = true;
    pEl.textContent = startPrompt;
    interval = setInterval(() => {{
      if (remaining > 0) {{ remaining--; render(); }}
      else {{ clearInterval(interval); running = false; }}
    }}, 1000);
  }};
  document.getElementById('pause').onclick = () => {{
    running = false;
    if (interval) clearInterval(interval);
  }};
  document.getElementById('reset').onclick = () => {{
    running = false;
    if (interval) clearInterval(interval);
    remaining = total;
    pEl.textContent = startPrompt;
    render();
  }};
  render();
}})();
</script>
""",
        height=360,
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
  .step-icon {{ font-size: 4rem; line-height:1; }}
  .step-label {{ font-size: 1.6rem; font-weight:700; color: var(--komodo-navy); margin: 10px 0; }}
  .step-body  {{ font-size: 1.15rem; line-height:1.5; white-space: pre-line; color: var(--black-blue); }}
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


# ---------- Widget: list of prompts with input boxes ----------
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
  .prompt-row .head .icon {{ font-size:1.6rem; }}
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
  .reset-row {{ text-align:right; margin-top:12px; }}
</style>
<div class="panel">
  {examples_html}
  <div id="rows"></div>
  <div class="reset-row">
    <button id="reset" class="btn ghost">↺ Clear all</button>
  </div>
</div>
<script>
(function() {{
  const items = {json.dumps(items)};
  const rows = document.getElementById('rows');

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
      }});
      ir.appendChild(num);
      ir.appendChild(inp);
      row.appendChild(ir);
    }}
    rows.appendChild(row);
  }}

  items.forEach((it, i) => buildRow(it, i));

  document.getElementById('reset').onclick = () => {{
    rows.querySelectorAll('input, textarea').forEach(el => el.value = '');
    rows.querySelectorAll('.check-num').forEach(el => el.classList.remove('filled'));
  }};
}})();
</script>
""",
        height=_estimate_list_height(items),
    )


def _estimate_list_height(items: list[dict[str, Any]]) -> int:
    """Roughly size the iframe based on number of inputs."""
    h = 130  # base
    for it in items:
        h += 80  # row header + spacing
        per_input = 90 if it.get("multiline") else 60
        h += per_input * max(1, int(it.get("count", 1)))
    return min(h, 900)


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
  .breath-row {{ display:flex; align-items:center; gap:30px; justify-content:center; flex-wrap:wrap; }}
  svg.hand {{ width: 240px; height: 280px; }}
  .finger {{
    fill: var(--pale-blue); stroke: var(--black-blue); stroke-width: 3;
    transition: fill 0.5s ease;
  }}
  .finger.active {{ fill: var(--vibrant-blue); }}
  .finger.tracing {{ fill: var(--light-green); }}
  .palm {{ fill: var(--white); stroke: var(--black-blue); stroke-width: 3; }}
  .info {{ text-align:center; min-width: 240px; }}
  .info .phase {{
    font-size: 2.6rem; font-weight: 700; color: var(--komodo-navy);
    margin: 14px 0 6px;
  }}
  .info .instruction {{ font-size: 1.05rem; color: var(--komodo-navy); margin-bottom: 10px; }}
  .info .cycle {{ color: var(--vibrant-blue); font-weight:700; }}
  .breath-circle {{
    width: 140px; height: 140px; border-radius:50%;
    background: var(--pastel-blue); border: 4px solid var(--black-blue);
    margin: 6px auto; transition: transform 4s ease, background 0.8s ease;
  }}
  .breath-circle.in {{ transform: scale(1.4); background: var(--light-green); }}
  .breath-circle.out {{ transform: scale(0.7); background: var(--pastel-blue); }}
</style>
<div class="panel">
  <div class="breath-row">
    <svg class="hand" viewBox="0 0 200 240">
      <!-- Palm -->
      <ellipse class="palm" cx="100" cy="180" rx="60" ry="50"/>
      <!-- Thumb -->
      <rect class="finger" id="f0" x="22" y="120" width="32" height="70" rx="16" transform="rotate(-30 38 155)"/>
      <!-- Index -->
      <rect class="finger" id="f1" x="50" y="40"  width="28" height="100" rx="14"/>
      <!-- Middle -->
      <rect class="finger" id="f2" x="84" y="20"  width="28" height="120" rx="14"/>
      <!-- Ring -->
      <rect class="finger" id="f3" x="118" y="40" width="28" height="100" rx="14"/>
      <!-- Pinky -->
      <rect class="finger" id="f4" x="152" y="70" width="28" height="80"  rx="14"/>
    </svg>
    <div class="info">
      <div class="phase" id="phase">Ready</div>
      <div class="instruction" id="instr">Press start and trace your fingers in time with the breath.</div>
      <div class="breath-circle" id="circle"></div>
      <div class="cycle"><span id="cycle">0</span> / {cycles} cycles</div>
      <div style="margin-top:14px;">
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
  .weather-opt .emoji {{ font-size: 2.6rem; line-height:1; margin-bottom:4px; }}
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
  <div class="summary" id="summary"></div>
</div>
<script>
(function() {{
  let chosen = null;
  document.querySelectorAll('.weather-opt').forEach(b => {{
    b.addEventListener('click', () => {{
      document.querySelectorAll('.weather-opt').forEach(x => x.classList.remove('selected'));
      b.classList.add('selected');
      chosen = b.dataset.key;
    }});
  }});
  document.getElementById('show').onclick = () => {{
    const f = document.getElementById('forecast').value.trim();
    const p = document.getElementById('prepare').value.trim();
    const sum = document.getElementById('summary');
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
    chosen = null;
  }};
}})();
</script>
""",
        height=620,
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
