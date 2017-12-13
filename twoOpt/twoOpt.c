#include "twoOpt.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Takes parallel arrrays of a route. Each city only once
// Input: an array of int city id's,
//        an array of int city x
//        an array of int city y
//        an integer for length of the arrays
// Output: Returns total route distance (Each leg of the trip is
//        rounded to nearest integer)
//        Updated arguments parallel arrays of a shorter route
long int twoOpt( int *c, int *x, int *y, int num ) {
  // init 2D Array for distance squared. init to -1
  int i,j,k;
  long int **m;
  m = (long int **) malloc(sizeof(long int *) * num);
  for (k = 0; k < num; k++) {
      m[k] = (long int *) malloc(sizeof(long int) * num);
      for (i = 0; i < num; i++) {
        m[k][i] = -1;
      }
  }
  for (i = 0; i < num; i++) {
    for (j = i; j < num; j++) {
      if (c[i] == c[j]) {       // If same city, set to INFINITY
        m[i][j] = INFINITY;
      }
      else {           // Save distance squared between the two different cities
        m[c[i]][c[j]] = dist_sqd( x[i], y[i], x[j], y[j] );
        m[c[j]][c[i]] = m[c[i]][c[j]];
      }
    }
  }

  // optimize traverse city ID array (aka route)
  long int change = -1;
  int maxIterations = 5000;
  int iterations = 0;
  // while ( (change < 0) && ( iterations < maxIterations)) {
  while (change < 0) {
    int i;
    for (i = 1; i < num - 2; i++ ) {
      iterations++;
      // int flag = 0;
      for (j = i+1; j < num - 1; j++ ) {
        // printf("here1");
        // Add distance of i-1 to i with j to j+1
        long int curSum = m[c[i-1]][c[i]] + m[c[j]][c[j+1]];
        // Add distance of i-1 to j with i to j+1
        long int newSum = m[c[i-1]][c[j]] + m[c[i]][c[j+1]];
        // Calculate change. If negative change, keep new version via a swap
        change = newSum - curSum;
        if (change < 0) {
          twoOptSwap( c, x, y, num, i, j);
          break;
        }
      }
      if (change < 0) {
        break;
      }
      else {
        continue;
      }
    }
  }

  // Calculate Distance with Matrix already made
  long int totalDist = 0;
  for (i = 0; i < num-1; i++ ) {
    // printf("%d to %d: %ld\n", c[i], c[i+1], m[ c[i] ] [c[i+1]]);
    long int dist = m[ c[i] ] [c[i+1]];
    // printf("%ld\n", dist);
    totalDist += ( long int )round( sqrt( (double) m[ c[i] ] [c[i+1]] ) );
  }
  // printf("%d to %d: %ld\n", c[num-1], c[0], m[ c[0] ] [c[num-1]]);
  long int dist =  m[ c[0] ][ c[num-1] ];
  // printf("%ld\n", dist);
  totalDist += ( long int )round( sqrt( (double) m[ c[0] ][ c[num-1] ] ) );
  // printf("%d\n", totalDist);
  for (i = 0; i < num-1; i++ ) {
    // printf("%d\n", c[i]);
    // printf("%d (%d,%d) to %d (%d,%d): %ld\n", c[i], x[i], y[i], c[i+1], x[i+1], y[i+1],( long int )round( sqrt( (double) m[ c[i] ] [c[i+1]] ) ));
  }
  // printf("%d to %d: %ld\n", c[num-1], c[0], ( long int )round( sqrt( (double) m[ c[0] ][ c[num-1] ] ) ));

  // Free 2D Matrix
  for (k = 0; k < num; k++) {
    free(m[k]);
    m[k] = NULL;
  }
  free(m);
  return totalDist;
}

// Euclidean Distance Squared between (x,y) of two cities
// e.g.  (x1,y1) and (x2,y2). returns: (x1-x2)^2 + (y1-y2)^2
long int dist_sqd( int x1, int y1, int x2, int y2) {
  return (long int)( ( x1 - x2 )*( x1 - x2 ) + ( y1 - y2 )*( y1 - y2 ) );
}

// c: City id
// x: city x coordinate
// y: city y coordinate
// i and j: indices to complete 2-OPT swap
void twoOptSwap( int* c, int* x, int* y, int n, int i, int j) {
  // Swap in place from i to j... inclusive
  int s = i;
  int t = j;
  int tmp;
  while (s < t) {
    // Swap City ID
    tmp = c[s];
    c[s] = c[t];
    c[t] = tmp;

    // Swap City X
    tmp = x[s];
    x[s] = x[t];
    x[t] = tmp;

    // Swap City X
    tmp = y[s];
    y[s] = y[t];
    y[t] = tmp;

    // Increment
    s += 1;
    t -= 1;
  }
}

// int main(int argc, char ** argv) {
//   int n = 4;
//   int c[n];
//   int x[4] = {0,4,4,0};
//   int y[4] = {0,4,0,4};
//   int i, j;
//
//   // Init city data
//   for ( i = 0; i < n; i++ ) {
//     c[i] = i;
//     // x[i] = i*3;
//     // y[i] = i*4;
//   }
//
//   // fix
//   // for (i = 0; i < n; i++) {
//   //   printf("%d ",c[i]);
//   // }
//   // printf("\n");
//   // long int d = twoOpt(c, x, y, n);
//   // for (i = 0; i < n; i++) {
//   //   printf("%d ",c[i]);
//   // }
//   long int d = twoOpt(c, x, y, n);
//   printf("Distance: %ld\n",d);
//   return 0;
// }
