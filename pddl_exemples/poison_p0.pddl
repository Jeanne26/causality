(define (problem poison_p0)
    (:domain poison)
    (:objects
        V)
        
    (:init
        (ok V)
    )

    (:goal (or (vivant V) (mort V)))  
        
)