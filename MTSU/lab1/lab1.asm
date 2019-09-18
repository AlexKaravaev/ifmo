; Order of bytes: high, low
; Multi-byte operation: +
; Single-byte operation: /
; 1 operand - High: 200, Low: 100
; 2 operand - High: 100, Low: 190

VAL1L EQU 10h
VAL1H EQU 11h

VAL2L EQU 18h
VAL2H EQU 19h

REZL EQU 20h
REZH EQU 21h
REZE1 EQU 22h
REZE2 EQU 23h
DIVRL EQU 24h
DIVRH EQU 25h

; Begginning of the program
org 0
ajmp 30h
org 30h

mov VAL1L, #100
mov VAL1H, #200

mov VAL2L, #190
mov VAL2H, #100

;Add low-bytes, with possible overflow
mov A, VAL1L
addc A, VAL2L

mov REZL, A

mov A, #0
addc A, #0

mov REZE1, A

;Add high bytes, with possible overflow
mov A, VAL1H
addc A, VAL2H

mov REZH, A

mov A, #0
addc A, #0
mov REZE2, A

; Divide two low-bytes
mov A, VAL2L
mov B, VAL1L

div AB

mov DIVRH, A
mov DIVRL, B


END