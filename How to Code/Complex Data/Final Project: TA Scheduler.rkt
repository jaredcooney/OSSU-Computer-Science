;; Final Project: Social Network Graph and TA Scheduler
;; How to Code: Complex Data (University of British Columbia)

;; Student: Jared Cooney
;; jaredcooney2@gmail.com

;; Runs in DrRacket (Advanced Student Language)

;; ======================================================================

;; PROBLEM 1:
;; 
;; Consider a social network similar to Twitter called Chirper. Each user has a name, a note about
;; whether or not they are a verified user, and a list of users they are following.
;; 
;; Design a data definition for Chirper, including a template that is tail-recursive and avoids 
;; cycles. 
;; 
;; Then design a function called most-followers that determines which user in a Chirper Network is 
;; followed by the most people.


;; =============================
;; DATA:

(define-struct user (name verified? following))
;; User is (make-user String Boolean (listof User))
;; interp. a social network user account with name, verified status, and a list of followed accounts
(define N0 (make-user "Eiffel" false (list (make-user "Minkowski" true empty))))
(define N1 (shared ([-J- (make-user "Jim" false (list -D-))]
                    [-D- (make-user "Dwight" false (list -J-))])
             -J-))
(define N2 (shared ([-A- (make-user "Aubrey" false (list -D-))]
                    [-D- (make-user "Duck"   false (list -N-))]
                    [-N- (make-user "Ned"    true  (list -A-))])
             -A-))
;;                                                                         ;followers : following
(define N3 (shared ([-S- (make-user "@doc_tam"        true  (list -K-))]          ; 0 : 1
                    [-J- (make-user "@hero_of_canton" false (list -W- -K-))]      ; 1 : 2
                    [-W- (make-user "@Leaf0nTheW1nd"  false (list -Z- -M-))]      ; 4 : 2
                    [-Z- (make-user "@justZoeThings"  true  (list -W-))]          ; 1 : 1
                    [-K- (make-user "@well-versed"    false (list -W-))]          ; 2 : 1
                    [-M- (make-user "@MisbehavingMal" true  (list -J- -W- -R-))]  ; 1 : 3
                    [-R- (make-user "@sp4c3_psych1c"  true  empty)])              ; 1 : 0
             -S-))

;; template elements: mutual recursion encapsulated within local, tail-recursive via worklist,
;;                    context-preserving accumulator to ensure termination with cyclic data
#;
(define (fn-for-network u0)
  ;; to-do is (listof User); a worklist accumulator
  ;; visited is (listof User); a context-preserving accumulator, users fn-for-user has already seen
  (local [(define (fn-for-user u to-do visited)
            (... (user-name u)
                 (user-verified? u)
                 (if (member u visited)
                     (fn-for-lou to-do visited)
                     (fn-for-lou (append (user-following u) to-do)
                                 (cons u visited)))))

          (define (fn-for-lou to-do visited)
            (cond [(empty? to-do) (...)]
                  [else
                   (fn-for-user (first to-do)
                                (rest to-do)
                                visited)]))]

    (fn-for-user u0 empty empty)))


;; =============================
;; FUNCTIONS:

;; User -> String
;; produces the username of the user with the most followers who is reachable in the given network
;; (in the event of a tie, return any user with the maximum number of followers)
;; Assumes: all usernames are unique
(check-expect (most-followers N0) "Minkowski")
(check-expect (most-followers N3) "@Leaf0nTheW1nd")

