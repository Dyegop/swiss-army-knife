import sys
import re
import os
import datetime
import json
import tkinter
import pyinputplus as pyip


# __call__ example:
class Example:
    def __init__(self):
        print("Instance Created")

    # Defining __call__ method
    def __call__(self):
        print("Instance is called via special method")


e = Example()
e()



