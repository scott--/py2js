
// These hacks are required to use external arrays (i.e. arrays not defined in python)
Array.prototype.__getitem__=function(i) { return this[i]; }
Array.prototype.__setitem__=function(i, val) { this[i] = val; }

// these hacks are required for using image data (canvas.getContext("2d").createImage)
Uint8ClampedArray.prototype.__getitem__=function(i) { return this[i]; }
Uint8ClampedArray.prototype.__setitem__=function(i, val) { this[i] = val; }
