import pytest
from django.conf import settings
from app.vendors.helpers import remove_directory
from django.core.files.uploadedfile import SimpleUploadedFile
from .bstr import (
    content_jpeg,
    content_jpg,
    content_png,
    content_doc,
    content_docx,
    content_ico,
    content_mp3,
    content_mp4,
    content_pdf,
    content_svg,
    content_txt,
    content_zip,
    content_csv,
    content_xlsx,
    content_xml,
    content_rar,
)


_username = "admin"
_password = "!Q2w3e4r5t"


def get_test_user_data():
    return _username, _password


@pytest.fixture
def create_admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        _username, "admin@mail.com", _password
    )


@pytest.fixture
def logged_in_client(create_admin_user, client):
    client.login(username=_username, password=_password)
    return client


@pytest.fixture(scope="session")
def image_file_jpeg():
    return SimpleUploadedFile("test.jpeg", content_jpeg, content_type="image/jpeg")


@pytest.fixture(scope="session")
def image_file_jpg():
    return SimpleUploadedFile("test.jpg", content_jpg, content_type="image/jpeg")


@pytest.fixture(scope="session")
def image_file_png(tmp_path_factory):
    # import io
    # res = io.BytesIO(content_png)
    # res.size = 3000
    # res.name = "test.png"
    # return res
    return SimpleUploadedFile("test.png", content_png, content_type="image/png")


@pytest.fixture(scope="session")
def image_file_pdf():
    return SimpleUploadedFile("test.pdf", content_pdf, content_type="application/pdf")


@pytest.fixture(scope="session")
def image_file_ico():
    return SimpleUploadedFile("test.ico", content_ico, content_type="image/vnd.microsoft.icon")


@pytest.fixture(scope="session")
def audio_file_mp3():
    return SimpleUploadedFile("test.mp3", content_mp3, content_type="audio/mpeg")


@pytest.fixture(scope="session")
def video_file_mp4():
    return SimpleUploadedFile("test.mp4", content_mp4, content_type="video/mp4")


@pytest.fixture(scope="session")
def image_file_svg():
    return SimpleUploadedFile("test.svg", content_svg, content_type="image/svg+xml")


@pytest.fixture(scope="session")
def doc_file_txt():
    return SimpleUploadedFile("test.txt", content_txt, content_type="text/plain")


@pytest.fixture(scope="session")
def doc_file_doc():
    return SimpleUploadedFile("test.doc", content_doc, content_type="application/msword")


@pytest.fixture(scope="session")
def doc_file_docx():
    _content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return SimpleUploadedFile("test.docx", content_docx, content_type=_content_type)


@pytest.fixture(autouse=True)
def set_test_media_root():
    """Set settings.MEDIA_ROOT before each tests"""
    settings.MEDIA_ROOT = settings.BASE_DIR / settings.TMP_URL


@pytest.fixture(scope="session")
def clean_tmp_dir():
    """
    Clean tmp directory after all tests.
    Add in any test
    (before yield run before test, after yield run after all tests scope is session)
    """
    yield
    remove_directory(settings.BASE_DIR / settings.TMP_URL)
    print("remove settings.TMP_URL directory")
