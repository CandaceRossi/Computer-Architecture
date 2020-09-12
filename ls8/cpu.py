"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # memory/ram array
        self.reg = [0] * 8  # general purpose registers
        self.reg[SP] = 0xF4  # assign stack pointer
        self.pc = 0  # program counter
        self.running = True
        self.flag = 0b00000000
        self.branchtable = {LDI: self.ldi,
                            PRN: self.prn,
                            MUL: self.mul,
                            ADD: self.add,
                            PUSH: self.push,
                            POP: self.pop,
                            # CALL: self.call,
                            # RET: self.ret
                            }

    def ram_read(self, mar):
        # should accept the addres to read and return the value stored there
        # mar is the address value
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        # should accept a value to write, and the address to write it to
        self.ram[mdr] = mar

    def push(self, operand_a, operand_b):
        given_register = self.ram[self.pc + 1]
        value_in_register = self.reg[given_register]
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = value_in_register
        self.pc += 2

    def pop(self, operand_a, _):
        given_register = self.ram[self.pc + 1]
        value_from_ram = self.ram[self.reg[SP]]
        self.reg[given_register] = value_from_ram
        self.reg[SP] += 1
        self.pc += 2

    # def call(self, operand_a, operand_b):
    #     given_register = self.ram[self.pc + 1]
    #     self.reg[SP] -= 1
    #     self.ram[self.reg[SP]] = self.pc + 2
    #     self.pc = self.reg[given_register]

    # def ret(self, operand_a, _):
    #     self.pc = self.ram[self.reg[SP]]
    #     self.reg[SP] += 1

    def alu(self, opcode, reg_a, reg_b):
        """ALU operations."""

        if opcode == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        # elif opcode == "AND"
        elif opcode == "CMP":
            self.fl &= 0b00000000
            # fl bits 00000LGE
            if self.reg[reg_a] == self.reg[reg_b]:
                # set E flag to 1
                self.fl = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                # set L flag to 1
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                # set G flag to 1
                self.fl = 0b00000010

        else:
            raise Exception("Unsupported ALU operation")
        self.pc += 3

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

    def load(self):
        if len(sys.argv) != 2:
            print("usage: example_cpu.py filename")
            sys.exit(1)
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                split_line = line.split("#")
                code_value = split_line[0].strip()
                if code_value == "":
                    continue
                num = code_value
                self.ram[address] = int(num, 2)
                address += 1
        # print(self.ram)

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def prn(self, operand_a, _):
        print(self.reg[operand_a])
        self.pc += 2

    def mul(self, operand_a, operand_b):
        print(self.reg[operand_a] * self.reg[operand_b])
        self.pc += 3

    def add(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)

    def run(self):
        # self.load()
        while self.running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if ir in self.branchtable:
                self.branchtable[ir](operand_a, operand_b)
            elif ir == PUSH:
                self.push(operand_a, _)
            elif ir == POP:
                self.pop(operand_a, reg_a)
            elif ir == HLT:
                self.running = False
                sys.exit()
            else:
                raise Exception("Unsupported operation")
