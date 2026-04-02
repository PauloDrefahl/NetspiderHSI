"""Rule-based post classification engine.

Reads scraped posts from the normalized clean views, scores them using
weighted keyword-category matching and contextual signals, then writes
classification results to the post_classifications table.
"""

import json
import logging
import os
import re
from datetime import datetime

from .. import database

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Bucket thresholds (adjustable based on review feedback over time)
# ---------------------------------------------------------------------------
BUCKET_MONITOR_MAX = 0       # 0     -> Bucket 1 (Monitor)
BUCKET_REVIEW_MAX = 19       # 1-19  -> Bucket 2 (Review)
                             # 20+   -> Bucket 3 (Priority)
                             # Linked -> Bucket 4 (Alert)

# Regex for extracting phone numbers from contact fields
PHONE_PATTERN = re.compile(r"\d{7,}")

# ---------------------------------------------------------------------------
# Category weights -- how much each keyword category contributes to score
# ---------------------------------------------------------------------------
CATEGORY_WEIGHTS = {
    "child trafficker darknet code words": 15,
    "child trafficking trends": 10,
    "adult trafficking": 5,
    "working keywords": 3,
}
DEFAULT_CATEGORY_WEIGHT = 5  # for user-defined investigation sets

# High-risk categories that trigger combo bonuses
HIGH_RISK_CATEGORIES = {
    "child trafficking trends",
    "child trafficker darknet code words",
}

# Bonus score values
PAYMENT_BONUS = 5
PAYMENT_HIGH_RISK_COMBO_BONUS = 10
SOCIAL_BONUS = 3
SOCIAL_HIGH_RISK_COMBO_BONUS = 5
MULTI_CATEGORY_BONUS = 8

# Clean view names mapped to their source raw table
CLEAN_VIEWS = {
    "raw_eros_posts": "clean_eros_view",
    "raw_escort_alligator_posts": "clean_escort_alligator_view",
    "raw_mega_personals_posts": "clean_mega_personals_view",
    "raw_rub_ratings_posts": "clean_rub_ratings_view",
    "raw_skipthegames_posts": "clean_skipthegames_view",
    "raw_yesbackpage_posts": "clean_yesbackpage_view",
}


def _find_keyword_sets_path():
    """Locate the keyword_sets.txt file relative to the project root."""
    # When run from the server directory, the project root is one level up.
    candidates = [
        os.path.join(os.getcwd(), "keyword_sets.txt"),
        os.path.join(os.getcwd(), "..", "keyword_sets.txt"),
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "keyword_sets.txt"),
    ]
    for path in candidates:
        resolved = os.path.realpath(path)
        if os.path.isfile(resolved):
            return resolved
    return None


