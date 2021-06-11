TITLE String Primitives/Macros     (Proj6_kuoala.asm)

; Author: Alan Kuo
; Last Modified: 3/14/2021
; OSU email address: kuoala@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: 06                Due Date: 3/14/2021
; Description: Program that takes 10 user input integers, saves them into an array, and then prints the array along with the sum and average.
;				Uses macros and procedures to replace the functionality of ReadInt/ReadDec/WriteInt/WriteDec.

INCLUDE Irvine32.inc

; MACROS
; -------------------------------------------------------------
; Name: mGetString
;
; Displays a prompt and saves user input into a memory location.
; 
; Preconditions: Do not use EDX, ECX, EDI, EAX as arguments. These registers are used in the macro.
;
; Postconditions: None, all registers are saved and restored.
;
; Receives:
; promptAddr	= the address of the string being displayed as a prompt (input, reference)
; bufferAddr	= the address of the memory location to save the user input to (output, reference)
; bufferSize	= the maximum number of characters that can be accomodated (input, value)
; byteCountAddr	= the address of the memory location to save the number of characters entered by the user (output, reference)
;
; Returns:
;	The prompt is printed to the console. The user input is saved in bufferAddr. The number of characters entered by the user is saved to byteCountAddr.
; --------------------------------------------------------------
mGetString MACRO promptAddr:REQ, bufferAddr:REQ, bufferSize:REQ, byteCountAddr:REQ
	PUSH	EDX
	PUSH	ECX
	PUSH	EDI
	PUSH	EAX
	mDisplayString promptAddr
	MOV		EDX, bufferAddr
	MOV		ECX, bufferSize
	CALL	ReadString
	MOV		EDI, byteCountAddr
	MOV		[EDI], EAX
	POP		EAX
	POP		EDI
	POP		ECX
	POP		EDX
ENDM

; -------------------------------------------------------------
; Name: mDisplayString
;
; Prints the string that is stored in a specified memory location to the console.
;
; Preconditions: Do not use EDX as an argument. This register is used in the macro.
;
; Postconditions: None, all registers are saved and restored.
;
; Receives:
; stringAddr	= the address of the memory location where the string is stored (input, reference)
;
; Returns:
;	The specified string is printed to the console.
; --------------------------------------------------------------
mDisplayString MACRO stringAddr:REQ
	PUSH	EDX
	MOV		EDX, stringAddr
	CALL	WriteString
	POP		EDX
ENDM

; CONSTANTS
; Constant representing the number of valid integers that the user should enter. Set to 10 by default for project requirements.
NUMOFINPUTS = 10

; Text macro to dynamically change the number of integers to input that is displayed in the introduction string.
NUM_STR TEXTEQU <">, %NUMOFINPUTS, <">


.data
	introStr				BYTE	"PROGRAMMING ASSIGNMENT 6: DESIGNING LOW-LEVEL I/O PROCEDURES", 13,10,"Written by: Alan Kuo",0
	extraCredStr			BYTE	"**EC: Number each line of user input and display a running subtotal of the user's valid numbers.**",0
	instrStr				BYTE	"Please provide ", NUM_STR, " signed decimal integers. Each number needs to be small enough to fit inside a 32 bit register.",13,10,
									"After you have finished inputting the raw numbers, I will display a list of the integers, their sum, and ",13,10,"their average value. ",
									"The maximum number of characters that can be entered (including + and -) is 30.",0
	subtotalStr				BYTE	"The current subtotal is ",0
	promptStr				BYTE	". Please enter a signed number: ",0
	userInputLen			DWORD	?
	errorStr				BYTE	"ERROR: You did not enter a signed number, or your number was too big. Please try again!",0
	curUserVal				SDWORD	?
	userValArr				SDWORD	NUMOFINPUTS DUP(0)
	commaStr				BYTE	", ",0
	periodStr				BYTE	". ",0
	sumVals					SDWORD	?
	avgVals					SDWORD	?
	arrayIntroStr			BYTE	"You entered the following numbers:",0
	sumStr					BYTE	"The sum of these numbers is: ",0
	avgStr					BYTE	"The rounded average (using floor rounding) is: ",0
	farewellStr				BYTE	"Thanks for playing!",0


