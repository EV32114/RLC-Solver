import math
import cmath
import sys
from math import pi


def print_complex(name, number, unit):
    print('{0}: {1}, phase: {2} [{3}]'.format(name, abs(number), math.degrees(cmath.phase(number)), unit))


def get_input():
    x = 0
    comp_list = []
    print('R. add a resistor')
    print('L. add an inductor')
    print('C. add a capacitor')
    print('S. start calculations')
    while x != 'S':
        x = input()
        if x == 'S':
            break
        val = float(input('Enter value: '))
        comp_list.append([x, val])
        print('Enter another component')
    return comp_list


def main():
    print('Welcome to the RLC calculator!\n')
    max_v = float(input('Enter max voltage: '))
    phase = float(input('Enter source phase: '))
    if len(sys.argv) > 1:
        if sys.argv[1] == 'R':
            freq = 0
        else:
            raise ValueError
    else:
        freq = float(input('Enter frequency: '))
    comp_list = get_input()
    circuit_type = input('finally, is the circuit [S]eries or [P]arallel: ')
    calculate(cmath.rect(max_v, math.radians(phase)), freq, comp_list, circuit_type, freq == 0)


def calc_freq(comp):
    C = 0
    L = 0
    for c in comp:
        if c[0] == 'L':
            L = c[1]
        elif c[0] == 'C':
            C = c[1]
    return 1/(2*pi*math.sqrt(L*C))


def calculate(source: complex, freq: float, comp: list, circuit_type, resonance):
    if circuit_type != 'S' and circuit_type != 'P':
        raise ValueError
    L = 0
    R = 0
    if resonance:
        freq = calc_freq(comp)
        print('f0: {0} [Hz]'.format(freq))
    print('w: {0} [rad/sec]'.format(2*pi*freq))
    for c in comp:
        if c[0] == 'R':
            c.append(c[1])
            R = c[1]
        elif c[0] == 'L':
            c.append(2 * pi * freq * c[1] * 1j)
            L = c[1]
            print_complex('Xl', c[2], 'Ohm')
        elif c[0] == 'C':
            c.append(1 / (2 * pi * freq * c[1]) * -1j)
            print_complex('Xc', c[2], 'Ohm')
        else:
            raise ValueError

    circuit_type = circuit_type == 'S'
    if circuit_type:
        z = sum([c[2] for c in comp])
    else:
        z = sum([1/c[2] for c in comp])
        z = 1/z
    i = source / z
    print_complex('Z', z, 'Ohm')
    print_complex('I', i, 'A')
    pt = 0.0
    for c in comp:
        x = i * c[2] if circuit_type else source / c[2]
        p = pow(abs(i if circuit_type else x) / math.sqrt(2), 2) * c[2]
        pt += p
        print_complex(('U' if circuit_type else 'I') + c[0], x, 'V' if circuit_type else 'A')
        print_complex('P' + c[0], p, 'W' if cmath.phase(p) == 0 else 'VAR')
    print_complex('S', pt, 'VA')
    print_complex('Veff', abs(source) / math.sqrt(2), 'V')
    print_complex('Ieff', abs(i) / math.sqrt(2), 'A')
    if resonance:
        if circuit_type:
            Q = (2*pi*freq*L)/R
        else:
            Q = R/(2*pi*freq*L)
        BW = freq/Q
        print('Q: {0}'.format(Q))
        print('BW: {0} [Hz]'.format(BW))
        print('f1: {0} [Hz]'.format(freq - BW*0.5))
        print('f2: {0} [Hz]'.format(freq + BW*0.5))


if __name__ == '__main__':
    main()
