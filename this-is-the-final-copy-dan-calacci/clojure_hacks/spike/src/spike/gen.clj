(require '[clj-http.client :as client])

(def url "https://gist.githubusercontent.com/anonymous/440e49b70657dc15e2c7/raw/92c77a27ccbb8127acb4434148a969f3398c0c08/hahahaha")
; (def url "https://gist.githubusercontent.com/dcalacci/88dee1cef6b5ff51206d/raw/6a6f4346ef07f8a0fc34931528492e6ef663605e/example%20data")

(def response (client/get url {:as :json}))

(def fr-array
  (:attention (:body response)))

(def BPM 
  (int (:bpm (:body response))))

(def jbst-array
  (:jb_distances (:body response)))
  
(def sn-array
  (:neg (:sentiment (:body response))))

(def sp-array
  (:pos (:sentiment (:body response))))

(defn average [coll] 
    (/ (reduce + coll) (count coll)))

;;; BPM of song
;; single integer value 80 - 240
(def test-bpm 120)
;;; Positive sentiments
;; array of size |tweets| between 0-1 
(def test-sp [0,0,0,0,0,0.9234,0.1234,0,0])
;;; Negative sentiments
;; array of size |tweets| between 0-1
(def test-sn [0,0,0,0,0,0.9234,0.1234,0,0])
;;; Favourite and Retweet
;; array of size |tweets| between 0-1
(def test-fr [0,0,0,0,0,0.9999,0.2424,0,0])
;;; Jawbone Step Data
;; normalized variable array of 0-1
(def test-jbst [0,0,0.1,0,0.2,0.51,0.231,0,0.1])
;;; Jawbone Sleep data
;; normalized variable array of 0-1
(def test-jbsl [0.2,0.1,0.5,0.2,0.1,0.41,0.123,0.4,0.1])


;;;; TEST SYNTH
(definst saw-wave [freq 440 attack 0.01 sustain 0.4 release 0.1 vol 0.4]
  (* (env-gen (env-lin attack sustain release) 1 1 0 1 FREE)
              (pulse freq)
              vol))

(definst sine-wave [freq 440 attack 0.01 sustain 0.4 release 0.1 vol 0.4]
  (* (env-gen (env-lin attack sustain release) 1 1 0 1 FREE)
              (f-sin-osc freq)
              vol))

(definst blip-wave [freq 440 attack 0.01 sustain 0.4 release 0.1 vol 0.4]
  (* (env-gen (env-lin attack sustain release) 1 1 0 1 FREE)
              (blip freq)
              vol))

;;; CONVENIENCE METHOD
(defn saw2 [music-note]
  (saw-wave (midi->hz (note music-note))))

(defn sin2 [music-note]
  (sine-wave (midi->hz (note music-note))))

;;; Hi-level algorithm
;; get bpm
;; choose harmony
;; create melodies
;; bit of random

;(def BPM test-bpm)
;(def sn-array test-sn)
;(def sp-array test-sp)
;(def fr-array test-fr)
;(def jbst-array test-jbst)
;(def jbsl-array test-jbsl)

; create a metronome
(defonce metro (metronome 120))

;;;;;;;;;;;;;;;; RHYTHM ;;;;;;;;;;;;;;;;;;;;

;; kick
(definst kick [freq 120 dur 0.3 width 0.5]
    (let [freq-env (* freq (env-gen (perc 0 (* 0.99 dur))))
                  env (env-gen (perc 0.01 dur) 1 1 0 1 FREE)
                          sqr (* (env-gen (perc 0 0.01)) (pulse (* 2 freq) width))
                                  src (sin-osc freq-env)
                                          drum (+ sqr (* env src))]
          (compander drum drum 0.2 1 0.1 0.01 0.01)))

;; hats
(definst c-hat [amp 0.8 t 0.04]
  (let [env (env-gen (perc 0.001 t) 1 1 0 1 FREE)
        noise (white-noise)
        sqr (* (env-gen (perc 0.01 0.04)) (pulse 880 0.2))
        filt (bpf (+ sqr noise) 9000 0.5)]
    (* amp env filt)))

;; DRUM FUNCTION
(defn drums [beat k h s]
  (at (metro beat) (k))
  (at (metro (+ (average jbst-array) beat)) (h))
  (apply-by (metro (inc beat)) drums (inc beat) k h s []))

;;;;;;;;;;;;;;;; HARMONY ;;;;;;;;;;;;;;;;

; sum sentiments
(def sum-p (reduce + sp-array))
(def sum-n (reduce + sn-array))
; is positive
(def is-pos (> sum-p sum-n))
; get the maximum sentiment value
(def max-sent-val 
  (if is-pos
    (apply max sp-array)
    (apply max sn-array)))
; get sent level
(def sent-level
  (cond
    (< max-sent-val 0.51) 1
    (< max-sent-val 0.76) 2
    :else 3))
; set of chords to choose from
(def chord-arr
  [:C3, :D3, :E3, :F3, :G3, :A3, :B3,
   :Db3, :Eb3, :Gb3, :Ab3, :Bb3,
   :Db4, :Eb4, :Gb4, :Ab4, :Bb4,
   :C4, :D4, :E4, :F4, :G4, :A4, :B4])

; probability function for chord progression
(def chord-type-arr
  (let [remainder (/ (- 1 max-sent-val) 4)]
    (if is-pos
      {:major max-sent-val, :minor remainder, :major7 remainder, :major6 remainder, :minor7 remainder} 
      {:minor max-sent-val, :major remainder, :minor7 remainder, :minor6 remainder, :major7 remainder}))) 

; arbitray number of chords
(def num-chords (choose [4,6,8,12]))

; select some random chord tones
(def chord-tones (choose-n num-chords chord-arr))

; select the weighted random chord types
(defn get-chord-type [x]
 (weighted-choose chord-type-arr))

; a dummy array to be popluated
(def dummy-arr 
  (into [] (range (count chord-tones))))

; the array of chord types 
(def chord-vals
  (map get-chord-type dummy-arr))

; a function to generate chord functions
(defn get-chord [c ctype]
  (chord c ctype))

; the array of chord functions
(def chord-funcs
  (map get-chord chord-tones chord-vals))

; returns a function that plays a-chord in a-synth
(defn get-play-chord [a-synth]
  (fn [a-chord]
    (doseq [note a-chord] (a-synth note))))

(def play-chord (get-play-chord sin2))
(def play-chord1 (get-play-chord sin2))
(def play-chord2 (get-play-chord saw2))

(def chord-dist 
  (min 8 (max 1 (int (* 10 (average jbst-array))))))

(defn harmony [m beat-num cars cd]
    (let [ c 
          (if (= (mod beat-num 2) 0)
            (cons (first (rest cars)) (reverse cars))
            cars)]
    (at (m (+ 0 beat-num)) (play-chord (first c)))
    (apply-at (m (+ cd  beat-num)) harmony m (+ cd beat-num) (rotate 1 cars) cd [])))

;;;;;;;;;;;;;;; MELODY ;;;;;;;;;;;;;;;;;

;;; get all the notes
(def notes (vec (map (comp midi->hz note) (map find-note-name (range 24 72)))))

;;; choose 24 random notes
; (def notes-selection (choose-n 24 notes))
(def notes-selection (shuffle (into (choose-n chord-dist (scale (first chord-tones) (if is-pos :major :minor)))
                                    (choose-n chord-dist (scale (first chord-tones) (if is-pos :major :minor))))))

(def note-time (min 0.5 (average jbst-array)))

;; call on (cycle notes)
(defn melody [m nm nts]
  (at (m nm)
      (sine-wave (first nts)))
  (apply-at (m (+ note-time nm)) melody m (+ note-time nm) (next nts) []))

(metro)
(defn run-it []
 (do
  (harmony metro (metro) chord-funcs 0.5)
  (melody metro (metro) (cycle notes-selection))
  (drums (metro) kick c-hat c-hat)
 )
)

