#! /usr/bin/env python
# -*- coding: utf-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Breeze adapter module for XXXX.

"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# configuration

import os, sys
DIR_THIS = os.path.dirname(os.path.abspath(__file__))
DIR_HOME = os.path.dirname(DIR_THIS)
sys.path.append(DIR_HOME)

# current adapter server port, starts from 8601
PORT = 8600

# python encoding for arguments and returns
ENCODING_PY = 'utf-8'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# API functions

def getSum(nA, nB):
    r"""返回两个数的和
    """
    return {"sum":nA+nB}
    