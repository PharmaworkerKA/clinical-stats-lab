"""臨床統計ラボ - ブログ固有設定"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

BLOG_NAME = "臨床統計ラボ"
BLOG_DESCRIPTION = (
    "臨床試験の統計解析手法をSAS/Rのコード付きで毎日更新。"
    "海外の最新統計手法・ICH E9(R1) Estimandフレームワーク等を"
    "日本語で翻訳・要約し実践的に解説。"
)
BLOG_URL = "https://pharmaworkerka.github.io/clinical-stats-lab"
BLOG_TAGLINE = "臨床統計の実務情報をSAS/Rコード付きで発信"
BLOG_LANGUAGE = "ja"

GITHUB_REPO = "PharmaworkerKA/clinical-stats-lab"
GITHUB_BRANCH = "gh-pages"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

OUTPUT_DIR = BASE_DIR / "output"
ARTICLES_DIR = OUTPUT_DIR / "articles"
SITE_DIR = OUTPUT_DIR / "site"
TOPICS_DIR = OUTPUT_DIR / "topics"

TARGET_CATEGORIES = [
    "SAS実践テクニック",
    "R for Clinical Trials",
    "統計解析計画書・SAP",
    "生存時間解析",
    "混合効果モデル",
    "ICH E9(R1) Estimand",
    "臨床統計最新ニュース",
    "海外トレンド翻訳",
]

THEME = {
    "primary": "#7c3aed",
    "accent": "#5b21b6",
    "gradient_start": "#7c3aed",
    "gradient_end": "#6d28d9",
    "dark_bg": "#0f0a1e",
    "dark_surface": "#1e1533",
    "light_bg": "#f5f0ff",
    "light_surface": "#ffffff",
}

MAX_ARTICLE_LENGTH = 4000
ARTICLES_PER_DAY = 1
SCHEDULE_HOURS = [8]

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

ENABLE_SEO_OPTIMIZATION = True
MIN_SEO_SCORE = 75
MIN_KEYWORD_DENSITY = 1.0
MAX_KEYWORD_DENSITY = 3.0
META_DESCRIPTION_LENGTH = 120
ENABLE_INTERNAL_LINKS = True

AFFILIATE_LINKS = {
    "SAS認定資格": {
        "url": "https://www.sas.com/ja_jp/certification.html",
        "text": "SAS認定資格を取得する",
        "description": "SASプログラミングの公式認定",
    },
    "Amazon 統計学書籍": {
        "url": "https://www.amazon.co.jp",
        "text": "Amazonで統計学書籍を探す",
        "description": "臨床統計・生物統計の参考書",
    },
    "Udemy SAS/R講座": {
        "url": "https://www.udemy.com",
        "text": "UdemyでSAS/R講座を探す",
        "description": "動画で学ぶSAS/R統計プログラミング",
    },
    "楽天 統計書籍": {
        "url": "https://www.rakuten.co.jp",
        "text": "楽天で統計書籍を探す",
        "description": "統計学・データサイエンスの参考書",
    },
}
AFFILIATE_TAG = "musclelove07-22"

ADSENSE_CLIENT_ID = os.environ.get("ADSENSE_CLIENT_ID", "")
ADSENSE_ENABLED = bool(ADSENSE_CLIENT_ID)

DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 8093

# Google Analytics (GA4)
GOOGLE_ANALYTICS_ID = "G-CSFVD34MKK"

# Google Search Console 認証ファイル
SITE_VERIFICATION_FILES = {
    "googlea31edabcec879415.html": "google-site-verification: googlea31edabcec879415.html",
}
