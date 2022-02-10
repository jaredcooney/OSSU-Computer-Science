;; Design Quiz 3: Generative Recursion
;; How to Code: Complex Data (University of British Columbia)

;; Student: Jared Cooney
;; jaredcooney2@gmail.com

;; Runs in DrRacket (Intermediate Student Language)

;;===========================================================
(require 2htdp/image)


;; PROBLEM 1:
;; 
;; In the lecture videos we designed a function to make a Sierpinski triangle fractal. 
;; Here is another geometric fractal that is made of circles rather than triangles:
;;
;; [image]
;;
;; Design a function to create this circle fractal of size n and colour c.
 

(define CUTOFF 5)

;; Natural String -> Image
;; produce a circle fractal of size n and colour c
(check-expect (circle-fractal CUTOFF "blue") (circle CUTOFF "outline" "blue"))
(check-expect (circle-fractal (* 2 CUTOFF) "red")
              (overlay (local [(define sub (circle CUTOFF "outline" "red"))]
                         (beside sub sub))
                       (circle (* 2 CUTOFF) "outline" "red")))

(define (circle-fractal n c)
  (cond [(<= n CUTOFF) (circle n "outline" c)]
        [else
         (overlay (local [(define sub (circle-fractal (/ n 2) c))]
                    (beside sub sub))
                  (circle n "outline" c))]))


;;===========================================================

;; PROBLEM 2:
;; 
;; Below you will find some data definitions for a tic-tac-toe solver. 
;; 
;; In this problem, you will design a function that produces all 
;; possible filled boards that are reachable from the current board. 
;; 
;; In actual tic-tac-toe, O and X alternate playing. For this problem
;; you can disregard that. You can also assume that the players keep 
;; placing Xs and Os after someone has won. This means that a board that 
;; is completely filled with Xs, for example, is valid.
 

;; Value is one of:
;; - false
;; - "X"
;; - "O"
;; interp. a square is either empty (represented by false) or has and "X" or an "O"

#;
(define (fn-for-value v)
  (cond [(false? v) (...)]
        [(string=? v "X") (...)]
        [(string=? v "O") (...)]))

;; Board is (listof Value)
;; a board is a list of 9 Values
(define B0 (list false false false
                 false false false
                 false false false))

(define B1 (list false "X"   "O"   ; a partly finished board
                 "O"   "X"   "O"
                 false false "X")) 

(define B2 (list "X"  "X"  "O"     ; a mostly finished board
                 "O"  "X"  "O"
                 "X" false "X"))

(define B3 (list "X" "O" "X"       ; a mostly finished board
                 "O" "O" false
                 "X" "X" false))

(define B4 (list "X" "O" "X"       ; a completely filled board
                 "O" "O" "X"
                 "X" "X" "O"))

#;
(define (fn-for-board b)
  (cond [(empty? b) (...)]
        [else 
         (... (fn-for-value (first b))
              (fn-for-board (rest b)))]))


;; Note: Solution for Problem 2 is omitted due to redundancy.
;;       See Problem 3 below for the complete solution.


;;===========================================================

;; PROBLEM 3:
;; 
;; Now adapt your solution to filter out the boards that are impossible if 
;; X and O are alternating turns. You can continue to assume that they keep 
;; filling the board after someone has won. 
;; 
;; You can assume X plays first, so all valid boards will have 5 Xs and 4 Os.
;;
;; NOTE: make sure you keep a copy of your solution from problem 2 to answer 
;; the questions on edX.
 

;; Board -> (listof Board)
;; produce a list of all possible finished boards that could be reached from the given
;; board state; fill boards completely even if someone has already won
(check-expect (gen-possible-outcomes B4) (list B4))
(check-expect (gen-possible-outcomes (list false)) (list (list "X")))
(check-expect (gen-possible-outcomes (list "X" false)) (list (list "X" "O")))
(check-expect (gen-possible-outcomes (list "X"  "X"   "O"
                                           "O"  false "O"
                                           "X"  "O"   "X"))
              (list (list "X"  "X" "O"
                          "O"  "X" "O"
                          "X"  "O" "X")))

