import logging
import os
import importlib
import re
from pathlib import Path

# noinspection PyPackageRequirements
from telegram.ext import Updater, ConversationHandler

logger = logging.getLogger(__name__)


class TorrentsBot(Updater):
    @staticmethod
    def _load_manifest(manifest_path):
        if not manifest_path:
            return

        try:
            with open(manifest_path, 'r') as f:
                manifest_str = f.read()
        except FileNotFoundError:
            logger.debug('manifest <%s> not found', os.path.normpath(manifest_path))
            return

        if not manifest_str.strip():
            return

        manifest_str = manifest_str.replace('\r\n', '\n')
        manifest_lines = manifest_str.split('\n')

        modules_list = list()
        for line in manifest_lines:
            line = re.sub(r'(?:\s+)?#.*(?:\n|$)', '', line)  # remove comments from the line
            if line.strip():  # ignore empty lines
                items = line.split()  # split on spaces. We will consider only the first word
                modules_list.append(items[0])  # tuple: (module_to_import, [callbacks_list])

        return modules_list

    @classmethod
    def import_handlers(cls, directory):
        """A text file named "manifest" can be placed in the dir we are importing the handlers from.
        It can contain the list of the files to import, the bot will import only these
        modules as ordered in the manifest file.
        Inline comments are allowed, they must start by #"""

        paths_to_import = list()

        manifest_modules = cls._load_manifest(os.path.join(directory, 'manifest'))
        if manifest_modules:
            # build the base import path of the plugins/jobs directory
            target_dir_path = os.path.splitext(directory)[0]
            target_dir_import_path_list = list()
            while target_dir_path:
                target_dir_path, tail = os.path.split(target_dir_path)
                target_dir_import_path_list.insert(0, tail)
            base_import_path = '.'.join(target_dir_import_path_list)

            for module in manifest_modules:
                import_path = base_import_path + module

                logger.debug('importing module: %s', import_path)

                paths_to_import.append(import_path)
        else:
            for path in sorted(Path(directory).rglob('*.py')):
                file_path = os.path.splitext(str(path))[0]

                import_path = []

                while file_path:
                    file_path, tail = os.path.split(file_path)
                    import_path.insert(0, tail)

                import_path = '.'.join(import_path)

                paths_to_import.append(import_path)

        for import_path in paths_to_import:
            logger.debug('importing module: %s', import_path)
            importlib.import_module(import_path)

    def run(self, jobs_enabled=True, *args, **kwargs):
        logger.warning('running as @%s', self.bot.username)
        self.start_polling(*args, **kwargs)
        if not jobs_enabled:
            self.job_queue.stop()
        self.idle()

    def add_handler(self, *args, **kwargs):
        if isinstance(args[0], ConversationHandler):
            # ConverstaionHandler.name or the name of the first entry_point function
            logger.info('adding conversation handler: %s', args[0].name or args[0].entry_points[0].callback.__name__)
        else:
            logger.info('adding handler: %s', args[0].callback.__name__)

        self.dispatcher.add_handler(*args, **kwargs)

    def register_job(self, *args, **kwargs):
        logger.info('registering job: %s', args[0].__name__)

        self.job_queue.run_repeating(*args, **kwargs)
