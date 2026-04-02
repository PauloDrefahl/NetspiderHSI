'use strict';

document.addEventListener('DOMContentLoaded', function () {
    var currentPage = 1;
    var perPage = 50;
    var currentDetailId = null;

    // Filter elements
    var bucketFilter = document.getElementById('review-bucket-filter');
    var sourceFilter = document.getElementById('review-source-filter');
    var reviewedFilter = document.getElementById('review-status-filter');
    var refreshBtn = document.getElementById('review-refresh-btn');
    var classifyBtn = document.getElementById('review-classify-btn');
    var crossSiteBtn = document.getElementById('review-crosssite-btn');

    // Pagination
    var prevPageBtn = document.getElementById('review-prev-page');
    var nextPageBtn = document.getElementById('review-next-page');
    var pageInfo = document.getElementById('review-page-info');

    // Detail panel
    var detailPanel = document.getElementById('review-detail-panel');
    var closeDetailBtn = document.getElementById('close-detail-btn');

    // Bind events
    if (refreshBtn) refreshBtn.addEventListener('click', function () { loadReviewQueue(); });
    if (classifyBtn) classifyBtn.addEventListener('click', runClassification);
    if (crossSiteBtn) crossSiteBtn.addEventListener('click', runCrossSiteAnalysis);
    if (closeDetailBtn) closeDetailBtn.addEventListener('click', closeDetail);

    if (bucketFilter) bucketFilter.addEventListener('change', function () { currentPage = 1; loadReviewQueue(); });
    if (sourceFilter) sourceFilter.addEventListener('change', function () { currentPage = 1; loadReviewQueue(); });
    if (reviewedFilter) reviewedFilter.addEventListener('change', function () { currentPage = 1; loadReviewQueue(); });

    if (prevPageBtn) prevPageBtn.addEventListener('click', function () { if (currentPage > 1) { currentPage--; loadReviewQueue(); } });
    if (nextPageBtn) nextPageBtn.addEventListener('click', function () { currentPage++; loadReviewQueue(); });

    // Save review button (delegated since it's inside the detail panel)
    var saveReviewBtn = document.getElementById('save-review-btn');
    if (saveReviewBtn) saveReviewBtn.addEventListener('click', saveReview);

    // ---------------------------------------------------------------
    // Socket listeners
    // ---------------------------------------------------------------
    socket.on('classification_stats', function (response) {
        if (response.error) {
            console.error('Stats error:', response.error);
            return;
        }
        updateStats(response.data);
    });

    socket.on('review_queue', function (response) {
        if (response.error) {
            console.error('Review queue error:', response.error);
            return;
        }
        renderReviewTable(response.data, response.total, response.page, response.per_page);
    });

    socket.on('classified_post_detail', function (response) {
        if (response.error) {
            console.error('Post detail error:', response.error);
            return;
        }
        renderDetail(response);
    });

    socket.on('reclassify_result', function (response) {
        if (response.error) {
            console.error('Reclassify error:', response.error);
            return;
        }
        closeDetail();
        loadStats();
        loadReviewQueue();
    });

    socket.on('classification_update', function (response) {
        if (response.status === 'completed') {
            loadStats();
            loadReviewQueue();
        } else if (response.status === 'error') {
            console.error('Classification error:', response.error);
            var tbody = document.querySelector('#review-table tbody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="10">Classification failed: ' +
                    escapeHtml(response.error) + '. Try clicking "Run Classification" manually.</td></tr>';
            }
        }
    });

    socket.on('cross_site_result', function (response) {
        if (response.status === 'completed') {
            loadStats();
            loadReviewQueue();
        }
    });

    // ---------------------------------------------------------------
    // Load functions
    // ---------------------------------------------------------------
    function loadStats() {
        socket.emit('get_classification_stats');
    }

    function loadReviewQueue() {
        var filters = {
            page: currentPage,
            per_page: perPage
        };

        var bucket = bucketFilter ? bucketFilter.value : '';
        var source = sourceFilter ? sourceFilter.value : '';
        var reviewed = reviewedFilter ? reviewedFilter.value : '';

        if (bucket !== '') filters.bucket = parseInt(bucket, 10);
        if (source !== '') filters.source_table = source;
        if (reviewed !== '') filters.reviewed = reviewed === 'true';

        socket.emit('get_review_queue', filters);
        loadStats();
    }

    function loadPostDetail(classificationId) {
        currentDetailId = classificationId;
        socket.emit('get_classified_post', { classification_id: classificationId });
    }

    // ---------------------------------------------------------------
    // Render functions
    // ---------------------------------------------------------------
    function updateStats(data) {
        var b1 = document.getElementById('stat-bucket-1');
        var b2 = document.getElementById('stat-bucket-2');
        var b3 = document.getElementById('stat-bucket-3');
        var b4 = document.getElementById('stat-bucket-4');
        var unrev = document.getElementById('stat-unreviewed');

        if (b1) b1.textContent = data.bucket_1_count || 0;
        if (b2) b2.textContent = data.bucket_2_count || 0;
        if (b3) b3.textContent = data.bucket_3_count || 0;
        if (b4) b4.textContent = data.bucket_4_count || 0;
        if (unrev) unrev.textContent = data.unreviewed_count || 0;
    }

    function renderReviewTable(data, total, page, itemsPerPage) {
        var tbody = document.querySelector('#review-table tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10">No classified posts found. Run classification first.</td></tr>';
            updatePagination(0, 1, itemsPerPage);
            return;
        }

        data.forEach(function (row) {
            var tr = document.createElement('tr');

            // Risk Score
            var scoreClass = row.risk_score < 1 ? 'score-low' : (row.risk_score < 20 ? 'score-medium' : 'score-high');
            tr.innerHTML =
                '<td class="' + scoreClass + '">' + parseFloat(row.risk_score).toFixed(1) + '</td>' +
                '<td><span class="bucket-label bucket-' + row.bucket + '">' + getBucketName(row.bucket) + '</span></td>' +
                '<td>' + formatSourceName(row.source_table) + '</td>' +
                '<td>' + escapeHtml(row.post_city) + '</td>' +
                '<td class="desc-cell" title="' + escapeHtml(row.post_link) + '">' + escapeHtml(row.post_link) + '</td>' +
                '<td>' + formatKeywordHits(row.keyword_hits) + '</td>' +
                '<td>' + (row.payment_flag ? 'Yes' : 'No') + '</td>' +
                '<td>' + (row.social_flag ? 'Yes' : 'No') + '</td>' +
                '<td class="' + (row.reviewed ? 'review-status-yes' : 'review-status-no') + '">' +
                    (row.reviewed ? 'Reviewed' : 'Pending') + '</td>' +
                '<td><button class="btn-review" data-id="' + row.id + '">Review</button></td>';

            tbody.appendChild(tr);
        });

        // Bind review buttons
        tbody.querySelectorAll('.btn-review').forEach(function (btn) {
            btn.addEventListener('click', function () {
                loadPostDetail(parseInt(this.getAttribute('data-id'), 10));
            });
        });

        updatePagination(total, page, itemsPerPage);
    }

    function updatePagination(total, page, itemsPerPage) {
        var totalPages = Math.max(1, Math.ceil(total / itemsPerPage));
        if (pageInfo) pageInfo.textContent = 'Page ' + page + ' of ' + totalPages + ' (' + total + ' total)';
        if (prevPageBtn) prevPageBtn.disabled = page <= 1;
        if (nextPageBtn) nextPageBtn.disabled = page >= totalPages;
    }

    function renderDetail(response) {
        if (!detailPanel) return;
        detailPanel.classList.add('active');

        var cls = response.classification;
        var post = response.post_data;
        var crossLinks = response.cross_links || [];
        var clusterPosts = response.cluster_posts || [];

        // Score breakdown
        var scoreSection = document.getElementById('detail-score');
        if (scoreSection) {
            var scoreClass = cls.risk_score < 1 ? 'score-low' : (cls.risk_score < 20 ? 'score-medium' : 'score-high');
            scoreSection.innerHTML =
                '<p>Risk Score: <span class="' + scoreClass + '">' + parseFloat(cls.risk_score).toFixed(1) + '</span></p>' +
                '<p>Bucket: <span class="bucket-label bucket-' + cls.bucket + '">' + getBucketName(cls.bucket) + '</span></p>' +
                '<p>Payment Methods: ' + (cls.payment_flag ? 'Detected' : 'None') + '</p>' +
                '<p>Social Media: ' + (cls.social_flag ? 'Detected' : 'None') + '</p>' +
                '<p>Classified: ' + (cls.classified_at || 'N/A') + '</p>' +
                (cls.original_bucket ? '<p>Original Bucket: ' + getBucketName(cls.original_bucket) + '</p>' : '');
        }

        // Keyword hits
        var keywordsSection = document.getElementById('detail-keywords');
        if (keywordsSection) {
            var hits = cls.keyword_hits || {};
            var html = '';
            for (var cat in hits) {
                if (hits.hasOwnProperty(cat) && cat !== '_reuse') {
                    html += '<div class="keyword-hit-category">';
                    html += '<span class="cat-name">' + escapeHtml(cat) + ':</span>';
                    html += '<div class="cat-keywords">';
                    hits[cat].forEach(function (kw) {
                        html += '<span class="keyword-tag">' + escapeHtml(kw) + '</span>';
                    });
                    html += '</div></div>';
                }
            }

            // Display contact reuse info if present
            var reuse = hits._reuse;
            if (reuse && reuse.contact_reuse_count > 0) {
                html += '<div class="keyword-hit-category">';
                html += '<span class="cat-name">Contact Reuse:</span>';
                html += '<div class="cat-keywords">';
                html += '<span class="keyword-tag" style="background-color:#8e44ad;">' +
                    reuse.contact_reuse_count + ' other post(s) share a phone number</span>';
                if (reuse.phones_matched && reuse.phones_matched.length > 0) {
                    reuse.phones_matched.forEach(function (phone) {
                        html += '<span class="keyword-tag" style="background-color:#2c3e50;">' +
                            escapeHtml(phone) + '</span>';
                    });
                }
                html += '</div></div>';
            }

            keywordsSection.innerHTML = html || '<p>No keyword hits</p>';
        }

        // Post content
        var contentSection = document.getElementById('detail-content');
        if (contentSection && post) {
            contentSection.innerHTML =
                '<p><strong>Source:</strong> ' + formatSourceName(cls.source_table) + '</p>' +
                '<p><strong>City:</strong> ' + escapeHtml(post.city_or_region || 'N/A') + '</p>' +
                '<p><strong>Link:</strong> ' + escapeHtml(post.link || 'N/A') + '</p>' +
                '<p><strong>Contacts:</strong> ' + escapeHtml(post.contacts || 'N/A') + '</p>' +
                '<p><strong>Poster:</strong> ' + escapeHtml(post.poster || 'N/A') + '</p>' +
                '<pre>' + escapeHtml(post.description || 'No description available') + '</pre>';
        }

        // Cross-site clusters
        var clusterSection = document.getElementById('detail-clusters');
        if (clusterSection) {
            if (crossLinks.length > 0) {
                var clusterHtml = '<h4>Cross-Site Links</h4>';
                crossLinks.forEach(function (link) {
                    clusterHtml += '<p>Match: <strong>' + escapeHtml(link.match_type) +
                        '</strong> - ' + escapeHtml(link.match_value) + '</p>';
                });
                if (clusterPosts.length > 0) {
                    clusterHtml += '<h4>Related Posts</h4>';
                    clusterPosts.forEach(function (cp) {
                        clusterHtml += '<div class="cluster-post">' +
                            '<span class="cluster-source">' + formatSourceName(cp.source_table) + '</span>' +
                            '<span>' + escapeHtml(cp.post_city || '') + '</span>' +
                            '<span class="bucket-label bucket-' + cp.bucket + '">' + getBucketName(cp.bucket) + '</span>' +
                            '<span>Score: ' + parseFloat(cp.risk_score).toFixed(1) + '</span>' +
                            '</div>';
                    });
                }
                clusterSection.innerHTML = clusterHtml;
                clusterSection.style.display = 'block';
            } else {
                clusterSection.innerHTML = '';
                clusterSection.style.display = 'none';
            }
        }

        // Set reclassify dropdown to current bucket
        var reclassifySelect = document.getElementById('reclassify-bucket');
        if (reclassifySelect) reclassifySelect.value = cls.bucket;

        // Show review notes if already reviewed
        var notesArea = document.getElementById('reclassify-notes');
        if (notesArea) notesArea.value = cls.review_notes || '';

        detailPanel.scrollIntoView({ behavior: 'smooth' });
    }

    function closeDetail() {
        if (detailPanel) detailPanel.classList.remove('active');
        currentDetailId = null;
    }

    // ---------------------------------------------------------------
    // Actions
    // ---------------------------------------------------------------
    function runClassification() {
        socket.emit('run_classification', {});
    }

    function runCrossSiteAnalysis() {
        socket.emit('run_cross_site_analysis');
    }

    function saveReview() {
        if (!currentDetailId) return;

        var newBucket = document.getElementById('reclassify-bucket');
        var notes = document.getElementById('reclassify-notes');

        socket.emit('reclassify_post', {
            classification_id: currentDetailId,
            new_bucket: parseInt(newBucket.value, 10),
            review_notes: notes.value,
            reviewed_by: 'agent'
        });
    }

    // ---------------------------------------------------------------
    // Helpers
    // ---------------------------------------------------------------
    function getBucketName(bucket) {
        var names = { 1: 'Monitor', 2: 'Review', 3: 'Priority', 4: 'Alert' };
        return names[bucket] || 'Unknown';
    }

    function formatSourceName(sourceTable) {
        var names = {
            'raw_eros_posts': 'Eros',
            'raw_escort_alligator_posts': 'Escort Alligator',
            'raw_mega_personals_posts': 'Mega Personals',
            'raw_rub_ratings_posts': 'Rub Ratings',
            'raw_skipthegames_posts': 'Skip The Games',
            'raw_yesbackpage_posts': 'Yes Back Page'
        };
        return names[sourceTable] || sourceTable;
    }

    function formatKeywordHits(hits) {
        if (!hits || typeof hits !== 'object') return 'None';
        var count = 0;
        for (var cat in hits) {
            if (hits.hasOwnProperty(cat) && cat !== '_reuse') count += hits[cat].length;
        }
        return count > 0 ? count + ' hits' : 'None';
    }

    function escapeHtml(text) {
        if (!text) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(String(text)));
        return div.innerHTML;
    }

    // ---------------------------------------------------------------
    // Initial load
    // ---------------------------------------------------------------
    loadStats();
    loadReviewQueue();
});
