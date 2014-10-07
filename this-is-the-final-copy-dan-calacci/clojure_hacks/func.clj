(definst sim-saw [] (saw 220))

(definst trem [freq 440 depth 10 rate 6 length 3]
  (* 0.3
    (line:kr 0 1 length FREE)
      (saw (+ freq (* depth (sin-osc:kr rate))))))


;; kick drumb
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

;; metronome
(defonce metro (metronome 120))
(metro)

;; live coding
(defn player [beat]
  (at (metro beat) (kick))
  (at (metro (+ 0.5 beat)) (c-hat))
  (apply-by (metro (inc beat)) #'player (inc beat) []))


;;; loooper
(defn looper [nome sound]    
    (let [beat (nome)]
        (at (nome beat) (sound))
        (apply-by (nome (inc beat)) looper nome sound [])))

;; chord progressions
;; ----------------------------------------------;;;

;; We use a saw-wave that we defined in the oscillators tutorial
(definst saw-wave [freq 440 attack 0.01 sustain 0.4 release 0.1 vol 0.4] 
    (* (env-gen (env-lin attack sustain release) 1 1 0 1 FREE)
            (saw freq)
                 vol))

;; We can play notes using frequency in Hz
;(saw-wave 440)
;(saw-wave 523.25)
;(saw-wave 261.62) ; This is C4

;; We can also play notes using MIDI note values
;(saw-wave (midi->hz 69))
;(saw-wave (midi->hz 72))
;(saw-wave (midi->hz 60)) ; This is C4

;; We can play notes using standard music notes as well
;(saw-wave (midi->hz (note :A4)))
;(saw-wave (midi->hz (note :C5)))
;(saw-wave (midi->hz (note :C4))) ; This is C4! Surprised?

;; Define a function for convenience
(defn note->hz [music-note]
      (midi->hz (note music-note)))

; Slightly less to type 
;(saw-wave (note->hz :C5))

;; Let's make it even easier
(defn saw2 [music-note]
      (saw-wave (midi->hz (note music-note))))

;; Great!
;(saw2 :A4)
;(saw2 :C5)
;(saw2 :C4)

;; Let's play some chords

;; this is one possible implementation of play-chord
(defn play-chord [a-chord]
    (doseq [note a-chord] (saw2 note)))

;; We can play many types of chords.
;(play-chord (chord :C4 :major))

;; We can play a chord progression on the synth
;; using times:
(defn chord-progression-time []
    (let [time (now)]
          (at time (play-chord (chord :C4 :major)))
              (at (+ 2000 time) (play-chord (chord :G3 :major)))
                  (at (+ 3000 time) (play-chord (chord :F3 :sus4)))
                      (at (+ 4300 time) (play-chord (chord :F3 :major)))
                          (at (+ 5000 time) (play-chord (chord :G3 :major)))))

;(chord-progression-time)

;; or beats:
(defn chord-progression-beat [m beat-num]
    (at (m (+ 0 beat-num)) (play-chord (chord :C4 :major)))
      (at (m (+ 4 beat-num)) (play-chord (chord :G3 :major)))
        (at (m (+ 8 beat-num)) (play-chord (chord :A3 :minor)))
          (at (m (+ 14 beat-num)) (play-chord (chord :F3 :major)))  
          )

;(chord-progression-beat metro (metro))

;; We can use recursion to keep playing the chord progression
(defn chord-progression-beat [m beat-num]
    (at (m (+ 0 beat-num)) (play-chord (chord :C4 :major)))
      (at (m (+ 4 beat-num)) (play-chord (chord :G3 :major)))
        (at (m (+ 8 beat-num)) (play-chord (chord :A3 :minor)))
          (at (m (+ 12 beat-num)) (play-chord (chord :F3 :major)))
            (apply-at (m (+ 16 beat-num)) chord-progression-beat m (+ 16 beat-num) [])
            )
;(chord-progression-beat metro (metro))



;;;;; SAVE SONG TO WAV
;(recording-start "./test.wav")
;(demo 0.5 (trem))
;(recording-stop)