.code

; -----------------------------------------------------------------------
; Name: main
;
; Contains procedure calls and parameters for each section of the program.
; -----------------------------------------------------------------------
main PROC
	PUSH	OFFSET introStr
	PUSH	OFFSET extraCredStr
	PUSH	OFFSET instrStr
	CALL	displayIntro
	PUSH	NUMOFINPUTS
	PUSH	OFFSET userValArr
	PUSH	OFFSET periodStr
	PUSH	OFFSET subtotalStr
	PUSH	OFFSET promptStr
	PUSH	OFFSET userInputLen
	PUSH	OFFSET errorStr
	PUSH	OFFSET curUserVal
	CALL	getUserInput
	CALL	CrLf
	PUSH	OFFSET arrayIntroStr
	PUSH	LENGTHOF userValArr
	PUSH	OFFSET userValArr
	PUSH	OFFSET commaStr
	CALL	printArray
	CALL	CrLf
	PUSH	OFFSET userValArr
	PUSH	LENGTHOF userValArr
	PUSH	OFFSET sumVals
	PUSH	OFFSET avgVals
	CALL	getSumAvg	
	PUSH	OFFSET sumStr
	PUSH	sumVals
	PUSH	OFFSET avgStr
	PUSH	avgVals
	CALL	displayResults
	PUSH	OFFSET farewellStr
	CALL	displayFarewell

	Invoke ExitProcess,0															; exit to operating system
main ENDP


; -----------------------------------------------------------------------
; Name: displayIntro
;
; Function for printing an introduction message and instructions to the user.
; 
; Preconditions: The following macro is used: 
;						mDisplayString (for displaying strings)
;
; Postconditions: None, all registers used are saved and restored within the mDisplayString macro.
;
; Receives:
;		[EBP+16] = reference to introStr, a string containing the program title and programmer name
;		[EBP+12] = reference to extraCredStr, a string containing the extra credit option selected
;		[EBP+8] = reference to instrStr, a string containing instructions for using the program.
;
; Returns:
;		The introduction string, extra credit string, and instruction string are printed to the console.
; -----------------------------------------------------------------------
displayIntro PROC
	PUSH	EBP
	MOV		EBP, ESP
	mDisplayString [EBP+16]
	CALL	CrLf
	mDisplayString [EBP+12]
	CALL	CrLf
	CALL	CrLf
	mDisplayString [EBP+8]
	CALL	CrLf
	CALL	CrLf
	POP		EBP
	RET		12
displayIntro ENDP


; -----------------------------------------------------------------------
; Name: getUserInput
;
; Function for getting a specified number of valid integer inputs from the user. Uses the *ReadVal* subprocedure to handle receiving the input and validation.
; 
; Preconditions: The constant NUMINPUTS (which represents the number of valid integers to be entered by the user) has been defined. A variable for holding the current integer entered
;					by the user (curUserVal) and an empty array of size NUMINPUTS (userValArr) to hold the integer inputs have been defined. Another variable (userInputLen) for holding
;					the length of the user input has also been defined (used in the *ReadVal* subprocedure)
;
;					The following macros are used in *getUserInput* and the *ReadVal* subprocedure: 
;						mDisplayString (for displaying strings) and mGetString (for saving a user entered input into a memory location)
;
;					The following local variables are used:
;						lineNum: used to store the line number of the current input
;						curSubTotal: used to store the current subtotal of valid integers that have been entered by the user
;
; Postconditions: None, all registers are saved and restored.
;
; Receives:
;
;		[EBP+36] = Value of NUMINPUTS, the number of valid integers to get from the user (defined as 10 for this project).
;		[EBP+32] = Reference to userValArr, the array to hold valid integers entered by the user.
;		[EBP+28] = Reference to periodStr, a string containing the characters ". ", used for printing the line number.
;		[EBP+24] = Reference to subtotalStr, a string for displaying the subtotal.
;		[EBP+20] = Reference to promptStr, a string for prompting the user to enter an integer.
;		[EBP+16] = Reference to userInputLen, a variable holding the length of the string of digits entered by the user.
;		[EBP+12] = Reference to errorStr, a string printed to the user if an invalid string of digits is entered.
;		[EBP+8]  = Reference to curUserVal, a variable that holds the integer value of the user input string.
;
; Returns:
;		The value of curUserVal is changed by the *ReadVal* subprocedure to the user-entered integer. Each user-entered integer is added to the userValArr array.
;		The values of the current subtotal (saved as a local variable) and current line number are incremented and pushed to the *ReadVal* subprocedure, 
;		where they are printed to the console.
; -----------------------------------------------------------------------