(define (most-followers u0)
  ;; to-do is (listof User); a worklist accumulator
  ;; visited is (listof String); a context-preserving accumulator, names of visited users
  ;; follow-counts is (listof FC); number of followers for each user so far
  (local [(define-struct fc (user count))
          ;; FC (Follow Count) is (make-fc User Natural)
          ;; interp. a user and their follower count
          
          (define (fn-for-user u to-do visited follow-counts)
            (if (member (user-name u) visited)
                (fn-for-lou to-do visited follow-counts)
                (fn-for-lou (append (user-following u) to-do)
                            (cons (user-name u) visited)
                            (update-follow-counts (user-following u) follow-counts))))

          (define (fn-for-lou to-do visited follow-counts)
            (cond [(empty? to-do) (user-name (choose-highest follow-counts))]
                  [else
                   (fn-for-user (first to-do)
                                (rest to-do)
                                visited
                                follow-counts)]))

          (define (update-follow-counts lou follow-counts)
            (add-new lou (increment-existing lou follow-counts)))
          
          (define (increment-existing lou follow-counts)
            (local [(define lou-names (map user-name
                                           lou))]
              (map (lambda (fc) (if (member (user-name (fc-user fc))
                                            lou-names)
                                    (make-fc (fc-user fc)
                                             (add1 (fc-count fc)))
                                    fc))
                   follow-counts)))

          (define (add-new lou follow-counts)
            (local [(define follow-counts-names (map (lambda (fc) (user-name (fc-user fc)))
                                                     follow-counts))]
              (append (filter (lambda (element) (not (false? element)))
                              (map (lambda (u) (if (member (user-name u) follow-counts-names)
                                                   false
                                                   (make-fc u 1)))
                                   lou))
                      follow-counts)))

          (define (choose-highest follow-counts)
            (fc-user (foldr (lambda (fc1 fc2) (if (> (fc-count fc1)
                                                     (fc-count fc2))
                                                  fc1
                                                  fc2))
                            (first follow-counts)
                            (rest follow-counts))))]

    (fn-for-user u0 empty empty empty)))

;; =======================================================================================

;; PROBLEM 2:
;; 
;; In UBC's version of How to Code, there are often more than 800 students taking 
;; the course in any given semester, meaning there are often over 40 Teaching Assistants. 
;; 
;; Designing a schedule for them by hand is hard work - luckily we've learned enough now to write 
;; a program to do it for us! 
;; 
;; Below are some data definitions for a simplified version of a TA schedule. There are some 
;; number of slots that must be filled, each represented by a natural number. Each TA is 
;; available for some of these slots, and has a maximum number of shifts they can work. 
;; 
;; Design a search program that consumes a list of TAs and a list of Slots, and produces one
;; valid schedule where each Slot is assigned to a TA, and no TA is working more than their 
;; maximum shifts. If no such schedules exist, produce false. 
;;
;; You should supplement the given check-expects and remember to follow the recipe!


;; =============================
;; DATA:

;; Slot is Natural
;; interp. each TA slot has a number, is the same length, and none overlap


(define-struct ta (name max avail))
;; TA is (make-ta String Natural (listof Slot))
;; interp. the TA's name, number of slots they can work, and slots they're available for

(define SOBA  (make-ta "Soba"  2 (list 1 3)))
(define UDON  (make-ta "Udon"  1 (list 3 4)))
(define RAMEN (make-ta "Ramen" 1 (list 2)))

(define ERIKA   (make-ta "Erika"   1 (list 1 3 7 9)))
(define RYAN    (make-ta "Ryan"    1 (list 1 8 10)))
(define REECE   (make-ta "Reece"   1 (list 5 6)))
(define GORDON  (make-ta "Gordon"  2 (list 2 3 9)))
(define DAVID   (make-ta "David"   2 (list 2 8 9)))
(define KATIE   (make-ta "Katie"   1 (list 4 6)))
(define AASHISH (make-ta "Aashish" 2 (list 1 10)))
(define GRANT   (make-ta "Grant"   2 (list 1 11)))
(define RAEANNE (make-ta "Raeanne" 2 (list 1 11 12)))

(define NOODLE-TAs (list SOBA UDON RAMEN))
(define CLASS-TAs (list ERIKA RYAN REECE GORDON DAVID KATIE AASHISH GRANT RAEANNE))


(define-struct assignment (ta slot))
;; Assignment is (make-assignment TA Slot)
;; interp. the TA is assigned to work the slot

;; Schedule is (listof Assignment)
;; interp. a TA shift schedule
(define S0 (list (make-assignment UDON 4)
                 (make-assignment SOBA 3)
                 (make-assignment RAMEN 2)
                 (make-assignment SOBA 1)))


;; =============================
;; FUNCTIONS:

