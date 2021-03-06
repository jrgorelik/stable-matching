'''
This is a simple one function implementation of the Irving's stable roommates algorithm.  
There are some modifications that occurred after the original formulation (such as in a
1989 textbook) which are given as togglable options.  Some of the togglable options are built using
snippets of code from the python matching package as there is no easy way to find the
source text in its entirety online.

This code is currently under construction.  I am actively debugging in order to ensure that in works
in every subcase that exists.
'''

import pickle

def phase1(n,roommatePreferences,verbose=True):
    '''
    The part of the function that corresponds most closely to the Gale-Shapley stable marriage
    algorithm.  Unlike Gale-Shapley, this only takes one set of preferences though and n 
    must be an even number.
    
    paramaters:
    n int: The number of roommates we are matching.  This must be even otherwise there will be
    an error
    roommatePreferences list of lists: A list of length n containing lists of length n-1 with
    the indices of the other roommates in order of preference
    verbose bool: Whether or not you would like step by step output
    
    return:
    roommate_has_forward_match list: A list containing which roommate the roommate corresponding
    to that index asked
    roommate_has_backward_match list: A list containing which roommate asked the corresponding
    indexed roommate
    next_roommate_choice list of lists: A slightly different version of preference list that
    is used only for debugging.  Can be considered as a relic of the Gale-Shapley
    implementation
    preference_list list of lists: The list of lists corresponding to the remaining available
    preferences for each roommate
    '''
    
    unmatched_forward_mates = [True]*n
    unmatched_backward_mates = [True]*n
    first_unmatched = 0
    roommate_has_forward_match = [-1]*n
    roommate_has_backward_match = [-1]*n
    
    #I have been using pickle since .copy() was giving issues (creating deep copies instead
    #of shallow ones
    next_roommate_choice = pickle.loads(pickle.dumps(roommatePreferences))
    
    #These two entries are for a quick debugging hack 
    preference_list = pickle.loads(pickle.dumps(roommatePreferences))
    spare_prefs = pickle.loads(pickle.dumps(roommatePreferences))
    
    #Phase 1 will terminate when there are no more options for a roommate
    while sum(unmatched_forward_mates)>0:
        if any([x==[] for x in preference_list]):
            raise ValueError("There are no preferences remaining for one of the roommates")
        first_unmatched = unmatched_forward_mates.index(True)

        if verbose:
            print(preference_list)
        
        for roommate_choice in next_roommate_choice[first_unmatched]:
            wanted_mate = roommate_choice
            #if the the wanted mate has no existing pair
            if roommate_has_backward_match[wanted_mate]==-1:
                roommate_has_forward_match[first_unmatched] = wanted_mate
                roommate_has_backward_match[wanted_mate] = first_unmatched
                unmatched_forward_mates[first_unmatched] = False
                unmatched_backward_mates[wanted_mate] = False
                next_roommate_choice[first_unmatched] = next_roommate_choice[first_unmatched][1:]
                #may need to have removal of match from wanted_mate.  This is a continued area of 
                #debugging
                break
            #if the roommate does have an existing pair
            elif roommate_has_backward_match[wanted_mate]!=-1:
                if roommate_has_backward_match[wanted_mate] not in next_roommate_choice[wanted_mate]:
                    next_roommate_choice[wanted_mate] = preference_list[wanted_mate]
                    #below is code to flip on if there continues to be issues surrounding preference list
                    #vs new_roommate_choice
                    #if roommate_has_backward_match[wanted_mate] not in next_roommate_choice[wanted_mate]:
                        #next_roommate_choice[wanted_mate] = spare_prefs[wanted_mate]
                if first_unmatched not in next_roommate_choice[wanted_mate]:
                    next_roommate_choice[wanted_mate] = preference_list[wanted_mate]
                if first_unmatched not in next_roommate_choice[wanted_mate]:
                    next_roommate_choice[first_unmatched] = next_roommate_choice[first_unmatched][1:]
                    preference_list = preference_list.copy()
                    preference_list[wanted_mate].remove(first_unmatched)
                    preference_list[first_unmatched].remove(wanted_mate)
                # if the new roommate that wants to pair is not preferred over the existing pairing
                else:
                    if next_roommate_choice[wanted_mate].index(first_unmatched) < next_roommate_choice[wanted_mate].index(roommate_has_backward_match[wanted_mate]):
                        preference_list[wanted_mate].remove(roommate_has_backward_match[wanted_mate])
                        preference_list[roommate_has_backward_match[wanted_mate]].remove(wanted_mate)
                        roommate_has_forward_match[roommate_has_backward_match[wanted_mate]] = -1
                        unmatched_forward_mates[roommate_has_backward_match[wanted_mate]] = True
                        roommate_has_forward_match[first_unmatched] = wanted_mate
                        unmatched_forward_mates[first_unmatched] = False
                        next_roommate_choice[first_unmatched] = next_roommate_choice[first_unmatched][1:]
                        roommate_has_backward_match[wanted_mate] = first_unmatched
                        break
                    else:
                        next_roommate_choice[first_unmatched] = next_roommate_choice[first_unmatched][1:]
                        preference_list = preference_list.copy()
                        preference_list[wanted_mate].remove(first_unmatched)
                        preference_list[first_unmatched].remove(wanted_mate)
            else:
                #will be replaced with a specific error message in the future
                print("You aren't supposed to be here")
        
    return roommate_has_forward_match, roommate_has_backward_match, next_roommate_choice, preference_list

