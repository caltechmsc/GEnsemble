""" Manager for completion lists.
"""

# Standard library imports.
import os
import re
import keyword
import inspect
import string
import __builtin__


def get_class_members(cls):
    """ Go through the class members of a class and all of its superclasses.
    """

    # Stolen from IPython.

    ret = dir(cls)
    if hasattr(cls,'__bases__'):
        for base in cls.__bases__:
            ret.extend(get_class_members(base))

    return ret


class Completer(object):
    """ An object that handles completion lists.
    """

    def __init__(self, interpreter, matchers=None, global_namespace=None,
        omit__names=True, merge_completions=True):

        # The interpreter instance to provide completions for.
        self.interpreter = interpreter

        # An optional global namespace for embedded applications.
        self.global_namespace = {}

        # Omit __special__ names unless the user specifically started with _.
        self.omit__names = omit__names

        # Should this merge completions from all of the matchers or just return the
        # results of the first matcher that returns anything.
        self.merge_completions = merge_completions

        # A list of callables for matching.
        if matchers is None:
            matchers = [self.python_matcher]
        self.matchers = matchers

        # The escaping character for IPython magics.
        # fixme: store this elsewhere!
        self.magic_escape = '%'

        # The prefix for transformed IPython magics.
        # fixme: store this elsewhere!
        self.magic_prefix = 'magic_'

        # A filtering regex for __ names.
        self.no__names = re.compile(r'.*\.__.*?__')

        # A filtering regex for _ names.
        self.no_names = re.compile(r'.*\._.*?')

        # Characters that separate words that we want to complete.
        self.delimiters = ' \t\n`~!@#$%^&*()-=+[{]}\\|;:\'",<>/?'

        # A regex for finding function parameters.
        self.func_params = re.compile(r'''
            '.*?' |    # single quoted strings or
            ".*?" |    # double quoted strings or
            \w+   |    # identifier
            \S         # other characters
            ''', re.VERBOSE | re.DOTALL)


    def set_default_matchers(self):
        """ Let the list of matchers be the default list.
        """

        self.matchers = [self.python_matcher,
                        ]

    def get_word(self, text):
        """ Extract a word for completion.
        """

        text_type = type(text)
        # fixme: cache the table somewhere.
        if text_type is str:
            table = string.maketrans(self.delimiters, ' '*len(self.delimiters))
        elif text_type is unicode:
            table = dict(zip(map(ord, self.delimiters), u' '*len(self.delimiters)))

        text = text.translate(table)
        words = text.rsplit(' ', 1)
        if words:
            return words[-1]
        else:
            return ''

    def complete(self, text):
        """ Return the completion list for a given piece of text.

        Parameters
        ----------
        text : str
            This must be the particular word to be completed, not the full
            input.

        Returns
        -------
        matches : list
            The possibly empty list of completions for the given text.
        """

        # The logic here is mostly taken from IPython.

        if text.startswith(self.magic_escape):
            text = text.replace(self.magic_escape, self.magic_prefix)
        elif text.startswith('~'):
            # Presumably, this is a filename starting with a user-twiddle to be
            # expanded.
            text = os.path.expanduser(text)
        
        if self.merge_completions:
            # Get all completions from each matcher.
            matches = []
            for matcher in self.matchers:
                matches.extend(matcher(text))
        else:
            for matcher in self.matchers:
                matches = matcher(text)
                if matches:
                    break

        return matches

    def python_matcher(self, text):
        """ Match global Python names and attributes.
        """

        # The logic here is mostly taken from IPython.

        if '.' in text:
            try:
                matches = self.attr_matcher(text)
                if text.endswith('.') and self.omit__names:
                    if self.omit__names == 1:
                        # Only allow attributes that are not __special__ names.
                        matches = [x for x in matches 
                                   if self.no__names.match(x) is None]
                    else:
                        # Only allow attributes that are not _private names.
                        matches = [x for x in matches
                                   if self.no_names.match(x) is None]
            except NameError:
                # Catch <undefined attributes>.<tab>
                matches = []
        else:
            matches = self.global_matcher(text)

            # This is so completion finds magics when automagic is on:
            # fixme: update this when I understand what's going on.
            if (matches == [] and 
                 not text.startswith(os.sep) and
                 not ' ' in self.lbuf):
                matches = self.attr_matcher(self.magic_prefix+text)

        return matches

    def global_matcher(self, text):
        """Compute matches when text is a simple name.

        Return a list of all keywords, built-in functions and names currently
        defined in the interpreter's namespace or self.global_namespace that match.
        """

        # More larceny from IPython.

        matches = []
        match_append = matches.append
        for lst in [keyword.kwlist,
                    __builtin__.__dict__.keys(),
                    self.interpreter.namespace.keys(),
                    self.global_namespace.keys()]:
            for word in lst:
                if word.startswith(text) and word != "__builtins__":
                    match_append(word)
        return matches

    def attr_matcher(self, text):
        """Compute matches when text contains a dot.

        Assuming the text is of the form NAME.NAME....[NAME], and is
        evaluatable in the interpreter's namespace or self.global_namespace, it
        will be evaluated and its attributes (as revealed by dir()) are used as
        possible completions.  (For class instances, class members are are also
        considered.)

        WARNING: this can still invoke arbitrary C code, if an object
        with a __getattr__ hook is evaluated.
        """

        # More larceny from IPython.

        # Another option, seems to work great. Catches things like ''.<tab>
        m = re.match(r"(\S+(\.\w+)*)\.(\w*)$", text)

        if not m:
            return []
        
        expr, attr = m.group(1, 3)
        try:
            object = eval(expr, self.interpreter.namespace)
        except:
            object = eval(expr, self.global_namespace)

        # fixme: Look into making the rest of this function into a generic
        # function so that it is easily extendable.

        # Start building the attribute list via dir(), and then complete it
        # with a few extra special-purpose calls.
        words = dir(object)

        if hasattr(object,'__class__'):
            words.append('__class__')
            words.extend(get_class_members(object.__class__))

        # This is the 'dir' function for objects with Enthought's traits
        if hasattr(object, 'trait_names'):
            try:
                words.extend(object.trait_names())
                # Eliminate possible duplicates, as some traits may also
                # appear as normal attributes in the dir() call.
                words = set(words)
            except TypeError:
                # This will happen if `object` is a class and not an instance.
                pass

        # Support for PyCrust-style _getAttributeNames magic method.
        if hasattr(object, '_getAttributeNames'):
            try:
                words.extend(object._getAttributeNames())
                # Eliminate duplicates.
                words = set(words)
            except TypeError:
                # `object` is a class and not an instance.  Ignore
                # this error.
                pass

        # Filter out non-string attributes which may be stuffed by dir() calls
        # and poor coding in third-party modules
        words = [w for w in words
                 if isinstance(w, basestring) and w != "__builtins__"]

        # Build match list to return
        return ["%s.%s" % (expr, w) for w in words if w.startswith(attr)]

    def _default_arguments(self, obj):
        """Return the list of default arguments of obj if it is callable,
        or empty list otherwise.
        """

        # Take me away, officer! Yup, this is from IPython.

        if not (inspect.isfunction(obj) or inspect.ismethod(obj)):
            # For classes, check for __init__,__new__
            if inspect.isclass(obj):
                obj = (getattr(obj,'__init__',None) or
                       getattr(obj,'__new__',None))
            # For all others, check if they are __call__able
            elif hasattr(obj, '__call__'):
                obj = obj.__call__
            # fixme: is there a way to handle the builtins?
            # I don't think so!
        try:
            args,_,_1,defaults = inspect.getargspec(obj)
            if defaults:
                return args[-len(defaults):]
        except TypeError: pass
        return []

    def python_func_kw_matcher(self, text):
        """Match named parameters (kwargs) of the last open function.
        """

        # This is stolen from IPython.

        # fixme: this is not yet integrated.

        if "." in text: 
            # A parameter cannot be dotted.
            return []

        regexp = self.func_params

        # 1. Find the nearest identifier that comes before an unclosed
        # parenthesis e.g. for "foo (1+bar(x), pa", the candidate is "foo"
        tokens = regexp.findall(self.get_line_buffer())
        itertokens = reversed(tokens)
        openPar = 0
        for token in itertokens:
            if token == ')':
                openPar -= 1
            elif token == '(':
                openPar += 1
                if openPar > 0:
                    # found the last unclosed parenthesis
                    break
        else:
            return []

        # 2. Concatenate dotted names ("foo.bar" for "foo.bar(x, pa" )
        ids = []
        is_id = re.compile(r'\w+$').match
        while True:
            try:
                ids.append(itertokens.next())
                if not is_id(ids[-1]):
                    ids.pop()
                    break
                if not itertokens.next() == '.':
                    break
            except StopIteration:
                break
        # Lookup the candidate callable matches either using global_matches
        # or attr_matches for dotted names
        if len(ids) == 1:
            callable_matches = self.global_matcher(ids[0])
        else:
            callable_matches = self.attr_matcher('.'.join(ids[::-1]))
        arg_matches = []
        for callable_match in callable_matches:
            try: 
                named_args = self._default_arguments(eval(callable_match,
                    self.interpreter.namespace))
            except: 
                continue
            for named_arg in named_args:
                if named_arg.startswith(text):
                    arg_matches.append("%s=" % named_arg)
        return arg_matches


