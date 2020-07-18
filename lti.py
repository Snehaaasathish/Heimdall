from scipy.signal import lti,lsim

x = lti([5,1,1],1)
print(x)
