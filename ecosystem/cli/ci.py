"""CliCI class for controlling all CLI functions."""
import os
from typing import Optional

from ecosystem.daos import DAO
from ecosystem.utils import logger, parse_submission_issue
from ecosystem.utils.utils import set_actions_output


class CliCI:
    """CliCI class.
    Entrypoint for all CLI CI commands.

    Each public method of this class is CLI command
    and arguments for method are options/flags for this command.

    Ex: `python manager.py ci parser_issue --body="<SOME_MARKDOWN>"`
    """

    def __init__(self, root_path: Optional[str] = None):
        """CliCI class."""
        self.current_dir = root_path or os.path.abspath(os.getcwd())
        self.resources_dir = "{}/ecosystem/resources".format(self.current_dir)
        self.dao = DAO(path=self.resources_dir)

    @staticmethod
    def add_member_from_issue(body: str) -> None:
        """Parse an issue created from the issue template and add the member to the database

        Args:
            body: body of the created issue

        Returns:
            None (side effect is updating database)
        """

        parsed_result = parse_submission_issue(body, self.current_dir)
        self.dao.write(parsed_result)
