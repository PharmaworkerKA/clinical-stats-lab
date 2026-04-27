# 臨床統計ラボ - スケジュールエージェントガイド

このリポジトリは **臨床試験統計（SAS/R）** の実務情報を発信するブログ `臨床統計ラボ` の本体です。
あなた（スケジュールエージェント）は毎日JST 03:45に起動し、最新ネタをリサーチして記事を **2本** 生成します。

## 1日のタスク

1. **リサーチ**: WebSearch / WebFetch で SAS/R/SAP/Estimand/混合効果/生存時間 に関する最新トピック2件を収集
   - 候補例: PROC MIXED 実践活用／R admiral パッケージで ADaM／ICH E9(R1) Estimand 実装／Cox回帰のPH仮定検証／rtables でTLF出力
   - 一次ソース: PMDA/FDA/EMA/ICH/CDISC/MHLW/学会/PHUSE/PharmaSUG 等の公式
2. **画像選定**: Unsplash 無料画像（クエリ例: `site:unsplash.com pharma`, `site:unsplash.com clinical trial`, `site:unsplash.com data science`）
3. **記事生成**: `output/site/articles/<slug>.html`、本文1500-2200字、h2を3-4本、コード/表を適宜挿入
4. **index.html 更新**: `output/site/index.html` 内のカード一覧を最新6件に保つ
5. **sitemap.xml 更新**: `output/site/sitemap.xml` に新記事URLを追記
6. **git push**: `[auto] Add daily articles YYYY-MM-DD`

## 執筆ルール

- 日本語、専門家向け中立トーン（「です・ます」or 技術記述は「である」OK）
- タイトル30-50字、規制名・用語・年号を入れる
- 投稿に**必ず以下の免責**を末尾に1段落入れる:
  > 本記事は情報提供を目的としており、規制要件の最終確認は各国規制当局の公式ドキュメントを参照してください。実務適用の判断は読者の責任で行ってください。
- **景表法/金商法 NG**: 絶対/必ず/100%/必勝/誰でも/儲か/元本保証
- **薬機法 NG**: 「効く」「治る」「副作用なし」等、医薬品の効能効果の断定的表現
- 実在の患者・医療従事者の写真NG、Unsplash の人物無記名のみ
- ガイドライン・条文番号は**必ず公式リンクと併記**（推測URL禁止、貼る前に curl HEAD で200/301/302確認）
- 既存記事タイトルと重複しない（`output/site/articles/` を確認）

## 記事HTMLテンプレート（output/site/articles/<slug>.html）

```html
<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{記事タイトル}} | 臨床統計ラボ</title>
<meta name="description" content="{{150字以内の要約}}">
<link rel="canonical" href="https://pharmaworkerka.github.io/clinical-stats-lab/articles/{{slug}}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{{タイトル}}">
<meta property="og:description" content="{{要約}}">
<meta property="og:image" content="{{Unsplash画像URL}}">
<meta property="og:url" content="https://pharmaworkerka.github.io/clinical-stats-lab/articles/{{slug}}.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{{Unsplash画像URL}}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{{タイトル}}","image":"{{Unsplash}}","datePublished":"{{YYYY-MM-DD}}","author":{{"@type":"Organization","name":"臨床統計ラボ"}}}}</script>
<link rel="stylesheet" href="../assets/style.css">
</head><body>
<div data-tag="ml-pr-bar-v1" style="background:#fef3c7;color:#78350f;padding:6px 12px;text-align:center;font-size:12px;border-bottom:1px solid #fcd34d;font-family:system-ui,sans-serif;line-height:1.4">当サイトの記事には広告（アフィリエイトリンク）が含まれる場合があります。掲載順位や紹介内容は当サイトの編集方針に基づきます。</div>
<nav class="filter-nav"><a href="../index.html" class="filter-btn">← トップに戻る</a></nav>
<main class="article-body">
<img class="article-hero-img" src="{{Unsplash}}" alt="{{タイトル}}">
<p class="article-meta">📅 {{YYYY-MM-DD}} · 🏷️ {{カテゴリ}}</p>
<h1>{{タイトル}}</h1>
<p>{{リード文200字程度}}</p>
<h2>{{見出し1}}</h2><p>{{本文}}</p>
<h2>{{見出し2}}</h2><p>{{本文}}</p>
<h2>{{見出し3}}</h2><p>{{本文}}</p>
<h2>まとめ</h2><p>{{結論}}</p>
<p style="color:#6b7280;font-size:0.8rem;margin-top:40px;">本記事は情報提供を目的としており、規制要件の最終確認は各国規制当局の公式ドキュメントを参照してください。実務適用の判断は読者の責任で行ってください。</p>
<a href="../index.html" class="back-link">← 他の記事を見る</a>
</main>
<footer class="site-footer"><div class="footer-inner">
<p class="copyright">© 2026 臨床統計ラボ</p>
</div></footer>
</body></html>
```

## index.html 更新

`output/site/index.html` の記事カード領域を最新6件に保つ（古いカードは削除）。

## sitemap.xml 更新

```xml
<url>
  <loc>https://pharmaworkerka.github.io/clinical-stats-lab/articles/{{slug}}.html</loc>
  <lastmod>{{今日}}</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>
```

## 守ること

- 毎日2本、タイトル重複NG（`output/site/articles/` の既存ファイル名を必ず確認）
- 免責1段落を末尾必須
- pages.yml は変更しない（push されれば GitHub Pages が自動デプロイする）
- アフィリエイトリンクが入る場合は冒頭の PR バー（既にテンプレに入っている）を必ず保持

## 外部リンク張る時は必ず到達確認
記事内で公式サイト・ガイダンス文書への外部リンクを張る時、URL を書く前に必ず `curl -sI -m 10 -L "<URL>" -A "Mozilla/5.0" | head -1` で HTTP 200/301/302 を確認すること。
- 採用OK: 200/301/302
- 採用NG: 404/410/0(DNS失敗)/5xx
- 推測URLでガイダンス文書のリンクを書くな（ICH/PMDA/FDAは構造が複雑で死にやすい）
