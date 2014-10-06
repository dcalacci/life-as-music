(ns spike.core)

(use '[overtone.core])
(boot-server)
(require '[spike.gen])

(refer 'spike.gen)



(defn -main
  [& args]
  (run-it))
