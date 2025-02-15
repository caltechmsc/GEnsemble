"""Input translator.

This module implements a class that translates user input from the various
forms accepted by IPython into pure valid Python.
"""

__docformat__ = "restructuredtext en"

# Standard library imports.
import codeop
import compiler
import re
import __builtin__

# Local imports.
from util import Bunch, make_quoted_expr


class IPythonTranslator(object):
    """ An object that translates IPython commands into real Python code.
    """

    def __init__(self, interpreter=None, magic=None, rc=None):
        """Construct the translator.

        :Parameters:

          interpreter : instance
            An isntance of 

        """

        # The configuration object.
        if rc is None:
            rc = Bunch(
                ESC_SHELL  = '!',
                ESC_HELP   = '?',
                ESC_MAGIC  = '%',
                ESC_QUOTE  = ',',
                ESC_QUOTE2 = ';',
                ESC_PAREN  = '/',
                autocall   = True,
                automagic  = True,
            )
        self.rc = rc

        # The mapping from escape characters to handler methods.
        self.esc_handlers = {
            self.rc.ESC_PAREN  : self.handle_auto,
            self.rc.ESC_QUOTE  : self.handle_auto,
            self.rc.ESC_QUOTE2 : self.handle_auto,
            self.rc.ESC_MAGIC  : self.handle_magic,
            self.rc.ESC_HELP   : self.handle_help,
            self.rc.ESC_SHELL  : self.handle_shell_escape,
        }

        # RegExp for splitting line contents into pre-char//first
        # word-method//rest.  For clarity, each group in on one line.

        # WARNING: update the regexp if the above escapes are changed, as they
        # are hardwired in.

        # Don't get carried away with trying to make the autocalling catch too
        # much:  it's better to be conservative rather than to trigger hidden
        # evals() somewhere and end up causing side effects.
        self.line_split = re.compile(r'^(\s*[,;/]?\s*)'
                                     r'([\?\w\.]+\w*\s*)'
                                     r'(\(?.*$)')

        self.shell_line_split = re.compile(r'^(\s*)'
                                     r'(\S*\s*)'
                                     r'(\(?.*$)')

        # A simpler regexp used as a fallback if the above doesn't work.  This
        # one is more conservative in how it partitions the input.  This code
        # can probably be cleaned up to do everything with just one regexp, but
        # I'm afraid of breaking something; do it once the unit tests are in
        # place.
        self.line_split_fallback = re.compile(r'^(\s*)'
                                              r'([%\!\?\w\.]*)'
                                              r'(.*)')

        # Original re, keep around for a while in case changes break something
        #self.line_split = re.compile(r'(^[\s*!\?%,/]?)'
        #                             r'(\s*[\?\w\.]+\w*\s*)'
        #                             r'(\(?.*$)')

        # RegExp to identify potential function names
        self.re_fun_name = re.compile(r'[a-zA-Z_]([a-zA-Z0-9_.]*) *$')

        # RegExp to exclude strings with this start from autocalling.  In
        # particular, all binary operators should be excluded, so that if foo
        # is callable, foo OP bar doesn't become foo(OP bar), which is
        # invalid.  The characters '!=()' don't need to be checked for, as the
        # _prefilter routine explicitely does so, to catch direct calls and
        # rebindings of existing names.

        # Warning: the '-' HAS TO BE AT THE END of the first group, otherwise
        # it affects the rest of the group in square brackets.
        self.re_exclude_auto = re.compile(r'^[<>,&^\|\*/\+-]'
                                          '|^is |^not |^in |^and |^or ')


    #######################################################################
    # Public interface
    #######################################################################

    def line_translate(self, line):
        """Calls different preprocessors, depending on the form of line."""

        # All handlers *must* return a value, even if it's blank ('').

        # Lines are NOT logged here. Handlers should process the line as
        # needed, update the cache AND log it (so that the input cache array
        # stays synced).

        # This function is _very_ delicate, and since it's also the one which
        # determines IPython's response to user input, it must be as efficient
        # as possible.  For this reason it has _many_ returns in it, trying
        # always to exit as quickly as it can figure out what it needs to do.

        # This function is the main responsible for maintaining IPython's
        # behavior respectful of Python's semantics.  So be _very_ careful if
        # making changes to anything here.

        #.....................................................................
        # Code begins

        interp = self.interpreter  # we'll need this a lot

        #if line.startswith('%crash'): raise RuntimeError,'Crash now!'  # dbg

        # save the line away in case we crash, so the post-mortem handler can
        # record it
        self._last_input_line = line

        #print '***line: <%s>' % line # dbg
        
        # the input history needs to track even empty lines
        stripped = line.strip()
        
        if not stripped:
            return self.handle_normal(line)

        # For the rest, we need the structure of the input
        pre,iFun,theRest = self.split_user_input(line)

        # See whether any pre-existing handler can take care of it
            
        #print 'pre <%s> iFun <%s> rest <%s>' % (pre,iFun,theRest)  # dbg
        
        # Next, check if we can automatically execute this thing

        # Allow ! in multi-line statements if multi_line_specials is on:
        if iFun.startswith(self.ESC_SHELL):
            return self.handle_shell_escape(line,pre,iFun,theRest)        

        # First check for explicit escapes in the last/first character
        handler = None
        if line[-1] == self.ESC_HELP and line[0] != self.ESC_SHELL:
            handler = self.esc_handlers.get(line[-1])  # the ? can be at the end
        if handler is None:
            # look at the first character of iFun, NOT of line, so we skip
            # leading whitespace in multiline input
            handler = self.esc_handlers.get(iFun[0:1])
        if handler is not None:
            return handler(line,pre,iFun,theRest)
        # Emacs ipython-mode tags certain input lines
        if line.endswith('# PYTHON-MODE'):
            return self.handle_emacs(line)

        # Let's try to find if the input line is a magic fn
        oinfo = None
        if interp.magic.has_magic(iFun):
            # WARNING: _ofind uses getattr(), so it can consume generators and
            # cause other side effects.
            oinfo = interp.object_find(iFun)
            if oinfo['ismagic']:
                # Be careful not to call magics when a variable assignment is
                # being made (ls='hi', for example)
                if self.rc.automagic and \
                       (len(theRest)==0 or theRest[0] not in '!=()<>,'):
                    return self.handle_magic(line,pre,iFun,theRest)
                else:
                    return self.handle_normal(line)

        # If the rest of the line begins with an (in)equality, assginment or
        # function call, we should not call _ofind but simply execute it.
        # This avoids spurious geattr() accesses on objects upon assignment.
        #
        # It also allows users to assign to either alias or magic names true
        # python variables (the magic/alias systems always take second seat to
        # true python code).
        if theRest and theRest[0] in '!=()':
            return self.handle_normal(line)
        
        if oinfo is None:
            # let's try to ensure that _oinfo is ONLY called when autocall is
            # on.  Since it has inevitable potential side effects, at least
            # having autocall off should be a guarantee to the user that no
            # weird things will happen.

            if self.rc.autocall:
                oinfo = interp.object_find(iFun)
            else:
                # in this case, all that's left is either an alias or
                # processing the line normally.
                if iFun in interp.alias_table:
                    # if autocall is off, by not running _ofind we won't know
                    # whether the given name may also exist in one of the
                    # user's namespace.  At this point, it's best to do a
                    # quick check just to be sure that we don't let aliases
                    # shadow variables.
                    head = iFun.split('.',1)[0]
                    if head in interp.user_ns or head in interp.internal_ns \
                       or head in __builtin__.__dict__:
                        return self.handle_normal(line)
                    else:
                        return self.handle_alias(line,pre,iFun,theRest)
                else:
                    return self.handle_normal(line)
        
        if not oinfo['found']:
            return self.handle_normal(line)
        else:
            #print 'pre<%s> iFun <%s> rest <%s>' % (pre,iFun,theRest) # dbg
            if oinfo['isalias']:
                return self.handle_alias(line,pre,iFun,theRest)

            if (self.rc.autocall 
                 and
                   (
                   #only consider exclusion re if not "," or ";" autoquoting
                   (pre == self.ESC_QUOTE or pre == self.ESC_QUOTE2
                     or pre == self.ESC_PAREN) or 
                   (not self.re_exclude_auto.match(theRest)))
                 and 
                   self.re_fun_name.match(iFun) and 
                   callable(oinfo['obj'])) :
                #print 'going auto'  # dbg
                return self.handle_auto(line,pre,iFun,theRest,oinfo['obj'])
            else:
                #print 'was callable?', callable(oinfo['obj'])  # dbg
                return self.handle_normal(line)

        # If we get here, we have a normal Python line. Log and return.
        return self.handle_normal(line)
    
    def block_translate(self, text):
        """Translate a block of code.

        Parameters
        ----------
        text : str
            The raw (I)Python commands that the user entered.  This can be a
        multiline block of text.

        Returns
        -------

        """

        try:
            ast = compiler.parse(text)

            # If we get to this point, then the text is pure Python, so we can
            # pass it along. It does not need translation.
            return text
        except SyntaxError, e:
            # Else, we need to try and break it apart into lines for
            # line-by-line filtering by the user-installed filters.
            lines = text.splitlines()
            return '\n'.join(map(self.line_translate,lines))

    #######################################################################
    # Private interface
    #######################################################################

    def split_user_input(self,line, pattern = None):
        """Split user input into pre-char, function part and rest."""

        if pattern is None:
            pattern = self.line_split
            
        lsplit = pattern.match(line)
        if lsplit is None:  # no regexp match returns None
            #print "match failed for line '%s'" % line  # dbg
            try:
                iFun,theRest = line.split(None,1)
            except ValueError:
                #print "split failed for line '%s'" % line  # dbg
                iFun,theRest = line,''
            pre = re.match('^(\s*)(.*)',line).groups()[0]
        else:
            pre,iFun,theRest = lsplit.groups()

        # iFun has to be a valid python identifier, so it better be only pure
        #ascii, no unicode:
        try:
            iFun = iFun.encode('ascii')
        except UnicodeEncodeError:
            theRest = iFun+u' '+theRest
            iFun = u''
            
        #print 'line:<%s>' % line # dbg
        #print 'pre <%s> iFun <%s> rest <%s>' % (pre,iFun.strip(),theRest) # dbg
        return pre,iFun.strip(),theRest

    #----------------------------------------------------------------------
    # Handlers for various types of special inputs we accept
    #----------------------------------------------------------------------
    
    def handle_normal(self,line,pre=None,iFun=None,theRest=None):
        """Handle normal input lines. Use as a template for handlers."""

        # XXX - This method may go away, if we really end up with it being
        # always a no-op
        
        # With autoindent on, we need some way to exit the input loop, and I
        # don't want to force the user to have to backspace all the way to
        # clear the line.  The rule will be in this case, that either two
        # lines of pure whitespace in a row, or a line of pure whitespace but
        # of a size different to the indent level, will exit the input loop.

        # OLD IPython code - logic to be moved into terminal client
        #if (continue_prompt and self.autoindent and line.isspace() and
        #    (0 < abs(len(line) - self.indent_current_nsp) <= 2 or
        #     (self.buffer[-1]).isspace() )):
        #    line = ''

        return line

    def handle_alias(self,line,continue_prompt=None,
                     pre=None,iFun=None,theRest=None):
        """Handle alias input lines. """

        # pre is needed, because it carries the leading whitespace.  Otherwise
        # aliases won't work in indented sections.
        transformed = self.expand_aliases(iFun, theRest)        
        line_out = '%s_ip.system(%s)' % (pre, make_quoted_expr( transformed ))        
        #print 'line out:',line_out # dbg
        return line_out

    def handle_auto(self, line, continue_prompt=None,
                    pre=None,iFun=None,theRest=None,obj=None):
        """Hande lines which can be auto-executed, quoting if requested."""

        #print 'pre <%s> iFun <%s> rest <%s>' % (pre,iFun,theRest)  # dbg
        
        # This should only be active for single-line input!
        if continue_prompt:
            self.log(line,line,continue_prompt)
            return line

        auto_rewrite = True
        
        if pre == self.ESC_QUOTE:
            # Auto-quote splitting on whitespace
            newcmd = '%s("%s")' % (iFun,'", "'.join(theRest.split()) )
        elif pre == self.ESC_QUOTE2:
            # Auto-quote whole string
            newcmd = '%s("%s")' % (iFun,theRest)
        elif pre == self.ESC_PAREN:
            newcmd = '%s(%s)' % (iFun,",".join(theRest.split()))
        else:
            # Auto-paren.
            # We only apply it to argument-less calls if the autocall
            # parameter is set to 2.  We only need to check that autocall is <
            # 2, since this function isn't called unless it's at least 1.
            if not theRest and (self.rc.autocall < 2):
                newcmd = '%s %s' % (iFun,theRest)
                auto_rewrite = False
            else:
                if theRest.startswith('['):
                    if hasattr(obj,'__getitem__'):
                        # Don't autocall in this case: item access for an object
                        # which is BOTH callable and implements __getitem__.
                        newcmd = '%s %s' % (iFun,theRest)
                        auto_rewrite = False
                    else:
                        # if the object doesn't support [] access, go ahead and
                        # autocall
                        newcmd = '%s(%s)' % (iFun.rstrip(),theRest)
                elif theRest.endswith(';'):
                    newcmd = '%s(%s);' % (iFun.rstrip(),theRest[:-1])
                else:
                    newcmd = '%s(%s)' % (iFun.rstrip(), theRest)

        if auto_rewrite:
            print >>Term.cout, self.outputcache.prompt1.auto_rewrite() + newcmd
        # log what is now valid Python, not the actual user input (without the
        # final newline)
        return newcmd

    def handle_emacs(self,line,continue_prompt=None,
                    pre=None,iFun=None,theRest=None):
        """Handle input lines marked by python-mode."""

        # Currently, nothing is done.  Later more functionality can be added
        # here if needed.

        # The input cache shouldn't be updated

        return line

    def handle_help(self, line, pre=None,iFun=None,theRest=None):
        """Try to get some help for the object.

        obj? or ?obj   -> basic information.
        obj?? or ??obj -> more details.
        """

        # We need to make sure that we don't process lines which would be
        # otherwise valid python, such as "x=1 # what?"
        try:
            codeop.compile_command(line)
        except SyntaxError:
            # We should only handle as help stuff which is NOT valid syntax
            if line[0]==self.ESC_HELP:
                line = line[1:]
            elif line[-1]==self.ESC_HELP:
                line = line[:-1]
            return '_ip.ipmagic("pinfo","%s")' % line
        except:
            # Pass any other exceptions through to the normal handler
            return self.handle_normal(line)
        else:
            # If the code compiles ok, we should handle it normally
            return self.handle_normal(line)

    def handle_magic(self, line, pre=None,iFun=None,theRest=None):
        """Execute magic functions."""

        cmd = '%s_ip.magic(%s)' % (pre,make_quoted_expr(iFun + " " + theRest))
        #print 'in handle_magic, cmd=<%s>' % cmd  # dbg
        return cmd

    def handle_shell_escape(self, line, continue_prompt=None,
                            pre=None,iFun=None,theRest=None):
        """Execute the line in a shell, empty return value"""

        #print 'line in :', `line` # dbg
        # Example of a special handler. Others follow a similar pattern.
        if line.lstrip().startswith('!!'):
            # rewrite iFun/theRest to properly hold the call to %sx and
            # the actual command to be executed, so handle_magic can work
            # correctly
            theRest = '%s %s' % (iFun[2:],theRest)
            iFun = 'sx'
            return self.handle_magic('%ssx %s' % (self.ESC_MAGIC,
                                     line.lstrip()[2:]),
                                     continue_prompt,pre,iFun,theRest)
        else:
            cmd=line.lstrip().lstrip('!')
            line_out = '%s_ip.system(%s)' % (pre,make_quoted_expr(cmd))
        # update cache/log and return
        return line_out
