import numpy as np

from matplotlib import pyplot as plt

class Perceptron():
    def __init__(self):
        # np.random.seed(0)
        self.rate = 0.1
    
    def fit(self, x, y):
        x = np.array([np.append(_x, [1]) for _x in x]) # Add bias

        n = len(x)
        d = len(x[0])
        epoch = 0

        self.w = np.random.rand(d)
        print('초기 w:', self.w)

        def tau(x):
            return 1 if x > 0 else -1

        while True:
            print('\r Epoch: '+str(epoch), end='\t')
            err_x = []
            err_y = []

            for j in range(n):
                _y = tau(np.dot(self.w, x[j].T))

                if _y != y[j]:
                    err_x.append(x[j])
                    err_y.append(y[j])
                
            if len(err_x) > 0:
                for i in range(d):
                    s = 0
                    for xk, yk in zip(err_x, err_y):
                        s += xk[i] * yk

                    self.w[i] += self.rate * s
            else:
                break
                
                # << STORM CASTING >>

                # if len(err_x) > 0:
                #     for i in range(d):
                #         # s = 0
                #         # for xk, yk in zip(err_x, err_y):
                #         #     s += xk[i] * yk

                #         s = x[j][i] * y[j]

                #         self.w[i] += self.rate * s
                # else:
                #     break

            epoch += 1
            if epoch < 10:
                print(self.w)

        print('')
        print('weights:', self.w)
        print('done')

X = np.array([
    [0, 0], [0, 1],
    [1, 0], [0, 0]
])
Y = np.array([ 1, -1, 1, 1])

p = Perceptron()
p.fit(X,Y)


# plt.figure(figsize=(12,9))

# for xi,yi in zip(X,Y):
#     if yi > 0:
#         plt.plot(xi,'bo')
#     else:
#         plt.plot(xi,'ro')

# # show line
# x = np.linspace(-0.2, 1.2, num=10)

# d = p.w[1]/p.w[0]
# y = d * x - p.w[2]
# plt.plot(x,y)
# plt.show()