class PostClassifier:
    """Scores and classifies scraped posts into risk buckets."""

    def __init__(self, keyword_sets_path=None):
        if keyword_sets_path is None:
            keyword_sets_path = _find_keyword_sets_path()
        if keyword_sets_path is None or not os.path.isfile(keyword_sets_path):
            raise FileNotFoundError(
                f"keyword_sets.txt not found (tried: {keyword_sets_path})"
            )
        with open(keyword_sets_path, "r", encoding="utf-8") as f:
            self.keyword_sets = json.load(f)
        logger.info(
            "Loaded %d keyword categories from %s",
            len(self.keyword_sets),
            keyword_sets_path,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify_post(self, post):
        """Classify a single post dict (from a clean view row).

        Args:
            post: dict with keys matching the clean view columns:
                  link, city_or_region, description, payment_methods,
                  social_media_accounts, contacts, poster, etc.

        Returns:
            dict with: bucket, risk_score, keyword_hits, payment_flag, social_flag
        """
        # Build the full text to scan from all relevant fields
        text_parts = [
            post.get("description", ""),
            post.get("poster", ""),
            post.get("contacts", ""),
            post.get("specified_location", ""),
        ]
        full_text = " ".join(str(p) for p in text_parts if p).lower()

        keyword_hits = self._scan_keywords(full_text)

        payment_methods = post.get("payment_methods", [])
        has_payment = bool(
            payment_methods
            and payment_methods != ["N/A"]
            and payment_methods != []
        )

        social_media = post.get("social_media_accounts", [])
        has_social = bool(
            social_media
            and social_media != ["N/A"]
            and social_media != []
        )

        risk_score = self._compute_score(keyword_hits, has_payment, has_social)
        bucket = self._assign_bucket(risk_score)

        return {
            "bucket": bucket,
            "risk_score": risk_score,
            "keyword_hits": keyword_hits,
            "payment_flag": has_payment,
            "social_flag": has_social,
        }

    def classify_all(self, source_table=None):
        """Classify all posts from clean views and write results to the database.

        Args:
            source_table: if given (e.g. 'raw_escort_alligator_posts'),
                          only classify posts from that table's clean view.
                          If None, classify posts from all tables.

        Returns:
            Number of posts classified.
        """
        conn = database.connect()
        try:
            # Log the classification run
            run_id = self._start_run(conn, source_table)

            tables = CLEAN_VIEWS
            if source_table and source_table in CLEAN_VIEWS:
                tables = {source_table: CLEAN_VIEWS[source_table]}

            total = 0
            for raw_table, clean_view in tables.items():
                count = self._classify_table(conn, raw_table, clean_view)
                total += count
                logger.info(
                    "Classified %d posts from %s", count, clean_view
                )

            self._finish_run(conn, run_id, total)
            logger.info("Classification complete: %d posts processed", total)
            return total
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Internal methods
    # ------------------------------------------------------------------

    def _scan_keywords(self, text):
        """Scan text for keywords from each category.

        Returns:
            dict mapping category name -> list of matched keywords
        """
        hits = {}
        for category, keywords in self.keyword_sets.items():
            matched = []
            for keyword in keywords:
                if keyword and keyword.lower() in text:
                    matched.append(keyword)
            if matched:
                hits[category] = matched
        return hits

    def _compute_score(self, keyword_hits, has_payment, has_social):
        """Compute the risk score from keyword hits and contextual signals.

        Returns:
            float clamped to 0-100
        """
        score = 0.0

        # Weighted keyword category scoring
        has_high_risk = False
        categories_hit = 0
        for category, matched_keywords in keyword_hits.items():
            weight = CATEGORY_WEIGHTS.get(category, DEFAULT_CATEGORY_WEIGHT)
            score += weight * len(matched_keywords)
            categories_hit += 1
            if category in HIGH_RISK_CATEGORIES:
                has_high_risk = True

        # Payment method bonus
        if has_payment:
            score += PAYMENT_BONUS
            if has_high_risk:
                score += PAYMENT_HIGH_RISK_COMBO_BONUS

        # Social media bonus
        if has_social:
            score += SOCIAL_BONUS
            if has_high_risk:
                score += SOCIAL_HIGH_RISK_COMBO_BONUS

        # Multi-category signal bonus
        if categories_hit >= 2:
            score += MULTI_CATEGORY_BONUS

        return min(100.0, max(0.0, score))

    def _assign_bucket(self, risk_score):
        """Determine the bucket from the risk score.

        Bucket 4 (Alert) is not assigned here — it is set by linkage
        detection in _classify_table after scoring.
        """
        if risk_score <= BUCKET_MONITOR_MAX:
            return 1
        elif risk_score <= BUCKET_REVIEW_MAX:
            return 2
        else:
            return 3

    def _classify_table(self, conn, raw_table, clean_view):
        """Classify all posts from a single clean view."""
        count = 0
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {clean_view}")  # noqa: S608
            columns = [desc.name for desc in cur.description]
            rows = cur.fetchall()

        if not rows:
            logger.warning("No posts found in %s — nothing to classify", clean_view)

        for row in rows:
            post = dict(zip(columns, row))
            try:
                result = self.classify_post(post)

                # Check for contact reuse across all posts
                reuse_info = self._get_reuse_info(conn, post)
                result["keyword_hits"]["_reuse"] = reuse_info

                # Promote to Bucket 4 (Alert) if contact appears in other posts
                if reuse_info.get("contact_reuse_count", 0) > 0:
                    result["keyword_hits"]["_reuse"]["original_bucket"] = result["bucket"]
                    result["bucket"] = 4

                self._upsert_classification(
                    conn,
                    source_table=raw_table,
                    post_link=post["link"],
                    post_city=post["city_or_region"],
                    result=result,
                )
                count += 1
            except Exception as e:
                logger.warning(
                    "Failed to classify post %s: %s",
                    post.get("link", "unknown"),
                    e,
                )

        return count

    def _get_reuse_info(self, conn, post):
        """Check if this post's contact info appears in other posts.

        Extracts phone numbers from the contacts field and queries all
        clean views for other posts sharing the same number.

        Returns:
            dict with contact_reuse_count and phones_matched.
        """
        contacts = str(post.get("contacts", ""))
        post_link = post.get("link", "")
        phones = PHONE_PATTERN.findall(contacts)

        contact_reuse = 0
        phones_matched = []

        for phone in phones:
            for _raw_table, cv in CLEAN_VIEWS.items():
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT COUNT(*) FROM {cv} "  # noqa: S608
                        "WHERE contacts LIKE %s AND link != %s",
                        (f"%{phone}%", post_link),
                    )
                    match_count = cur.fetchone()[0]
                    if match_count > 0:
                        contact_reuse += match_count
                        if phone not in phones_matched:
                            phones_matched.append(phone)

        return {
            "contact_reuse_count": contact_reuse,
            "phones_matched": phones_matched,
        }

    def _upsert_classification(self, conn, source_table, post_link, post_city, result):
        """Insert or update a classification record."""
        # Store original_bucket when post is promoted to Bucket 4 by reuse
        reuse = result["keyword_hits"].get("_reuse", {})
        original_bucket = reuse.get("original_bucket")

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO post_classifications
                    (source_table, post_link, post_city, bucket, risk_score,
                     keyword_hits, payment_flag, social_flag, classified_at,
                     original_bucket)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_table, post_link, post_city)
                DO UPDATE SET
                    bucket = EXCLUDED.bucket,
                    risk_score = EXCLUDED.risk_score,
                    keyword_hits = EXCLUDED.keyword_hits,
                    payment_flag = EXCLUDED.payment_flag,
                    social_flag = EXCLUDED.social_flag,
                    classified_at = EXCLUDED.classified_at,
                    original_bucket = EXCLUDED.original_bucket
                WHERE post_classifications.reviewed = false;
                """,
                (
                    source_table,
                    post_link,
                    post_city,
                    result["bucket"],
                    result["risk_score"],
                    json.dumps(result["keyword_hits"]),
                    result["payment_flag"],
                    result["social_flag"],
                    datetime.now(),
                    original_bucket,
                ),
            )

    def _start_run(self, conn, source_filter):
        """Create a classification_runs record and return its id."""
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO classification_runs (source_filter, status)
                VALUES (%s, 'running')
                RETURNING id;
                """,
                (source_filter,),
            )
            return cur.fetchone()[0]

    def _finish_run(self, conn, run_id, posts_processed):
        """Mark a classification run as finished."""
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE classification_runs
                SET finished_at = %s, posts_processed = %s, status = 'completed'
                WHERE id = %s;
                """,
                (datetime.now(), posts_processed, run_id),
            )
