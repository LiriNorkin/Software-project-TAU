#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "kmeans.h"

/*
This function is used to calculate and return the distance between two vectors:
the cluster in current_clusters[cluster] and the given vector
*/
static double calculate_difference(double **current_clusters, double* vector, int cluster, int d){
    double sum = 0;
    int j;
    for (j = 0; j<d; j++){
        sum += ((vector[j] - current_clusters[cluster][j])*(vector[j] - current_clusters[cluster][j]));
    }
    return sum;
}

/*
This function is used to find and return the closest cluster to the given vector
*/
static int check_min_cluster(double **current_clusters, double *vector, int k, int d){
    int i;
    int cluster;
    double new_dist;
    double dist;
    i = 0;
    dist = calculate_difference(current_clusters, vector, i, d);
    for (cluster = 1; cluster<k; cluster++){
        new_dist = calculate_difference(current_clusters, vector, cluster, d);
        if (new_dist<dist){
            i = cluster;
            dist = new_dist;
        }
    }
    return i;
}

/*
This function is used to calculate the Kmeans algoritem of the given Data-
N observations of d dimensions stored in obs,
devided to k clusters from the k initial clusters stored in first,
while preforming at most MAX_ITER iterations.
It stores the results to clusters.txt
*/
int calc(int k, int N, int d, int MAX_ITER, int* first, double** obs){
    int i;
    int j;
    int counter;
    int centroid;
    int prev;
    int change;
    int cluster;
    double new_val;
    int *counts;
    double *p2;
    double **sums;
    int *members;
    double *p3;
    double **current_clusters;
    FILE *f;
    char **strs;
    char *p4;
    char *istr;

    /*    Initial all the arrays in memory    */
    counts = calloc(k, sizeof(int));
    if(counts == NULL){
      printf("Error! Problem with calloc");
      exit(1);
    }

    p2 = calloc(k*d, sizeof(double));
    sums = calloc(k, sizeof(double*));
    if(p2 == NULL || sums == NULL){
      printf("Error! Problem with calloc");
      exit(1);
    }
    for (i = 0; i<k; i++){
        sums[i] = p2 + i*d;
    }

    members = calloc(N, sizeof(int));
    if(members == NULL){
      printf("Error! Problem with calloc");
      exit(1);
    }

    p3 = calloc(k*d, sizeof(double));
    current_clusters = calloc(k, sizeof(double*));
    if(p3 == NULL || current_clusters == NULL){
      printf("Error! Problem with calloc");
      exit(1);
    }
    for (i = 0; i<k; i++){
        current_clusters[i] = p3 + i*d;
    }

    p4 = calloc(k*(12*N+1), sizeof(char));
    strs = calloc(k, sizeof(char*));
    if(p4 == NULL || strs == NULL){
      printf("Error! Problem with calloc");
      exit(1);
    }
    for(i = 0; i < k; i++) {
        strs[i] = p4 + i*(12*N+1);
        strcpy(strs[i], "");
    }

    istr = calloc(100, sizeof(char));

    /*    Initial members    */
    for(i = 0; i<N; i++){
        members[i] = k;
    }

    /*    Initial k first clusters    */
    for(i = 0; i < k; i++) {
        for(j = 0; j < d; j++) {
            sums[i][j] = obs[first[i]][j];
            current_clusters[i][j] = obs[first[i]][j];
        }
        counts[i] = 1;
        members[first[i]] = i;
    }

    /*    The Kmeans algorithem    */
    for(counter = 0; counter < MAX_ITER; counter++){
        change = 1;
        for(i = 0; i < N; i++){
            centroid = check_min_cluster(current_clusters, obs[i], k, d);
            prev = members[i];
            if(prev != centroid){
                for(j = 0; j < d; j++){
                    if (prev != k){
                        sums[prev][j] -= obs[i][j];
                    }
                    sums[centroid][j] += obs[i][j];
                }
                if (prev != k){
                    counts[prev] -= 1;
                }
                counts[centroid] += 1;
                members[i] = centroid;
            }
        }
        for(cluster = 0; cluster < k; cluster++){
            for(j = 0; j<d; j++){
                new_val = sums[cluster][j]/counts[cluster];
                if (current_clusters[cluster][j] != new_val){
                    change = 0;
                }
                current_clusters[cluster][j] = new_val;
            }
        }

        /*        If no change happened, finish the run        */
        if(change){
            break;
        }
    }

    /*    Divide the observations to the relevant cluster and prepare for print    */
    for(i = 0; i < N; i++) {
        cluster = members[i];
        sprintf(istr, "%d", i);
        if(strlen(strs[cluster]) == 0){
            strcat(strs[cluster], istr);
        }
        else{
            strcat(strs[cluster], ",");
            strcat(strs[cluster], istr);
        }
    }

    /*    Print the results in clusters.txt    */
    f = fopen("clusters.txt", "a");
    if(f == NULL){
      printf("Error! Can't open clusters.txt");
      exit(1);
    }

    for(i = 0; i < k; i++) {
        fprintf(f, "%s","\n");
        fprintf(f, "%s",strs[i]);
    }
    fclose(f);

    /*    Free all of memory    */
    free(strs);
    free(counts);
    free(sums);
    free(members);
    free(current_clusters);
    free(p2);
    free(p3);
    free(p4);
    free(istr);
    return 0;
}

