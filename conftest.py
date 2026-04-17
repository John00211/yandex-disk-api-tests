import pytest
import os


def pytest_addoption(parser):
    parser.addoption(
        "--token",
        action="store",
        default=os.getenv("YANDEX_DISK_TOKEN"),
        help="Yandex.Disk OAuth token",
    )


@pytest.fixture(scope="session")
def token(request):
    tok = request.config.getoption("--token")
    if not tok:
        pytest.exit(
            "OAuth token is required. Use --token or env YANDEX_DISK_TOKEN",
            returncode=1,
        )
    return tok


@pytest.fixture(scope="session")
def auth_headers(token):
    return {"Authorization": f"OAuth {token}"}