// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// *input = 0

@input
M = 0
(loop)
    // if *KBD != 0: *KBD = -1
    @KBD
    D = M
    @endStandarize
    D; JEQ
    D = -1
    (endStandarize)
    // D = *KBD

    // if *KBD == *input: continue
    @KBDRes
    M = D
    @input
    D = D - M
    @loop
    D; JEQ

    // *input = *KBDRes
    @KBDRes
    D = M
    @input
    M = D

    // a = SCREEN
    @SCREEN
    D = A
    @a
    M = D
    // *i = 0
    @i
    M = 0
    (fillLoop)
        // if *i >= 131072: goto endFillLoop
        @8192
        D = A
        @i
        D = M - D
        @endFillLoop
        D; JGE

        // *a = *KBDRes
        @KBDRes
        D = M
        @a
        A = M
        M = D

        // *a++ 
        @a
        M = M + 1
        // *i++
        @i
        M = M + 1

        @fillLoop
        0; JMP
        (endFillLoop)

    @loop
    0; JMP
