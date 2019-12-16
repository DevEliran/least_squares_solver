from numpy.random import normal
import matplotlib.pyplot as plt
import numpy

def solve_ls(coords, w, r, w_path, degree):
    mat = open(coords, "r").read().splitlines()
    values = []
    for l in mat:
        f, s = l.split(",")
        values.append((float(f),float(s)))

    values_noisy = []
    mid_div = 0.1
    edges_div = 0.5
    mean = 0
    #Creating noise for y axis values
    for v in values:
        noise = 0
        x,y = v
        if ((x >= -0.5) and (x <= 0.1)):
            noise = normal(mean, mid_div)
        else:
            noise = normal(mean, edges_div)
        values_noisy.append((x, y + noise))

    x_axis =[]
    y_axis = []
    for (x,y) in values:
        x_axis.append(x)
        y_axis.append(y)

    plot=plt.plot(x_axis,y_axis,'-k', label = 'Original data')
    x_axis_noisy =[]
    y_axis_noisy = []
    for (x,y) in values_noisy:
        x_axis_noisy.append(x)
        y_axis_noisy.append(y)
    plot=plt.plot(x_axis_noisy,y_axis_noisy,'c.', label = 'Noisy f(x)')

    A = numpy.vander(x_axis, int(degree), True)
    piA = numpy.linalg.pinv(A)
    sol = piA.dot(y_axis_noisy)

    pol = numpy.poly1d(numpy.flip(sol))
    new_y = []
    new_x = []
    for x_fic in range(-100, 100):
        x = x_fic/100.0
        temp = 0.0
        for i in range(len(sol)):
            coef = sol[i]
            temp += coef*(x**i)
        new_y.append(temp)
        new_x.append(x)
    plot = plt.plot(new_x, new_y,'-r', label="Polynomial estimation to f(x)")
    if(w == True):
        W = numpy.zeros((len(values), len(values)))
        #w_path format 'left , right , weigth'
        with open(w_path,'r') as w_file:
            for line in w_file:
                left,right,weigth = line.split(',')
                for i,x in enumerate(x_axis):
                    if ((x >= float(left)) and (x <= float(right))):
                        W[i][i] = float(weigth)

        A_T = A.transpose()
        A_TWA_inv = numpy.linalg.inv(numpy.matmul(numpy.matmul(A_T, W), A))
        sol_w = (numpy.matmul(numpy.matmul(A_TWA_inv,A_T), W)).dot(y_axis_noisy)

        pol_w = numpy.poly1d(numpy.flip(sol_w))
        y_w = []
        x_w = []
        for x_fic in range(-100, 100):
            x = x_fic/100.0
            temp = 0.0
            for i in range(len(sol_w)):
                coef = sol_w[i]
                temp += coef*(x**i)
            y_w.append(temp)
            x_w.append(x)

        plot = plt.plot(x_w, y_w,'-g', label="Weighted polynomial estimation to f(x)")
    plt.legend()
    plt.show()