def phase2(preference_list,roommate_has_forward_match, roommate_has_backward_match,verbose=True):
    '''
    A clean-up step where indices that have no chance of being part of a match are preemptively
    eliminated.  This takes the results of phase 1.
    
    parameters:
    preference_list list of lists: The list of lists corresponding to the remaining available
    preferences for each roommate
    roommate_has_forward_match list: A list containing which roommate the roommate corresponding
    to that index asked
    roommate_has_backward_match: A list containing which roommate asked the corresponding indexed
    roommate
    verbose bool: Whether or not you would like step by step output
    
    return:
    preference_list_copy: The updated list of lists corresponding to the remaining available
    preferences for each roommate
    '''
    preference_list_copy = pickle.loads(pickle.dumps(preference_list))
    for i in range(0,len(preference_list_copy)):
        if any([x==[] for x in preference_list_copy]):
            raise ValueError("There are no preferences remaining for one of the roommates")
        #this finds the worst case scenario for each roommate and gets rid of any potential matches
        #that would be worse
        best_backward = preference_list_copy[i].index(roommate_has_backward_match[i])
        for j in preference_list_copy[i][(best_backward+1):len(preference_list_copy[i])]:
            preference_list_copy[j].remove(i)
            preference_list_copy[i].remove(j)
            
            if verbose:
                print(preference_list_copy)
    return preference_list_copy

def addendum_89(preference_list_copy,to_remove):
    """A change from the original Irving implementation used (but not mentioned) in the wikipedia example
    and implemented in python matching
    This code uses a handful of lines from get_pairs_to_delete as the textbook containing the
    updated implementation is behind a paywall
    
    parameters:
    preference_list_copy list of lists: The list of lists corresponding to the remaining available
    preferences for each roommate
    to_remove list of tuples: A list of tuples where the first value indicates the index of the roommate
    and the second value indicates the 2nd or last preference value
    
    return:
    pairs: list of tuples: A list of tuples containing the values that now need to be removed
    
    """
    #I am going to attempt to replace right with first and left with second as that appears to fix the existing issue
    #on the wiki example
    #this will require more testing and debugging
    #this is the part of the implementation I am least sure of given the limited info on it
    pairs = []
    cycle = [to_remove[x] for x in range(1,len(to_remove)) if x%2==0]
    cycle = [(y,x) for x,y in cycle]
    
    for i, (_, right) in enumerate(cycle):
        left = cycle[(i - 1) % len(cycle)][0]
        successors = preference_list_copy[right][preference_list_copy[right].index(left) + 1 :]
        for successor in successors:
            pair = (right, successor)
            if pair not in pairs and pair[::-1] not in pairs:
                pairs.append((right, successor))

    return pairs

