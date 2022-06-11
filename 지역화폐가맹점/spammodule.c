#include <python.h>

static PyObject *

spam_count(PyObject* self, PyObject* n)
{
	char* str1;

	if (!PyArg_ParseTuple(n, "s", &str1))
		return NULL;
	char *str2 = "were searched";

	strcat(str1, str2);

	return Py_BuildValue("s", str1);
}

static PyMethodDef SpamMethods[] = {

	{"count", spam_count, METH_VARARGS, "count"},
	{NULL, NULL, 0, NULL}
};

static PyModuleDef spammodule = { 
	PyModuleDef_HEAD_INIT, 
	"spam", 
	"It is a test module.",
	-1, SpamMethods 
};

PyMODINIT_FUNC PyInit_spam(void) {
	return PyModule_Create(&spammodule); 
}