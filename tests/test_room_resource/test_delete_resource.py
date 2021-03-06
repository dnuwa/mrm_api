import sys
import os

from tests.base import BaseTestCase, CommonTestCases
from fixtures.room_resource.delete_room_resource import (  # noqa: F401
  delete_resource, expected_query_after_delete, delete_non_existant_resource)  # noqa: E501


sys.path.append(os.getcwd())


class TestDeleteRoomResource(BaseTestCase):

    def test_deleteresource_mutation_when_not_admin(self):
        CommonTestCases.user_token_assert_in(
            self,
            delete_resource,
            "You are not authorized to perform this action"
        )

    def test_delete_resource_mutation_when_admin(self):
        CommonTestCases.admin_token_assert_in(
            self,
            delete_resource,
            "Markers"
        )

    def test_non_existant_deleteresource_mutation(self):
        CommonTestCases.admin_token_assert_in(
            self,
            delete_non_existant_resource,
            "Resource not found"
        )

    def test_delete_resource_in_room_that_is_not_in_admin_location(self):
        CommonTestCases.lagos_admin_token_assert_in(
            self,
            delete_resource,
            "You are not authorized to make changes in Kampala"
        )

    def test_database_connection_error(self):
        """
        test a user friendly message is returned to a user when database
        cannot be reached
        """
        BaseTestCase().tearDown()
        CommonTestCases.admin_token_assert_in(
            self,
            delete_resource,
            "The database cannot be reached"
            )