;; (listof TA) (listof Slot) -> Schedule or false
;; produce valid schedule given TAs and Slots; false if impossible
;; Assumes: all TA names are unique
(check-expect (schedule-tas empty empty) empty)
(check-expect (schedule-tas empty (list 1 2)) false)
(check-expect (schedule-tas (list SOBA) empty) empty)
(check-expect (schedule-tas (list SOBA) (list 1)) (list (make-assignment SOBA 1)))
(check-expect (schedule-tas (list SOBA) (list 2)) false)
(check-expect (schedule-tas (list SOBA) (list 1 3)) (list (make-assignment SOBA 3)
                                                          (make-assignment SOBA 1)))

(check-expect (schedule-tas NOODLE-TAs (list 1 2 3 4 5)) false)
(check-expect (not (false? (schedule-tas NOODLE-TAs (list 4 1 3 2)))) true)
(check-expect (schedule-tas NOODLE-TAs (list 1 2 3 4))
              (list (make-assignment UDON 4)
                    (make-assignment SOBA 3)
                    (make-assignment RAMEN 2)
                    (make-assignment SOBA 1)))

(check-expect (schedule-tas CLASS-TAs (list 1 2 3 4 5 6 7 8 9 10 11 12)) false)
(check-expect (not (false? (schedule-tas CLASS-TAs (list 1 2 3 4 6 7 8 9 10 11 12)))) true) ; no 5

;; template elements: generative recursion for arbitrary-arity tree, mutual recursion
;;                    encapsulated within local, tail-recursive with worklist accumulator

(define (schedule-tas tas slots)
  ;; to-do is (listof WLE); a worklist accumulator
  (local [(define-struct wle (schedule remaining-slots))
          ;; WLE (Worklist Entry) is (make-wle Schedule Slot)
          ;; interp. a worklist entry; a schedule and its unfilled slots
                 
          (define (schedule-tas schedule remaining-slots to-do)
            (cond [(valid-schedule? tas schedule)
                   (if (all-slots-filled? slots schedule)
                       schedule
                       (fn-for-losch (append (map (lambda (schedule)
                                                    (make-wle schedule
                                                              (rest remaining-slots)))
                                                  (next-schedules tas
                                                                  (first remaining-slots)
                                                                  schedule))
                                             to-do)))]
                  [else
                   (fn-for-losch to-do)]))

          (define (fn-for-losch to-do)
            (cond [(empty? to-do) false]
                  [else
                   (schedule-tas (wle-schedule (first to-do))
                                 (wle-remaining-slots (first to-do))
                                 (rest to-do))]))]

    (schedule-tas empty slots empty)))



;; Schedule -> Boolean
;; produce true iff the schedule has no availability conflicts nor overworked TAs
(check-expect (valid-schedule? NOODLE-TAs empty) true)
(check-expect (valid-schedule? NOODLE-TAs (list (make-assignment UDON 4))) true)
(check-expect (valid-schedule? NOODLE-TAs (list (make-assignment UDON 2))) false)
(check-expect (valid-schedule? NOODLE-TAs (list (make-assignment UDON 4)
                                     (make-assignment SOBA 3)
                                     (make-assignment RAMEN 2)
                                     (make-assignment SOBA 1)))
              true)
(check-expect (valid-schedule? NOODLE-TAs (list (make-assignment UDON 4)
                                     (make-assignment UDON 3)
                                     (make-assignment RAMEN 2)
                                     (make-assignment SOBA 1)))
              false)

(define (valid-schedule? tas schedule)
  (and (no-conflicts? schedule) (no-overworked-tas? tas schedule)))



;; (listof Slot) Schedule -> Boolean
;; produce true iff the schedule has a TA assigned to every slot in slots
(check-expect (all-slots-filled? empty empty) true)
(check-expect (all-slots-filled? (list 3 6) empty) false)
(check-expect (all-slots-filled? empty   ; shouldn't happen in main function
                                 (list (make-assignment UDON 4)
                                       (make-assignment SOBA 3)))
              true)
(check-expect (all-slots-filled? (list 3 4)
                                 (list (make-assignment UDON 4)
                                       (make-assignment SOBA 3)))
              true)
