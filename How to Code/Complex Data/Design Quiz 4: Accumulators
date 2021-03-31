;; Design Quiz 4: Accumulators
;; How to Code: Complex Data (University of British Columbia)

;; Student: Jared Cooney
;; jaredcooney2@gmail.com

;;Runs in DrRacket (Intermediate Student Language)

;;===========================================================

;; PROBLEM 1:
;; 
;; Assuming the use of at least one accumulator, design a function that consumes a 
;; list of strings and produces the length of the longest string in the list. 
 

;; (listof String) -> Natural
;; produce the length of the longest string in the given list
(check-expect (longest empty) 0)
(check-expect (longest (list "" "" "")) 0)
(check-expect (longest (list "egg" "apple" "rice" "okra")) 5)
(check-expect (longest (list "egg" "apple" "rice" "onion")) 5)
(check-expect (longest (list "" "clementine" "" "" "fig" "")) 10)

(define (longest los)
  ;; rsf is Natural; a context-preserving accumulator
  (local [(define (longest los rsf)
            (cond [(empty? los) rsf]
                  [else
                   (if (> (string-length (first los)) rsf)
                       (longest (rest los)
                                (string-length (first los)))
                       (longest (rest los)
                                rsf))]))]
    
    (longest los 0)))

;;===========================================================

;; PROBLEM 2:
;; 
;; The Fibbonacci Sequence (https://en.wikipedia.org/wiki/Fibonacci_number) is 
;; the sequence 0, 1, 1, 2, 3, 5, 8, 13,... where the nth element is equal to 
;; the sum of element n-2 and element n-1.
;; 
;; Design a function that, given a list of numbers at least two elements long, 
;; determines whether the list obeys the fibonacci rule, f(n-2) + f(n-1) = f(n), for  
;; every element in the list. The sequence does not have to start at zero, so for 
;; example, the sequence 4, 5, 9, 14, 23 would follow the rule. 
 

;; (listof Number) -> Boolean
;; produce true iff the sequence of numbers follows the rule: f(n) = f(n-2) + f(n-1)
;; Assumes: the given list contains at least two elements
(check-expect (fib-pattern? (list 0 0)) true)
(check-expect (fib-pattern? (list 1 1 1 1 1)) false)
(check-expect (fib-pattern? (list 4 6 10 16 20 36)) false)
(check-expect (fib-pattern? (list 0 0 0 0)) true)
(check-expect (fib-pattern? (list 1 -1 0 -1 -1 -2 -3 -5)) true)
(check-expect (fib-pattern? (list 0 1 1 2 3 5 8 13 21)) true)
(check-expect (fib-pattern? (list 7 4 11 15 26 41)) true)

(define (fib-pattern? lon)
  ;; last-two is (listof Number) of length 2; the first two list elements from the previous call
  ;; Outer call example: (fib-pattern? (list 0 1 1 2 3))
  ;;   (fib-pattern? (list     1 2 3) (list 0 1))
  ;;   (fib-pattern? (list       2 3) (list 1 1))
  ;;   (fib-pattern? (list         3) (list 1 2))
  (local [(define (fib-pattern? lon last-two)
            (cond [(empty? lon) true]  ; this only occurs if the initial list is length 2
                  [(= 1 (length lon)) (= (first lon)
                                         (+ (first last-two)
                                            (second last-two)))]
                  [else
                   (if (= (first lon)
                          (+ (first last-two)
                             (second last-two)))
                       (fib-pattern? (rest lon)
                                     (list (second last-two)
                                           (first lon)))
                       false)]))]

    (fib-pattern? (rest (rest lon)) (list (first lon) (second lon)))))

;;===========================================================

;; PROBLEM 3:
;; 
;; Refactor the function below to make it tail-recursive.  


;; Natural -> Natural
;; produces the factorial of the given number
(check-expect (fact 0) 1)
(check-expect (fact 3) 6)
(check-expect (fact 5) 120)

(define (fact n0)
  ;; acc is Number; the product of all numbers in Natural[n, n0]
  (local [(define (fact n acc)
            (cond [(zero? n) acc]
                  [else 
                   (fact (sub1 n) (* n acc))]))]
    (fact n0 1)))

;;===========================================================

;; PROBLEM 4:
;; 
;; Recall the data definition for Region from the Abstraction Quiz. Use a worklist 
;; accumulator to design a tail-recursive function that counts the number of regions 
;; within and including a given region. 
;; So (count-regions CANADA) should produce 7.


(define-struct region (name type subregions))
;; Region is (make-region String Type (listof Region))
;; interp. a geographical region

;; Type is one of:
;; - "Continent"
;; - "Country"
;; - "Province"
;; - "State"
;; - "City"
;; interp. categories of geographical regions

(define VANCOUVER (make-region "Vancouver" "City" empty))
(define VICTORIA (make-region "Victoria" "City" empty))
(define BC (make-region "British Columbia" "Province" (list VANCOUVER VICTORIA)))
(define CALGARY (make-region "Calgary" "City" empty))
(define EDMONTON (make-region "Edmonton" "City" empty))
(define ALBERTA (make-region "Alberta" "Province" (list CALGARY EDMONTON)))
(define CANADA (make-region "Canada" "Country" (list BC ALBERTA)))

#;
(define (fn-for-region r)
  (local [(define (fn-for-region r)
            (... (region-name r)
                 (fn-for-type (region-type r))
                 (fn-for-lor (region-subregions r))))
          
          (define (fn-for-type t)
            (cond [(string=? t "Continent") (...)]
                  [(string=? t "Country") (...)]
                  [(string=? t "Province") (...)]
                  [(string=? t "State") (...)]
                  [(string=? t "City") (...)]))
          
          (define (fn-for-lor lor)
            (cond [(empty? lor) (...)]
                  [else 
                   (... (fn-for-region (first lor))
                        (fn-for-lor (rest lor)))]))]
    (fn-for-region r)))



;; Region -> Natural
;; produce the number of regions within and including the given region
(check-expect (count-regions VANCOUVER) 1)
(check-expect (count-regions CANADA) 7)

(define (count-regions r)
  ;; to-do is (listof Region); a worklist accumulator
  ;; rsf is Natural; the number of regions seen so far by fn-for-region
  (local [(define (fn-for-region r to-do rsf)
            (fn-for-lor (append (region-subregions r) to-do)
                        (add1 rsf)))
          
          (define (fn-for-lor to-do rsf)
            (cond [(empty? to-do) rsf]
                  [else 
                   (fn-for-region (first to-do)
                                  (rest to-do)
                                  rsf)]))]
    
    (fn-for-region r empty 0)))
