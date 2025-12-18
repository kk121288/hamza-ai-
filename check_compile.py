import py_compile,traceback\ntry:\n    py_compile.compile('main.py', doraise=True)\n    print('py_compile OK')\nexcept Exception:\n    traceback.print_exc()
