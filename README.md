# simple-shapely-simplify-alternative

Most of the time the `simplify()` method in shapely gets rid of points that the user deems may be unnecessary. Sometimes it is unable to and I've found myself in a heuristic battle playing with the tolerance values to get the right result.

More specifically I may come across a polygon that is represented by more coordinates than necessary. Typically we only need the vertices to represent an 'obvious' polygono but sometimes there will be points along, and collinear, with the edges between vertices and `simplify()` fails to remove them.

Here I look at a simple method that uses simple trigonometry to look at the interior angles to eliminate these pesky points
