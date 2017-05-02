import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8]
y = [5,2,4,2,1,4,5,2]

# mark --> shape of the scatter dot, s is the size of the scatter dot
# like ^,*,o,X etc ... refer to the online document
plt.scatter(x,y, label='skitscat', color='k', s=25, marker="x")
# plt.scatter(x,y, label='skitscat', color='k')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()