; Operation - increasing
; Handling byte condition <150
; Stop condition overflow or zaem

HIGHBYTE EQU 10h
LOWBYTE  EQU 11h
RAM      EQU 20h
N1 EQU 20h
N2 EQU 21h
N3 EQU 22h
N4 EQU 23h
N5 EQU 24h
N6 EQU 25h
N7 EQU 26h
STACKEND EQU 27h

; Procedure for increasing byte
increase:
	MOV A,  @R0
	mov R7, A
	mov A,  R2
    	ADD A,  R7
    	mov R2, A
    	mov A,  #0
    	addc A, #0
    	add A,  R1
    	JC myend ;check overflow
    	mov R1, A    

	ret
	
continue:
	lcall increase
	lcall while
	
while:
	;inc R0
	dec STACKEND
	inc R0
	mov A, STACKEND
	jnz main

org 0h
jmp startup
org 38h

; Initial startup-procedure, writing inital values to all adresses
startup:
	MOV HIGHBYTE, #255
	MOV LOWBYTE,  #255
	mov N1,#151
	mov N2,#200
	mov N3,#10
	mov N4,#10
	mov N5,#100
	mov N6,#50
	mov N7,#230
	mov R0,#20h
	mov R1, HIGHBYTE
	mov R2, LOWBYTE
	mov STACKEND, #07

; main loop
main: 
	mov A, @R0
	mov R5, A
	
	;check if byte less than 150
	mov A, #150
	CLR C
	subb A, R5
	JNC continue
	lcall while
	
	
myend:
	sjmp startup
end
