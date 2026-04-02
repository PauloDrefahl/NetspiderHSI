"""Cross-site linking engine for Bucket 4 (Alert).

Scans Bucket 3 (Priority) and Bucket 4 (Alert) posts across all source
tables to find posts that can be linked to the same person via shared
phone numbers, email addresses, or social media handles. Matched posts
are promoted to Bucket 4 and grouped into clusters.
"""

import logging
import re
import uuid

from .. import database

logger = logging.getLogger(__name__)

# Clean views and their source tables
CLEAN_VIEWS = {
    "raw_eros_posts": "clean_eros_view",
    "raw_escort_alligator_posts": "clean_escort_alligator_view",
    "raw_mega_personals_posts": "clean_mega_personals_view",
    "raw_rub_ratings_posts": "clean_rub_ratings_view",
    "raw_skipthegames_posts": "clean_skipthegames_view",
    "raw_yesbackpage_posts": "clean_yesbackpage_view",
}

# Regex for extracting phone numbers (sequences of 7+ digits)
PHONE_PATTERN = re.compile(r"\d{7,}")

# Regex for extracting email addresses
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Known social media handle patterns
SOCIAL_HANDLE_PATTERN = re.compile(r"@[\w.]{3,}")


class CrossSiteLinker:
    """Finds cross-site identity matches among Priority and Alert posts."""

    def find_links(self):
        """Run cross-site analysis on all Priority and Alert posts.

        Returns:
            dict with clusters_found and posts_linked counts.
        """
        conn = database.connect()
        try:
            # Load all Priority/Alert classified posts with their source data
            posts = self._load_risky_posts(conn)
            if not posts:
                logger.info("No Priority/Alert posts found for cross-site analysis")
                return {"clusters_found": 0, "posts_linked": 0}

            logger.info(
                "Analyzing %d Priority/Alert posts for cross-site links", len(posts)
            )

            # Build identifier maps: normalized_value -> list of (classification_id, source_table)
            phone_map = {}
            email_map = {}
            social_map = {}

            for post in posts:
                cid = post["classification_id"]
                source = post["source_table"]

                # Extract and normalize phone numbers
                contacts = str(post.get("contacts", ""))
                phones = PHONE_PATTERN.findall(contacts)
                for phone in phones:
                    normalized = phone.strip()
                    if len(normalized) >= 7:
                        phone_map.setdefault(normalized, []).append(
                            (cid, source)
                        )

                # Extract emails from contacts and description
                text = contacts + " " + str(post.get("description", ""))
                emails = EMAIL_PATTERN.findall(text.lower())
                for email in emails:
                    email_map.setdefault(email, []).append((cid, source))

                # Extract social media handles
                socials = post.get("social_media_accounts", [])
                if isinstance(socials, list):
                    for handle in socials:
                        normalized = str(handle).lower().strip().lstrip("@")
                        if len(normalized) >= 3 and normalized != "n/a":
                            social_map.setdefault(normalized, []).append(
                                (cid, source)
                            )

            # Find cross-site matches (value appears in 2+ different source tables)
            clusters_found = 0
            posts_linked = set()

            # Clear previous cross-site links before rebuilding
            self._clear_links(conn)

            for match_type, identifier_map in [
                ("phone", phone_map),
                ("email", email_map),
                ("social_media", social_map),
            ]:
                for value, entries in identifier_map.items():
                    sources = set(source for _, source in entries)
                    if len(sources) >= 2:
                        # Cross-site match found
                        cluster_id = str(uuid.uuid4())
                        clusters_found += 1
                        for cid, _ in entries:
                            posts_linked.add(cid)
                            self._insert_link(
                                conn, cluster_id, cid, match_type, value
                            )

            # Promote linked posts to Bucket 4
            if posts_linked:
                self._promote_to_bucket_4(conn, posts_linked)

            logger.info(
                "Cross-site analysis complete: %d clusters, %d posts linked",
                clusters_found,
                len(posts_linked),
            )
            return {
                "clusters_found": clusters_found,
                "posts_linked": len(posts_linked),
            }
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Internal methods
    # ------------------------------------------------------------------

    def _load_risky_posts(self, conn):
        """Load Priority/Alert posts joined with their source data from clean views."""
        posts = []
        with conn.cursor() as cur:
            for raw_table, clean_view in CLEAN_VIEWS.items():
                cur.execute(
                    f"""
                    SELECT pc.id as classification_id, pc.source_table,
                           cv.link, cv.city_or_region, cv.contacts,
                           cv.description, cv.social_media_accounts
                    FROM post_classifications pc
                    JOIN {clean_view} cv
                        ON pc.post_link = cv.link
                        AND pc.post_city = cv.city_or_region
                    WHERE pc.source_table = %s AND pc.bucket >= 3
                    """,  # noqa: S608
                    (raw_table,),
                )
                columns = [desc.name for desc in cur.description]
                for row in cur.fetchall():
                    posts.append(dict(zip(columns, row)))
        return posts

    def _clear_links(self, conn):
        """Remove all existing cross-site links to rebuild from scratch."""
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cross_site_links")

    def _insert_link(self, conn, cluster_id, classification_id, match_type, match_value):
        """Insert a cross-site link record."""
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cross_site_links
                    (cluster_id, classification_id, match_type, match_value)
                VALUES (%s::uuid, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (cluster_id, classification_id, match_type, match_value),
            )

    def _promote_to_bucket_4(self, conn, classification_ids):
        """Promote a set of classification IDs to Bucket 4."""
        with conn.cursor() as cur:
            for cid in classification_ids:
                cur.execute(
                    """
                    UPDATE post_classifications
                    SET bucket = 4,
                        original_bucket = CASE
                            WHEN original_bucket IS NULL THEN bucket
                            ELSE original_bucket
                        END
                    WHERE id = %s AND reviewed = false;
                    """,
                    (cid,),
                )
