from matplotlib import pyplot as plt

def plot(ys, *args, **kwargs):
    if 'xs' in kwargs:
        xs = kwargs['xs']
        plt.plot(ys,xs)
    else:
        plt.plot(ys)
    plt.show()