from fstat import app

import unittest
import json
from datetime import datetime, timedelta


class TestRestfulApis(unittest.TestCase):
    """ Integration tests for the rest apis """

    def setUp(self):
        self.tester = app.test_client()

    def test_get_failure_route(self):
        """ Tests /api/failures route """
        endpoint = '/api/failures'
        # HACK: spliting string by T to get only date
        query_string_params = {
            'start_date': str(datetime.today() - timedelta(days=7)).split(" "),
            'end_date': str(datetime.today()).split(" "),
            'branch': 'master'
        }

        response = self.tester.get(endpoint, query_string=query_string_params)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['response']) > 0
        expected_keys = ['id', 'type', 'signature', 'bugs', 'failure_count']
        for key in expected_keys:
            assert key in data['response'][0]

    def test_get_failure_instances_route(self):
        """ Tests get failure instances api """
        endpoint = '/api/failure/{}'.format(11)
        query_string_params = {
            'start_date': str(datetime.today() - timedelta(days=7)).split(" "),
            'end_date': str(datetime.today()).split(" "),
            'branch': 'master'
        }

        response = self.tester.get(endpoint, query_string=query_string_params)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data['response'], list)
        expected_keys = ['node', 'url', 'timestamp', 'failure_id', 'branch', 'patchset', 'job_name']
        for key in expected_keys:
            assert key in data['response'][0]
