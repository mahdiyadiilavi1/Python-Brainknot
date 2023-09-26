def execute(filename):
  f = open(filename, "r")
  evaluate(f.read())
  f.close()


def evaluate(code,inputs,inptr=0,stack0=[0],cellptr=0,crbit=0):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)
  outputs = []
  codeptr = 0

  while codeptr < len(code):
    command = code[codeptr]
    tmp = 0
    if command == "+":
      stack0[cellptr] = crbit
      cellptr += 1
      if cellptr == len(stack0): stack0.append(0)

    if command == "-":
      crbit = stack0[cellptr]
      cellptr -= 1
    if command == "*":
      crbit = 1 - crbit
    if command == "(" and crbit == 0: codeptr = bracemap[codeptr]
    if command == ")" and crbit != 0: codeptr = bracemap[codeptr]
    if command == "<":
      outputs.append(str(crbit))
    if command == ">":
      if len(inputs)==inptr:
        return [stack0,cellptr,crbit,''.join(outputs)]
      crbit = int(inputs[inptr])
      inptr += 1
    if command == "[":
      if crbit == 1:
        for p,i in enumerate(code[codeptr+1:]):
          if i == "[":
            tmp += 1
          if i == "]":
            tmp -= 1
          if i == "," and tmp == 0:
            comma = p+codeptr+1
          if i in ["]",","] and tmp == -1:
            finish = p+codeptr+1
        stack0,codeptr,crbit,out = evaluate(code[codeptr+1:comma],inputs,inptr,stack0,cellptr,crbit)
        outputs.append(out)
      else:
        for p,i in enumerate(code[codeptr+1:]):
          if i == "[":
            tmp += 1
          if i == "]":
            tmp -= 1
          if i == "," and tmp == 0:
            comma = p+codeptr+1
          if i == "]" and tmp == -1:
            finish = p+codeptr+1
        stack0,codeptr,crbit,out = evaluate(code[comma:finish],inputs,inptr,stack0,cellptr,crbit)
        outputs.append(out)
      codeptr = finish-1
    codeptr += 1
  return [stack0,cellptr,crbit,''.join(outputs)]


def cleanup(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '*', '(', ')', '+', '-'], code))


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "(": temp_bracestack.append(position)
    if command == ")":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def main():
  while 1:
    code=input("Code:")
    if code != '':
      prevcode=code
    else:
      code=prevcode
    print("Output:",evaluate(code=code,inputs=input("Inputs:"))[3])

if __name__ == "__main__": main()
