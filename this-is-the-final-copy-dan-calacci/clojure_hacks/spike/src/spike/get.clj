(require '[clj-http.client :as client])

(def response (client/get "http://gist.githubusercontent.com/dcalacci/88dee1cef6b5ff51206d/raw/a7f920a78d785be5f36424ce89972569bbcf69e2/example%20data" {:as :json}))

(def attention
  (:attention (:body response)))

(def bpm
  (:bpm (:body response)))

(def jb_distances
  (:jb_distances (:body response)))
  
(def sn-array
  (:neg (:sentiment (:body response))))

(def sp-array
  (:pos (:sentiment (:body response))))
