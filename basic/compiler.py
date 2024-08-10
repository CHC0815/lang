from llvmlite import binding, ir

from basic.error import Error
from basic.lexer import Lexer
from basic.parser import Parser


def create_execution_engine():
    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = binding.parse_assembly("")
    engine = binding.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    # Create a LLVM module object from the IR
    mod = binding.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod


def compile_lang(fn: str, text: str, emit_ir: bool = False) -> Error | None:
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

    if emit_ir:
        print(module)

    # Initialize the LLVM JIT
    binding.initialize()
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    # compile
    engine = create_execution_engine()
    mod = compile_ir(engine, str(module))
    pass_manager = binding.PassManagerBuilder()
    pass_manager.opt_level = 3
    pm = binding.ModulePassManager()
    pass_manager.populate(pm)
    pm.run(mod)

    engine.finalize_object()

    func_ptr = engine.get_function_address("add")
    import ctypes

    cfunc = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_int32)(func_ptr)

    result = cfunc(1, 2)
    print(result)

    return None
