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
              (saw freq)
              vol))

;;; CONVENIENCE METHOD
(defn saw2 [music-note]
  (saw-wave (midi->hz (note music-note))))


;;; Hi-level algorithm
;; get bpm
;; choose harmony
;; create melodies
;; bit of random

(def BPM test-bpm)
(def sn-array test-sn)
(def sp-array test-sp)
(def fr-array test-fr)
(def jbst-array test-jbst)
(def jbsl-array test-jbsl)

; create a metronome
(defonce metro (metronome BPM))
(metro)

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
  (at (metro (+ 0.5 beat)) (h))
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
      {:major max-sent-val, :minor remainder, :major7 remainder, :sus4 remainder, :minor7 remainder} 
      {:minor max-sent-val, :major remainder, :minor7 remainder, :sus4 remainder, :major7 remainder}))) 

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

(def play-chord (get-play-chord saw2))

(defn harmony [m beat-num cars]
    (at (m (+ 0 beat-num)) (play-chord (first cars)))
    (apply-at (m (+ 1  beat-num)) harmony m (+ 1 beat-num) (rotate 1 cars) []))

(harmony metro (metro) chord-funcs)

;;;;;;;;;;;;;;; MELODY ;;;;;;;;;;;;;;;;;

;;; get all the notes
(def notes (vec (map (comp midi->hz note) (map find-note-name (range 24 72)))))

;;; choose 24 random notes
(def notes-selection (choose-n 24 notes))

;; call on (cycle notes)
(defn melody [m nm notes]
  (at (m nm)
      (saw-wave (first notes)))
  (apply-at (m (inc nm)) melody m (inc nm) (next notes) []))

(defn run-it []
 (do
  (harmony metro (metro) chord-funcs)
  (melody metro (metro) (cycle notes))
  (drums (metro) kick c-hat c-hat)
 )
)