(define (gen-possible-outcomes b)
  (local [(define (gen-possible-outcomes--b b)
            (if (full? b)
                (list b)
                (gen-possible-outcomes--lob (next-boards b))))
          
          (define (gen-possible-outcomes--lob lob)
            (cond [(empty? lob) empty]
                  [else
                   (append (gen-possible-outcomes--b (first lob))
                           (gen-possible-outcomes--lob (rest lob)))]))]
    
    (filter-invalid (gen-possible-outcomes--b b))))



;; Board -> Boolean
;; produce true if every square in the board is filled, false otherwise
(check-expect (full? B0) false)
(check-expect (full? B2) false)
(check-expect (full? B4) true)

(define (full? b)
  (not (ormap false? b)))



;; Board -> (listof Board) or false
;; find the first blank (false) square in b, and produce a list containing two new
;;  boards where that square is filled with "X" and "O"
;; Assume: the given board is not full
(check-expect (next-boards B0) (list (list "X"   false false
                                           false false false
                                           false false false)
                                     (list "O"   false false
                                           false false false
                                           false false false)))
(check-expect (next-boards (list "X"  "X"   "O"
                                 "O"  false "O"
                                 "X"  "O"   "X"))
              (list (list "X" "X" "O"
                          "O" "X" "O"
                          "X" "O" "X")
                    (list "X" "X" "O"   ;this function doesn't care about board validity
                          "O" "O" "O"
                          "X" "O" "X")))

(define (next-boards b)
  (next-both-options (first-blank-idx b) b))



;; (listof Board) -> (listof Board)
;; filter invalid boards from the given list
;; Validity invariant: The number of Xs minus the number of Os must be 0 or 1
(check-expect (filter-invalid empty) empty)
(check-expect (filter-invalid (list B0 B1 B2 B3 B4)) (list B0 B1 B3 B4))
(check-expect (filter-invalid (list (list "X" "X" "O"
                                          "O" "O" "O"
                                          "X" "O" "X")))
              empty)

(define (filter-invalid lob)
  (filter valid-board? lob))



;; Board -> Boolean
;; prodduce true if the given board is valid
;; Validity invariant: The number of Xs minus the number of Os must be 0 or 1
(check-expect (valid-board? B0) true)
(check-expect (valid-board? B1) true)
(check-expect (valid-board? B4) true)
(check-expect (valid-board? B2) false)
(check-expect (valid-board? (list "X" "X" "O"
                                  "O" "O" "O"
                                  "X" "O" "X"))
              false)

(define (valid-board? b)
  (local [(define x-minus-o (- (val-count "X" b)
                               (val-count "O" b)))]
    (or (= 0 x-minus-o)
        (= 1 x-minus-o))))



;; Value Board -> Natural
;; produce the number of times the value v appears on the board
(check-expect (val-count "X" B0) 0)
(check-expect (val-count "X" B2) 5)
(check-expect (val-count "O" B2) 3)

(define (val-count v b)
  (cond [(empty? b) 0]
        [else 
         (if (and (string? (first b)) (string=? v (first b)))
             (add1 (val-count v (rest b)))
             (val-count v (rest b)))]))



;; Natural[0, 8] Board -> (listof Board)
;; produce a list containing two new boards, where the value at the given index
;; in the given board is replaced with "X" in the first and "O" in the second
(check-expect (next-both-options 5 B0) (list (list false false false
                                                   false false "X"
                                                   false false false)
                                             (list false false false
                                                   false false "O"
                                                   false false false)))

(define (next-both-options idx b)
  (list (fill-square idx "X" b) (fill-square idx "O" b)))



;; Natural[0, 8] Value Board -> Board
;; produce a new board where the value at the given 
;; index in the given board is replaced with val
(check-expect (fill-square 5 "O" B0) (list false false false
                                           false false "O"
                                           false false false))

(define (fill-square idx val b)
  (cond [(zero? idx) (cons val (rest b))]
        [else
         (cons (first b)
               (fill-square (sub1 idx)
                            val
                            (rest b)))]))



;; Board -> Natural
;; produce the index of the first blank (false) square in the given tic-tac-toe board
;; Assume: the given board is not full
(check-expect (first-blank-idx B0) 0)
(check-expect (first-blank-idx B2) 7)

(define (first-blank-idx b)
  (cond [(empty? b) (error "The function first-blank-idx received a full board.")]
        [else
         (if (false? (first b))
             0
             (add1 (first-blank-idx (rest b))))]))

