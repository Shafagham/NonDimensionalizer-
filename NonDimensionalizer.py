import re
import numpy

String = '4*pi*rho^3*v*dTOd(T,x) + 4*rho*pi*mu*r^2*lambda*T'
TermSplitPattern = '(\+|\-)' # split each term of the equation with + or -
TermSplitPattern_1 = '\+|\-' # split each term of the equation with + or - but do not keep the sign
CrossSplitPattern = '(\*|\/)' #'[^\*]\*[^\*]' 
PowerPattern = '\^'
FractionPattern = '\/'
ArgsDict = {
        'rho' : numpy.array([1, -3, 0, 0, 0, 0, 0]), #[kg m s K A mol Cd]
        'nu' : numpy.array([0, 2, -1, 0, 0, 0, 0]), # momentum diffusivity
        'v' : numpy.array([0, 1, -1, 0, 0, 0, 0]), # Velocity
        'L' : numpy.array([0, 1, 0, 0, 0, 0, 0]), # characteristic length
        'd' : numpy.array([0, 1, 0, 0, 0, 0, 0]), # characteristic length
        'mu' : numpy.array([1, -1, -1, 0, 0, 0, 0]), # viscosity
        'c_p' : numpy.array([0, 2, -2, -1, 0, 0, 0]), # specific heat capacity
        'C_p' : numpy.array([1, 2, -2, -1, 0, 0, 0]), # heat capacity
        'lambda' : numpy.array([1, 1, -3, -1, 0, 0, 0]), # Thermal conductivity
        'alpha' : numpy.array([0, 2, 1, 0, 0, 0, 0]), # Thermal Diffusivity Coefficient
        'r' : numpy.array([0, 1, 0, 0, 0, 0, 0]),
        'D' : numpy.array([0, 2, -1, 0, 0, 0, 0]), # Diffusivity Coefficient
        'omega' : numpy.array([1, 5, 0, 0, 0, 0, 0]),
        'tetta' : numpy.array([1, 6, 0, 0, 0, 0, 0])
        }
Termarray = numpy.array([0, 0, 0, 0, 0, 0, 0])
NonDimArgs = {
        'Re' : numpy.array ([[1, -3, 0, 0, 0, 0, 0],
                             [0, 1, -1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0],
                             [-1, 1, 1, 0, 0, 0, 0],
                             [1, 1, 1, -1, 0, 0, 0]
                             ]),
        'Pe' : numpy.array ([[0, 1, 0, 0, 0, 0, 0],
                             [0, 1, -1, 0, 0, 0, 0],
                             [0, -2, 1, 0, 0, 0, 0],
                             [1, 1, -1, 0, 0, 0, 0]
                             ]),
        'Pr' : numpy.array ([[0, 2, -1, 0, 0, 0, 0],
                             [0, -2, 1, 0, 0, 0, 0],
                             [1, -1, 0, 0, 0, 0, 0]
                             ]),
        'Pra' : numpy.array ([[1, 2, -2, -1, 0, 0, 0],
                              [1, -1, -1, 0, 0, 0, 0],
                              [-1, -1, 3, 1, 0, 0, 0],
                              [1, 1, -1, 0, 0, 0, 0]
                              ]),
        'Le' : numpy.array ([[0, 2, 1, 0, 0, 0, 0],
                             [0, -2, -1, 0, 0, 0, 0],
                             [1, -1, 0, 0, 0, 0, 0]
                             ]),
        'Lew' : numpy.array ([[1, 1, -3, -1, 0, 0, 0],
                              [-1, 3, 0, 0, 0, 0, 0],
                              [0, -2, 1, 0, 0, 0, 0],
                              [0, -2, 2, 1, 0, 0, 0],
                              [1, -1, -1, -1, 0, 0, 0 ]
                              ]),
        'Sch' : numpy.array ([[0, 2, -1, 0, 0, 0, 0],
                              [0, -2, 1, 0, 0, 0, 0],
                              [1, -1, 0, 0, 0, 0, 0]
                              ]),
        'sch' : numpy.array ([[1, -1, -1, 0, 0, 0, 0],
                              [-1, 3, 0, 0, 0, 0, 0],
                              [0, -2, 1, 0, 0, 0, 0],
                              [1, -1, -1, 0, 0, 0, 0]
                              ])
        }
SplitedResult_1 = re.split(TermSplitPattern, String)
SplitedResult = re.split(TermSplitPattern_1, String)
#print ( SplitedResult)
i = -1 # Term Counter initialization
TermArray = [0]*len(SplitedResult)
Bonusdictionary = dict((name,[0]*len(SplitedResult)) for name in NonDimArgs.keys())
DenominatorBonusdictionary = dict((name,[0]*len(SplitedResult)) for name in NonDimArgs.keys())
ExpectedBonusdictionary = {name:len(val)-1 for name, val in NonDimArgs.items()}

# Carving inside each term
for Args in SplitedResult:
    i += 1
    j = -1
    SplitedArgs = re.split(CrossSplitPattern, Args)
    #print ( SplitedArgs)
    Temp_NonDimArgs = NonDimArgs
    Temp_Denominator_NonDimArgs = NonDimArgs
    for array in SplitedArgs:
        j += 1

        # Power
        if re.findall(PowerPattern, SplitedArgs[j]):
            PowerSplitedArg = re.split(PowerPattern, SplitedArgs[j])
            SplitedArgs[j] = PowerSplitedArg [0]
            Power = PowerSplitedArg [1]
            ArgsDict[SplitedArgs[j]] = ArgsDict[SplitedArgs[j]] * int(Power)

        # Fraction
        if re.findall(FractionPattern, SplitedArgs[j]):
            #print(ArgsDict[SplitedArgs[j+1]])
            ArgsDict[SplitedArgs[j+1]] = ArgsDict[SplitedArgs[j+1]] * -1
            #print(ArgsDict[SplitedArgs[j+1]])
        
        if SplitedArgs[j] in ArgsDict:
            
            # Finding potential Numbers:
            for name in Temp_NonDimArgs.keys():
                if list(ArgsDict[SplitedArgs[j]]) in Temp_NonDimArgs.get(name).tolist():
                    Bonusdictionary[name][i] += 1
                    x = Temp_NonDimArgs.get(name).tolist()
                    x.remove(list(ArgsDict[SplitedArgs[j]]))
                    Temp_NonDimArgs[name]=numpy.array(x)
                    #print (Temp_NonDimArgs)
                #print (Bonusdictionary)
        
        # Checking to see if any arg is in denominator
            for name in Temp_Denominator_NonDimArgs.keys():
                if list(-ArgsDict[SplitedArgs[j]]) in Temp_Denominator_NonDimArgs.get(name).tolist():
                    DenominatorBonusdictionary[name][i] += 1
                    x = Temp_Denominator_NonDimArgs.get(name).tolist()
                    x.remove(list(-ArgsDict[SplitedArgs[j]]))
                    Temp_Denominator_NonDimArgs[name]=numpy.array(x)
                    #print (Temp_NonDimArgs)
                #print (DenominatorBonusdictionary)
                    
                    
            # Summing up Dimension matrix
            Termarray = Termarray + ArgsDict[SplitedArgs[j]]
            TermArray[i] = Termarray.tolist()
#print (TermArray)
print (Bonusdictionary)
print (DenominatorBonusdictionary)
