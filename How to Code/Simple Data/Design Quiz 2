;; Design Quiz 2: How to Design Data
;; How to Code: Simple Data (University of British Columbia)

;; Student: Jared Cooney
;; jaredcooney2@gmail.com

;; Runs in DrRacket (Beginning Student Language)

;;===========================================================

;; Age is Natural
;; interp. the age of a person in years
(define A0 18)
(define A1 25)

#;
(define (fn-for-age a)
  (... a))

;; Template rules used:
;; - atomic non-distinct: Natural

;;===========================================================
;; Problem 1:
;; Consider the above data definition for the age of a person.
;; Design a function called teenager? that determines whether a person
;; of a particular age is a teenager (i.e., between the ages of 13 and 19).


;; Age -> Boolean
;; produces true if the given age is between 13 and 19 (inclusive), else produces false
(check-expect (teenager? 3) false)
(check-expect (teenager? 13) true)
(check-expect (teenager? 15) true)
(check-expect (teenager? 19) true)
(check-expect (teenager? 50) false)

;(define (teenager? a) false)  ;stub

;; <use template from Age>

(define (teenager? a)
  (and (<= 13 a) (<= a 19)))

;;===========================================================
;; Problem 2:
;; Design a data definition called MonthAge to represent a person's age
;  in months.


;; MonthAge is Natural
;; interp. a person's age in months
(define MA1 3)
(define MA2 72)

#;
(define (fn-for-month-age ma)
  (... ma))

;; Template rules used:
;;  - atomic non-distinct: Number

;;===========================================================
;; Problem 3:
;; Design a function called months-old that takes a person's age in years 
;; and yields that person's age in months.


;; Age -> MonthAge
;; produces the number of months in the given number of years
(check-expect (months-old 1) 12)
(check-expect (months-old 5) 60)

;(define (months-old a) 0)  ;stub

;; <use template from Age>

(define (months-old a)
  (* a 12))

;;===========================================================
;; Problem 4:
;; Consider a video game where you need to represent the health of your
;; character. The only thing that matters about their health is:
;;
;;   - if they are dead (which is shockingly poor health)
;;   - if they are alive then they can have 0 or more extra lives
;;
;; Design a data definition called Health to represent the health of your
;; character.
;; Design a function called increase-health that allows you to increase the
;; lives of a character.  The function should only increase the lives
;; of the character if the character is not dead, otherwise the character
;; remains dead.

;;=================================
;; Data Definitions

;; Health is one of:
;;  - Natural
;;  - false
;; interp. the number of extra lives the game character has; false means the character is dead
(define H1 0)
(define H2 5)
(define H3 false)

#;
(define (fn-for-health h)
  (cond [(integer? h)
         (... h)]
        [else
         (...)]))

;; Template rules used:
;;  - one of: 2 cases
;;  - atomic non-distinct: Natural
;;  - atomic distinct: false


;;=================================
;; Functions

;; Health -> Health
;; increment the given health value by 1 and return the result; if given false, return false
(check-expect (increase-health 0) 1)
(check-expect (increase-health 5) 6)
(check-expect (increase-health false) false)

;(define (increase-health h) 0)  ;stub

;; <use template from Health>

(define (increase-health h)
  (cond [(integer? h)
         (+ h 1)]
        [else
         false]))
