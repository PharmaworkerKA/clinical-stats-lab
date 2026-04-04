#!/usr/bin/env python3
"""臨床統計ラボ - GitHub Actions用一括実行スクリプト

キーワード選定 → トピック収集 → 記事生成 → アフィリエイト挿入 → サイトビルド
を一括で実行する。

blog_engine共通モジュールを使用し、フォールバックとしてローカル実装を持つ。
"""
import json
import re
import time
import logging
import sys
from datetime import datetime
from pathlib import Path

# パス設定
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

import config
import prompts


def robust_json_parse(text):
    """堅牢なJSONパース: 不正エスケープ修復 + json_repairフォールバック"""
    # 1. そのままパース
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError:
        pass

    # 2. 不正エスケープを修復してリトライ
    fixed = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)
    try:
        return json.loads(fixed, strict=False)
    except json.JSONDecodeError:
        pass

    # 3. json_repairで修復
    try:
        import json_repair
        return json_repair.loads(text)
    except Exception:
        pass

    raise json.JSONDecodeError("全てのJSONパース手法が失敗", text, 0)


def run(cfg=None, prm=None):
    """メイン処理: キーワード選定 → 記事生成 → サイトビルド

    Args:
        cfg: ブログ設定モジュール（省略時はローカルconfig使用）
        prm: プロンプトモジュール（省略時はローカルprompts使用）
    """
    cfg = cfg or config
    prm = prm or prompts

    logger.info("=== %s 自動生成開始 ===", cfg.BLOG_NAME)
    start_time = datetime.now()

    # ディレクトリ確保
    for attr in ["OUTPUT_DIR", "ARTICLES_DIR", "SITE_DIR", "TOPICS_DIR"]:
        d = getattr(cfg, attr, None)
        if d:
            Path(d).mkdir(parents=True, exist_ok=True)

    # ステップ0: トピック収集（オプション）
    logger.info("ステップ0: トピック収集")
    try:
        from topic_collector import TopicCollector
        collector = TopicCollector(cfg, prm)
        topics = collector.collect_all()
        next_topic = collector.get_next_topic()
        if next_topic:
            logger.info("次のトピック: %s (スコア: %s)", next_topic.get("title", "?"), next_topic.get("score", "?"))
    except Exception as e:
        logger.warning("トピック収集スキップ: %s", e)
        next_topic = None

    # ステップ1: キーワード選定
    logger.info("ステップ1: キーワード選定")
    try:
        if next_topic and next_topic.get("keyword"):
            # トピックコレクターからキーワードを取得
            category = next_topic.get("category", cfg.TARGET_CATEGORIES[0])
            keyword = next_topic["keyword"]
            logger.info("トピックから選定: カテゴリ=%s, キーワード=%s", category, keyword)
        else:
            # Gemini APIでキーワード選定
            from google import genai

            if not cfg.GEMINI_API_KEY:
                logger.error("GEMINI_API_KEY が設定されていません")
                sys.exit(1)

            client = genai.Client(api_key=cfg.GEMINI_API_KEY)

            if prm and hasattr(prm, "build_keyword_prompt"):
                prompt = prm.build_keyword_prompt(cfg)
            else:
                categories_text = "\n".join(f"- {cat}" for cat in cfg.TARGET_CATEGORIES)
                prompt = (
                    f"{cfg.BLOG_NAME}用のキーワードを選定してください。\n\n"
                    f"カテゴリ一覧:\n{categories_text}\n\n"
                    'JSON形式のみ: {"category": "カテゴリ名", "keyword": "キーワード"}'
                )

            from google.genai import types as genai_types
            response = client.models.generate_content(
                model=cfg.GEMINI_MODEL,
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            response_text = response.text.strip()

            if "```" in response_text:
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            data = robust_json_parse(response_text)
            if isinstance(data, list):
                data = data[0]
            category = data["category"]
            keyword = data["keyword"]

        logger.info("選定結果 - カテゴリ: %s, キーワード: %s", category, keyword)

    except Exception as e:
        logger.error("キーワード選定失敗: %s", e)
        sys.exit(1)

    # ステップ2: 記事生成
    logger.info("ステップ2: 記事生成")
    max_retries = 3
    base_delay = 5
    article = None
    for attempt in range(1, max_retries + 1):
        try:
            from article_generator import ArticleGenerator
            from seo_optimizer import SEOOptimizer

            generator = ArticleGenerator(cfg)
            article = generator.generate_article(keyword=keyword, category=category, prompts=prm)
            logger.info("記事生成完了: %s", article.get("title", "不明"))

            optimizer = SEOOptimizer(cfg)
            seo_result = optimizer.check_seo_score(article)
            logger.info("SEOスコア: %d/100 (グレード: %s)", seo_result.get("total_score", 0), seo_result.get("grade", "?"))
            break
        except Exception as e:
            logger.warning("記事生成失敗 (試行%d/%d): %s", attempt, max_retries, e)
            if attempt == max_retries:
                logger.error("記事生成が%d回失敗しました。終了します。", max_retries)
                sys.exit(1)
            import time
            wait = base_delay * (2 ** (attempt - 1))
            logger.info("エクスポーネンシャルバックオフ: %d秒待機", wait)
            time.sleep(wait)

    # ステップ2.5: アフィリエイトリンク挿入
    logger.info("ステップ2.5: アフィリエイトリンク挿入")
    try:
        from affiliate import AffiliateManager
        aff = AffiliateManager(cfg, prm)
        article = aff.insert_affiliate_links(article)
        logger.info("アフィリエイト: %d件挿入", article.get("affiliate_count", 0))
    except Exception as e:
        logger.warning("アフィリエイト挿入スキップ: %s", e)

    # ステップ2.7: アイキャッチ画像挿入
    logger.info("ステップ2.7: アイキャッチ画像挿入")
    try:
        eyecatch_path = str(Path(__file__).parent.parent)
        if eyecatch_path not in sys.path:
            sys.path.insert(0, eyecatch_path)
        from eyecatch import add_eyecatch_to_article
        article = add_eyecatch_to_article(article, cfg.BLOG_NAME)
        logger.info("アイキャッチ画像: %s", article.get("eyecatch_url", "なし")[:80])
    except Exception as e:
        logger.warning("アイキャッチ画像挿入スキップ: %s", e)

    # ステップ2.8: 記事JSON再保存（アイキャッチ・アフィリエイト追加後）
    try:
        file_path = article.get("file_path")
        if file_path:
            save_data = {k: v for k, v in article.items() if k != "file_path"}
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            logger.info("記事を再保存: %s", file_path)
    except Exception as e:
        logger.warning("記事の再保存スキップ: %s", e)

    # ステップ3: サイトビルド
    logger.info("ステップ3: サイトビルド")
    try:
        from site_generator import SiteGenerator
        site_gen = SiteGenerator(cfg)
        site_gen.build_site()
        logger.info("サイトビルド完了")
    except Exception as e:
        logger.error("サイトビルド失敗: %s", e)
        sys.exit(1)

    # 完了
    duration = (datetime.now() - start_time).total_seconds()
    logger.info("=== 自動生成完了（%.1f秒） ===", duration)
    logger.info("  カテゴリ: %s", category)
    logger.info("  キーワード: %s", keyword)
    logger.info("  タイトル: %s", article.get("title", "不明"))
    logger.info("  SEOスコア: %d/100", seo_result.get("total_score", 0))


if __name__ == "__main__":
    run()
