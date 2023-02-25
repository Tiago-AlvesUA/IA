from bayes_net import *

bn = BayesNet()

variables = ['sc', 'pt', 'cp', 'fr', 'pa', 'cnl']


bn.add('pt',[],0.05)
bn.add('sc',[],0.60)

bn.add('pa',[('pt',True)], 0.25)
bn.add('pa',[('pt',False)], 0.004)

bn.add('cnl',[('sc',True)],0.9)
bn.add('cnl',[('sc',False)],0.001)

bn.add('fr',[('pt',True),('pa',True)],0.9)
bn.add('fr',[('pt',True),('pa',False)],0.9)
bn.add('fr',[('pt',False),('pa',True)],0.1)
bn.add('fr',[('pt',False),('pa',False)],0.01)

bn.add('cp',[('pa',True),('sc',True)],0.02)
bn.add('cp',[('pa',False),('sc',True)],0.01)
bn.add('cp',[('pa',True),('sc',False)],0.011)
bn.add('cp',[('pa',False),('sc',False)],0.001)

# bn.add('r',[],0.001)
# bn.add('t',[],0.002)

# bn.add('a',[('r',True ),('t',True )],0.950)
# bn.add('a',[('r',True ),('t',False)],0.940)
# bn.add('a',[('r',False),('t',True )],0.290)
# bn.add('a',[('r',False),('t',False)],0.001)

# bn.add('j',[('a',True )],0.900)
# bn.add('j',[('a',False)],0.050)

# bn.add('m',[('a',True )],0.700)
# bn.add('m',[('a',False)],0.100)

# conjunction = [('j',True),('m',True),('a',True),('r',False),('t',False)]

# print(bn.jointProb(conjunction))