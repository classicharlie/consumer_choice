import time
import math


# this version uses the linear combination of values along an equivalence class,
# which are constrained to a sublattice valued budget set.

def marshellianDemand(income,preferences,prices):
    '''
    computes an optimal bundle given a convex objective and a linear constraint, 
    in the context of consumer theory; this particular instance limits the user 
    to a Cobb-Douglas utility function, but can easily be expanded to more 
    general expressions.

    parameters:
        income (int): the amount of money that the  consumer is constrained to 
        spending
        preferences (array): an array of taste parameters that applies to 
        utility
        prices (array): an array containing the prices of good 1 and good 2

    returns:
        bundle (tuple): the optimal bundle x to maximize utility subject to a 
        budget constraint
    '''

    a = preferences[0]
    b = preferences[1]
    m = income
    p = prices
    
    u = ((.5*m/p[0])**a)*((.5*m/p[1]))**(b)

    def U(x1,utl):
        return (utl*x1**(-a))**(1/b)


    def B(x1,inc):
        return ((inc-p[0]*x1)/p[1])


    def findIntersection(utility):
        '''
        Calculates the intersection of two curves using a dynamic step size that 
        finds a lower limit and divides that interval by 10 each time.

        returns:
            bounds (array): structured like (min,max), this array represents the 
            points of intersection of the given curve
        '''

        def findMin(x,k):
            min_f = abs(U(x[0],utility) - B(x[0],m))
            min_x = x[0]

            for i in x:
                diff = U(i,utility) - B(i,m)
                next_diff = U(i+k,utility) - B(i+k,m)
                if diff < min_f:
                    min_f = abs(diff)
                    min_x = i
                    if abs(diff) <= abs(next_diff):
                        break

            return min_x

        # still broken somehow
        def findMax(x,k):
            max_f = abs(U(x[-1],utility) - B(x[-1],m))
            max_x = x[-1]

            for i in list(reversed(x)):
                diff = U(i,utility) - B(i,m)
                prev_diff = U(i+k,utility) - B(i+k,m)
                if diff < max_f:
                    max_f = abs(diff)
                    max_x = i
                    if abs(diff) <= abs(prev_diff):
                        break

            return max_x


        n = 4
        x = range(1,math.floor(m/p[0])+1)

        min_x = [findMin(x,1)]
        max_x = [findMax(x,1)]

        for i in range(1,n+1):
            k = 10**(-i)
            mnx = [round(min_x[-1]+j*(k),i) for j in range(0,10)]
            mxx = [round(max_x[-1]+j*(k),i) for j in range(0,10)]

            min_x.append(findMin(mnx,k))
            max_x.append(findMax(mxx,k))

        final_min = min_x[-1]
        final_max = max_x[-1]

        bds = [final_min,final_max]
        return bds


    def adjust(lower_bound,upper_bound):
        x1 = (lower_bound+upper_bound)/2
        x2 = B(x1,m)
        utility = ((x1)**a)*((x2))**(b)

        return utility


    bounds = findIntersection(u)

    while True:
        if abs(bounds[1] - bounds[0]) > .001:
            u = adjust(bounds[0],bounds[1])
        else:
            break
        bounds = findIntersection(u)

    bundle = (bounds[0],U(bounds[0],u))

    return bundle

start_time = time.time()
bundle = marshellianDemand(9,[1,1],[1,1])
elapsed_time = time.time() - start_time

print('bundle:\t(%.2f,%.2f)' % bundle)
print('time:\t%.3f ms' % (elapsed_time*1000))