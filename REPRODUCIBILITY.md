# Reproducibility

From the repository root, with Python 3.11 or later and Git:

~~~sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
~~~

The standard-library replay checks 28,125 occupancy and return identities, and exact rank and domain conditions for 14 quadratic grids. It tests 15,563 ordered pairs of state–action reward tables at discount 1/2, and 42 exact sign comparisons across the two illustrated examples. [Expected output](verification/logs/replay.txt)

The replay checks finite cases. The paper proves the general polynomial and facewise sign conditions. [Build the manuscript](paper/BUILD.md) · [Rebuild the figure and open the explorer](visualization/README.md)