/*
This function is used to connect between the Python code calling this extension and this file.
It is used to transfer and translate all relevant data to c types, and send it to the connect
function in order to preform the Kmeans algorithem.
*/
static PyObject* connect(PyObject *self, PyObject *args){
    int k;
    int N;
    int d;
    int MAX_ITER;
    int* first_c;
    double** obs_c;
    double* p1;
    PyObject *first_p;
    PyObject *obs_p;
    PyObject *all;
    PyObject *item;
    int i;
    int j;

    /*    transalte given arguments by the python code    */
    if(!PyArg_ParseTuple(args, "O:c function getting arguments", &all)) {
        printf("Error in c extension");
        return NULL;
    }
    if (!PyList_Check(all)){
        printf("Error in c extension");
        return NULL;
    }
    k = (int)PyLong_AsLong(PyList_GetItem(all, 0));
    N = (int)PyLong_AsLong(PyList_GetItem(all, 1));
    d = (int)PyLong_AsLong(PyList_GetItem(all, 2));
    MAX_ITER = (int)PyLong_AsLong(PyList_GetItem(all, 3));
    first_p = PyList_GetItem(all, 4);
    obs_p = PyList_GetItem(all, 5);
    if (!PyList_Check(first_p)){
        printf("Error in c extension");
        return NULL;
    }
    first_c = calloc(k, sizeof(int));
    if(first_c == NULL){
      printf("Error! Problem with calloc");
      exit(1);
    }
    for (i = 0; i<k; i++){
        first_c[i] = (int)PyLong_AsLong(PyList_GetItem(first_p, i));
    }

    if (!PyList_Check(obs_p)){
        printf("Error in c extension");
        return NULL;
    }

    p1 = calloc(N*d, sizeof(double));
    obs_c = calloc(N, sizeof(double*));
    if(p1 == NULL || obs_c == NULL){
      printf("Error! Problem with calloc");
      exit(1);
    }
    for (i = 0; i<N; i++){
        obs_c[i] = p1 + i*d;
    }

    for (i = 0; i<N; i++){
        item = PyList_GetItem(obs_p, i);
        if (!PyList_Check(item)){
            printf("Error in c extension");
            return NULL;
        }
        for (j = 0; j<d; j++){
            obs_c[i][j] = PyFloat_AsDouble(PyList_GetItem(item, j));
        }
    }

    calc(k, N, d, MAX_ITER, first_c, obs_c);
    free(first_c);
    free(obs_c);
    free(p1);
    Py_RETURN_NONE;
}

static PyMethodDef capiMethods[] = {
    {"connect",                   /* the Python method name that will be used */
      (PyCFunction) connect, /* the C-function that implements the Python function and returns static PyObject*  */
      METH_VARARGS,           /* flags indicating parametersaccepted for this function */
      PyDoc_STR("kmeans calculator")}, /*  The docstring for the function */
    {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all
                                 of the functions for the module have been defined. */
};

/* This initiates the module using the above definitions. */
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    capiMethods /* the PyMethodDef array from before containing the methods of the extension */
};

PyMODINIT_FUNC PyInit_mykmeanssp(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}


