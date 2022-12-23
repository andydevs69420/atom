import dis


code = """

try:
    2 + 2
    print()

except:
    2 + 2

"""

dis.dis(code)