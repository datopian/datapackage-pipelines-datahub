import json
import os
import unittest
import datetime

try:
    from unittest.mock import Mock, patch, mock_open
except ImportError:
    from mock import Mock, patch, mock_open

from datapackage_pipelines.utilities.lib_test_helpers import (
    mock_processor_test
)

import datapackage_pipelines_datahub.processors

import logging
log = logging.getLogger(__name__)


class TestToDatahubProccessor(unittest.TestCase):

    def setUp(self):
        self.resources = [{
            'name': 'resource',
            "format": "csv",
            "path": "data/test.csv",
            "dpp:streaming": True,
            "schema": {
                "fields": [
                    {
                        "name": "Date",
                        "type": "date",
                    },
                    {
                        "name": "Name",
                        "type": "string",
                    }
                ]
            }
         }]
        self.datapackage = {
            'owner': 'me',
            'name': 'my-datapackage',
            'project': 'my-project',
            'resources': self.resources
        }

    @patch('subprocess.check_output')
    def test_pushes_fine(self, check_output_mock):
        check_output_mock.return_value = ("output", "Alles gut!")
        class DummyList(list):
            pass

        rows = [{'Date': datetime.datetime(2001, 2, 3), 'Name': 'Name'}]
        res =  DummyList(rows)
        res.spec = self.resources[0]
        res_iter = [res]

        processor_dir = os.path.dirname(datapackage_pipelines_datahub.processors.__file__)
        processor_path = os.path.join(processor_dir, 'dump', 'to_datahub.py')
        spew_args, _ = mock_processor_test(processor_path, ({}, self.datapackage, res_iter))


        _, spew_res_iter = spew_args[0], spew_args[1]

        process_rows = [list(res) for res in spew_res_iter]
        self.assertListEqual(process_rows, [rows])