(check-expect (all-slots-filled? (list 3 6 2)
                                 (list (make-assignment UDON 4)
                                       (make-assignment SOBA 3)
                                       (make-assignment RAMEN 2)))
              false)

(define (all-slots-filled? slots schedule)
  (andmap (lambda (slot) (member slot (map assignment-slot schedule)))
          slots))



;; Schedule -> Boolean
;; produce true iff no TAs in the schedule are assigned to shifts outside their availability
(check-expect (no-conflicts? empty) true)
(check-expect (no-conflicts? (list (make-assignment UDON 4))) true)
(check-expect (no-conflicts? (list (make-assignment UDON 2))) false)
(check-expect (no-conflicts? (list (make-assignment UDON 4)
                                   (make-assignment SOBA 3)
                                   (make-assignment RAMEN 2)
                                   (make-assignment SOBA 1)))
              true)
(check-expect (no-conflicts? (list (make-assignment UDON 4)
                                   (make-assignment SOBA 2)
                                   (make-assignment RAMEN 3)
                                   (make-assignment SOBA 1)))
              false)

(define (no-conflicts? schedule)
  (andmap (lambda (assignment) (member (assignment-slot assignment)
                                       (ta-avail (assignment-ta assignment))))
          schedule))



;; (listof TA) Schedule -> Boolean
;; produce true iff no TAs in the schedule are assigned to more than their maximum shifts
(check-expect (no-overworked-tas? NOODLE-TAs empty) true)
(check-expect (no-overworked-tas? NOODLE-TAs (list (make-assignment UDON 4)
                                                   (make-assignment SOBA 3)
                                                   (make-assignment RAMEN 2)
                                                   (make-assignment SOBA 1)))
              true)
(check-expect (no-overworked-tas? NOODLE-TAs (list (make-assignment UDON 4)
                                                   (make-assignment UDON 3)
                                                   (make-assignment RAMEN 2)
                                                   (make-assignment SOBA 1)))
              false)

(define (no-overworked-tas? tas schedule0)
  (local [(define (no-overworked-tas? schedule ta-list)
            (cond [(empty? ta-list) true]
                  [else
                   (if (> (shift-count (first ta-list) schedule)
                          (ta-max (first ta-list)))
                       false
                       (no-overworked-tas? schedule (rest ta-list)))]))]
                     
    (no-overworked-tas? schedule0 tas)))



;; TA Schedule -> Natural
;; produce the number of shifts the given TA is assigned to in the schedule
(check-expect (shift-count SOBA empty) 0)
(check-expect (shift-count UDON (list (make-assignment UDON 4)
                                      (make-assignment SOBA 3)
                                      (make-assignment RAMEN 2)
                                      (make-assignment SOBA 1)))
              1)
(check-expect (shift-count SOBA (list (make-assignment UDON 4)
                                      (make-assignment SOBA 3)
                                      (make-assignment RAMEN 2)
                                      (make-assignment SOBA 1)))
              2)

(define (shift-count ta schedule)
  (local [(define schedule-tas (map assignment-ta schedule))]
    (foldr (lambda (schedule-ta count) (if (string=? (ta-name ta)
                                                     (ta-name schedule-ta))
                                           (add1 count)
                                           count))
           0
           schedule-tas)))



;; (listof TA) Slot Schedule -> (listof Schedule)
;; using the given schedule as a base, produce one new schedule for
;; each TA in which that TA is now assigned to the given slot
(check-expect (next-schedules (list SOBA) 3 empty)
              (list (list (make-assignment SOBA 3))))
(check-expect (next-schedules (list SOBA UDON) 4 empty)
              (list (list (make-assignment SOBA 4))
                    (list (make-assignment UDON 4))))
(check-expect (next-schedules (list SOBA) 8 (list (make-assignment UDON 4)
                                                  (make-assignment RAMEN 2)
                                                  (make-assignment SOBA 1)))
              (list (list (make-assignment SOBA 8)
                          (make-assignment UDON 4)
                          (make-assignment RAMEN 2)
                          (make-assignment SOBA 1))))

(define (next-schedules ta-list slot schedule)
  (foldr (lambda (ta los) (cons (cons (make-assignment ta slot)
                                      schedule)
                                los))
         empty
         ta-list))
