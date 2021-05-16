from wasmer import engine, Store, Module, Instance, ImportObject, Function, FunctionType, Type
from wasmer_compiler_cranelift import Compiler

store = Store(engine.JIT(Compiler))

import_object = ImportObject()


def sum(x: int):
    exit(x)


sum_host_function = Function(store, sum)

# See how we have used Python annotations to help `wasmer` to infer
# the types of the host function? Well, it could be limited. For
# example, `int` in Python matches to `i32` in WebAssembly. We can't
# represent `i64`. Or… we can use a function type.
# def sum(x, y):
#     return x + y

sum_host_function = Function(
    store,
    sum,
    #             x         y           result
    FunctionType([Type.I32], [])
)

import_object.register(
    "wasi_snapshot_preview1",
    {
        "proc_exit": sum_host_function,
    }
)
# Let's define the store, that holds the engine, that holds the compiler.

# Let's compile the module to be able to execute it!
module = Module(store, open('Wasm.wasm', 'rb').read())

# Now the module is compiled, we can instantiate it.
instance = Instance(module, import_object)

# Call the exported `sum` function.
result = instance.exports.encrypt(3, 3)
# 5246480

print(result)  # 42!
