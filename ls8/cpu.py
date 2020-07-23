"""CPU functionality."""

import sys
LDI = 0b10000010 
PRN = 0b01000111 
HLT = 0b00000001 
MUL = 0b10100010 
PUSH = 0b01000101
POP = 0b01000110 
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0 
        self.running = True
        self.reg = [0] * 8
        self.reg[SP] = 0xf4
        self.branch_table = {
            LDI: self.ldi,
            PRN: self.prn,
            HLT: self.hlt,
            MUL: self.mul,
            PUSH: self.push,
            POP: self.pop,
        }

    def mul(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def hlt(self):
        self.pc += 1
        self.running = False

    def prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print("PRN:", self.reg_read(reg_num))
        self.pc += 2

    def ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        reg_val = self.ram_read(self.pc + 2)
        self.reg_write(reg_num, reg_val)
        self.pc += 3

    def push(self):
        self.reg[SP] -= 1
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        top_of_stack_addr = self.reg[SP]
        self.ram[top_of_stack_addr] = value
        self.pc += 2

    def pop(self):
        top_stack_val = self.reg[SP]
        reg_addr = self.ram[self.pc + 1]
        self.reg[reg_addr] = self.ram[self.reg[SP]]
        self.reg[SP] += 1
        self.pc += 2

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as f:
            for line in f:
                line = line.split('#')

                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue

                self.ram[address] = v

                address += 1

        # hardcoded program:
        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def ram_read(self, mar):
        mar_reg = self.ram[mar]
        return mar_reg

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr 

    def reg_read(self, mar):
        mar_reg = self.reg[mar]  
        return mar_reg

    def reg_write(self, mar, mdr):
        self.reg[mar] = mdr
    def run(self):
        while self.running:
            ir = self.ram[self.pc]

            if ir in self.branch_table:
                self.branch_table[ir]()

            else:
                print(f"Unknown expression {ir} at address {self.pc}")
                sys.exit(1)