from enthought.block_canvas.context.api import DataContext

from ipython1.core1.interpreter import Interpreter

interp = Interpreter()

namespace = DataContext()
#namespace = {}

interp = Interpreter(namespace=namespace, translator=None, magic=None,
                     display_formatters=None, traceback_formatters=None,
                     output_trap=None, history=None, message_cache=None,
                     filename='<string>', config=None)

interp.execute_python("a=1")

print namespace['a']


