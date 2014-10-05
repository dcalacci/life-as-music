(ns spike.core)
(use 'overtone.core)
(boot-external-server)

(require '[overtone.core])

(definst foo [] (saw 220))

(foo)