getUserInput PROC
	; LOCAL directive automatically preserves EBP, adjusts ESP, and restores EBP at the end of the procedure
	LOCAL lineNum: DWORD, curSubtotal: DWORD
	PUSHAD
	; Set loop counter equal to the number of integers to be entered. Set EDI to point to the address of userValArr to prepare for storing integers.
	MOV		ECX, [EBP+36]
	MOV		EDI, [EBP+32]
	MOV		lineNum, 1
	MOV		curSubtotal, 0
_inputLoop:
	; Reset the value of curUserVal to 0 by indirect operand
	MOV		EBX, [EBP+8]
	MOV		EAX, 0
	; Push parameters to ReadVal subprocedure
	PUSH	lineNum																	; current line number (value)
	PUSH	[EBP+28]																; periodStr (reference)
	PUSH	curSubtotal																; current subtotal (value)
	PUSH	[EBP+24]																; subtotalStr (reference)
	PUSH	[EBP+20]																; promptStr (reference)
	PUSH	[EBP+16]																; userinputlen (reference)
	PUSH	[EBP+12]																; error Str (reference)
	PUSH	[EBP+8]																	; curUserVal (reference)
	CALL	ReadVal
	; Move the value of the validated integer to EAX by indirect operand, update current subtotal, store in array with register indirect addressing, and increment line number.
	MOV		EBX, [EBP+8]
	MOV		EAX, [EBX]
	ADD		curSubtotal, EAX
	MOV		[EDI], EAX
	ADD		EDI, 4
	INC		lineNum
	LOOP	_inputLoop
	POPAD
	RET		32
getUserInput ENDP

; -----------------------------------------------------------------------
; Name: ReadVal
;
; Function for prompting and receiving user input, validating that input is a valid integer, and storing the integer in a memory location. 
; For implementing Extra Credit #1, the current line number and subtotal will be printed as part of the prompt.
; 
; Preconditions: The current line number and subtotal (integer values) are provided by the parent procedure as parameters. 
;					A variable for holding the current integer entered by the user (curUserVal) and a variable (userInputLen) for holding
;					the length of the user input have been defined.
;
;					The following macros are used in the *ReadVal* subprocedure: 
;						mDisplayString (for displaying strings) and mGetString (for saving a user entered input into a memory location).
;
;					The following local variables are used:
;						inputVal: used to store the value of the user input (as an integer) during processing
;						signValue: used to store a flag (0 indicating sign has not yet been set, 1 indicating positive, 2 indicating negative) for the sign of the user input
;						inputBuffer: A 32 byte array for storing the user input (as a string) during processing
;
; Postconditions: None, all registers are saved and restored.
;
; Receives:
;
;		[EBP+36] = Value of lineNum, a local variable from the parent procedure that tracks the current line number
;		[EBP+32] = Reference to periodStr, a string containing the characters ". ", used for printing the line number.
;		[EBP+28] = Value of curSubtotal, a local variable from the parent procedure (getUserInput)
;		[EBP+24] = Reference to subtotalStr, a string for displaying the subtotal.
;		[EBP+20] = Reference to promptStr, a string for prompting the user to enter an integer.
;		[EBP+16] = Reference to userInputLen, a variable holding the length of the string of digits entered by the user.
;		[EBP+12] = Reference to errorStr, a string printed to the user if an invalid string of digits is entered.
;		[EBP+8]  = Reference to curUserVal, a variable that holds the integer value of the user input string.
;
; Returns:
;		The value of curUserVal is changed to the user-entered integer (the memory location where the user input integer is stored)
;		The values of the current subtotal (saved as a local variable) and current line number are printed to the console as part of the input prompt.
; -----------------------------------------------------------------------
ReadVal PROC
	LOCAL inputVal: SDWORD, signValue: DWORD, inputBuffer[32]:BYTE
	PUSHAD
	; Set local variables to 0, clear inputBuffer local array by setting all values to 0
	MOV		signValue, 0
	MOV		inputVal, 0
	MOV		ECX, 32
	MOV		EAX, 0
	LEA		EDI, inputBuffer														; set EDI to point to the memory location of inputBuffer local array
	REP		STOSB
