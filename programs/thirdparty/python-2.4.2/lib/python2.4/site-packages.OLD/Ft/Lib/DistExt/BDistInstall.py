import Install

class BDistInstall(Install.Install):

    command_name = 'bdist_install'

    description = "'install' used by the bdist commands (internal use only)"

    user_options = Install.Install.user_options + [
        ('root=', None,
         "install everything relative to this alternate root directory"),
        ]

    def __init__(self, *args, **kwords):
        Install.Install.__init__(self, *args, **kwords)
        # Replace standard install with ourself
        self.distribution.command_obj['install'] = self
        return

    def initialize_options(self):
        Install.Install.initialize_options(self)
        # Disable PYTHONPATH warning (this is distribution build after all!)
        self.warn_dir = 0
        # Force documentation creation
        self.with_docs = 1
        return
