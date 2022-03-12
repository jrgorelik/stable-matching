'''
This is a simple one function implementation of the basic Gale-Shapley algorithm.
It uses traditional terminology with men proposing and women accepting
These terms do not represent any political beliefs and is meant to
align with terms used in Coursera and other spaces
'''

def stableMatching(n, menPreferences, womenPreferences):
    '''
    The main function that performs stable matching according to the Gale-Shapley
    algorithm
    
    paramaters:
    n int: The number of couples you are matching
    menPrefernces list: a list of lists containing the preferences of the men in
    order such that the first list is the first man's prefernce, the following
    list is the second man's preference, and so on
    womenPrefernces list: a list of lists that is the mirror of menPreferences
    
    return:
    menSpouse: list which man is assigned to which woman
    '''
    
    unmarriedMen = [True]*n
    first_unmarried = 0
    manSpouse = [-1]*n
    womanSpouse = [-1]*n
    nextManChoice = menPreferences.copy()
    

    while sum(unmarriedMen)>0:
        #tracking how many men are unmarried and which one is the first unmarried in the list
        first_unmarried = unmarriedMen.index(True)
        
        for man_choice in nextManChoice.copy()[first_unmarried]:
            wanted_woman = man_choice
            #-1 indicates that the man or woman is not matched
            if womanSpouse[wanted_woman]==-1:
                manSpouse[first_unmarried] = wanted_woman
                womanSpouse[wanted_woman] = first_unmarried
                unmarriedMen[first_unmarried] = False
                nextManChoice[first_unmarried] = nextManChoice[first_unmarried][1:]
                break
            elif womanSpouse[wanted_woman]!=-1:
                #seeing if the women prefers the new man more
                if womenPreferences[wanted_woman].index(first_unmarried) < womenPreferences[wanted_woman].index(womanSpouse[wanted_woman]):
                    manSpouse[womanSpouse[wanted_woman]] = -1
                    unmarriedMen[womanSpouse[wanted_woman]] = True
                    manSpouse[first_unmarried] = wanted_woman
                    unmarriedMen[first_unmarried] = False
                    nextManChoice[first_unmarried] = nextManChoice[first_unmarried][1:]
                    womanSpouse[wanted_woman] = first_unmarried
                    break
                else:
                    nextManChoice[first_unmarried] = nextManChoice[first_unmarried][1:]
            else:
                print("You aren't even supposed to be here today")
        
    return manSpouse