"""臨床統計ラボ - 記事生成エンジン（スタンドアロン版）

blog_engineの共通モジュールを使用し、フォールバックとしてローカル実装を持つ。
"""
import sys
from pathlib import Path

# blog_engine へのフォールバックimport
_engine_path = str(Path(__file__).parent.parent)
if _engine_path not in sys.path:
    sys.path.insert(0, _engine_path)

try:
    from blog_engine.article_generator import ArticleGenerator
except ImportError:
    # スタンドアロンフォールバック
    import json
    import logging
    import re
    import time
    from datetime import datetime

    from google import genai

    logger = logging.getLogger(__name__)

    class ArticleGenerator:
        """Gemini APIを使ったブログ記事生成エンジン（スタンドアロン版）"""

        def __init__(self, config, prompts=None):
            if not config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY が設定されていません。")

            self.config = config
            self.prompts = prompts
            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
            self.model_name = config.GEMINI_MODEL

            self.articles_dir = Path(config.BASE_DIR) / "output" / "articles"
            self.articles_dir.mkdir(parents=True, exist_ok=True)
            logger.info("ArticleGenerator (fallback) を初期化しました（モデル: %s）", config.GEMINI_MODEL)

        def generate_article(self, keyword: str, category: str, prompts=None) -> dict:
            """キーワードとカテゴリからSEO最適化されたブログ記事を生成する（最大5回リトライ）"""
            logger.info("記事生成を開始: キーワード='%s', カテゴリ='%s'", keyword, category)
            prompts = prompts or self.prompts

            if prompts and hasattr(prompts, "build_article_prompt"):
                prompt = prompts.build_article_prompt(keyword, category, self.config)
            else:
                prompt = self._build_default_prompt(keyword, category)

            max_retries = 5
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    from google.genai import types as genai_types
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=genai_types.GenerateContentConfig(
                            response_mime_type="application/json",
                        ),
                    )
                    article = self._parse_response(response.text)
                    break
                except (json.JSONDecodeError, ValueError) as e:
                    last_error = e
                    if attempt < max_retries:
                        logger.warning(
                            "JSONパース失敗（試行%d/%d）、リトライします: %s",
                            attempt, max_retries, e,
                        )
                        time.sleep(2 * attempt)
                    else:
                        logger.error("JSONパースに失敗（%d回リトライ後）: %s", max_retries, e)
                        raise ValueError(f"JSONパースに失敗: {e}") from e

            article["keyword"] = keyword
            article["category"] = category
            article["generated_at"] = datetime.now().isoformat()

            file_path = self._save_article(article)
            article["file_path"] = str(file_path)
            logger.info("記事生成完了: '%s' -> %s", article["title"], file_path)
            return article

        def _build_default_prompt(self, keyword, category):
            config = self.config
            return (
                f"あなたはClaude AIのエキスパートブロガーです。\n"
                f"キーワード「{keyword}」、カテゴリ「{category}」で\n"
                f"{config.MAX_ARTICLE_LENGTH}文字程度のSEO最適化された記事を\n"
                f"JSON形式で生成してください。\n\n"
                "```json\n"
                "{\n"
                '  "title": "タイトル",\n'
                '  "content": "本文（Markdown形式）",\n'
                '  "meta_description": "120文字以内",\n'
                '  "tags": ["タグ1", "タグ2", "タグ3", "タグ4", "タグ5"],\n'
                '  "slug": "url-friendly-slug",\n'
                '  "faq": [{"question": "Q", "answer": "A"}]\n'
                "}\n"
                "```"
            )

        @staticmethod
        def _fix_invalid_escapes(text):
            """JSON内の無効なエスケープシーケンスを修正"""
            import re as _re
            # JSON標準で許可されているエスケープ: \" \\ \/ \b \f \n \r \t \uXXXX
            return _re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)

        @staticmethod
        def _repair_json(text):
            """壊れたJSONを修復する（Geminiの長文生成で発生しがちな問題に対応）"""
            # 1. BOMや不可視文字を除去
            text = text.strip().lstrip('\ufeff')
            # 2. ```json ... ``` ブロックを除去
            json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if json_match:
                text = json_match.group(1)
            # 3. JSONオブジェクト部分を抽出
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                text = text[start:end]
            # 4. 文字列値内の生の改行をエスケープ
            result = []
            in_string = False
            escape_next = False
            for ch in text:
                if escape_next:
                    result.append(ch)
                    escape_next = False
                    continue
                if ch == '\\' and in_string:
                    result.append(ch)
                    escape_next = True
                    continue
                if ch == '"':
                    in_string = not in_string
                    result.append(ch)
                    continue
                if in_string:
                    if ch == '\n':
                        result.append('\\n')
                    elif ch == '\r':
                        result.append('\\r')
                    elif ch == '\t':
                        result.append('\\t')
                    elif ord(ch) < 0x20:
                        pass  # 制御文字を除去
                    else:
                        result.append(ch)
                else:
                    result.append(ch)
            repaired = ''.join(result)

            # 5. 切り詰められたJSONを閉じる
            open_braces = repaired.count('{') - repaired.count('}')
            open_brackets = repaired.count('[') - repaired.count(']')
            if open_braces > 0 or open_brackets > 0:
                if in_string:
                    repaired += '"'
                repaired += ']' * max(open_brackets, 0)
                repaired += '}' * max(open_braces, 0)

            return repaired

        @staticmethod
        def _extract_fields_fallback(text):
            """JSONパースが完全に失敗した場合、正規表現でフィールドを個別抽出する"""
            result = {}
            for field in ["title", "meta_description", "slug", "hero_emoji", "hero_gradient"]:
                m = re.search(rf'"{field}"\s*:\s*"((?:[^"\\]|\\.)*)"', text)
                if m:
                    result[field] = m.group(1).replace('\\"', '"')
            # tags
            m = re.search(r'"tags"\s*:\s*\[(.*?)\]', text, re.DOTALL)
            if m:
                result["tags"] = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
            # faq
            m = re.search(r'"faq"\s*:\s*\[(.+)\]', text, re.DOTALL)
            if m:
                questions = re.findall(r'"question"\s*:\s*"((?:[^"\\]|\\.)*)"', m.group(1))
                answers = re.findall(r'"answer"\s*:\s*"((?:[^"\\]|\\.)*)"', m.group(1))
                result["faq"] = [
                    {"question": q.replace('\\"', '"'), "answer": a.replace('\\"', '"')}
                    for q, a in zip(questions, answers)
                ]
            # content - 最も重要なフィールド
            m = re.search(r'"content"\s*:\s*"', text)
            if m:
                start_pos = m.end()
                pos = start_pos
                content_chars = []
                while pos < len(text):
                    ch = text[pos]
                    if ch == '\\' and pos + 1 < len(text):
                        content_chars.append(ch)
                        content_chars.append(text[pos + 1])
                        pos += 2
                        continue
                    if ch == '"':
                        break
                    content_chars.append(ch)
                    pos += 1
                result["content"] = ''.join(content_chars).replace('\\"', '"').replace('\\n', '\n')

            if result:
                logger.warning(
                    "フォールバック抽出で%d個のフィールドを回収: %s",
                    len(result), list(result.keys()),
                )
            return result

        def _parse_response(self, response_text):
            """APIレスポンスをパースする（複数の修復手法で堅牢に）"""
            json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)

            if json_match:
                raw = json_match.group(1).strip()
            else:
                cleaned = response_text.strip()
                start = cleaned.find("{")
                end = cleaned.rfind("}") + 1
                if start >= 0 and end > start:
                    raw = cleaned[start:end]
                else:
                    raw = cleaned

            # 1. そのままパース
            try:
                return self._validate_fields(json.loads(raw, strict=False))
            except json.JSONDecodeError:
                pass

            # 2. 不正エスケープ修復後にリトライ
            try:
                fixed = self._fix_invalid_escapes(raw)
                return self._validate_fields(json.loads(fixed, strict=False))
            except json.JSONDecodeError:
                pass

            # 3. JSON修復（制御文字・未閉じブラケット対応）
            try:
                repaired = self._repair_json(response_text)
                return self._validate_fields(json.loads(repaired, strict=False))
            except json.JSONDecodeError:
                pass

            # 4. json_repairライブラリ
            try:
                import json_repair
                return self._validate_fields(json_repair.loads(raw))
            except Exception:
                pass

            # 5. 正規表現でフィールド個別抽出（最後の手段）
            extracted = self._extract_fields_fallback(raw)
            if extracted and "title" in extracted and "content" in extracted:
                logger.warning("正規表現フォールバックで記事を回収しました")
                return self._validate_fields(extracted)

            raise ValueError(
                f"JSONパース失敗: 全てのパース手法が失敗しました。レスポンス先頭200文字: {response_text[:200]}"
            )

        def _validate_fields(self, data):
            """フィールドの検証と補完"""
            data.setdefault("hero_emoji", "\U0001f4dd")
            data.setdefault("hero_gradient", "135deg")

            if "title" not in data and "content" not in data:
                raise ValueError("titleとcontentの両方が不足しています")

            if "title" not in data:
                content = data.get("content", "")
                first_line = content.split("\n")[0].lstrip("# ").strip()
                data["title"] = first_line or "無題の記事"

            if "content" not in data:
                data["content"] = f"# {data['title']}\n\n記事の内容を生成できませんでした。"

            if "meta_description" not in data:
                content_text = re.sub(r'[#*\[\]()]', '', data["content"])
                data["meta_description"] = content_text[:120].strip()

            if "tags" not in data:
                data["tags"] = ["自動生成", "ブログ", "記事", "SEO", "最新"]

            if "slug" not in data:
                slug = re.sub(r'[^a-zA-Z0-9\s-]', '', data["title"].lower())
                slug = re.sub(r'\s+', '-', slug).strip('-') or "untitled-article"
                data["slug"] = slug

            if not isinstance(data["tags"], list):
                data["tags"] = [data["tags"]]

            data["slug"] = re.sub(
                r"[^a-z0-9-]", "", data["slug"].lower().replace(" ", "-")
            )
            return data

        def _save_article(self, article):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            slug = article.get("slug", "untitled")
            filename = f"{timestamp}_{slug}.json"
            file_path = self.articles_dir / filename

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(article, f, ensure_ascii=False, indent=2)
            logger.info("記事を保存しました: %s", file_path)
            return file_path
