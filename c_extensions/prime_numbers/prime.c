/*
Quite important: Need to keep reference counts for booleans/null too, otherwise it works but randomly crashes
if function is called >30 times (probably due to bad dereferences).
*/

#include <Python.h>
#include <math.h>

static PyObject * is_prime(PyObject * self, PyObject * args){
    int number, i = 2;

    if(!PyArg_ParseTuple(args, "K", &number)){
        Py_INCREF(Py_None);
        return NULL;
    }

    if (number < 2){
        Py_INCREF(Py_False);
        return Py_False;
    }

    for (;i < sqrt(number) + 1; i++){
        if (number % i == 0){
            Py_INCREF(Py_False);
            return Py_False;
        }
    }
    Py_INCREF(Py_True);
    return Py_True;
};

static PyMethodDef PrimeMethods[] = {
    {"is_prime", is_prime, METH_VARARGS, "Python3 interface for the prime C library function"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef is_prime_module = {
    PyModuleDef_HEAD_INIT,
    "primes",
    "Python3 interface for the prime C library function",
    -1,
    PrimeMethods
};

PyMODINIT_FUNC PyInit_is_prime(void) {
    return PyModule_Create(&is_prime_module);
};
