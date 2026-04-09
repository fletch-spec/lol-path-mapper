print("[SYSTEM]: Loading...")

from . import cache
from . import utils
from . import cli
from . import render
from . import api

import os

class System:
    def __init__(self, args):

        self.api = api
        self.utils = utils
        self.config = self.utils.get_config()
        self.cli = cli
        self.render = render
        try: 
            self.initialize(args)
        except Exception as e:
            self.cli.error(f"{e}")

    def initialize(self, args):
        self.cli.system("Initializing...")

        if args.restore:
            self.cli.system("--restore: wiping cache and restoring to default")

        self._cache = cache.CacheController(self.cli.cache, self.config, reset=args.restore)
        
        from ._test.system_tests import run_test
        if run_test(self):
            raise Exception("Failed system test.")

        return self
    
    def start(self):
        pass


print("[SYSTEM]: Modules Loaded.")