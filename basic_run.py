from basic import values
from basic.lexer import *
from basic.parser import *
from basic.interpreter import *
from basic.context import *
from basic.symboltable import *
from basic.values import *

#############################################################
# RUN
#############################################################

# init global_symbol_table
global_symbol_table = SymbolTable()

# built-in values
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)
global_symbol_table.set("MATH_E", Number.math_E)

# built-in functions
global_symbol_table.set("SIN", BuiltInFunction.sin)
global_symbol_table.set("COS", BuiltInFunction.cos)
global_symbol_table.set("TAN", BuiltInFunction.tan)
global_symbol_table.set("PRINT", BuiltInFunction.print)
global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("CLEAR", BuiltInFunction.clear)
global_symbol_table.set("CLS", BuiltInFunction.clear)
global_symbol_table.set("IS_NUM", BuiltInFunction.is_number)
global_symbol_table.set("IS_STR", BuiltInFunction.is_string)
global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
global_symbol_table.set("IS_FUN", BuiltInFunction.is_function)
global_symbol_table.set("APPEND", BuiltInFunction.append)
global_symbol_table.set("POP", BuiltInFunction.pop)
global_symbol_table.set("EXTEND", BuiltInFunction.extend)
global_symbol_table.set("LEN", BuiltInFunction.len)
global_symbol_table.set("RUN", BuiltInFunction.run)
global_symbol_table.set("IMPORT", BuiltInFunction.import_fun)
global_symbol_table.set("FWRITE", BuiltInFunction.write_to_file)
global_symbol_table.set("FREAD", BuiltInFunction.read_file)
global_symbol_table.set("DELFILE", BuiltInFunction.delete_file)
global_symbol_table.set("RAISE", BuiltInFunction.raise_error)
global_symbol_table.set("STR", BuiltInFunction.str)
global_symbol_table.set("FILE", BuiltInFunction.file)


def run(fn, text, ctx='<program>'):
    # generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # generate AST

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # run program
    interpreter = Interpreter()
    context = Context(ctx)
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
