'''
    Copyright (C) 2020, Sathira Silva
    
    Problem Statement:  https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b62
    
    Approach:   Since the size of the ith jump is 2^(i - 1), the easiest way to think about the problem is in binary numbers. So the
    problem can be broken down into jumping between the digits of the binary representation of sum of the coordinates until we reach 
    the MSB (Most Significant Bit). Since the smallest size of a jump is 1, the LSB (Least Significant Bit) of the sum, which is the 
    initial jump must be set (1) in order to reach the goal (X, Y) from (0, 0), because we always have to make a jump of size 
    2 ^ (i - 1) (2 ^ (1 - 1) = 1 in this case) in order to make the next jump (i.e. the sum must be odd). Therefore, if the sum is
    even, we terminate because reaching the goal from (0, 0) is impossible.
    
    Otherwise, the problem can be solved by backtracking. The first thing we have to do when we're at digit position j is to guess the
    direction of the move we've to make. So we try all the directions possible because there's only one such jump in each horizontal
    and vertical directions. Then, we check whether the next jump is possible due to the previous jump and pick the one that's possible.
    Since we're traversing backwards from the MSB, a jump is actually a reduction in the target coordinates (We start from (X, Y)
    and traverse until we hit (0, 0)). Thus, if the next target is reachable after the current jump, we reduce the jump from the
    coordinate in the respective direction. Otherwise, we increment the coordinate by the current jump so that we can make that jump
    in the future.
'''


import math


def move(currentbit, x, y):
    global result
    if currentbit == -1:
        return
    for direction in ['N', 'E', 'S', 'W']:
        next_x = jump_x(currentbit, x, direction)
        next_y = jump_y(currentbit, y, direction)
        # Check if the next jump is possible after the jump in the current direction.
        if can(currentbit - 1, abs(next_x) + abs(next_y)):
            # If possible, move to the next target.
            move(currentbit - 1, next_x, next_y)
            # Build the solution incrementally using backtracking.
            result += direction
            break
            
            
def can(currentbit, target):
    # (1 << (currentbit + 1)) - 1 is the maximum that the target can get.
    return target <= (1 << (currentbit + 1)) - 1


def jump_x(currentbit, x, direction):
    # Since we're traversing backwards, a decrement in x means the jump is in the positive direction.
    # An increment means the jump is in the negative direction.
    if direction == 'W':
        x += 1 << currentbit
    if direction == 'E':
        x -= 1 << currentbit
    return x


def jump_y(currentbit, y, direction):
    if direction == 'S':
        y += 1 << currentbit
    if direction == 'N':
        y -= 1 << currentbit
    return y


if __name__ == '__main__':
    T = int(input())
    for x in range(1, T + 1):
        X, Y = map(int, input().split())
        result = ''
        goal = abs(X) + abs(Y)
        if goal % 2 != 0:
            # The Most Significant Bit of a number is the floor of the log base 2 of that number.
            # Proof:
            #   Let position of MSB of n be x.
            #   Therefore, n can be written as, n = 2 ^ x + y, where y is the remaining sum of the values of the bits below MSB.
            #   Thus, taking log base 2 of both sides, log2(n) = log2(2 ^ x + y)
            #   But, 2 ^ x >>> y and x is an integer.
            #   Therefore, log2(2 ^ x) = floor(log2(n))
            #   =>  x = floor(log2(n))
            msb = int(math.log(goal, 2))
            move(msb, X, Y)
        else:
            result = 'IMPOSSIBLE'
        print('Case #{0}: {1}'.format(x, result))
