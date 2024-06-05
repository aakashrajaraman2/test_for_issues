import issues_modular
import os 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="cred.json"
example = '''
def factorial(number):

  if number < 0:
    return "Factorial is not defined for negative numbers"
  factorial = 1
  for i in range(1, number + 1):
    factorial *= i
  return factorial
'''

print(issues_modular.predict(example))