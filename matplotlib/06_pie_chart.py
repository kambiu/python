import matplotlib.pyplot as plt

slices = [7,2,2,13]
activities = ['sleeping','eating','working','playing']
cols = ['c','m','r','b']


plt.pie(slices,
        labels=activities,
        colors=cols,
        startangle=90,
        shadow= True,
        explode=(0,0.1,0,0), # pull out the portion
        autopct='%1.1f%%') # auto show the percentage, %1.1f%% is the format of percentage


plt.title('Interesting Graph\nCheck it out')
plt.show()
