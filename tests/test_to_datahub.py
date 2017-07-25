import json
import os
import unittest
import datetime

from datapackage_pipelines.utilities.lib_test_helpers import (
    mock_processor_test
)

import datapackage_pipelines_datahub.processors

import logging
log = logging.getLogger(__name__)


class TestToS3Proccessor(unittest.TestCase):

    def test_working(self):
        assert 1 == 1
