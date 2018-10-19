import logging
import os
import shutil
import subprocess
import tempfile

from datapackage_pipelines.lib.dump.dumper_base import FileDumper


class DataHubDumper(FileDumper):

    def initialize(self, params):
        super(DataHubDumper, self).initialize(params)
        self.tmpfolder = tempfile.mkdtemp()
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

        # Get the total number of file to push including dp.json
        files_in_paths = [x[2] for x in os.walk(self.tmpfolder) if len(x[2])]
        all_files = []
        for file in files_in_paths:
            all_files += file

        # Check if number of files and number of resources + dp.json are equal
        # and push all together
        if len(all_files) == len(self.datapackage['resources']) + 1:
            out = subprocess.check_output(["data", "push", self.tmpfolder])
            logging.info(out)
        return path

    @staticmethod
    def __makedirs(path):
        if not os.path.exists(path):
            os.makedirs(path)


DataHubDumper()()
