// Takes parallel arrrays of a route. Each city only once
// Input: an array of int city id's,
//        an array of int city x
//        an array of int city y
// Output: Returns total route distance (Each leg of the trip is
//        rounded to nearest integer
//        Updated arguments parallel arrays of a shorter route
long int twoOpt( int *c, int *x, int *y, int num );
long int dist_sqd( int x1, int y1, int x2, int y2);
void twoOptSwap( int* c, int* x, int* y, int n, int i, int j);
