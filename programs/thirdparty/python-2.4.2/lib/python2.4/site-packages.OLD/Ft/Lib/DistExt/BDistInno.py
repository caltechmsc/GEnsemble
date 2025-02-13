import os, sys, re, imp
from distutils import util
from distutils.core import Command
from distutils.errors import DistutilsInternalError, DistutilsSetupError
from distutils.dir_util import remove_tree

_can_read_reg = False
try:
    import _winreg
    RegOpenKeyEx = _winreg.OpenKeyEx
    RegQueryValue = _winreg.QueryValue
    RegError = _winreg.error
    HKEY_CLASSES_ROOT = _winreg.HKEY_CLASSES_ROOT

    _can_read_reg = True

except ImportError:
    try:
        import win32api
        import win32con
        RegOpenKeyEx = win32api.RegOpenKeyEx
        RegQueryValue = win32api.RegQueryValue
        RegError = win32api.error
        HKEY_CLASSES_ROOT = win32con.HKEY_CLASSES_ROOT

        _can_read_reg = True

    except ImportError:
        pass

PY_SOURCE_EXTS = [ s for s,m,t in imp.get_suffixes() if t == imp.PY_SOURCE ]

ISCC_TEMPLATE = """
[Setup]
OutputDir=%(output-dir)s
OutputBaseFilename=%(name)s-%(version)s.win32-py%(target-version)s
AppName=%(name)s
AppVersion=%(version)s
AppVerName=%(name)s %(version)s for Python %(target-version)s
AppId=%(name)s %(version)s for Python %(target-version)s
AppPublisher=%(publisher)s
AppPublisherURL=%(publisher-url)s
AppSupportURL=%(support-url)s
UninstallFilesDir=%(uninstall-dir)s
DefaultDirName=ignored
DefaultGroupName={code:GetPythonGroup}
LicenseFile=%(license-file)s
UserInfoPage=no
DisableDirPage=yes
DisableReadyMemo=yes
FlatComponentsList=no

[Types]
Name: "full"; Description: "Full installation"
Name: "compact"; Description: "Compact installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "Main"; Description: "Python Library"; Types: full compact custom; Flags: fixed
%(components)s

[Dirs]
%(dirs)s

[Icons]
%(icons)s

[Files]
%(files)s

[UninstallDelete]
%(uninstall)s

[Run]
%(run)s

[Code]
const
  AppName = '%(name)s';
  PythonVersion = '%(target-version)s';
  UseCustomLocation = False; { Disabled until custom locations are fixed }

var
  PythonGroup: String;
  PythonBaseDir: String;
  PythonDir: String;
  CustomDir: String;
  InstallDir: String;
  CustomRadio: TRadioButton;
  CustomBrowse: TButton;
  CustomEdit: TEdit;
  CustomPage: Integer;

function GetPythonGroup(Default: String): String;
begin
  Result := PythonGroup;
end; { GetPythonGroup }

function GetPythonDir(Default: String): String;
begin
  Result := PythonBaseDir;
end; { GetPythonDir }

function GetInstallDir(Default: String): String;
begin
  Result := InstallDir;
end; { GetInstallDir }

procedure MutateConfigFile(Filename: String);
var
  Config: String;
  PrefixDir: String;
begin
  PrefixDir := AddBackslash(PythonBaseDir);
  StringChange(PrefixDir, '\\', '\\\\');

  Filename := ExpandConstant(Filename);
  LoadStringFromFile(Filename, Config);
  StringChange(Config, 'PREFIX\\\\', PrefixDir);
  SaveStringToFile(Filename, Config, False);
end; { MutateConfigFile }

{ OnChange handler for custom edit box }
procedure CustomEditChange(Sender: TObject);
begin
  CustomRadio.Checked := True;
end; { CustomEditChange }

{ OnClick handler for custom button }
procedure BrowseClick(Sender: TObject);
var
  Directory: String;
begin
  if BrowseForFolder('Select folder for installation:', Directory, True) then
  begin
    CustomEdit.Text := Directory;
  end;
end; { BrowseClick }

procedure InitializeWizard;
var
  Page: TWizardPage;
  Top: Integer;
  Registry: TRadioButton;
  Caption, Note: TLabel;
begin
  Page := CreateCustomPage(%(custom-page)s, 'Select Destination Directory',
                           'Where should ' + AppName + ' be installed?');
  CustomPage := Page.ID;

  Caption := TLabel.Create(Page);
  Caption.Parent := Page.Surface;
  Caption.Caption := 'Select the folder where you would like ' + AppName +
                     ' to be installed, then click Next.';
  Top := Caption.Height + 8;

  if PythonDir <> '' then
  begin
    Registry := TRadioButton.Create(Page);
    Registry.Parent := Page.Surface;
    Registry.Caption := PythonDir;
    Registry.Top := Top;
    Registry.Width := Page.SurfaceWidth;
    Registry.Checked := (PythonDir = InstallDir);
    Top := Top + Registry.Height + 8;
  end;

  CustomRadio := TRadioButton.Create(Page);
  CustomRadio.Visible := UseCustomLocation;
  CustomRadio.Parent := Page.Surface;
  CustomRadio.Caption := '';
  CustomRadio.Width := 16;
  CustomRadio.Top := Top;
  CustomRadio.Checked := (CustomDir = InstallDir);
  CustomBrowse := TButton.Create(Page);
  CustomBrowse.Visible := UseCustomLocation;
  CustomBrowse.Parent := Page.Surface;
  CustomBrowse.OnClick := @BrowseClick;
  CustomBrowse.Caption := 'Browse...';
  CustomBrowse.Height := 23;
  CustomBrowse.Top := Top;
  CustomBrowse.Left := Page.SurfaceWidth - CustomBrowse.Width;
  CustomEdit := TEdit.Create(Page);
  CustomEdit.Visible := UseCustomLocation;
  CustomEdit.Parent := Page.Surface;
  CustomEdit.OnChange := @CustomEditChange;
  CustomEdit.OnClick := @CustomEditChange;
  CustomEdit.Text := CustomDir;
  CustomEdit.Top := Top;
  CustomEdit.Left := CustomRadio.Width;
  CustomEdit.Width := CustomBrowse.Left - 8 - CustomRadio.Width;
  Note := TLabel.Create(Page);
  Note.Visible := UseCustomLocation;
  Note.Parent := Page.Surface;
  Note.AutoSize := False;
  Note.WordWrap := True;
  Note.Top := Top + CustomEdit.Height + 4;
  Note.Left := CustomRadio.Width + 8;
  Note.Width := CustomEdit.Width - 16;
  Note.Height := Page.SurfaceHeight - Note.Top;
  Note.Caption := 'NOTE: Be sure to use a folder that is on the PYTHONPATH.';
end; { InitializeWizard }

function InitializeSetup(): Boolean;
var
  Key: String;
begin
  Key := 'Software\\Python\\PythonCore\\' + PythonVersion + '\\InstallPath';
  if not RegQueryStringValue(HKEY_CURRENT_USER, Key, '', PythonBaseDir) then
    RegQueryStringValue(HKEY_LOCAL_MACHINE, Key, '', PythonBaseDir);

  if (PythonBaseDir <> '') then
  begin
    PythonBaseDir := RemoveBackslashUnlessRoot(PythonBaseDir);
    if (CompareStr(PythonVersion, '2.2') >= 0) then
      PythonDir := PythonBaseDir + '\\Lib\\site-packages';
  end
  else
    PythonDir := PythonBaseDir;

  Key := Key + '\\InstallGroup';
  if not RegQueryStringValue(HKEY_CURRENT_USER, Key, '', PythonGroup) then
    RegQueryStringValue(HKEY_LOCAL_MACHINE, Key, '', PythonGroup);

  PythonGroup := AddBackslash(PythonGroup) + AppName;

  InstallDir := PythonDir;
  CustomDir := '';

  Result := True;
end; { InitializeSetup }

function NextButtonClick(CurPage: Integer): Boolean;
begin
  if CurPage = CustomPage then
  begin
    { Save the selection into InstallDir }
    if CustomRadio.Checked then
    begin
      InstallDir := RemoveBackslashUnlessRoot(CustomEdit.Text);
      CustomDir := InstallDir;
    end
    else
      InstallDir := PythonDir;
  end
  Result := True;
end; { NextButtonClick }
"""

