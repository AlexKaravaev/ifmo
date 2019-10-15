FIRST_LED EQU 00h
hi EQU P0.0
BUTTON1 EQU P3.0
BUTTON2 EQU P3.1
BUTTON3 EQU P3.2
BUTTON4 EQU P3.3
BUTTON5 EQU P3.4

ORG 0h
ajmp INIT

; Переход к обработке прерывания по кнопке 1
org 0003h
ajmp enter

; Переход к обработке прерывания по кнопке 2
org 0013h
ajmp display

ORG 30h

INIT:
	mov P0, #0d
	clr P1.0
	clr P1.1
	setb P1.1
	clr P1.1
	setb IT0
	setb IT1
	setb EA
	setb EX0
	setb EX1
	X equ R2
	OST equ R3
	COUNTER equ R4
	mov COUNTER, #0d
	mov OST, #224d
	mov X, #0d

loop:
	ajmp loop
	
display_4:
	setb P0.7
	ret
	
enter:
	; Кладем значения в регистр Х и вычитаем из Х остаток
	MOV X, P2
	MOV A, X
	SUBB A, OST
	MOV X, A
	INC COUNTER
 	reti
	
display:
	clr P1.0
	clr P1.1
	; Показываем число
	mov P0, X
	; Показываем номер
	MOV A, #00000001
	ANL A, COUNTER
	ADDC A, #255d
	;JBC  PSW.OV, lamp1
	
	MOV A, #00000010
	ANL A, COUNTER
	ADDC A, #255d
	;JBC  PSW.OV, lamp2
	reti
	
lamp1:
	setb P1.0
	ret
lamp2:
	setb P1.1
	ret