_getInput:
	; Print line number, subtotal, and prompt
	MOV		EBX, [EBP+36]
	PUSH	EBX
	CALL	WriteVal
	mDisplayString [EBP+32]
	mDisplayString [EBP+24]
	MOV		EBX, [EBP+28]
	PUSH	EBX
	CALL	WriteVal
	; Set EBX to address of inputBuffer local array, maximum of 30 characters can be read (ECX set to buffer size - 1, and null byte will be stored at the end of the string)
	LEA		EBX, inputBuffer
	MOV		ECX, SIZEOF inputBuffer
	DEC		ECX
	mGetString [EBP+20], EBX, ECX, [EBP+16]
	; Set loop counter = to the number of characters entered by indirect operand, and then set ESI equal to the memory location of the inputBuffer local array
	MOV		ESI, [EBP+16]
	MOV		ECX, [ESI]
	LEA		ESI, inputBuffer
	; To convert string into an integer, multiply previously saved input(s) (if any) by 10, and then add the next number in the string. Used pseudocode provided in lecture as a reference.
_processInput:
	MOV		EAX, inputVal
	MOV		EBX, 10
	MOV		EDX, 0
	IMUL	EBX
	JO		_invalidInput															; If multiplication by 10 caused an overflow, then the input is invalid
	MOV		inputVal, EAX
	XOR		EAX, EAX																; Clear EAX register to prepare for character processing
	LODSB
	CMP		signValue, 0															; Check if sign value has been set. If already set, skip to checking if character is an integer
	JE		_checkIfSign
	JMP		_checkForNumber
	; Set signValue flag to appropriate value if character is a negative or positive sign, and move to next character. Otherwise, jump to chekcing if character is an integer.
_checkIfSign:
	CMP		EAX, 45															
	JE		_negativeSign
	CMP		EAX, 43
	JNE		_checkForNumber													
	MOV		signValue, 1
	LOOP	_processInput
_negativeSign:
	MOV		signValue, 2
	LOOP	_processInput
	; Check if user input is in the correct range for numerical ASCII characters
_checkForNumber:
	CMP		EAX, 48
	JB		_invalidInput
	CMP		EAX, 57
	JA		_invalidInput
	; Convert from ASCII code to decimal value. If there is no leading sign character (sign has not been set at this point), set sign to positive
_isNumber:
	SUB		EAX, 48
	CMP		signValue, 0
	JNE		_checkIfNeg
	MOV		signValue, 1
	JMP		_positiveNum
	; If negative flag is set, negate the current integer character to allow for proper signed addition
_checkIfNeg:
	CMP		signValue, 1
	JE		_positiveNum
	NEG		EAX
	; Add this digit to the current total. If this addition causes an overflow, the input is invalid.
_positiveNum:
	ADD		EAX, inputVal
	MOV		inputVal, EAX
	LOOP	_processInput
	JO		_invalidInput													
	MOV		EAX, inputVal
	JMP		_saveNumber
	; If input is invalid, show error message and reset local variables and inputBuffer local array to prepare for receiving another input
_invalidInput:
	mDisplayString [EBP+12]
	CALL	CrLf
	MOV		inputVal, 0														
	MOV		signValue, 0
	MOV		EAX, 0
	LEA		EDI, inputBuffer														
	REP		STOSB
	JMP		_getInput
	; Save the validated user input number to curUserVal by indirect operand.
_saveNumber:
	MOV		EDI, [EBP+8]
	MOV		EAX, inputVal
	MOV		[EDI], EAX
	POPAD
	RET		32
ReadVal ENDP


