from logic import * #import everything from logic.py

rain = Symbol("rain") # It is raining
hagrid = Symbol("hagrid") # Harry visited Hagrid
dumbledore = Symbol("dumbledore") # Harry visited Dumbledore

"""
EXAMPLE
If we have a sentence such as: 
sentence = And(rain, hagrid)

and we print it: 
print(sentence.formula())  # Output: (rain ∧ hagrid)
"""

knowledge = And(                     # I know multiple sentences: 
    Implication(Not(rain), hagrid),  # If it is not raining, Harry visited Hagrid -> (¬rain => hagrid)
    Or(hagrid, dumbledore),          # Harry visited Hagrid or Dumbledore -> (hagrid ∨ dumbledore)
    Not(And(hagrid, dumbledore)),    # Harry did not visit both Hagrid and Dumbledore -> ¬(hagrid ∧ Dumbledore)
    dumbledore                       # Harry visited Dumbledore -> dumbledore
)

print(model_check(knowledge, rain))
