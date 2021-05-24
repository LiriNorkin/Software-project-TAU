static double calculate_difference(double **current_clusters, double* vector, int cluster, int d);
static int check_min_cluster(double **current_clusters, double *vector, int k, int d);
static PyObject* connect(PyObject *self, PyObject *args);
int calc(int k, int N, int d, int MAX_ITER, int* first, double** obs);
PyMODINIT_FUNC PyInit_mykmeanssp(void);