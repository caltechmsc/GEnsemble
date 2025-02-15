import os
from distutils.command import install_lib

class InstallLib(install_lib.install_lib):

    command_name = 'install_lib'

    user_options = [
        ('force', 'f', "force installation (overwrite existing files)"),
        ('compile', 'c', "compile .py to .pyc [default]"),
        ('no-compile', None, "don't compile .py files"),
        ('optimize=', 'O',
         "also compile with optimization: -O1 for \"python -O\", "
         "-O2 for \"python -OO\", and -O0 to disable [default: -O0]"),
        ('skip-build', None, "skip the build steps"),
        ]

    boolean_options = ['force', 'compile', 'skip-build']
    negative_opt = {'no-compile' : 'compile'}

    def install(self):
        # Overridden to install only the files from the "build" commands
        # instead of copying the entire build tree.  This change is mostly
        # for developers benefit.
        outfiles = []
        if os.path.isdir(self.build_dir):
            self.mkpath(self.install_dir)
            # Unfortunately, each command could have a different
            # build directory.
            pure = self._copy_outputs(self.distribution.has_pure_modules(),
                                      'build_py', 'build_lib')
            outfiles.extend(pure)

            ext = self._copy_outputs(self.distribution.has_ext_modules(),
                                     'build_ext', 'build_lib')
            outfiles.extend(ext)
        else:
            self.warn("'%s' does not exist -- no Python modules to install" %
                      self.build_dir)
        return outfiles

    def _copy_outputs (self, has_any, build_cmd, dir_option):
        if not has_any:
            return []

        build_cmd = self.get_finalized_command(build_cmd)
        build_files = build_cmd.get_outputs()
        build_dir = getattr(build_cmd, dir_option)

        prefix_len = len(build_dir) + len(os.sep)
        outputs = []
        for source in build_files:
            # Trim off the build directory
            outfile = os.path.join(self.install_dir, source[prefix_len:])
            self.mkpath(os.path.dirname(outfile))
            self.copy_file(source, outfile)
            outputs.append(outfile)
        return outputs

    def get_source_files(self):
        # The sources are assumed to be reported by 'build_py' and 'build_ext'
        return []
