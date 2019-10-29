FIRST_IND EQU 00h
SECOND_IND EQU 01h
THIRD_IND EQU 02h
TEMPA EQU 03h
TOZERO EQU 05h
COUNTER EQU 06h
FOUR EQU 07h
MULRES EQU 08h


ButtonUpdate EQU P3.2
ButtonMul EQU P3.1

ORG 0
jmp init
ORG 30h

init:
    mov DPTR, #Table
    mov P0, #0
    mov P1, #0
    mov P2, #0
    mov FIRST_IND, #00000000
    mov SECOND_IND, #00000000
    mov THIRD_IND, #00000000
    mov COUNTER, #0d
    mov MULRES, #0d
    mov FOUR, #3d
    jmp main

display:
    jb ButtonUpdate, display
    mov P0, FIRST_IND
    mov P1, SECOND_IND
    mov P2, THIRD_IND
    jmp continue3

decode:
    mov A, P3
    mov TOZERO, #11110000b
    anl A, TOZERO
    rr A
    rr A
    rr A
    rr A

    mov COUNTER, A
    add A, MULRES
    mov B, #10d
    div AB
    mov TEMPA, A
    mov A, B


    movc A, @A+DPTR


    mov THIRD_IND, A
    mov A, TEMPA
    mov B, #10d
    div AB
    movc A, @A+DPTR


    mov FIRST_IND, A
    mov A, B


    movc A, @A+DPTR


    MOV SECOND_IND, A

    jmp continue1

mulFour:
    jb ButtonMul, mulFour
    mov A, COUNTER
    mov B, FOUR
    mul AB
    mov MULRES, A

    jmp continue2

main:
    jmp decode
continue1:
    jb ButtonMul, mulFour
continue2:
    jb ButtonUpdate, display
continue3:
    ljmp main

Table:
    DB 3Fh
    DB 06h
    DB 5Bh
    DB 4Fh
    DB 66h
    DB 6Dh
    DB 7Dh
    DB 07h
    DB 7Fh
    DB 6Fh

END