; -----------------------------------------------------------------------
; Name: WriteVal
;
; Function that converts an integer value to a string of ASCII digits, then uses the mDisplayString macro to print the value to the console. WriteVal can only print integers that will fit in a 32 bit register without overflowing.
; 
; Preconditions: A valid integer value is passed to the function as a parameter. 
;
;					The following macro is used in the *WriteVal* subprocedure: 
;						mDisplayString (for displaying strings)
;
;					The following local variables are used:
;						charCount: a variable for keeping track of how many characters are needed to print the integer value (number of digits)
;						negSign: a variable used as a flag (set to 1 if the integer value is negative) to determine if a negative sign should be printed
;						valString: a BYTE array used to hold the converted string for printing
;
; Postconditions: None, all registers are saved and restored.
;
; Receives:
;
;		[EBP+8] = the value of the integer to be printed to the console.
;
; Returns:
;		The integer is printed to the console as a string.
; -----------------------------------------------------------------------
WriteVal PROC
	LOCAL charCount: DWORD, negSign: DWORD, valString[12]:BYTE
	PUSHAD
	; Setting valString local array to 0's
	MOV		ECX, 12
	MOV		EAX, 0
	LEA		EDI, valString
	REP		STOSB
	; Setting local variables to 0
	MOV		charCount, 0
	MOV		negSign, 0
	; Set negSign flag if value is negative. Otherwise, continue to processing
	MOV		EAX, [EBP+8]
	CMP		EAX, 0
	JGE		_processingStep
	MOV		negSign, 1
	NEG		EAX
	; Sequentially divide by 10 to split integer into separate digits. Each remainder represents a digit of the integer number in reverse order. Push each remainder onto the stack and increment charCount
_processingStep:
	MOV		EDX, 0
	MOV		EBX, 10
	DIV		EBX
	PUSH	EDX
	INC		charCount
	; Check if remainder is 0. If remainder is 0, all digits have been pushed onto the stack. Otherwise continue looping
	CMP		EAX, 0
	JE		_writeToArray
	JMP		_processingStep
	; Set loop counter equal to the number of digits, set EDI to point to the valString local array. If integer value was negative, set first byte in valString equal to the ASCII code for negative sign
_writeToArray:
	MOV		ECX, charCount
	LEA		EDI, valString
	CMP		negSign, 1
	JNE		_writeLoop
	MOV		EAX, 45
	STOSB
	; Pop each digit off the stack (will now be in correct order) and store in valString. Loop until all digits have been popped off the stack.
_writeLoop:
	POP		EAX
	ADD		EAX, 48
	STOSB
	LOOP	_writeLoop
	; set EBX to point to the valString local array and use mDisplayString macro to print the final string version of the original integer
	LEA		EBX, valString
	mDisplayString EBX
	POPAD
	RET		4
WriteVal ENDP

; -----------------------------------------------------------------------
; Name: printArray
;
; Function for printing an array of integers to the console, using the *WriteVal* subprocedure. Integers are separated by commas. WriteVal can only print integers that will fit in a 32 bit register without overflowing.
; 
; Preconditions: An array of valid integer values of type DWORD has been defined.
;
;					The following macro is used in the *WriteVal* subprocedure: 
;						mDisplayString (for displaying strings)
;
; Postconditions: None, all registers are saved and restored.
;
; Receives:
;
;		[EBP+20] = reference to arrayIntroStr, a string to be printed prior to the array
;		[EBP+16] = value of the number of items contained in the array to be printed (in this case it is the number of integers entered by the user)
;		[EBP+12] = reference to array to print (in this case it is userValArr, an array that contains the integers entered by the user)
;		[EBP+8] = reference to commaStr, a string used to print commas in between the integer values
;
; Returns:
;		The array of integers is printed to the console.
; -----------------------------------------------------------------------
printArray PROC
	PUSH	EBP
	MOV		EBP, ESP
	PUSHAD
	; Display intro string, set loop counter equal to the number of integers to print, set ESI to point to the beginning of the array
	mDisplayString [EBP+20]
	CALL	CrLf
	MOV		ECX, [EBP+16]
	MOV		ESI, [EBP+12]
	; Get the integer value of each item, push as value parameter to *WriteVal*. If this is the last item in the array, don't print a comma afterwards. Otherwise, print a comma and loop.
_printArray:
	MOV		EAX, [ESI]
	PUSH	EAX
	CALL	WriteVal
	CMP		ECX, 1
	JE		_skipComma
	mDisplayString [EBP+8]
