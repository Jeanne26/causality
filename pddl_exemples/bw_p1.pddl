(define (problem bw-simple)
  (:domain bw)
  (:objects a b )
  (:init (clear a) (arm-empty) (on a b) (on-table b))
;   restriction des états terminaux 
  (:goal (and (on-table a) (clear b) (not (clear a)))))