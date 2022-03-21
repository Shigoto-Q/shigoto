import logging
import pathlib
import subprocess

from django.conf import settings

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[GITHUB-CLIENT]"


class GithubClient:
    @classmethod
    def clone_repository(cls, url: str, user_id: int):
        path = settings.TEMP_REPOSITORY_DIR.format(user_id=user_id)
        logger.info(f"{_LOG_PREFIX} Cloning repository {url} into {path}.")

        full_dir = pathlib.Path(path)
        try:
            full_dir.mkdir(parents=True)
        except FileExistsError:
            logger.info(f"{_LOG_PREFIX} File already exists, proceding.")
        subprocess.Popen(["/usr/bin/git", "clone", url, path])
