"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # self.ram = [0] * 256  # memory/ram array
        self.reg = [0] * 8  # general purpose registers
        self.reg[5]  # reserved as the interrupt mask (IM)
        self.reg[6]  # reserved as interrupt status (IS)
        self.reg[7]  # reserved as stack pointer (SP)
        self.pc = 0  # program counter
        self.running = True
        self.opcode = {SAVE_REG: '0b10000010',
                       PRINT_REG: '0b01000111',
                       HALT: '0b00000001'}

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # instruction tells cpu to do an operation (load data)
            # From print8.ls8
            0b10000010,  # SAVE_REG LDI R0,8 //Save Reg? load immediately store a value in register
            # or set register to this value
            # this instruction gives the register number to load that info into
            0b00000000,  # 00000rrr : register number (REGISTER NUMBER)
            # this is the information to load (the number 8)
            0b00001000,  # iiiiiiii : 8-bit immediate value (VALUE)

            # this next instruction will print whatever is located
            # at next provided register number (reg[0])
            0b01000111,  # PRN R0
            0b00000000,
            # Once we advance the pc we'll hit HLT Op Code and terminate program.
            0b00000001,  # HLT
        ]
        # program = [0b10000010,  0b00000000,
        #            0b00001000, 0b01000111, 0b00000000, 0b00000001, ]

        program = [0] * 256
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # def load(filename):

    #     # open a file and load into memory
    #     address = 0

    #     # get file name from command line arguments
    #     if len(sys.argv) != 2:
    #         print("usage: example_cpu.py filename")
    #         sys.exit(1)
    #     try:
    #         with open(filename) as f:
    #             for line in f:
    #                 # split the current line on the # symbol
    #                 split_line = line.split("#")
    #                 # romoves whitespace and \n character
    #                 code_value = split_line[0].strip()
    #                 if code_value = "":
    #                     continue
    #                 num = int(code_value)
    #                 program[address] = num
    #                 address += 1
    #         except FileNotFoundError:
    #             print(f"{sys.argv[1]} file not found")
    #             sys.exit(2)

    def ram_read(self, mar):
        # should accept the addres to read and return the value stored there
        # mar is the address value
        # if else for length of ram vs length of mar
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        # should accept a value to write, and the address to write it to
        self.ram[mdr] = mar

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if opcode == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        # elif opcode == "AND"
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # while true
        # if else statements
        # use functions to make code cleaner - lots to add in run function
        # day 1 - just print numbers. Save number into register, then print it out
        while self.running:
            # Read line by line from memory
            instruction = program[self.pc]
            if instruction == opcode[SAVE_REG]:
                # Save some value to some register
                # First number after instruction will be the Value to store
                # second number after instruction will be register
                num = program[self.pc + 2]
                reg_location = program[self.pc + 1]
                self.reg[reg_location] = num
                self.pc += 3

            elif instruction == opcode[PRINT_REG]:
                reg_location = program[self.pc + 1]
                print(self.reg[reg_location])
                self.pc += 2

            elif instruction == opcode[HLT]:
                self.running = False
                self.pc += 1

            else:
                print("Unknown instruction {instruction}")
                sys.exit(1)
