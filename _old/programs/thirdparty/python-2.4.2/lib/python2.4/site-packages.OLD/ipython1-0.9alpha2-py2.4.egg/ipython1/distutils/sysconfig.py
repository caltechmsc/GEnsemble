# encoding: utf-8
__docformat__ = "restructuredtext en"

print "Here is ipython1.distutils.sysconfig!!!!!!"

import distutils.sysconfig
import os

def customize_compiler(compiler):
    """Do any platform-specific customization of a CCompiler instance.

    Mainly needed on Unix, so we can plug in the information that
    varies across Unices and is stored in Python's Makefile.
    """
    if compiler.compiler_type == "unix":
        (cc, cxx, opt, basecflags, ccshared, ldshared, so_ext) = \
            distutils.sysconfig.get_config_vars('CC', 'CXX', 'OPT', 'BASECFLAGS', 'CCSHARED', 'LDSHARED', 'SO')

        if os.environ.has_key('CC'):
            cc = os.environ['CC']
        if os.environ.has_key('CXX'):
            cxx = os.environ['CXX']
        if os.environ.has_key('LDSHARED'):
            ldshared = os.environ['LDSHARED']
        if os.environ.has_key('CPP'):
            cpp = os.environ['CPP']
        else:
            cpp = cc + " -E"           # not always
        if os.environ.has_key('LDFLAGS'):
            ldshared = ldshared + ' ' + os.environ['LDFLAGS']
        if basecflags:
            opt = basecflags + ' ' + opt
        if os.environ.has_key('CFLAGS'):
            opt = opt + ' ' + os.environ['CFLAGS']
            ldshared = ldshared + ' ' + os.environ['CFLAGS']
        if os.environ.has_key('CPPFLAGS'):
            cpp = cpp + ' ' + os.environ['CPPFLAGS']
            opt = opt + ' ' + os.environ['CPPFLAGS']
            ldshared = ldshared + ' ' + os.environ['CPPFLAGS']

        cc_cmd = cc + ' ' + opt
        compiler.set_executables(
            preprocessor=cpp,
            compiler=cc_cmd,
            compiler_so=cc_cmd + ' ' + ccshared,
            compiler_cxx=cxx,
            linker_so=ldshared,
            linker_exe=cc)

        compiler.shared_lib_extension = so_ext
        
python_version = distutils.sysconfig.get_python_version()

if python_version == '2.3':
    distutils.sysconfig.customize_compiler = customize_compiler