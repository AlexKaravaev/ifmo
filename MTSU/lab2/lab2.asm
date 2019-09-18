; BANK - 1(ADRESSES 8-F)
; X - 2059
; Y - 5555
; ADRESS Z - 48
; F = 4*X + Y

; X ADRESS
setb RS0

VAL1L EQU R0
VAL1H EQU R1

; Y ADRESS
VAL2L EQU R2
VAL2H EQU R3

; 4*X ADRESS
VALMUL1L EQU R5
VALMUL1H EQU R6
VALMUL2L EQU R7

; Z ADRESS
VALRES1L EQU 46h
VALRES1H EQU 47h

org 0
ajmp 30
org 30

; Write values to registers
mov VAL1L, #11
mov VAL1H, #8
mov VAL2L, #179
mov VAL2H, #21

; Multiply lower byte
mov A, #4
mov B, VAL1L
mul AB

mov VALMUL1L, A
mov VALMUL2L, B

; Multiply high byte
mov A, #4
mov B, VAL1H
mul AB

mov VALMUL1H, A


; Add result of multiplication to y, lower bytes
mov A, VALMUL1L
add A, VAL2L

mov VALRES1L, A


; Add result of multiplication to y, high bytes
mov A, VALMUL1H
add A, VAL2H

mov VALRES1H, A

END