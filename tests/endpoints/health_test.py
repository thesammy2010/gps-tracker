from unittest import TestCase

import pytest

from gps_tracker.main import APP


class TestHealth(TestCase):
    def setUp(self) -> None:
        self.client = APP.test_client()

    def test_health1(self) -> None:
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.get_data(), b"alive")
        self.assertEqual(response.status_code, 200)

    @pytest.mark.integration
    def test_health2(self) -> None:
        response = self.client.get("/api/v1/health?db=true")
        self.assertEqual(response.get_json(), {"db": True})
        self.assertEqual(response.status_code, 200)
