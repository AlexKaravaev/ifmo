; Operation - increasing
; Handling byte condition <150
; Stop condition overflow or zaem

HIGHBYTE EQU 10h
LOWBYTE  EQU 11h
RAM      EQU 20h

MOV HIGHBYTE, #00
MOV LOWBYTE,  #00
org 0
jmp main
org 100
; Procedure for increasing byte
increase:
        inc HIGHBYTE
        inc LOWBYTE
	JB OV, myend


; main loop
main: 
	sjmp increase
	sjmp main
	
myend:
	sjmp myend
end