from llvmlite import binding, ir

from basic.error import Error
from basic.lexer import Lexer
from basic.parser import Parser


def compile_lang(fn: str, text: str) -> Error | None:
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return ast.error

    module = ir.Module(name="basic")
    func_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
    function = ir.Function(module, func_type, name="add")

    block = function.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    arg1, arg2 = function.args

    result = builder.add(arg1, arg2, name="result")
    builder.ret(result)

    print(module)

    return None
