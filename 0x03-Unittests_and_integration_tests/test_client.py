#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock, PropertyMock, Mock
import client
from parameterized import parameterized, parameterized_class
from typing import Dict, Mapping, Union
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """Test the TestGithubClient class"""

    @parameterized.expand([
        ("google", {"message": "google"}),
        ("abc", {"message": "abc"})
    ])
    @patch('client.get_json')
    def test_org(
        self,
        test_name: str,
        response: Dict,
        mock_get_json: MagicMock,
    ):
        """Test the test_org function of the class"""
        mock_get_json.return_value = MagicMock(return_value=response)
        client_obj = GithubOrgClient(test_name)
        self.assertEqual(client_obj.org(), response)
        url = client_obj.ORG_URL.format(org=test_name)
        mock_get_json.assert_called_once_with(url)

    def test_public_repos_url(self):
        """Test the property function of the class"""
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            org_return_value = {
                'repos_url': "https://api.github.com/orgs/response"}
            mock_org.return_value = org_return_value
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                             "https://api.github.com/orgs/response")

    @patch("client.get_json")
    def test_public_repos(self, mock_json):
        """Test the public_repos function of the class"""
        json_return_value = {
            "repos_url": "https://github.com/response",
            "payload": [
                {
                    "name": "abraham"
                },
                {
                    "name": "osazee"
                }
            ]
        }
        mock_json.return_value = json_return_value['payload']

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value=json_return_value['repos_url']
        ) as mock_obj:
            test_obj = GithubOrgClient("google")
            self.assertEqual(test_obj.public_repos(), [
                "abraham",
                "osazee"
            ])
            mock_obj.assert_called_once()
        mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Mapping, license_key: str, expected: bool):
        """"test the has_license function of the class"""
        self.assertEqual(GithubOrgClient.has_license(
            repo, license_key), expected)
        with self.assertRaises(AssertionError):
            GithubOrgClient.has_license(repo, None)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """peerform integrated test for the GithubOrgClient class"""

    @classmethod
    def setUpClass(cls) -> Union[Mock, HTTPError]:
        """mock the utils.requests.get object before running all tests"""

        payload_dict = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload
        }

        def get_payload(url):
            """
            get the value of the url from the payload_ dict
            variable
            """
            if url in payload_dict:
                return Mock(**{'json.return_value': payload_dict[url]})
            return HTTPError

        cls.get_patcher = patch('utils.requests.get', side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self):
        """Test the public repos method of the class"""
        self.assertEqual(GithubOrgClient(
            "google").public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the publick repos method with license argument
        license="apache-2.0"
        """
        self.assertEqual(GithubOrgClient("google").public_repos(
            "apache-2.0"), self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """Remove the mock object after running all tests"""
        cls.get_patcher.stop()
