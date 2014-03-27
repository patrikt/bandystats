#!/usr/bin/python

import pandas as pd
import numpy as np

df = pd.read_csv('data/merged.csv', sep="|", header=0, parse_dates=[0])
