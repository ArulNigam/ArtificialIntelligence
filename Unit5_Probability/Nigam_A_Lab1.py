# Arul Nigam
# Period 3

from pomegranate import *

Graduation = DiscreteDistribution({'graduation': 0.9, 'no-graduation': 0.1}) # given base probabilities

Tester1 = ConditionalProbabilityTable([ # conditional table for offer_1
    ['graduation', 'o1', 0.5],
    ['graduation', 'no_o1', 0.5],
    ['no-graduation', 'o1', 0.05],
    ['no-graduation', 'no_o1', 0.95]], [Graduation])

Tester2 = ConditionalProbabilityTable([ # conditional table for offer_2
    ['graduation', 'o2', 0.75],
    ['graduation', 'no_o2', 0.25],
    ['no-graduation', 'o2', 0.25],
    ['no-graduation', 'no_o2', 0.75]], [Graduation])

s_graduation = State(Graduation, 'graduate')
s_offer_1 = State(Tester1, 'offer_1')
s_offer_2 = State(Tester2, 'offer_2')

model = BayesianNetwork('graduate')

model.add_states(s_graduation, s_offer_1, s_offer_2)

model.add_transition(s_graduation, s_offer_1)
model.add_transition(s_graduation, s_offer_2)

model.bake()  # finalize the topology of the model

# predict_proba(Given factors)

print("Pop Quiz:")
print()
print("a) P(o2 | g, ~o1) = ", model.predict_proba({'graduate':'graduation', 'offer_1':'o1'})[2].parameters[0]['o2'])
print("b) P(g | o1, o2) = ", model.predict_proba({'offer_1':'o1', 'offer_2':'o2'})[0].parameters[0]['graduation'])
print("c) P(g | ~o1, o2) = ", model.predict_proba({'offer_1':'no_o1', 'offer_2':'o2'})[0].parameters[0]['graduation'])
print("d) P(g | ~o1, ~o2) = ", model.predict_proba({'offer_1':'no_o1', 'offer_2':'no_o2'})[0].parameters[0]['graduation'])
print("e) P(o2 | o1) = ", model.predict_proba({'offer_1':'o1'})[2].parameters[0]['o2'])

#########################################################################################################################################

Sunniness = DiscreteDistribution({'sunny': 0.7, 'not_sunny': 0.3}) # given base probabilities
Raise = DiscreteDistribution({'raise': 0.01, 'no_raise': 0.99}) # given base probabilities

Tester = ConditionalProbabilityTable([ # conditional table for happiness
    ['sunny', 'raise', 'happy', 1],
    ['sunny', 'no_raise', 'happy', 0.7],
    ['not_sunny', 'raise', 'happy', 0.9],
    ['not_sunny', 'no_raise', 'happy', 0.1],
    ['sunny', 'raise', 'not_happy', 0],
    ['sunny', 'no_raise', 'not_happy', 0.3],
    ['not_sunny', 'raise', 'not_happy', 0.1],
    ['not_sunny', 'no_raise', 'not_happy', 0.9]], [Sunniness, Raise])


s_sunniness = State(Sunniness, 'sunny')
s_raise = State(Raise, 'raise')
s_happy = State(Tester, 'happiness')

model = BayesianNetwork('happy')

model.add_states(s_sunniness, s_raise, s_happy)

model.add_transition(s_sunniness, s_happy)
model.add_transition(s_raise, s_happy)

model.bake()  # finalize the topology of the model

# predict_proba(Given factors)

print()
print("Day 2 Example 3:")
print()
print("a) P(r | s) = ", model.predict_proba({'sunny':'sunny'})[1].parameters[0]['raise'])
print("b) P(r | h, s) = ", model.predict_proba({'happiness':'happy', 'sunny':'sunny'})[1].parameters[0]['raise'])
print("c) P(r | h) = ", model.predict_proba({'happiness':'happy'})[1].parameters[0]['raise'])
print("d) P(r | h, ~s) = ", model.predict_proba({'happiness':'happy', 'sunny':'not_sunny'})[1].parameters[0]['raise'])
