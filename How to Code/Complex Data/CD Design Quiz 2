;; Design Quiz 2: Abstraction
;; How to Code: Complex Data (University of British Columbia)

;; Student: Jared Cooney
;; jaredcooney2@gmail.com

;; Runs in DrRacket (Intermediate Student Language)

;;===========================================================
(require 2htdp/image)


;; PROBLEM 1:
;; 
;; Design an abstract function called arrange-all to simplify the 
;; above-all and beside-all functions defined below. Rewrite above-all and
;; beside-all using your abstract function.


;;(Image X -> X) (listof Image) -> X
;; abstract function for operating on a list of images
;; NOTE: the prescribed function name suggests the intended output is Image
(check-expect (arrange-all above (list (rectangle 20 40 "solid" "red") (star 30 "solid" "yellow")))
              (above (rectangle 20 40 "solid" "red") (star 30 "solid" "yellow")))
(check-expect (arrange-all beside (list (circle 10 "outline" "red")
                                        (circle 20 "outline" "blue")
                                        (circle 10 "outline" "yellow")))
              (beside (circle 10 "outline" "red")
                      (circle 20 "outline" "blue")
                      (circle 10 "outline" "yellow")))

;(define (arrange-all fn loi) empty-image)  ;stub

(define (arrange-all fn loi)
  (cond [(empty? loi) empty-image]
        [else
         (fn (first loi)
             (arrange-all fn (rest loi)))]))



;; (listof Image) -> Image
;; combines a list of images into a single image, each image above the next one
(check-expect (above-all empty) empty-image)
(check-expect (above-all (list (rectangle 20 40 "solid" "red") (star 30 "solid" "yellow")))
              (above (rectangle 20 40 "solid" "red") (star 30 "solid" "yellow")))
(check-expect (above-all (list (circle 30 "outline" "black")
                               (circle 50 "outline" "black")
                               (circle 70 "outline" "black")))
              (above (circle 30 "outline" "black")
                     (circle 50 "outline" "black")
                     (circle 70 "outline" "black")))

;(define (above-all loi) empty-image)  ;stub

(define (above-all loi)
  (arrange-all above loi))



;; (listof Image) -> Image
;; combines a list of images into a single image, each image beside the next one
(check-expect (beside-all empty) (rectangle 0 0 "solid" "white"))
(check-expect (beside-all (list (rectangle 50 40 "solid" "blue") (triangle 30 "solid" "pink")))
              (beside (rectangle 50 40 "solid" "blue") (triangle 30 "solid" "pink")))
(check-expect (beside-all (list (circle 10 "outline" "red")
                                (circle 20 "outline" "blue")
                                (circle 10 "outline" "yellow")))
              (beside (circle 10 "outline" "red")
                      (circle 20 "outline" "blue")
                      (circle 10 "outline" "yellow")))

;(define (beside-all loi) empty-image)  ;stub

(define (beside-all loi)
  (arrange-all beside loi))

;;===========================================================

;; PROBLEM 2:
;; 
;; Finish the design of the following functions, using built-in abstract functions. 
 

;; Function 1
;; ==========

;; (listof String) -> (listof Natural)
;; produces a list of the lengths of each string in los
(check-expect (lengths empty) empty)
(check-expect (lengths (list "apple" "banana" "pear")) (list 5 6 4))

(define (lengths lst)
  (map string-length lst))



;; Function 2
;; ==========

;; (listof Natural) -> (listof Natural)
;; produces a list of just the odd elements of lon
(check-expect (odd-only empty) empty)
(check-expect (odd-only (list 1 2 3 4 5)) (list 1 3 5))

(define (odd-only lon)
  (filter odd? lon))



;; Function 3
;; ==========

;; (listof Natural -> Boolean
;; produce true if all elements of the list are odd
(check-expect (all-odd? empty) true)
(check-expect (all-odd? (list 1 2 3 4 5)) false)
(check-expect (all-odd? (list 5 5 79 13)) true)

(define (all-odd? lon)
  (andmap odd? lon))



;; Function 4
;; ==========

;; (listof Natural) -> (listof Natural)
;; subtracts n from each element of the list
(check-expect (minus-n empty 5) empty)
(check-expect (minus-n (list 4 5 6) 1) (list 3 4 5))
(check-expect (minus-n (list 10 5 7) 4) (list 6 1 3))

(define (minus-n lon n)
  (local [(define (subn num) (- num n))]
    (map subn lon)))

#; ;could also use a lambda:
(define (minus-n lon n)
  (map (lambda (x) (- x n)) lon))


;;===========================================================

;; PROBLEM 3
;; 
;; Consider the data definition below for Region. Design an abstract fold function for region, 
;; and then use it to design a function that produces a list of all the names of all the 
;; regions in that region.
;; 
;; Order the arguments in your fold function with combination functions first,
;; then bases, then the region. Number the bases and combination 
;; functions in order of where they appear in the function.
;; 
;; So (all-regions CANADA) would produce 
;; (list "Canada" "British Columbia" "Vancouver" "Victoria" "Alberta" "Calgary" "Edmonton")


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



;; (String Y Z -> X) (X Z -> Z) Y Y Y Y Y Z Region -> X
;; the abstract fold function for Region


(define (fold-region c1 c2 b1 b2 b3 b4 b5 b6 r)
  (local [(define (fn-for-region r)                    ;-> X
            (c1 (region-name r)
                (fn-for-type (region-type r))
                (fn-for-lor (region-subregions r))))
          
          (define (fn-for-type t)                      ;->Y
            (cond [(string=? t "Continent") b1]
                  [(string=? t "Country")   b2]
                  [(string=? t "Province")  b3]
                  [(string=? t "State")     b4]
                  [(string=? t "City")      b5]))
          
          (define (fn-for-lor lor)                     ;->Z
            (cond [(empty? lor) b6]
                  [else 
                   (c2 (fn-for-region (first lor))
                       (fn-for-lor (rest lor)))]))]
    (fn-for-region r)))



;; Region -> (listof String)
;; produce a list of the names of every region (including subregions) in the given region
(check-expect (all-regions EDMONTON)
              (list "Edmonton"))
(check-expect (all-regions CANADA)
              (list "Canada" "British Columbia" "Vancouver"
                    "Victoria" "Alberta" "Calgary" "Edmonton"))

;(define (all-regions r) empty)  ;stub

(define (all-regions r)
  (local [(define (c1 name type-dummyres sub-names) (cons name sub-names))
          (define (c2 region-names rest-names) (append region-names rest-names))]
    (fold-region c1 c2 "dummy1" "dummy2" "dummy3" "dummy4" "dummy5" empty r)))

