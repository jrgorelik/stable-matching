from Gale_Shapley import stableMatching

#inputs
#The number of women and men
n=5
#The order of preferences.  This is a list of lists
menPreferences = [[0,1,2,3,4],[2,3,4,1,0],[3,2,4,0,1],[0,4,1,3,2],[4,3,2,1,0]]
womenPreferences = [[0,1,2,3,4],[3,4,2,0,1],[1,0,4,2,3],[4,2,3,0,1],[3,4,1,2,0]]

print(n)
print(menPreferences)
print(womenPreferences)

results = stableMatching(n, menPreferences, womenPreferences)

print(results)