class BDistInno(Command):

    command_name = 'bdist_inno'

    description = "create an executable installer for MS Windows"

    user_options = [('bdist-dir=', None,
                     "temporary directory for creating the distribution"),
                    ('keep-temp', 'k',
                     "keep the pseudo-installation tree around after " +
                     "creating the distribution archive"),
                    ('dist-dir=', 'd',
                     "directory to put final built distributions in"),
                   ]

    boolean_options = ['keep-temp']

    def initialize_options(self):
        self.bdist_dir = None
        self.keep_temp = 0
        self.dist_dir = None
        return

    def finalize_options(self):
        if self.bdist_dir is None:
            bdist_base = self.get_finalized_command('bdist').bdist_base
            self.bdist_dir = os.path.join(bdist_base, 'inno')

        self.set_undefined_options('bdist', ('dist_dir', 'dist_dir'))

        # Runtime variables
        self.config_file = None
        self.license_file = None
        return

    def run(self):
        if sys.platform != 'win32':
            raise DistutilsPlatformError("InnoSetup distributions must be"
                                         " created on a Windows platform")

        self.run_command('build')

        self.mkpath(self.bdist_dir)

        config = self.reinitialize_command('config')
        config.ensure_finalized()
        config.prefix = 'PREFIX'

        install = self.reinitialize_command('install')
        install.root = self.bdist_dir
        install.install_lib = 'PYTHONLIB'

        # Don't include "compiled" py-files
        install.compile = 0
        install.optimize = 0

        # don't warn about installing into a directory not in sys.path
        install.warn_dir = 0

        # always include documentation
        install.with_docs = 1

        self.announce("installing to %s" % self.bdist_dir, 2)
        install.ensure_finalized()
        install.run()

        # Make the customized configuration file
        if self.distribution.config_module:
            p = self.distribution.config_module.split('.')
            self.config_file = os.path.join(install.install_lib, *p) + '.py'
            config.write_config_vars(self.config_file)

        if self.distribution.license_file:
            license_file = util.convert_path(self.distribution.license_file)
            self.copy_file(license_file, self.bdist_dir)
            self.license_file = os.path.basename(license_file)

        # create the InnoSetup script
        iss_file = self.build_iss_file()
        iss_path = os.path.join(self.bdist_dir,
                                '%s.iss' % self.distribution.get_name())
        self.announce("writing %r" % iss_path)
        if not self.dry_run:
            f = open(iss_path, "w")
            f.write(iss_file)
            f.close()

        # build distribution using the Inno Setup 4 Command-Line Compiler
        self.announce("creating Inno Setup", 2) # log.info
        compiler = 'iscc.exe'
        if _can_read_reg:
            try:
                key = RegOpenKeyEx(HKEY_CLASSES_ROOT,
                                   'InnoSetupScriptFile\shell\Compile\command')
                command = RegQueryValue(key, None)
            except RegError:
                pass
            else:
                # if the command is in the form "name with spaces", then use
                # the string inside the quotes as the compiler, otherwise
                # use everything up to the first space as the compiler
                match = re.match('"([^\"]*)"', command)
                if match:
                    command = match.group(1)
                else:
                    command = command.split(' ')[0]
                compiler = os.path.join(os.path.dirname(command), compiler)
        self.spawn([compiler, iss_path])
        
        if not self.keep_temp:
            remove_tree(self.bdist_dir, self.verbose, self.dry_run)
        return

    def build_iss_file(self):
        """Generate the text of an InnoSetup iss file and return it as a
        list of strings (one per line).
        """
        # [Icons]
        iconspec = 'Name: "{group}\\%s"; Filename: "%s"; Components: %s'
        icons = []

        # [Run]
        runspec = ('Description: "%s"; Filename: "%s"; Components: %s; '
                   'Flags: %s')
        run = []

        # [Components]
        components = []
        for pkg in self.distribution.sub_packages:
            dist = self.distribution.get_package_distribution(pkg)
            component = 'Name: "Main\\%s"; ' % dist.get_name()
            component += 'Description: "%s - %s"; ' % (dist.get_name(),
                                                       dist.get_description())
            component += 'Types: full compact custom; Flags: fixed'
            components.append(component)

        # Add the docs component
        if self.distribution.has_docs():
            components.append('Name: "Docs"; '
                              'Description: "Documentation"; '
                              'Types: full')

        # Add the tests component
        if self.distribution.has_devel():
            components.append('Name: "Tests"; '
                              'Description: "Test suite"; '
                              'Types: full')

        # [Files] and [Dirs]
        files = []
        dirs = []
        uninstall = []
        install = self.get_finalized_command('install')
        for pkg in self.distribution.sub_packages:
            dist = self.distribution.get_package_distribution(pkg)
            dist_install = dist.get_command_obj('install')
            dist_install.compile = 0
            dist_install.optimize = 0
            # Ensure the install locations are the same
            for attr in ('install_lib',
                         'install_scripts',
                         'install_data',
                         'install_sysconf',
                         'install_localstate',
                         'install_docs',
                         'install_devel'):
                setattr(dist_install, attr, getattr(install, attr))

            component = 'Main\\' + dist.get_name()
            for command in ('install_lib',
                            'install_scripts',
                            'install_data',
                            'install_sysconf',
                            'install_localstate'):
                cmd_obj = dist.get_command_obj(command)
                cmd_obj.ensure_finalized()
                f, d, u = self._mutate_outputs(cmd_obj, component)
                files.extend(f)
                dirs.extend(d)
                uninstall.extend(u)

        if self.distribution.has_docs():
            build_docs = self.get_finalized_command('build_docs')
            install_docs = self.get_finalized_command('install_docs')
            links = []
            postinstall = []

            # The HTML index is always available
            path = os.path.join(install_docs.install_dir, 'html',
                                'index.html')
            links = [(self.distribution.get_name() + ' Documentation', path)]

            allfiles = build_docs.files + build_docs.documents
            for doc in allfiles:
                flags = getattr(doc, 'flags', ())
                if 'postinstall' in flags:
                    filename = os.path.basename(doc.source)
                    filename = os.path.splitext(filename)[0] + '.html'
                    filename = os.path.join(install_docs.install_dir, 'html',
                                            util.convert_path(doc.outdir),
                                            filename)
                    links.append((doc.title, filename))
                    postinstall.append((doc.title, filename))

            f, d, u = self._mutate_outputs(install_docs, 'Docs')
            files.extend(f)
            dirs.extend(d)
            uninstall.extend(u)

            for title, filename in links:
                source, dest = self._mutate_filename(filename)
                icons.append(iconspec % (title, dest, 'Docs'))

            for title, filename in postinstall:
                source, dest = self._mutate_filename(filename)
                run.append(runspec % ('View ' + title, dest, 'Docs',
                                      'postinstall shellexec skipifsilent'))

        if self.distribution.has_devel():
            install_devel = self.get_finalized_command('install_devel')
            f, d, u = self._mutate_outputs(install_devel, 'Tests')
            files.extend(f)
            dirs.extend(d)
            uninstall.extend(u)

        uninstall_dir = os.path.join(install.install_localstate, 'Uninstall')
        _, uninstall_dir = self._mutate_filename(uninstall_dir)
        subst = {
            'output-dir' : os.path.abspath(self.dist_dir),
            'name' : self.distribution.get_name(),
            'version' : self.distribution.get_version(),
            'publisher' : self.distribution.get_author(),
            'publisher-url' : self.distribution.get_author_email(),
            'support-url' : self.distribution.get_url(),
            'uninstall-dir' : uninstall_dir,
            'license-file' : self.license_file or '',
            'target-version' : sys.version[:3],
            'custom-page' : self.license_file and 'wpLicense' or 'wpWelcome',
            'components' : '\n'.join(components),
            'icons' : '\n'.join(icons),
            'files' : '\n'.join(files),
            'dirs' : '\n'.join(dirs),
            'run' : '\n'.join(run),
            'uninstall' : '\n'.join(uninstall),
            }

        return ISCC_TEMPLATE % subst

    def _mutate_filename(self, filename):
        # Strip the bdist_dir from the filename as the files will be
        # relative to the setup script which is in bdist_dir.  This
        # is to make the setup script more readable.
        source = filename[len(self.bdist_dir) + len(os.sep):]

        # Translate the filename to what is used in the setup script
        if source.startswith('PREFIX'):
            dest = '{code:GetPythonDir}' + source[6:]
        elif source.startswith('PYTHONLIB'):
            dest = '{code:GetInstallDir}' + source[9:]
        else:
            raise ValueError('bad filename: ' + filename)

        return source, dest

    def _mutate_outputs(self, cmd_obj, component):
        filespec = 'Source: "%s"; DestDir: "%s"; Components: ' + component
        dirspec = 'Name: "%s"; Components: ' + component
        uninstallspec = 'Type: files; Name: "%s"'
        files = []
        dirs = []
        uninstall = []
        for filename in cmd_obj.get_outputs():
            try:
                source, dest = self._mutate_filename(filename)
            except ValueError:
                raise DistutilsInternalError, \
                    'bad filename from %s: %s' % (cmd_obj.get_command_name(),
                                                  filename)

            if os.path.isdir(filename):
                # An empty directory
                dirs.append(dirspec % dest)
            else:
                destdir = os.path.dirname(dest)
                entry = filespec % (source, destdir)
                if filename == self.config_file:
                    entry += "; AfterInstall: MutateConfigFile('%s')" % dest
                files.append(entry)

            for ext in PY_SOURCE_EXTS:
                if filename.endswith(ext):
                    basename = dest[:-len(ext)]
                    uninstall.append(uninstallspec % (basename + '.pyc'))
                    uninstall.append(uninstallspec % (basename + '.pyo'))
        return files, dirs, uninstall
