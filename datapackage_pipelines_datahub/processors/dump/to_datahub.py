import logging
import os
import shutil
import subprocess
import tempfile

from datapackage_pipelines.lib.dump.dumper_base import FileDumper


class DataHubDumper(FileDumper):

    def initialize(self, params):
        super(DataHubDumper, self).initialize(params)
        self.file_counter = 0
        self.tmpfolder = tempfile.mkdtemp()
        self.findability = params.pop('findability', '--published')
        if not self.findability.startswith('--'):
            self.findability = '--' + self.findability
        if os.environ.get('DATAHUB_ENV') == 'testing':
            params['api'] = 'https://api-testing.datahub.io'
        self.options = ['--%s=%s' % (k, v) for k,v in params.items()]
        self.config_file = os.path.expanduser(params.pop(
            'config', '~/.config/datahub/config.json'
        ))
        subprocess.check_output(["data", "login"])

    def prepare_datapackage(self, datapackage, params):
        super(DataHubDumper, self).prepare_datapackage(datapackage, params)
        self.datapackage = datapackage
        return datapackage

    def write_file_to_output(self, filename, path):
        # Move tempfiles without names to tempfolder with names for upload
        path = os.path.join(self.tmpfolder, path)
        path_part = os.path.dirname(path)
        DataHubDumper.__makedirs(path_part)
        shutil.copy(filename, path)
        os.chmod(path, 0o666)

        # Check if number of files and number of resources + dp.json are equal
        self.file_counter += 1
        if self.file_counter == len(self.datapackage['resources']) + 1:
            os.environ['DATAHUB_JSON'] = self.config_file
            out = subprocess.check_output(
                ["data", "push", self.tmpfolder, self.findability] + self.options
            )
            logging.info(out)

        return path

    @staticmethod
    def __makedirs(path):
        if not os.path.exists(path):
            os.makedirs(path)


DataHubDumper()()
