import sys

import pytest


# to not automatically run integration tests unless specified
def pytest_runtest_setup(item):
    envmarker = item.get_closest_marker("integration")

    if envmarker and "integration" not in sys.argv and "all" not in sys.argv:
        pytest.skip("Skipping as the test has a marker")


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker("all")
