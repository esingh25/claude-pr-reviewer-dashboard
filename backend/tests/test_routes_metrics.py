def _payload(**overrides):
    base = {
        "repo": "esingh25/claude-pr-reviewer",
        "pr_number": 1,
        "head_sha": "abc123",
        "provider": "github",
        "model": "claude-sonnet-4-6",
        "files_reviewed": 3,
        "comments_posted": 2,
        "severity_counts": {"critical": 0, "high": 1, "medium": 1, "low": 0},
        "duration_seconds": 4.2,
        "status": "success",
        "timestamp": "2026-06-21T12:00:00+00:00",
    }
    base.update(overrides)
    return base


def test_create_review_run_requires_api_key(client):
    response = client.post("/api/metrics", json=_payload())

    assert response.status_code == 401


def test_create_review_run_succeeds_with_valid_api_key(client):
    response = client.post("/api/metrics", json=_payload(), headers={"X-API-Key": "test-api-key"})

    assert response.status_code == 201
    body = response.json()
    assert body["repo"] == "esingh25/claude-pr-reviewer"
    assert body["severity_high"] == 1


def test_create_review_run_rejects_wrong_api_key(client):
    response = client.post("/api/metrics", json=_payload(), headers={"X-API-Key": "wrong-key"})

    assert response.status_code == 401


def test_list_review_runs_is_public_no_auth_needed(client):
    client.post("/api/metrics", json=_payload(), headers={"X-API-Key": "test-api-key"})

    response = client.get("/api/metrics")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_review_runs_filters_by_repo(client):
    client.post("/api/metrics", json=_payload(repo="a/b"), headers={"X-API-Key": "test-api-key"})
    client.post("/api/metrics", json=_payload(repo="c/d"), headers={"X-API-Key": "test-api-key"})

    response = client.get("/api/metrics", params={"repo": "a/b"})

    assert len(response.json()) == 1
    assert response.json()[0]["repo"] == "a/b"


def test_list_review_runs_filters_by_provider(client):
    client.post(
        "/api/metrics", json=_payload(provider="github"), headers={"X-API-Key": "test-api-key"}
    )
    client.post(
        "/api/metrics", json=_payload(provider="gitlab"), headers={"X-API-Key": "test-api-key"}
    )

    response = client.get("/api/metrics", params={"provider": "gitlab"})

    assert len(response.json()) == 1
    assert response.json()[0]["provider"] == "gitlab"


def test_summary_returns_aggregates(client):
    client.post(
        "/api/metrics",
        json=_payload(files_reviewed=3, comments_posted=2),
        headers={"X-API-Key": "test-api-key"},
    )
    client.post(
        "/api/metrics",
        json=_payload(files_reviewed=5, comments_posted=1, status="error"),
        headers={"X-API-Key": "test-api-key"},
    )

    response = client.get("/api/metrics/summary")

    body = response.json()
    assert body["total_runs"] == 2
    assert body["total_files_reviewed"] == 8
    assert body["total_comments_posted"] == 3
    assert body["success_rate"] == 0.5


def test_summary_with_no_runs_does_not_divide_by_zero(client):
    response = client.get("/api/metrics/summary")

    assert response.status_code == 200
    assert response.json()["success_rate"] == 0.0
    assert response.json()["total_runs"] == 0


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
