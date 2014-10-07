Hey Dan,


It was a ton of fun working with you this weekend we should do it again somtime.

Here is the final working copy of the clojure code.

Everything that is important is in the file:
```
gen.clj
```

The way I was running this was by calling 
```
lein repl
```
from within the clojure_hacks/spike/ directory

From there I issued these three commands
```
(use 'overtone.core)
(boot-external-server)
(load-file "./src/spike/gen.clj")
(run-it)
```
As I side note, on linux I had to set up jack first for this to work.
The invocation is as follows

```
jackd -r -d alsa -r 44100
```
