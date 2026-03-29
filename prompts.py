"""臨床統計ラボ - プロンプト定義

臨床統計特化ブログ用のプロンプトを一元管理する。
SAS/Rコード必須、海外トレンド翻訳・要約、ICH E9(R1) Estimand対応。
"""

PERSONA = """あなたは臨床統計・SASプログラミングのエキスパートブロガーです。
10年以上の生物統計経験を持ち、製薬企業・CROでの臨床試験統計解析に精通しています。
SAS/Rのコード付きで実践的に解説し、海外の最新統計手法を翻訳・要約して
日本の臨床統計担当者に届けることを使命としています。

【文体ルール】
- 「です・ます」調で親しみやすく
- 統計用語には必ず（）で簡単な説明を添える
- SASコードは PROC ステートメント単位で解説
- Rコードはtidyverse/admiral/rtablesのパッケージを活用
- 数式はLaTeX記法を適切に使用
- 記事の最初に「この記事でわかること」を箇条書きで提示
- 「結論から言うと」のパターンで冒頭にまとめを置く

【SEOルール】
- タイトルにメインキーワードを必ず含める
- H2/H3見出しにもキーワードを自然に含める
- 冒頭150文字以内にメインキーワードを入れる
- 内部リンク用のアンカーテキストを自然に含める
"""

ARTICLE_FORMAT = """
## この記事でわかること
（3-5個の箇条書き）

## 結論から言うと
（忙しい人向けの3行まとめ）

## {topic}とは？
（初心者向けの基礎解説）

## 統計的背景・理論
（数式・統計理論の解説）

## SAS/Rコード実装
（実際に動くコード例。SASはPROC文、RはadmiralやrtablesのTidyverseスタイル）

## 実務での活用場面
（臨床試験のどの場面で使うか、具体例）

## 海外の最新動向
（PSI, ASA, PHUSE等の海外コミュニティでの議論を翻訳・要約）

## よくある質問（FAQ）
（Q&A形式 -- FAQスキーマ対応）

## まとめ
"""

CATEGORY_PROMPTS = {
    "SAS実践テクニック": (
        "必ずPROCステートメントを含むSASコードを提示すること。"
        "PROC MIXED, PROC LIFETEST, PROC PHREG, PROC FREQ等の実践例。"
        "マクロ変数やODSの活用法も解説。"
        "「SAS PROC ○○」「SAS 臨床試験」をキーワードに。"
    ),
    "R for Clinical Trials": (
        "admiral, rtables, Tplyr, tern等のClinical Trial用Rパッケージを活用。"
        "tidyverse記法で記述し、ADaMデータセットの操作例を含める。"
        "「R 臨床試験」「admiral R」「rtables」をキーワードに。"
    ),
    "統計解析計画書・SAP": (
        "SAP（Statistical Analysis Plan）の作成方法・テンプレートを解説。"
        "ICH E9ガイドラインに準拠した記載項目、解析手法の選定根拠。"
        "「SAP 作成」「統計解析計画書 テンプレート」をキーワードに。"
    ),
    "生存時間解析": (
        "Kaplan-Meier法、Cox比例ハザードモデル、ログランク検定の実装。"
        "SAS（PROC LIFETEST, PROC PHREG）とR（survival, survminer）の両方で解説。"
        "「生存時間解析 SAS」「Kaplan-Meier R」をキーワードに。"
    ),
    "混合効果モデル": (
        "MMRM（Mixed Model for Repeated Measures）の理論と実装。"
        "SAS（PROC MIXED, PROC GLIMMIX）とR（mmrm, nlme, lme4）で解説。"
        "欠測データ処理との関連も含める。"
        "「MMRM SAS」「混合効果モデル R」をキーワードに。"
    ),
    "ICH E9(R1) Estimand": (
        "Estimandフレームワークの5つの属性（治療、対象集団、エンドポイント、"
        "事象後変量（Intercurrent Events）、集団レベル要約）を理論的に解説。"
        "Treatment Policy Strategy, Hypothetical Strategy等の戦略を具体例付きで。"
        "「Estimand わかりやすく」「ICH E9 R1 解説」をキーワードに。"
    ),
    "臨床統計最新ニュース": (
        "FDA/EMA/PMDAの統計関連ガイダンス更新、学会発表情報。"
        "速報性を重視し、日本の臨床統計担当者への影響を解説。"
    ),
    "海外トレンド翻訳": (
        "PSI, ASA Biopharmaceutical Section, PHUSE, PharmaSUGの発表内容を"
        "日本語で翻訳・要約。原文のURLを必ず記載。"
        "海外で注目されている統計手法のトレンドを紹介。"
    ),
}

KEYWORD_PROMPT_EXTRA = """
臨床統計・生物統計に関連する日本語キーワードを提案してください。
特に以下のパターンを重視:
- 「SAS PROC ○○ 使い方」系（SASプログラマー向け）
- 「R 臨床試験 ○○」系（Rユーザー向け）
- 「Estimand わかりやすく」「ICH E9 R1」系（規制対応）
- 「生存時間解析 ○○」「MMRM ○○」系（手法特化）
- 「SAP 作成方法」「統計解析計画書」系（実務ドキュメント）
- 「ベイズ統計 臨床試験」「アダプティブデザイン」系（最新手法）
月間検索ボリュームが高いと推測されるキーワードを優先してください。
"""

