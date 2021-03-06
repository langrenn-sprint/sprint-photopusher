"""Unit test cases for the generateSpecification module."""
import json
import os
import time

from click.testing import CliRunner
from deepdiff import DeepDiff
import pytest
from pytest_mock import MockFixture
from sprint_photopusher.image_service import ImageService
from sprint_photopusher.photopusher import (
    cli,
    FileSystemMonitor,
    find_url_photofile_type,
)


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def fake_loop_action() -> None:
    """Fake loop action."""
    raise KeyboardInterrupt


def test_FileSystemMonitor_with_url_arguments_succeds(runner: CliRunner) -> None:
    """Should not raise any Exceptions."""
    url = "http://example.com"
    try:
        monitor = FileSystemMonitor(url, os.getcwd())
        monitor.start(loop_action=fake_loop_action)
    except Exception:
        pytest.fail("Unexpected Exception")


def test_cli_with_url_arguments_and_directory_succeds(runner: CliRunner) -> None:
    """Should not raise any Exceptions."""
    directory = "directory_to_be_monitored"
    url = "http://example.com"

    with runner.isolated_filesystem():
        os.makedirs(directory)

        try:
            monitor = FileSystemMonitor(url, directory)
            monitor.start(loop_action=fake_loop_action)
        except Exception:
            pytest.fail("Unexpected Exception")


def test_analyze_video_with_intelligence_detailed() -> None:
    """Should return at least 1 element from vision."""
    result = {}
    try:
        result = ImageService.analyze_video_with_intelligence_detailed(
            ImageService(),
            "tests/files/input/J15test1.mp4",
        )
    except Exception:
        pytest.fail("Unexpected Exception")

    resultlist = result.items()
    if len(resultlist) < 1:
        pytest.fail("Empty resultset from Google vision API")


def test_analyze_photo_with_google_detailed() -> None:
    """Should return at least 5 elements from vision."""
    result = {}
    try:
        result = ImageService.analyze_photo_with_google_detailed(
            ImageService(),
            "tests/files/input/Finish_8168.JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")

    resultlist = result.items()
    if len(resultlist) == 0:
        pytest.fail("Empty resultset from Google vision API")


def test_analyze_photo_with_google_for_langrenn() -> None:
    """Should return at least 5 elements from vision."""
    result = {}
    try:
        result = ImageService.analyze_photo_with_google_for_langrenn(
            ImageService(),
            "tests/files/input/Finish_8168.JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")

    resultlist = result.items()
    if len(resultlist) == 0:
        pytest.fail("Empty resultset from Google vision API")


def test_analyze_photo_with_azure_vision() -> None:
    """Should return element(s) from vision."""
    result = {}
    try:
        result = ImageService.analyze_photo_with_azure_vision(
            ImageService(),
            "tests/files/output/Finish_8168.JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")

    resultlist = result.items()
    if len(resultlist) == 0:
        pytest.fail("Empty resultset from Azure computer vision API")


def test_analyze_photo() -> None:
    """Should return element(s) from vision."""
    result = {}
    try:
        result = ImageService.analyze_photo(
            ImageService(),
            "tests/files/output/Finish_8168.JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")

    resultlist = result.items()
    if len(resultlist) == 0:
        pytest.fail("Empty resultset from selected vision API")


def test_identify_tags() -> None:
    """Should return correct tags."""
    tags_dict = ImageService.identify_tags(
        ImageService(), "tests/files/input/Finish_8168.JPG"
    )

    with open("tests/files/Finish_8168_tags.json") as json_file:
        correct_json = json.load(json_file)

    ddiff = DeepDiff(tags_dict, correct_json, ignore_order=True)
    assert ddiff == {}


def test_capture_camera_image() -> None:
    """Should not raise any Exceptions."""
    try:
        gmt = time.gmtime()
        outfile = "tests/files/capture/capture_cam_0_"
        ImageService.capture_camera_image(
            ImageService(),
            0,
            outfile + "1" + str(gmt.tm_sec) + ".JPG",
        )
        ImageService.capture_camera_image(
            ImageService(),
            0,
            outfile + "2" + str(gmt.tm_sec) + ".JPG",
        )
        ImageService.capture_camera_image(
            ImageService(),
            0,
            outfile + "3" + str(gmt.tm_sec) + ".JPG",
        )
        ImageService.capture_camera_image(
            ImageService(),
            0,
            outfile + "4" + str(gmt.tm_sec) + ".JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")


def test_create_thumb() -> None:
    """Should not raise any Exceptions."""
    try:
        ImageService.create_thumb(
            ImageService(),
            "tests/files/output/Finish_8168.JPG",
            "tests/files/thumbs/thumb_Finish_8168.JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")


def test_create_thumb_azure_vision() -> None:
    """Should not raise any Exceptions."""
    try:
        ImageService.create_thumb_with_azure_vision(
            ImageService(),
            "tests/files/output/Finish_8168.JPG",
            "tests/files/thumbs/thumb__Azure_Finish_8168.JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")


def test_create_thumb_with_pillow() -> None:
    """Should not raise any Exceptions."""
    try:
        ImageService.create_thumb_with_pillow(
            ImageService(),
            "tests/files/input/Finish_8168.JPG",
            "tests/files/thumbs/thumb_Finish_8168.JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")


def test_watermark_image() -> None:
    """Should not raise any Exceptions."""
    try:
        ImageService.watermark_image(
            ImageService(),
            "tests/files/input/Finish_8168.JPG",
            "tests/files/output/Finish_8168.JPG",
        )
    except Exception:
        pytest.fail("Unexpected Exception")


def test_find_photo_type() -> None:
    """Should return correct location."""
    result = {}
    result["Url"], result["PhotoType"] = find_url_photofile_type(
        "http://localhost:8080", "tests/files/input/Finish_8168.JPG"
    )

    with open("tests/files/Finish_8168_type.json") as json_file:
        correct_json = json.load(json_file)

    ddiff = DeepDiff(result, correct_json, ignore_order=True)
    assert ddiff == {}


# --- Bad cases ---
def test_cli_no_arguments_fails(runner: CliRunner) -> None:
    """Should return exit_code 2."""
    runner = CliRunner()

    result = runner.invoke(cli)
    assert "Error: Missing argument 'URL'" in result.output
    assert result.exit_code == 2


def test_cli_option_directory_does_not_exist(
    mocker: MockFixture, runner: CliRunner
) -> None:
    """Should return exit_code 0."""
    runner = CliRunner()

    result = runner.invoke(cli, ["-d does_not_exist"])
    assert "does not exist" in result.output
    assert result.exit_code == 2
