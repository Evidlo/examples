#!/usr/bin/env python3

import numpy as np

"""
Challenge by Sam

64 coins in random state with a key under 1 of them.

1. Prisoner 1 knows where the key is.  He is allowed to flip a single coin.
2. Prisoner 2 must look at the coins afterwards and determine where the key is.
"""

def coinhash(coins):
    """Special hash for coins
    Args:
        coins (ndarray): numpy array containing 0 or 1

    Returns:
        int: hash of coins
    """
    if type(coins) is not np.ndarray:
        coins = np.array(coins)
    firsthalf = slice(1, (len(coins) + 1) // 2)
    secondhalf = slice(len(coins) // 2 + 1, None)
    xor = np.ones_like(coins)
    xor[secondhalf] = -2 * ~np.logical_xor(coins[firsthalf], np.flip(coins[secondhalf])) + 1
    print(xor)
    return np.sum(coins * xor * np.arange(len(coins))) % len(coins)

def whichflip(coins, keypos):
    """Compute which coin to flip given current coin configuration and key position
    Args:
        coins (ndarray): numpy array containing 0 or 1
        keypos (int): an integer denoting key position in range [0, len(coins)-1]

    Returns:
        int: position of coin to flip
    """
    diff = keypos - coinhash(coins)
    if ((diff < 0) and coins[np.abs(diff)]) or ((diff >= 0) and not coins[np.abs(diff)]):
        return np.abs(diff)
    else:
        return len(coins) - np.abs(diff)


# if __name__ == '__main__':
#     num_coins = 8
#     coins = np.random.randint(2, size=num_coins)
#     print(coins)
#     keypos = np.random.randint(num_coins)

#     print('secret key position:', keypos)

#     # flip a single coin
#     flip_coin = whichflip(coins, keypos)
#     coins[flip_coin] = 1 - coins[flip_coin]

#     print('computed key position:', coinhash(coins))
