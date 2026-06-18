(define (domain poison)

  (:requirements :strips :negative-preconditions :disjunctive-preconditions)

  (:predicates
    (ok ?v)
    (emp ?v)
    (anti ?v)
    (vide ?v)
    (mort ?v)
    (vivant ?v)
    (final ?v)
  )
  (:action boire_vo
    :parameters (?v)
    :precondition   (or 
                      (and (ok ?v) (not (emp ?v)) (not (anti ?v)) (not (vide ?v)) (not (mort ?v)) (not (vivant ?v)) (not (final ?v)))
                      
                      )

    :effect (and (not (ok ?v))
                 (vivant ?v) (final ?v))
  )

  (:action emp_vo
    :parameters (?v)
    :precondition   (and (ok ?v) (not (emp ?v)) (not (anti ?v)) (not (vide ?v)) (not (mort ?v)) (not (vivant ?v)) (not (final ?v)))
    :effect (and
              (not (ok ?v))
              (emp ?v))
  )

  (:action vider_vo
    :parameters (?v)
    :precondition   (and (ok ?v) (not (emp ?v)) (not (anti ?v)) (not (vide ?v)) (not (mort ?v)) (not (vivant ?v)) (not (final ?v)))
    :effect (and
              (not (ok ?v))
              (vide ?v))
  )

  (:action anti_ve
    :parameters (?v)
    :precondition   (and (not (ok ?v)) (emp ?v) (not (anti ?v)) (not (vide ?v)) (not (mort ?v)) (not (vivant ?v)) (not (final ?v)))

    :effect (and
              (not (emp ?v))
              (anti ?v))
  )

  (:action boire_ve
    :parameters (?v)
    :precondition   (and (not (ok ?v)) (emp ?v) (not (anti ?v)) (not (vide ?v)) (not (mort ?v)) (not (vivant ?v)) (not (final ?v)))

    :effect (and (not(emp ?v)) (mort ?v) (final ?v))
  )

  (:action vider_ve
    :parameters (?v)
    :precondition   (and (not (ok ?v)) (emp ?v) (not (anti ?v)) (not (vide ?v)) (not (mort ?v)) (not (vivant ?v)) (not (final ?v)))
    :effect (and (not (emp ?v)) (vide ?v))
  )

  (:action rien_VV
    :parameters (?v)
    :precondition   (and (not (ok ?v)) (not (emp ?v)) (not (anti ?v)) (vide ?v) (not (mort ?v)) (not (vivant ?v)) (not (final ?v)))

    :effect (and (not (vide ?v)) (mort ?v)(final ?v))
  )

  (:action boire_va
    :parameters (?v)
    :precondition   (and (not (ok ?v)) (not (emp ?v)) (anti ?v) (not (vide ?v)) (not (mort ?v)) (not (vivant ?v)) (not (final ?v)))

    :effect (and (not (anti ?v)) (vivant ?v) (final ?v))
  )

)