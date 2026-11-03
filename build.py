#!/usr/bin/env python3
"""Build the VidDub project page (static GitHub Pages site)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "selection_manifest.json").read_text())
EXTRA = json.loads((ROOT / "project_page_manifest.json").read_text())
SHOWCASE = json.loads((ROOT / "benchmark_showcase_manifest.json").read_text())


def rename_display_text(value):
    """Update public-facing legacy names without rewriting stable asset paths."""
    if isinstance(value, dict):
        return {key: rename_display_text(item) for key, item in value.items()}
    if isinstance(value, list):
        return [rename_display_text(item) for item in value]
    if isinstance(value, str):
        return value.replace("CausalDub-Bench", "VidDub-Bench").replace(
            "CausalDub", "VidDub"
        )
    return value


DATA = rename_display_text(DATA)
EXTRA = rename_display_text(EXTRA)
SHOWCASE = rename_display_text(SHOWCASE)
EXTRA["comparisons"] = SHOWCASE["comparisons"]

# Later gallery should not repeat identities already shown in Baselines.
COMPARISON_KEYS = {
    item["key"] for item in EXTRA["comparisons"] if isinstance(item, dict) and item.get("key")
}
DATA["cases"] = [case for case in DATA["cases"] if case.get("key") not in COMPARISON_KEYS]
GALLERY_COUNT = len(DATA["cases"])
GALLERY_EN = sum(1 for case in DATA["cases"] if case.get("lang") == "en")
GALLERY_ZH = sum(1 for case in DATA["cases"] if case.get("lang") == "zh")

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VidDub — Replacement-Aware Distillation for Two-Step Video Dubbing</title>
<meta name="description" content="VidDub is a full-context video-dubbing editor trained with replacement-aware cross-audio supervision and distilled to two denoising steps.">
<meta property="og:title" content="VidDub — Two-Step Video Dubbing">
<meta property="og:description" content="Replacement-aware cross-audio supervision and full-context diffusion distillation for efficient video dubbing.">
<meta property="og:type" content="website">
<meta property="og:image" content="media/causaldub-og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="media/causaldub-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,550;9..144,700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#152228;
  --muted:#5a6a72;
  --line:rgba(21,34,40,.12);
  --soft:rgba(236,243,241,.78);
  --paper:#eef3f1;
  --panel:rgba(255,255,255,.72);
  --accent:#0f766e;
  --accent-2:#1d4e7a;
  --glow:#7eb8a8;
  --shadow:0 22px 60px rgba(18,34,40,.10);
  --radius:22px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;color:var(--ink);font-family:Manrope,ui-sans-serif,system-ui,sans-serif;line-height:1.55;
  background:
    radial-gradient(980px 520px at 8% -8%, rgba(126,184,168,.34), transparent 58%),
    radial-gradient(820px 460px at 96% 4%, rgba(29,78,122,.16), transparent 52%),
    radial-gradient(700px 420px at 50% 100%, rgba(15,118,110,.10), transparent 60%),
    linear-gradient(180deg,#f5f8f7 0%, #e8efed 48%, #f3f6f5 100%);
  min-height:100vh;overflow-x:hidden;
}
body::before,body::after{
  content:"";position:fixed;inset:auto;pointer-events:none;z-index:0;border-radius:999px;filter:blur(40px);
  opacity:.55;animation:drift 18s ease-in-out infinite alternate;
}
body::before{width:42vw;height:42vw;left:-12vw;top:12vh;background:rgba(126,184,168,.28)}
body::after{width:36vw;height:36vw;right:-10vw;top:48vh;background:rgba(29,78,122,.16);animation-delay:-7s}
.noise{
  position:fixed;inset:0;pointer-events:none;z-index:1;opacity:.035;mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
.page{position:relative;z-index:2}
a{color:var(--accent-2);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px}
nav{
  position:sticky;top:0;z-index:40;backdrop-filter:blur(16px) saturate(1.2);
  background:rgba(245,248,247,.78);border-bottom:1px solid rgba(21,34,40,.08);
}
.nav-inner{display:flex;align-items:center;gap:18px;min-height:58px}
.brand{display:inline-flex;align-items:center;gap:9px;font-weight:800;letter-spacing:-.04em;font-size:18px;color:var(--ink);text-decoration:none}
.brand img{width:34px;height:34px;border-radius:9px;display:block}
.nav-links{display:flex;gap:16px;margin-left:auto;flex-wrap:wrap;font-size:14px;font-weight:600}
.nav-links a{color:var(--muted);text-decoration:none;transition:color .2s ease}
.nav-links a:hover{color:var(--ink)}
.menu-button{display:none;margin-left:auto;border-color:var(--line);background:var(--panel)}

.hero{padding:64px 0 24px}
.hero-intro{display:grid;grid-template-columns:minmax(0,1fr) minmax(240px,330px);gap:54px;align-items:center;margin-bottom:34px}
.hero-copy{min-width:0}
.hero-logo{
  aspect-ratio:1;border-radius:28px;overflow:hidden;background:#0b1a1c;
  box-shadow:0 28px 70px rgba(15,45,50,.28);border:1px solid rgba(255,255,255,.08);
  animation:rise .8s cubic-bezier(.2,.7,.2,1) both;
}
.hero-logo img{width:100%;height:100%;display:block;object-fit:cover}
.eyebrow{
  display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:18px;
}
.hero-brand{
  font-family:Fraunces,Georgia,serif;font-size:clamp(56px,10vw,104px);line-height:.9;
  letter-spacing:-.05em;margin:0 0 16px;font-weight:700;
  background:linear-gradient(120deg,#12353a 10%, #0f766e 48%, #1d4e7a 92%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.hero h2{
  font-family:Fraunces,Georgia,serif;font-weight:550;font-size:clamp(22px,3.2vw,34px);
  line-height:1.2;letter-spacing:-.03em;max-width:18ch;margin:0 0 16px;
}
.lead{max-width:62ch;color:var(--muted);font-size:17px;margin:0 0 24px}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:34px}
.btn{
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  border-radius:999px;padding:11px 18px;font-weight:700;font-size:14px;
  border:1px solid var(--ink);text-decoration:none;transition:transform .2s ease, box-shadow .2s ease, background .2s ease;
}
.btn:hover{transform:translateY(-2px);text-decoration:none;box-shadow:0 12px 28px rgba(15,118,110,.18)}
.btn-primary{background:linear-gradient(120deg,var(--accent),var(--accent-2));border-color:transparent;color:#fff}
.btn-ghost{background:rgba(255,255,255,.45);color:var(--ink);backdrop-filter:blur(8px)}
.hero-visual{
  border-radius:20px;overflow:hidden;box-shadow:var(--shadow);
  border:1px solid rgba(19,32,40,.08);background:#111;
  animation:rise .85s cubic-bezier(.2,.7,.2,1) .08s both;
  transition:transform .35s ease, box-shadow .35s ease;
}
.hero-visual:hover{transform:translateY(-4px);box-shadow:0 28px 70px rgba(18,34,40,.16)}
.hero-visual img{display:block;width:100%;height:auto}
.caption{font-size:13px;color:var(--muted);margin-top:10px}

.stats{
  display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;
  margin:36px 0 8px;
}
.stat{
  background:var(--panel);border:1px solid var(--line);border-radius:18px;
  padding:16px 16px 14px;backdrop-filter:blur(10px);
  transition:transform .25s ease, box-shadow .25s ease;
  animation:rise .7s cubic-bezier(.2,.7,.2,1) both;
}
.stat:hover{transform:translateY(-3px);box-shadow:0 16px 36px rgba(18,34,40,.08)}
.stat:nth-child(2){animation-delay:.05s}
.stat:nth-child(3){animation-delay:.1s}
.stat:nth-child(4){animation-delay:.15s}
.stat b{display:block;font-family:Fraunces,Georgia,serif;font-size:28px;letter-spacing:-.03em;line-height:1.1}
.stat span{display:block;color:var(--muted);font-size:12px;font-weight:600;margin-top:4px}
.news-list{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.news-item{padding:18px 20px}
.news-item time{display:block;color:var(--accent);font-size:11px;font-weight:800;letter-spacing:.08em;margin-bottom:7px}
.news-item p{margin:0;font-weight:700}

section{padding:58px 0 10px}
section h3{
  font-family:Fraunces,Georgia,serif;font-size:clamp(28px,4vw,40px);
  letter-spacing:-.035em;margin:0 0 12px;font-weight:700;
}
.section-lead{color:var(--muted);max-width:70ch;margin:0 0 22px}
.panel{
  background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:22px;
  box-shadow:0 12px 34px rgba(19,32,40,.05);backdrop-filter:blur(12px);
}
.two{display:grid;grid-template-columns:1.1fr .9fr;gap:22px;align-items:start}
.panel img{width:100%;height:auto;border-radius:12px;display:block}
.bullets{margin:0;padding-left:18px}
.bullets li{margin:0 0 10px;color:var(--ink)}
.bullets li::marker{color:var(--accent)}

.table-wrap{overflow:auto;border-radius:14px;border:1px solid var(--line);box-shadow:inset -18px 0 18px -24px rgba(19,32,40,.65);background:rgba(255,255,255,.7)}
table{width:100%;border-collapse:collapse;font-size:13.5px;background:transparent;min-width:980px}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left}
th{background:rgba(236,243,241,.9);font-size:12px;letter-spacing:.02em}
tr.ours td{background:rgba(15,118,110,.10);font-weight:700}
.note{font-size:12.5px;color:var(--muted);margin-top:10px}

.toolbar{
  position:sticky;top:58px;z-index:30;background:rgba(245,248,247,.9);
  backdrop-filter:blur(12px);border:1px solid var(--line);border-radius:999px;
  padding:8px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0 18px;
}
button{
  border:1px solid transparent;background:transparent;color:var(--ink);
  border-radius:999px;padding:8px 14px;font-weight:700;font-size:13px;cursor:pointer;
  font-family:inherit;transition:transform .15s ease, background .15s ease, color .15s ease;
}
button:hover{transform:translateY(-1px)}
button.active,button.sync{background:var(--ink);color:#fff}
button.sync{margin-left:auto;background:var(--accent);border-color:var(--accent)}
button.ghost{border-color:var(--line);background:rgba(255,255,255,.7)}

.case{border-top:1px solid var(--line);padding:28px 0 36px}
.case-head{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:start;margin-bottom:14px}
.number{font-family:Fraunces,Georgia,serif;font-size:36px;font-weight:700;color:#9aafb4;letter-spacing:-.04em}
.title{font-size:18px;font-weight:800;margin-bottom:4px}
.prompt{color:var(--muted);font-size:13.5px;line-height:1.45;max-width:80ch;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.metrics{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}
.metric{background:var(--soft);border-radius:10px;padding:7px 9px;font-size:11px;color:var(--muted)}
.metric b{display:block;font-size:15px;color:var(--accent);font-weight:800}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.cell{min-width:0}
.label{display:flex;justify-content:space-between;align-items:center;font-size:12.5px;font-weight:800;margin:0 2px 6px}
.label small{font-weight:500;color:var(--muted)}
video{width:100%;display:block;background:#111;aspect-ratio:1/1;object-fit:contain;border-radius:10px;transition:transform .25s ease}
.cell:hover video,.compare-body figure:hover video,.long-card:hover video,.long-example:hover video{transform:scale(1.015)}
.grid.native video{aspect-ratio:7/4}
.cross video{outline:2px solid var(--accent);outline-offset:-2px}
.hint{font-size:12px;color:var(--muted);margin:0 0 14px}
.domain-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.domain-card,.evidence-card,.long-card{
  overflow:hidden;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  box-shadow:0 12px 34px rgba(19,32,40,.05);backdrop-filter:blur(10px);
  transition:transform .28s ease, box-shadow .28s ease;
}
.domain-card:hover,.evidence-card:hover,.long-card:hover,.comparison-card:hover,.long-example:hover{
  transform:translateY(-4px);box-shadow:0 20px 44px rgba(18,34,40,.10);
}
.card-copy{padding:20px 22px 16px}
.card-copy h4,.evidence-copy h4{font-family:Fraunces,Georgia,serif;font-size:24px;line-height:1.1;letter-spacing:-.025em;margin:0 0 7px}
.card-copy p,.evidence-copy p{margin:0;color:var(--muted);font-size:13.5px}
.tag{display:inline-block;color:var(--accent);font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px}
.media-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px;background:var(--line)}
.media-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.media-grid.four{grid-template-columns:repeat(4,minmax(0,1fr))}
.media-grid figure{min-width:0;margin:0;background:#fff}
.media-grid figcaption{padding:8px 11px 10px;color:var(--muted);font-size:11.5px;font-weight:700}
.media-grid.wide video{aspect-ratio:16/9}
.benchmark-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}
.benchmark-tabs button{border-color:var(--line);background:rgba(255,255,255,.75)}
.benchmark-tabs button.active{background:var(--ink);color:#fff;border-color:var(--ink)}
.comparison-list{display:grid;gap:18px}
.comparison-card{overflow:hidden;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:0 12px 34px rgba(19,32,40,.05);backdrop-filter:blur(10px);transition:transform .28s ease, box-shadow .28s ease}
.compare-controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:0 22px 18px}
.compare-controls audio{height:34px;max-width:280px}
.compare-body{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:2px;background:var(--line)}
.compare-body figure{margin:0;background:#fff;min-width:0}
.compare-body video{border-radius:0}
.compare-body.square video{aspect-ratio:1/1}
.compare-body.wide video{aspect-ratio:16/9}
.compare-body figcaption{padding:9px 11px 11px;color:var(--muted);font-size:11.5px;font-weight:800}
.compare-body figure:first-child{box-shadow:inset 0 3px 0 var(--accent-2)}
.sample-index{color:var(--muted);font-variant-numeric:tabular-nums}
.group-play{background:var(--ink);color:#fff}
.evidence-list{display:grid;gap:18px}
.evidence-card{display:block}
.evidence-copy{padding:28px;display:flex;flex-direction:column;justify-content:center}
.evidence-copy h4{font-size:28px;margin-bottom:12px}
.long-reference{display:grid;grid-template-columns:minmax(260px,.8fr) 1.2fr;gap:18px;margin-bottom:18px;align-items:center}
.long-reference figure{margin:0}
.long-input{padding:22px}
.long-input audio{width:100%;margin-top:10px}
.long-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.long-card figure{margin:0}
.long-card video{aspect-ratio:1/1;border-radius:0}
.long-card figcaption{padding:8px 12px 12px;color:var(--muted);font-size:11.5px;font-weight:700}
.long-card.failure{border-color:#e5c1a6}
.long-card.success{border-color:#9dccbd}
.long-controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 16px}
.long-controls audio{height:34px;max-width:320px}
.long-more-title{font-family:Fraunces,Georgia,serif;font-size:25px;margin:32px 0 7px}
.long-more-lead{color:var(--muted);font-size:13px;margin:0 0 16px}
.long-examples{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.long-example{padding:0;overflow:hidden;transition:transform .28s ease, box-shadow .28s ease}
.long-example-head{padding:18px 20px 12px}
.long-example-head h4{font-family:Fraunces,Georgia,serif;font-size:22px;margin:0 0 10px}
.long-example .compare-controls{padding:0}
.long-example .compare-controls audio{max-width:240px}
.long-example .media-grid video{aspect-ratio:1/1;border-radius:0}
.load-row{display:flex;justify-content:center;padding:18px 0 0}
.load-more{background:var(--ink);color:#fff;padding:11px 20px}
.limits{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;list-style:none;padding:0;margin:0}
.limits li{padding:18px;border-radius:14px;background:var(--soft);color:var(--muted);font-size:13px;backdrop-filter:blur(8px);transition:transform .25s ease}
.limits li:hover{transform:translateY(-2px)}

.reveal{opacity:0;transform:translateY(18px);transition:opacity .7s cubic-bezier(.2,.7,.2,1), transform .7s cubic-bezier(.2,.7,.2,1)}
.reveal.visible{opacity:1;transform:none}
.reveal-delay-1{transition-delay:.06s}
.reveal-delay-2{transition-delay:.12s}

.bib{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px;
  white-space:pre-wrap;background:var(--soft);border-radius:12px;padding:16px;overflow:auto;
  border:1px solid var(--line);
}
footer{padding:40px 0 70px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);margin-top:40px}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes drift{from{transform:translate3d(0,0,0) scale(1)}to{transform:translate3d(4vw,3vh,0) scale(1.08)}}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
  .reveal{opacity:1;transform:none}
}
@media(max-width:900px){
  .hero-intro{grid-template-columns:1fr minmax(200px,280px);gap:28px}
  .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
  .news-list{grid-template-columns:1fr}
  .two{grid-template-columns:1fr}
  .domain-grid,.long-grid,.long-examples,.evidence-card{grid-template-columns:1fr}
  .media-grid.four,.compare-body,.long-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .long-reference{grid-template-columns:1fr}
  .limits{grid-template-columns:1fr}
  .case-head{grid-template-columns:auto 1fr}
  .metrics{grid-column:1/-1;justify-content:flex-start}
  .grid{grid-template-columns:1fr}
  button.sync{margin-left:0}
  .menu-button{display:inline-flex}
  .nav-links{display:none;position:absolute;top:58px;left:16px;right:16px;padding:14px;background:rgba(255,255,255,.96);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}
  .nav-links.open{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:560px){
  .wrap{padding:0 16px}
  .hero{padding-top:38px}
  .hero-intro{grid-template-columns:1fr}
  .hero-logo{width:min(78vw,300px);justify-self:center}
  .stats{grid-template-columns:1fr 1fr}
  .compare-body,.long-grid{grid-template-columns:1fr}
  .toolbar{position:static;border-radius:16px}
  table{font-size:12px}
}
</style>
</head>
<body>
<div class="noise" aria-hidden="true"></div>
<div class="page">
<nav><div class="wrap nav-inner">
  <a class="brand" href="#">VidDub</a>
  <button class="menu-button" id="menu" aria-expanded="false" aria-controls="nav-links">Sections</button>
  <div class="nav-links" id="nav-links">
    <a href="#news">News</a>
    <a href="#abstract">Abstract</a>
    <a href="#method">Method</a>
    <a href="#results">Results</a>
    <a href="#comparisons">Baselines</a>
    <a href="#evidence">Ablations</a>
    <a href="#long">Long-20</a>
    <a href="#videos">Gallery</a>
    <a href="#cite">Cite</a>
  </div>
</div></nav>

<header class="hero"><div class="wrap">
  <div class="hero-intro">
    <div class="hero-copy">
      <div class="eyebrow">Replacement-aware video dubbing</div>
      <h1 class="hero-brand">VidDub</h1>
      <h2>Follow new speech. Preserve the source.</h2>
      <p class="lead">
        A full-context diffusion editor that learns from replacement speech and
        generates synchronized, source-preserving video in two denoising steps.
      </p>
      <div class="cta">
        <a class="btn btn-primary" href="https://github.com/LAW1223/VidDub">GitHub</a>
        <a class="btn btn-ghost" href="#comparisons">Compare methods</a>
        <a class="btn btn-ghost" href="https://arxiv.org/abs/2611.03404">Paper</a>
      </div>
    </div>
    <div class="hero-logo" aria-label="VidDub">
      <div style="height:100%;display:grid;place-items:center;color:white;font-family:Fraunces,Georgia,serif;font-size:clamp(42px,7vw,72px);font-weight:700;letter-spacing:-.05em;background:linear-gradient(145deg,#0b1a1c,#0f766e 55%,#1d4e7a)">VidDub</div>
    </div>
  </div>
  <div class="hero-visual">
    <img src="media/teaser.png" alt="VidDub replacement-speech dubbing across captured, web, generated, and long-form sources">
  </div>
  <p class="caption">VidDub edits captured, web, generated, and 60-second videos with replacement speech. It reaches 11.3 FPS on one H20 with two denoising steps.</p>

  <div class="stats">
    <div class="stat"><b>2</b><span>denoising steps per window</span></div>
    <div class="stat"><b>11.3</b><span>prepared-input FPS · single H20</span></div>
    <div class="stat"><b>10.102</b><span>HDTF replacement Sync-C</span></div>
    <div class="stat"><b>8.709</b><span>VidDub-Bench replacement Sync-C</span></div>
  </div>
</div></header>

<section id="news" class="reveal"><div class="wrap">
  <h3>News</h3>
  <div class="news-list">
    <article class="panel news-item"><time>2026-11-03</time><p><a href="https://github.com/LAW1223/VidDub">Training code released.</a></p></article>
    <article class="panel news-item"><time>2026-11-03</time><p><a href="https://huggingface.co/AIPeanutman/VidDub">Model weights released.</a></p></article>
    <article class="panel news-item"><time>2026-11-02</time><p><a href="https://arxiv.org/abs/2611.03404">Paper released on arXiv.</a></p></article>
  </div>
</div></section>

<section id="abstract" class="reveal"><div class="wrap">
  <h3>Abstract</h3>
  <div class="panel">
    <p style="margin:0;color:var(--ink)">
      Video dubbing aims to synthesize lip movements that match target speech while
      preserving the identity, head pose, and background of a source video. Existing
      editors are predominantly trained through self-reconstruction with the original
      paired audio, although the recorded mouth conflicts with the desired articulation
      after speech replacement. VidDub introduces replacement-aware cross-audio
      supervision: paired-audio samples retain full-frame reconstruction, while unpaired
      samples mask source-mouth reconstruction and use audio–visual synchronization to
      supervise articulation, with spatial reconstruction preserving the remaining
      content. A full-context teacher learns this objective before matched trajectory
      regression transfers its guided trajectories to a two-step student; distribution
      matching distillation then restores visual quality after compression. We will
      release 85,435 curated training clips, VidDub-Bench, fixed evaluation manifests,
      preprocessing outputs, and unified evaluation code. Across three training seeds,
      removing conflicting source-mouth reconstruction improves replacement-audio Sync-C
      by 0.833±0.040, and the final model combines strong synchronization with visual
      quality, identity preservation, and visual-speech recognition across four
      benchmarks.
    </p>
  </div>
</div></section>

<section id="method" class="reveal"><div class="wrap">
  <h3>Method</h3>
  <p class="section-lead">VidDub first removes conflicting source-mouth reconstruction under replacement speech, then compresses the resulting full-context teacher into a two-step full-context student.</p>
  <div class="two">
    <div class="panel">
      <img src="media/architecture.png" alt="VidDub full-context editing architecture">
      <p class="caption">Source and reference features preserve appearance, frame-local audio controls articulation, and bidirectional attention jointly models the complete 81-frame window.</p>
    </div>
    <div class="panel">
      <ul class="bullets">
        <li><b>Replacement-aware supervision</b> — reconstruct the complete frame for paired speech, but remove conflicting mouth reconstruction for replacement speech.</li>
        <li><b>Matched trajectory regression</b> — transfer guided same- and cross-audio teacher trajectories to a two-step student.</li>
        <li><b>Distribution matching distillation</b> — recover visual quality after step compression while preserving non-mouth source content.</li>
        <li><b>Full-context inference</b> — exploit the complete source video and target speech available in offline dubbing.</li>
      </ul>
    </div>
  </div>
  <div class="panel" style="margin-top:18px">
    <img src="media/training.png" alt="VidDub replacement-aware training and diffusion distillation">
    <p class="caption">Replacement-aware full-context training, matched trajectory regression, and guided distribution matching distillation. Auxiliary score networks are used only during training.</p>
  </div>
</div></section>

<section id="results" class="reveal"><div class="wrap">
  <h3>Results</h3>
  <p class="section-lead">Complete cross-audio summary across captured, web, and generated sources. Each cell is Sync-C↑ / FVD↓; results use each method’s scoreable subset, with coverage audited separately.</p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Method</th><th>NFE</th>
          <th>HDTF-30</th><th>VoxCeleb2-30</th><th>TalkVid-500</th><th>VDB-256</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Wav2Lip</td><td>1</td><td>8.782 / 129.51</td><td>7.800 / 71.73</td><td>6.750 / 111.19</td><td>6.922 / 98.62</td></tr>
        <tr><td>Diff2Lip</td><td>25</td><td>8.680 / 99.70</td><td>7.533 / 67.15</td><td>6.944 / 73.37</td><td>7.575 / 58.87</td></tr>
        <tr><td>LatentSync 1.6</td><td>20</td><td>8.160 / 28.05</td><td>6.239 / 28.89</td><td>6.860 / 59.27</td><td>7.544 / 46.77</td></tr>
        <tr><td>Lip Forcing</td><td>2</td><td>6.884 / 33.80</td><td>4.871 / 41.03</td><td>5.610 / 12.68</td><td>5.192 / 15.78</td></tr>
        <tr><td>Full-context teacher</td><td>30/30/48</td><td>9.422 / 27.49</td><td>7.382 / 39.11</td><td>7.663 / 8.51</td><td>8.718 / 15.23</td></tr>
        <tr class="ours"><td>VidDub</td><td>2</td><td>10.102 / 27.66</td><td>8.454 / 46.52</td><td>7.646 / 10.25</td><td>8.709 / 17.50</td></tr>
      </tbody>
    </table>
  </div>
  <p class="note">Swipe horizontally on small screens. VDB is the source-disjoint VidDub-Bench. TalkVid success ranges from 402/500 to 500/500; its all-method common intersection has 308 items. Full coverage, Sync-D, confidence intervals, VSR, preservation, and human evaluation are reported in the paper.</p>
  <div class="panel" style="margin-top:18px">
    <img src="media/results.jpg" alt="Cross-audio synchronization versus distribution quality on four benchmarks">
    <p class="caption">Replacement-audio synchronization and distribution quality across four benchmarks; complete metrics and coverage are reported in the paper.</p>
  </div>
</div></section>

<section id="comparisons" class="reveal"><div class="wrap">
  <h3>Comparison with prior methods</h3>
  <p class="section-lead">Six matched examples from each of four benchmarks. Every row fixes both the reference video and replacement-speech input across methods; these examples complement—not replace—the frozen aggregate metrics above.</p>
  <div class="benchmark-tabs" id="benchmark-tabs"></div>
  <div class="comparison-list" id="comparison-list"></div>
</div></section>

<section id="evidence" class="reveal"><div class="wrap">
  <h3>Matched interventions</h3>
  <p class="section-lead">The page separates the source of replacement control from the role of few-step quality recovery.</p>
  <div class="evidence-list" id="evidence-list"></div>
</div></section>

<section id="long" class="reveal"><div class="wrap">
  <h3 id="long-title">Long-20</h3>
  <p class="section-lead" id="long-description"></p>
  <div class="long-reference panel">
    <div id="long-source"></div>
    <div class="long-input">
      <span class="tag">Shared inputs</span>
      <h4>Reference video + replacement speech</h4>
      <p class="hint">All four outputs below use this same visual reference and target audio.</p>
      <audio id="long-audio" controls preload="metadata"></audio>
      <div class="long-controls" style="margin-top:14px">
        <button class="group-play" data-group="long-grid">Play all from start</button>
        <button class="ghost group-pause" data-group="long-grid">Pause all</button>
      </div>
    </div>
  </div>
  <div class="long-grid" id="long-grid"></div>
  <h4 class="long-more-title">Five additional 60-second cases</h4>
  <p class="long-more-lead">For five of the six cases, the generated lower-face region is pasted back into the native Long-20 frames. References retain original speech; VidDub outputs contain replacement speech. Pair 14 remains a 512-crop multi-method comparison.</p>
  <div class="long-examples" id="long-examples"></div>
</div></section>

<section id="videos" class="reveal"><div class="wrap">
  <h3>VidDub-Bench gallery</h3>
  <p class="section-lead">
    __GALLERY_COUNT__ additional source-disjoint VidDub-Bench examples (__GALLERY_EN__ English / __GALLERY_ZH__ Chinese),
    selected by a reproducible sync + reconstruction gate and visual farthest-point sampling.
    Cases already shown in the Baselines section are omitted here. Each case shows source, same-audio reconstruction, and replacement-speech edit.
  </p>
  <p class="hint">Six cases load initially. Clips autoplay muted when visible; unmuting one clip automatically mutes the others.</p>
  <div class="toolbar">
    <button class="filter active" data-lang="all">All</button>
    <button class="filter" data-lang="en">English</button>
    <button class="filter" data-lang="zh">Chinese</button>
    <button class="ghost" id="mute">Mute all</button>
    <button class="sync" id="play">Replay visible</button>
  </div>
  <main id="cases"></main>
  <div class="load-row"><button class="load-more" id="load-more">Load 6 more cases</button></div>
</div></section>

<section id="limits" class="reveal"><div class="wrap">
  <h3>Scope and limitations</h3>
  <ul class="limits" id="limitations"></ul>
</div></section>

<section id="cite" class="reveal"><div class="wrap">
  <h3>Cite</h3>
  <p class="section-lead">Paper: <a href="https://arxiv.org/abs/2611.03404">arXiv:2611.03404</a>.</p>
  <div class="bib" id="bib">@article{liu2026viddub,
  title   = {VidDub: Replacement-Aware Distillation for Two-Step Video Dubbing},
  author  = {Liu, Yexin and Lin, Yunlong and Wang, Zehan and He, Guangxin and
             Xu, Xinli and Zha, Jiajun and Liu, Yaofu and Wang, Yueze and
             Ping, Bowen and Li, Yuanming and Wang, Amie and Ghanem, Bernard and
             Li, Bing and Yang, Harry},
  journal = {arXiv preprint arXiv:2611.03404},
  year    = {2026}
}</div>
</div></section>

<footer><div class="wrap">
  VidDub project page · video results and benchmark numbers from VidDub-Bench.
  Lip-editing technology can be misused; use only with consent and provenance watermarking.
</div></footer>
</div>

<script>
const DATA = __DATA__;
const EXTRA = __EXTRA__;
const root = document.getElementById('cases');
let io = null;
let activeLang = 'all';
let visibleCount = 6;
function esc(x){
  return String(x||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function media(src,label){
  if(!src) return '';
  return `<figure><video controls loop playsinline preload="metadata" aria-label="${esc(label)}" title="${esc(label)}" src="${esc(src)}"></video><figcaption>${esc(label)}</figcaption></figure>`;
}
const benchmarks=[...new Set(EXTRA.comparisons.map(x=>x.benchmark))];
let activeBenchmark=benchmarks[0];
const tabs=document.getElementById('benchmark-tabs');
tabs.innerHTML=benchmarks.map((x,i)=>`<button class="${i===0?'active':''}" data-benchmark="${esc(x)}">${esc(x)} · 6</button>`).join('');
function renderComparisons(){
  document.getElementById('comparison-list').innerHTML=EXTRA.comparisons.filter(x=>x.benchmark===activeBenchmark).map((x,i)=>
    `<article class="comparison-card" data-sync-card><div class="card-copy"><span class="tag">${esc(x.regime)} · <span class="sample-index">sample ${String(i+1).padStart(2,'0')}/06</span></span><h4>${esc(x.title)}</h4><p>${esc(x.description)}</p></div><div class="compare-controls"><button class="group-play">Play synchronized</button><button class="ghost group-pause">Pause</button><span class="hint" style="margin:0">Aligned replacement speech:</span><audio controls preload="metadata" src="${esc(x.audio)}"></audio></div><p class="hint" style="padding:0 22px;margin-top:-8px">Two modes: use synchronized playback for a shared audio clock, or play any video directly with its own audio. Starting one individual player pauses other audio.</p><div class="compare-body ${esc(x.aspect)}">${x.items.map(v=>media(v.video,v.label)).join('')}</div></article>`
  ).join('');
  wireComparisonControls();
  wireExclusiveAudio(document.getElementById('comparison-list'));
}
tabs.querySelectorAll('button').forEach(b=>b.onclick=()=>{
  tabs.querySelectorAll('button').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');activeBenchmark=b.dataset.benchmark;renderComparisons();
});
document.getElementById('evidence-list').innerHTML=EXTRA.ablations.map(x=>
  `<article class="evidence-card"><div class="evidence-copy"><span class="tag">${esc(x.eyebrow)}</span><h4>${esc(x.title)}</h4><p>${esc(x.description)}</p></div></article>`
).join('');
document.getElementById('long-title').textContent=EXTRA.long_form.title;
document.getElementById('long-description').textContent=EXTRA.long_form.description;
document.getElementById('long-audio').src=EXTRA.long_form.audio;
document.getElementById('long-source').innerHTML=media(EXTRA.long_form.source,'Reference video');
document.getElementById('long-grid').innerHTML=EXTRA.long_form.items.map(x=>
  `<article class="long-card ${esc(x.kind)}"><div class="card-copy"><span class="tag">${esc(x.note)}</span><h4>${esc(x.label)}</h4></div>${media(x.video,x.label)}</article>`
).join('');
document.getElementById('long-examples').innerHTML=EXTRA.long_form.additional_cases.map(x=>
  `<article class="long-example panel" data-sync-card>
    <div class="long-example-head">
      <span class="tag">Overlapping windows · 60 seconds</span>
      <h4>${esc(x.label)}</h4>
      <div class="compare-controls">
        <audio controls preload="metadata" src="${esc(x.audio)}"></audio>
        <button class="group-play">Play together</button>
        <button class="ghost group-pause">Pause</button>
      </div>
    </div>
    <div class="media-grid">
      ${media(x.source,'Reference video')}
      ${media(x.output,'VidDub · replacement speech','replacement')}
    </div>
  </article>`
).join('');
document.getElementById('limitations').innerHTML=EXTRA.limitations.map(x=>`<li>${esc(x)}</li>`).join('');
let suppressExclusiveAudio=false;
function wireExclusiveAudio(scope=document){
  scope.querySelectorAll('video').forEach(v=>{
    if(v.dataset.audioWired) return;
    v.dataset.audioWired='1';
    v.addEventListener('play',()=>{
      if(activeSync||v.muted) return;
      document.querySelectorAll('video').forEach(other=>{if(other!==v) other.pause();});
      document.querySelectorAll('audio').forEach(a=>a.pause());
    });
    v.addEventListener('volumechange',()=>{
      if(suppressExclusiveAudio||v.muted) return;
      document.querySelectorAll('video').forEach(other=>{if(other!==v) other.muted=true;});
      document.querySelectorAll('audio').forEach(a=>a.pause());
    });
  });
  scope.querySelectorAll('audio').forEach(a=>{
    if(a.dataset.audioWired) return;
    a.dataset.audioWired='1';
    a.addEventListener('play',()=>{
      document.querySelectorAll('audio').forEach(other=>{if(other!==a) other.pause();});
      if(!activeSync) document.querySelectorAll('video').forEach(v=>v.pause());
    });
  });
}
let activeSync=null;
function stopActiveSync(reset=false){
  if(!activeSync) return;
  clearInterval(activeSync.timer);
  suppressExclusiveAudio=true;
  activeSync.videos.forEach((v,i)=>{
    v.pause();v.loop=true;v.muted=activeSync.mutedStates[i];
    if(reset)v.currentTime=0;
  });
  requestAnimationFrame(()=>{suppressExclusiveAudio=false;});
  activeSync.audio.pause();
  if(reset) activeSync.audio.currentTime=0;
  activeSync=null;
}
function playTogether(container,audio){
  stopActiveSync(false);
  const videos=[...container.querySelectorAll('video')];
  const mutedStates=videos.map(v=>v.muted);
  videos.forEach(v=>{v.pause();v.loop=false;v.currentTime=0;v.muted=true;});
  audio.currentTime=0;
  const align=()=>videos.forEach(v=>{
    if(Math.abs(v.currentTime-audio.currentTime)>.18) v.currentTime=Math.min(audio.currentTime,v.duration||audio.currentTime);
    if(!audio.paused && v.paused && !v.ended) v.play().catch(()=>{});
  });
  activeSync={videos,audio,mutedStates,timer:setInterval(align,250)};
  audio.onseeking=align;
  audio.onended=()=>stopActiveSync(true);
  audio.onpause=()=>{if(activeSync&&activeSync.audio===audio) videos.forEach(v=>v.pause());};
  videos.forEach(v=>v.play().catch(()=>{}));
  audio.play().catch(()=>stopActiveSync(false));
}
function pauseTogether(container,audio){
  if(activeSync&&activeSync.audio===audio) stopActiveSync(false);
  else{
    container.querySelectorAll('video').forEach(v=>v.pause());
    if(audio) audio.pause();
  }
}
function wireComparisonControls(){
  document.querySelectorAll('[data-sync-card]').forEach(card=>{
    const audio=card.querySelector('audio');
    card.querySelector('.group-play').onclick=()=>playTogether(card,audio);
    card.querySelector('.group-pause').onclick=()=>pauseTogether(card,audio);
  });
}
document.querySelector('#long .group-play').onclick=()=>playTogether(document.getElementById('long-grid'),document.getElementById('long-audio'));
document.querySelector('#long .group-pause').onclick=()=>pauseTogether(document.getElementById('long-grid'),document.getElementById('long-audio'));
function wireAutoplay(){
  if(io) io.disconnect();
  io = new IntersectionObserver((entries)=>{
    entries.forEach(en=>{
      const v = en.target;
      if(en.isIntersecting && en.intersectionRatio >= 0.35){
        v.play().catch(()=>{});
      }else{
        v.pause();
      }
    });
  }, {threshold:[0,0.35,0.7]});
  document.querySelectorAll('#cases video').forEach(v=>io.observe(v));
}
function render(reset=true){
  const filtered=DATA.cases.filter(x=>activeLang==='all'||x.lang===activeLang);
  const start=reset?0:root.children.length;
  if(reset) root.innerHTML='';
  filtered.slice(start,visibleCount).forEach(x=>{
    const m=x.metrics;
    const el=document.createElement('section');
    el.className='case';
    const vattrs=`controls muted autoplay loop playsinline preload="metadata"`;
    el.innerHTML=`<div class="case-head"><div class="number">${String(x.rank).padStart(2,'0')}</div><div><div class="title">${esc(x.lang.toUpperCase())} · ${esc(x.age_group)} · ${esc(x.gender_group)}</div><div class="prompt" title="${esc(x.prompt)}">${esc(x.prompt)}</div><div class="compare-controls" style="padding:10px 0 0"><span class="hint" style="margin:0">Replacement-speech input:</span><audio controls preload="metadata" src="${esc(x.files.audio_cross)}"></audio></div></div><div class="metrics"><div class="metric"><b>${m.cross_sync_c.toFixed(2)}</b>Cross Sync-C</div><div class="metric"><b>${m.same_ssim.toFixed(3)}</b>Same SSIM</div><div class="metric"><b>${m.cross_sync_d.toFixed(2)}</b>Cross Sync-D</div></div></div><div class="grid ${x.presentation==='native'?'native':''}"><div class="cell"><div class="label">Reference video <small>original</small></div><video ${vattrs} src="${x.files.source}"></video></div><div class="cell"><div class="label">Same audio <small>reconstruction</small></div><video ${vattrs} src="${x.files.same}"></video></div><div class="cell cross"><div class="label">Replacement <small>VidDub</small></div><video ${vattrs} src="${x.files.cross}"></video></div></div>`;
    root.appendChild(el);
  });
  wireExclusiveAudio(root);
  wireAutoplay();
  const more=document.getElementById('load-more');
  const remaining=filtered.length-visibleCount;
  more.hidden=remaining<=0;
  more.textContent=remaining>0?`Load ${Math.min(6,remaining)} more cases`:'All cases loaded';
}
document.querySelectorAll('.filter').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.filter').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
  activeLang=b.dataset.lang;
  visibleCount=6;
  render(true);
});
document.getElementById('mute').onclick=()=>{
  document.querySelectorAll('video').forEach(v=>v.muted=true);
  document.querySelectorAll('audio').forEach(a=>a.pause());
};
document.getElementById('play').onclick=()=>document.querySelectorAll('#cases video').forEach(v=>{
  const r=v.getBoundingClientRect();
  const vis=r.top<window.innerHeight && r.bottom>0;
  if(vis){v.currentTime=0;v.play().catch(()=>{});}
});
document.getElementById('load-more').onclick=()=>{visibleCount+=6;render(false);};
const menu=document.getElementById('menu');
const navLinks=document.getElementById('nav-links');
menu.onclick=()=>{
  const open=navLinks.classList.toggle('open');
  menu.setAttribute('aria-expanded',String(open));
};
navLinks.querySelectorAll('a').forEach(a=>a.onclick=()=>{navLinks.classList.remove('open');menu.setAttribute('aria-expanded','false');});
wireExclusiveAudio();
renderComparisons();
render(true);
const revealIo=new IntersectionObserver((entries)=>{
  entries.forEach(en=>{if(en.isIntersecting){en.target.classList.add('visible');revealIo.unobserve(en.target);}});
},{threshold:.12,rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal').forEach(el=>revealIo.observe(el));
</script>
</body>
</html>
'''


def main() -> None:
    html = (
        HTML.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
        .replace("__EXTRA__", json.dumps(EXTRA, ensure_ascii=False))
        .replace("__GALLERY_COUNT__", str(GALLERY_COUNT))
        .replace("__GALLERY_EN__", str(GALLERY_EN))
        .replace("__GALLERY_ZH__", str(GALLERY_ZH))
    )
    (ROOT / "index.html").write_text(html)
    print(ROOT / "index.html")
    print(f"gallery cases kept: {GALLERY_COUNT} ({GALLERY_EN} en / {GALLERY_ZH} zh)")


if __name__ == "__main__":
    main()
