import unittest
import os

os.environ["TESTING"] = "true"

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert (
            '<link href="https://fonts.googleapis.com/css2?family=Ubuntu+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">'
            in html
        )
        assert '<link rel="preconnect" href="https://fonts.gstatic.com">' in html

    def test_timeline(self):
        # GET testcases
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # POST testcases
        testPost = {
            "name": "john",
            "email": "john@example.com",
            "content": "Hello world",
        }
        response = self.client.post("/api/timeline_post", json=testPost)
        assert response.status_code == 201
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json = response.get_json()
        assert len(json["timeline_posts"]) > 0

        # Timeline page testcases
        html = response.get_data(as_text=True)
        # Timeline button in navbar
        assert '<li><a href="/timeline">Timeline</a></li>' in html
        assert "<script>" in html
