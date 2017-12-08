// http://dfm.io/posts/python-c-extensions/
// http://scipy-cookbook.readthedocs.io/items/C_Extensions_NumPy_arrays.html
#include <Python.h>
#include <numpy/arrayobject.h>
#include "twoOpt.h"

// To compile this 2.7 script run:
//    python setup.py build_ext -i
//
//  C header:
//    long int twoOpt( int *c, int *x, int *y, int num )
//
// In calling python script:
//    import _twoOpt
//    value = _twoOpt.twoOpt(c, x, y, n)
//            c: city ID parallel array
//            x: city x parallel array
//            y: city y parallel array
//            n: number of cities in arrays


/* Doc String*/
static char module_docstring[] =
    "This module provides an interface for performing a 2-Opt Swap for TSP.";
static char twoOpt_docstring[] =
    "Calculate a 2-Opt Swap improvement on a valid TSP route";

/* Python Function Header */
static PyObject * twoOpt_twoOpt( PyObject * self, PyObject * args );

/* Module Spec & Init Module */
static PyMethodDef module_methods[] = {
  {"twoOpt", twoOpt_twoOpt, METH_VARARGS, twoOpt_docstring },
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_twoOpt(void) {
  PyObject *m = Py_InitModule3("_twoOpt", module_methods, module_docstring);
  if (m == NULL) {
    return;
  }
  /* Add functionality if needed (such as any numpy imports) */
  import_array();
}



/*
 * twoOpt function wrapper
 */
static PyObject *twoOpt_twoOpt( PyObject * self, PyObject * args ) {
  PyArrayObject *c_obj, *x_obj, *y_obj;
  long n;
  
  /* Parse input tuple as 3 arrays and 1 int, return NULL on failure */
  if (!PyArg_ParseTuple(args, "O!O!O!l", &PyArray_Type, &c_obj, &PyArray_Type, &x_obj, &PyArray_Type, &y_obj, &n)) {
    return NULL;
  }

  /* Interpret arrays as numpy arrays */
  PyObject *c_array = PyArray_FROM_OTF( c_obj, NPY_INT, NPY_IN_ARRAY);
  PyObject *x_array = PyArray_FROM_OTF( x_obj, NPY_INT, NPY_IN_ARRAY);
  PyObject *y_array = PyArray_FROM_OTF( y_obj, NPY_INT, NPY_IN_ARRAY);

  /* Test that Arrays were created correctly */
  if (c_array == NULL || x_array == NULL || y_array == NULL) {
      Py_XDECREF(c_array);
      Py_XDECREF(x_array);
      Py_XDECREF(y_array);
      return NULL;
  }

  // /* How many data points are there? */
  // int N = (int)PyArray_DIM(x_array, 0);

  /* Get pointers to the data as C-types. */
  int *c = (int*)PyArray_DATA(c_array);
  int *x = (int*)PyArray_DATA(x_array);
  int *y = (int*)PyArray_DATA(y_array);

  /* Call C function to compute route distance */
  long int dist = twoOpt(c, x, y, n);

  /* Clean up. */
  Py_DECREF(c_array);
  Py_DECREF(x_array);
  Py_DECREF(y_array);

  /* Validate result */
  if (dist < 0) {
    PyErr_SetString(PyExc_RuntimeError, "dist returned impossible value.");
    return NULL;
  }

  /* Make result a Python Object */
  PyObject *ret = Py_BuildValue("l", dist);
  return ret;
}
