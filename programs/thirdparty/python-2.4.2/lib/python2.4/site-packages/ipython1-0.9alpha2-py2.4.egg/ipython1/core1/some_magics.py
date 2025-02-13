
# Standard library imports.
import optparse
import shlex


def magic_fwrite(interpreter, parameter_s=''):
    """ Write the string representation of a variable out to a file.

      %fwrite myvar myfile.txt

    Usually, simply str(myvar) will be the string that gets written out. Unicode
    strings will be encoded to a byte string (as UTF-8 by default) first.
    """

    varname, filename = shlex.split(parameter_s)
    value = interpreter.pull(varname)
    
    # Special case unicode strings.
    # fixme: allow the caller to specify an encoding.
    if isinstance(value, unicode):
        stringrep = value.encode('utf-8')
    else:
        stringrep = str(value)

    # Write the string out to a file.
    # fixme: Allow the user to change the mode.
    f = open(filename, 'wb')
    f.write(stringrep)
    f.close()





