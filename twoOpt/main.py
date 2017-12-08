import _twoOpt
import numpy as np
import timeit
import sys
if __name__ == '__main__':
    ARRAY_SIZE = 4
    c = np.array( [ i for i in range(ARRAY_SIZE) ], dtype=np.int32)
    x = np.array( [ 0, 4, 4, 0 ], dtype=np.int32 )
    y = np.array( [ 0, 4, 0, 4 ], dtype=np.int32 )

    t1 = timeit.default_timer()
    dist = _twoOpt.twoOpt(c, x, y, ARRAY_SIZE)
    t2 = timeit.default_timer()
    time = t2 - t1

    print("C-extension: ")
    print("dist " + str(dist))
    print("TIME: " + str(time))
    sys.exit()
