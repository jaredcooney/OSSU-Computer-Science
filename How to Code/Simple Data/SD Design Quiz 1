;; Design Quiz 1: How to Design Functions
;; How to Code: Simple Data (University of British Columbia)

;; Student: Jared Cooney
;; jaredcooney2@gmail.com

;; Runs in DrRacket (Beginning Student Language)

;;===========================================================
(require 2htdp/image)

;; Image Image -> Boolean
;; returns true if the area of img1 (width * length) is greater than that of img2, else returns false
(check-expect (larger? (rectangle 20 40 "solid" "red") (rectangle 60 15 "solid" "red")) false)
(check-expect (larger? (rectangle 50 30 "solid" "red") (rectangle 60 20 "solid" "red")) true)
(check-expect (larger? (rectangle 10 20 "solid" "red") (rectangle 20 10 "solid" "red")) false)

;(define (larger? img1 img2) false)  ;stub

;(define (larger? img1 img2)         ;template
;  (... img1 img2))

(define (larger? img1 img2)
  (> (* (image-width img1) (image-height img1))
     (* (image-width img2) (image-height img2))))