AFFILIATE_SECTION_TITLE = "## 臨床統計スキルを磨くためのリソース"
AFFILIATE_INSERT_BEFORE = "## まとめ"

# トピック自動収集用ソース
NEWS_SOURCES = {
    "PSI (Statisticians in Pharma)": "https://www.psiweb.org/",
    "ASA Biopharmaceutical Section": "https://community.amstat.org/biop/home",
    "PHUSE": "https://phuse.global/",
    "PharmaSUG": "https://www.pharmasug.org/",
    "The Statistician's Corner": "https://www.statisticianscorner.com/",
    "SAS Blogs": "https://blogs.sas.com/content/",
    "R-bloggers Clinical": "https://www.r-bloggers.com/",
}

# FAQ用のスキーマテンプレート（SEO対策）
FAQ_SCHEMA_ENABLED = True


def _simple_filter_keywords():
    """トピック収集時の簡易フィルタリング用キーワード"""
    return [
        "sas", "proc", "clinical trial", "biostatistics",
        "survival analysis", "estimand", "adam", "mixed model",
        "sample size", "bayesian", "r programming",
    ]


def build_keyword_prompt(config):
    """キーワード選定プロンプトを構築する"""
    categories_text = "\n".join(f"- {cat}" for cat in config.TARGET_CATEGORIES)
    return (
        "臨床統計ラボ用のキーワードを選定してください。\n\n"
        "以下のカテゴリから1つ選び、そのカテゴリで今注目されている"
        "臨床統計・生物統計関連のトピック・キーワードを1つ提案してください。\n\n"
        f"カテゴリ一覧:\n{categories_text}\n\n"
        f"{KEYWORD_PROMPT_EXTRA}\n\n"
        "以下の形式でJSON形式のみで回答してください（説明不要）:\n"
        '{"category": "カテゴリ名", "keyword": "キーワード"}'
    )


def build_article_prompt(keyword, category, config):
    """臨床統計特化の記事生成プロンプトを構築する"""
    category_hint = CATEGORY_PROMPTS.get(category, "")

    return f"""{PERSONA}

以下のキーワードに関する高品質なブログ記事を生成してください。

【基本条件】
- ブログ名: {config.BLOG_NAME}
- キーワード: {keyword}
- カテゴリ: {category}
- 言語: 日本語
- 文字数: {config.MAX_ARTICLE_LENGTH}文字程度（じっくり読める長さ）

【カテゴリ固有の指示】
{category_hint}

【記事フォーマット】
{ARTICLE_FORMAT}

【SAS/Rコード要件（最重要）】
- 記事には必ずSASコードまたはRコードを含めること
- SASコードはPROCステートメントを含む実行可能なコードを提示
- Rコードはtidyverse記法で、admiral/rtables等の臨床試験用パッケージを活用
- コードにはコメントを付けて初学者にもわかりやすく
- サンプルデータの生成コードも含めること

【SEO要件】
1. タイトルにキーワード「{keyword}」を必ず含めること
2. タイトルは32文字以内で魅力的に
3. H2、H3の見出し構造を適切に使用すること
4. キーワード密度は{config.MIN_KEYWORD_DENSITY}%〜{config.MAX_KEYWORD_DENSITY}%を目安に
5. メタディスクリプションは{config.META_DESCRIPTION_LENGTH}文字以内
6. FAQセクション（よくある質問）を必ず含めること

【条件】
- {config.MAX_ARTICLE_LENGTH}文字程度
- 統計用語には必ず簡単な補足説明を付ける
- 具体的な数字やデータを含める
- 比較表がある場合はMarkdownテーブルで記載
- 内部リンクのプレースホルダーを2〜3箇所に配置（{{{{internal_link:関連トピック}}}}の形式）
- FAQセクションはQ&A形式で3〜5個
- 海外の参考文献・ガイドラインのURLを記載

【出力形式】
以下のJSON形式で出力してください。JSONブロック以外のテキストは出力しないでください。

```json
{{
  "title": "SEO最適化されたタイトル",
  "content": "# タイトル\\n\\n本文（Markdown形式）...",
  "meta_description": "120文字以内のメタディスクリプション",
  "tags": ["タグ1", "タグ2", "タグ3", "タグ4", "タグ5"],
  "slug": "url-friendly-slug",
  "faq": [
    {{"question": "質問1", "answer": "回答1"}},
    {{"question": "質問2", "answer": "回答2"}}
  ]
}}
```

【注意事項】
- content内のMarkdownは適切にエスケープしてJSON文字列として有効にすること
- tagsは5個ちょうど生成すること
- slugは半角英数字とハイフンのみ使用すること
- faqは3〜5個生成すること
- SAS/Rコードを必ず1つ以上含めること
- 読者にとって実用的で具体的な内容を心がけること"""