def phase3(preference_list,n,addendum=True,finish_cycle_on_last="False",verbose=True):
    '''
    The final phase of Irving's algorithm.  This contains an addendum that changes
    the algorithm from the 1985 to 1989 version
    
    parameters:
    preference_list_copy list of lists: The list of lists corresponding to the remaining available
    preferences for each roommate
    n int: The number of roommates we are matching
    addendum bool: A flag to decide whether or not we will be using the 1989 version
    of the algorithm
    verbose bool: Whether or not you would like step by step output
    
    return:
    preference_list_copy: The updated list of lists corresponding to the remaining available
    preferences for each roommate.  This should only have a single value for each roommate.
    Otherwise the model will throw out an error indicating that no full matching exists.
    '''
    preference_list_copy = pickle.loads(pickle.dumps(preference_list))
    #need to verify if we delete a different amount based on whether it is even or odd
    len_list = [0]*n
    add_one=False
    while sum([len(x) for x in preference_list_copy])>n:
        if any([x==[] for x in preference_list_copy]):
            raise ValueError("There are no preferences remaining for one of the roommates")
        to_remove=[]
        second=True
        for i in range(0,n):
            len_list[i] = len(preference_list_copy[i])
        
        first_non_one = [x>1 for x in len_list].index(True)
        if add_one:
            first_non_one +=1
        to_remove.append(tuple([-1,first_non_one]))
        current_last_val = first_non_one
        #creating the cycles
        #the cycle alternates between 2nd and last
        if finish_cycle_on_last == "True":
            print("finish_cycle_on_last")
            while ((to_remove[0][1]!=to_remove[-1][1]) & second == False) | (len(to_remove)==1):
                if second==True:
                    to_remove.append(tuple([current_last_val,preference_list_copy[current_last_val][1]]))
                    current_last_val = preference_list_copy[current_last_val][1]
                    second=False
                else:
                    to_remove.append(tuple([current_last_val,preference_list_copy[current_last_val][-1]]))
                    current_last_val = preference_list_copy[current_last_val][-1]
                    second=True
        else:
            while (to_remove[0][1]!=to_remove[-1][1]) | (len(to_remove)==1):
                if second==True:
                    to_remove.append(tuple([current_last_val,preference_list_copy[current_last_val][1]]))
                    current_last_val = preference_list_copy[current_last_val][1]
                    second=False
                else:
                    to_remove.append(tuple([current_last_val,preference_list_copy[current_last_val][-1]]))
                    current_last_val = preference_list_copy[current_last_val][-1]
                    second=True
        #togglable 1989 addendum
        if addendum:
            removables = addendum_89(preference_list_copy,to_remove)
            if removables == []:
                add_one = True
            else:
                add_one=False
            if verbose:
                print(preference_list_copy)
            for i in range(0,len(removables)):
                preference_list_copy[removables[i][0]].remove(removables[i][1])
                preference_list_copy[removables[i][1]].remove(removables[i][0])
        else: 
            for i in range(2,len(to_remove)):
                if i%2==0:
                    preference_list_copy[to_remove[i][0]].remove(to_remove[i][1])
                    preference_list_copy[to_remove[i][1]].remove(to_remove[i][0])
                if verbose:
                    print(preference_list_copy)
    return(preference_list_copy)

def stable_roommates_matching(roommatePreferences,n,addendum=True,timeout=False,verbose=True):
    '''
    The main function that allows a single call to calculate the find whether stable
    roommate pairing exists.
    
    parameters:
    roommatePreferences list of lists: A list of length n containing lists of length n-1 with
    the indices of the other roommates in order of preference
    n int: The number of roommates we are matching.  This must be even otherwise there will be
    an error
    addendum bool: A flag to decide whether or not we will be using the 1989 version
    of the algorithm
    timeout bool/int:  Whether or not you want a timeout and if so, for how long
    verbose bool: Whether or not you would like step by step output
    
    return:
    final_preferences list of lists: The updated list of lists corresponding to the final
    preference for each roommate.  This should only have a single value for each roommate.
    Otherwise the model will throw out an error indicating that no full matching exists.
    
    '''
    
    if timeout:
        def handler(signum, frame):
            raise Exception("Timed Out")

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)
    try:
        roommate_forward_match, roommate_backward_match, next_roommate_choice, preference_list1 = phase1(n=n,roommatePreferences=roommatePreferences,verbose=verbose)
    except:
        raise ValueError("There does not appear to be any stable matching.  There was a failure in Phase 1")
    print("End of Phase 1")
    try:
        preference_list2 = phase2(preference_list1,roommate_forward_match,roommate_backward_match,verbose=verbose)
    except:
        raise ValueError("There does not appear to be any stable matching.  There was a failure in Phase 2")
    print("End of Phase 2")
    try:
        final_preferences = phase3(preference_list2,n,addendum,verbose)
    except:
        raise ValueError("There does not appear to be any stable matching.  There was a failure in Phase 3")
    print("End of Phase 3")
    print("The final matching is: {}".format(final_preferences))
    return final_preferences