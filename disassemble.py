#!/usr/bin/env python2
from sys import argv
from capstone import *

# ./disassemble.py x86 64 '\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05'
# len = 23
# 0x1000: xor     esi, esi
# 0x1002: movabs  rbx, 0x68732f2f6e69622f
# 0x100c: push    rsi
# 0x100d: push    rbx
# 0x100e: push    rsp
# 0x100f: pop     rdi
# 0x1010: push    0x3b
# 0x1012: pop     rax
# 0x1013: xor     edx, edx
# 0x1015: syscall


CODE = argv[3].replace('\\x', '').decode('hex')
print 'len =', len(CODE)

ARCH = {
    'all': CS_ARCH_ALL,
    'arm': CS_ARCH_ARM,
    'arm64': CS_ARCH_ARM64,
    'mips': CS_ARCH_MIPS,
    'ppc': CS_ARCH_PPC,
    'x86': CS_ARCH_X86,
    'xcore': CS_ARCH_XCORE
}

MODE = {
    '16': CS_MODE_16,
    '32': CS_MODE_32,
    '64': CS_MODE_64,
    'arm': CS_MODE_ARM,
    'be': CS_MODE_BIG_ENDIAN,
    'le': CS_MODE_LITTLE_ENDIAN,
    'micro': CS_MODE_MICRO,
    'thumb': CS_MODE_THUMB
}

md = Cs(ARCH[argv[1]], MODE[argv[2]])
for i in md.disasm(CODE, 0x1000):
    print '0x%x:\t%s\t%s' % (i.address, i.mnemonic, i.op_str)