_skipComma:
	ADD		ESI, 4
	LOOP	_printArray
	POPAD
	POP		EBP
	RET		16
printArray ENDP

; -----------------------------------------------------------------------
; Name: getSumAvg
;
; Function for finding the sum and average (rounded using floor rounding) of an array of integers and saving these to memory locations.
; 
; Preconditions: An array of valid integer values has been defined.
;
;					The following local variable is used:
;						currTotal: used to store the running total during summation
;
; Postconditions: None, all registers are saved and restored.
;
; Receives:
;		[EBP+20] = reference to array to find the sum and average of (in this case it is userValArr, an array that contains the integers entered by the user)
;		[EBP+16] = value of the number of items contained in the array (in this case it is the number of integers entered by the user)
;		[EBP+12] = reference to sumVals, a variable that will contain the value of the sum of the integers
;		[EBP+8] = reference to avgVals, a variable that will contain the average (using floor rounding) of the integers.
;
; Returns:
;		The array of integers is printed to the console.
; -----------------------------------------------------------------------
getSumAvg PROC
	LOCAL currTotal: SDWORD
	PUSHAD
	; Reset local variable to 0, set loop counter to the number of items in the array, set ESI to point to the beginning of the array
	MOV		currTotal, 0
	MOV		ECX, [EBP+16]
	MOV		ESI, [EBP+20]
	; Get the value of each item in the array, add to total
_sumTotal:
	MOV		EAX, [ESI]
	ADD		currTotal, EAX
	ADD		ESI, 4
	LOOP	_sumTotal
	; Set sumVals equal to the sum by indirect operand
	MOV		EAX, currTotal
	MOV		EBX, [EBP+12]
	MOV		[EBX], EAX
	; Set EBX equal to the number of items in the array and divide
	MOV		EBX, [EBP+16]
	CDQ
	IDIV	EBX
	; Set avgVals equal to the average (floor rounding) by indirect operand
	MOV		EBX, [EBP+8]
	MOV		[EBX], EAX
	POPAD
	RET		16
getSumAvg ENDP

; -----------------------------------------------------------------------
; Name: displayResults
;
; Function for printing the sum and average of an array of integers to the console. Uses the *WriteVal* subprocedure for printing integers.
; 
; Preconditions: Valid integer values for the sum and average have been passed as parameters to this function. *WriteVal* can only print integers that will fit in a 32 bit register without overflowing.
;
;					The following macro is used in the *WriteVal* subprocedure: 
;						mDisplayString (for displaying strings)
;
; Postconditions: None, all registers are saved and restored by the called procedures and macros.
;
; Receives:
;		[EBP+20] = reference to sumStr, a string to be printed before printing the sum of the integers.
;		[EBP+16] = value of sumVals, a variable containing the integer sum of the user-entered values
;		[EBP+12] = reference to avgStr, a string to be printed before printing the average of the integers
;		[EBP+8] = value of avgVals, a variable containing the average (using floor rounding) of the integers.
;
; Returns:
;		The sum and average of an array of integers is printed to the console with supporting strings.
; -----------------------------------------------------------------------
displayResults PROC
	PUSH	EBP
	MOV		EBP, ESP
	mDisplayString	[EBP+20]
	PUSH	[EBP+16]
	CALL	WriteVal	
	CALL	CrLf
	mDisplayString	[EBP+12]
	PUSH	[EBP+8]
	CALL	WriteVal
	POP		EBP
	RET		16
displayResults ENDP

; -----------------------------------------------------------------------
; Name: displayFarewell
;
; Function for printing a farewell message to the user.
; 
; Preconditions: The following macro is used: 
;						mDisplayString (for displaying strings)
;
; Postconditions: None, all registers used are saved and restored within the mDisplayString macro.
;
; Receives:
;		[EBP+8] = reference to farewellStr, a string containing a farewell message to the user
;
; Returns:
;		The farewell string is printed to the console.
; -----------------------------------------------------------------------
displayFarewell PROC
	PUSH	EBP
	MOV		EBP, ESP
	CALL	CrLf
	CALL	CrLf
	mDisplayString [EBP+8]
	POP		EBP
	RET		4
displayFarewell ENDP

END main
