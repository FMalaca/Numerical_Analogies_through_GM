from math import log, floor, ceil

def mean(a:float, a_m:float, d:float, d_m:float, p:float):
    '''Calculates the value of m_p(a,d)'''
    if p==float("inf"):
        return abs(a) if abs(a)>abs(d) else abs(d)
    elif p==-float("inf"):
        return abs(a) if abs(a)<abs(d) else abs(d)
    elif p==0:
        return a**(1/2) * d**(1/2)
    elif p>0:
        return (1/2*(a**p + d**p))**(1/p)
    else:
        return (1/2*(a_m**p + d_m**p))**(1/p)
    

def additive_inverse(a:float, b:float, c:float, d:float):
    '''(a,b,c,d) -> (-a, -b, -c, -d)'''
    return -a, -b, -c, -d

def exchange_of_the_means(a:float, b:float, c:float, d:float):
    '''(a,b,c,d) -> (a,c,b,d)'''
    return a, c, b, d

def exchange_of_the_extremes(a:float, b:float, c:float, d:float):
    '''(a,b,c,d) -> (d,b,c,a)'''
    return d, b, c, a

def inversion_of_ratios(a:float, b:float, c:float, d:float):
    '''(a,b,c,d) -> (b,a,d,c)'''
    return b, a, d, c

def canonical_form(a:float, b:float, c:float, d:float):

    if sum(x<0 for x in [a, b, c, d]) > sum(x>0 for x in [a, b, c, d]):
        a, b, c, d = additive_inverse(a,b,c,d)
    if a > d:
        a, b, c, d = exchange_of_the_extremes(a,b,c,d)
    if b > c:
        a, b, c, d = exchange_of_the_means(a,b,c,d)
    if a == b and c > d:
        a, b, c, d = inversion_of_ratios(a,b,c,d)
    if a > b:
        a, b, c, d = inversion_of_ratios(a,b,c,d)
    return a, b, c, d


def _DS_cicle(S:str, lower:float, upper:float, f):
    assert(f(lower)*f(upper)<=0)

    eps = 10**-6 if S == 'R' else 2
    
    while abs(upper-lower) > eps:
        middle = (lower+upper)/2

        if (S=='PO' or S=='O') and middle%2==0:
            middle += 1
        elif S == 'NO' and middle%2==0:
            middle -= 1
        elif S == 'E' and middle%2==1:
            middle = middle + 1 if middle!=-1 else middle-1
        elif S == 'E' and middle==0:
            middle = 2
            if lower==-2 and upper==2:
                eps = 4

        if f(middle)>0:
            upper = middle
        else:
            lower = middle

    return (lower, upper) 

def DS(a:float, a_m:float, b:float, b_m:float, c:float, c_m:float, d:float, d_m:float, S:str, lower:float, upper:float):
    f   = lambda p : mean(a,a_m,d,d_m,p)-mean(b,b_m,c,c_m,p)
    lower, upper = _DS_cicle(S,lower,upper,f)
    if f(lower) == 0:
        return [lower]
    elif f(upper) == 0:
        return [upper]
    elif S == 'R':
        return [(lower+upper)/2]
    else:
        return []
    

def case_i_set_choice(a:float, b:float, c:float, d:float):
    '''Gives numbers l and u with m_l(-a,d)<b and m_u(-a,d)>c'''

    lower = floor(log(2) / log(a/b))
    if lower % 2 != 0:
        lower -= 1

    upper = ceil(log(2) / log(d/c))
    if upper % 2 != 0:
        upper += 1

    return (lower, upper)

def case_i(a:float, a_m:float, b:float, b_m:float, c:float, c_m:float, d:float, d_m:float):
    '''0 < a < b < c, d'''

    assert(0<a and 0<b and 0<c and 0<d)

    sol = []

    if a<b<=c<d and mean(a,a_m,d,d_m,0) != mean(b,b_m,c,c_m,0):
        #Search for the solution
        lower, upper = case_i_set_choice(a, b, c, d)
        sol += DS(a,a_m,b,b_m,c,c_m,d,d_m,'R',lower,upper)
        
    return sol

def case_ii_b(a:float, a_m:float, b:float, b_m:float, c:float, c_m:float, d:float, d_m:float):
    '''a < 0 < b < d < c'''

    assert(a<0<b<=d<=c)

    sol = []

    if b<abs(a)<c:
        a_even, b_even, c_even, d_even = canonical_form(abs(a),b,c,d)
        a_m_even, b_m_even, c_m_even, d_m_even = canonical_form(abs(a_m),b_m,c_m,d_m)

        lower_even, upper_even, success_even = case_i_set_choice(a_even,b_even,c_even,d_even)
        
        if success_even:
            sol += DS(a_even,a_m_even,b_even,b_m_even,c_even,c_m_even,d_even,d_m_even,'E',lower_even,upper_even)
    
    return sol


def case_ii_c_set_choice(a:float, b:float, c:float, d:float):
    '''Gives number u such that m_u(a,d)>m_u(b,c)'''

    lower1 = floor(log(2) / log(d / max(b, min(abs(a), c))))
    lower2 = floor(log(3) / log(d / min(abs(a),b)))
    lower = max(lower1, lower2, 1)

    if lower % 2 != 1:
        lower -= 1

    upper = ceil(log(3) / log(d / max(abs(a),c)))

    if upper % 2 != 1:
        upper += 1

    return (lower, upper)
    
def case_ii_c(a:float, a_m:float, b:float, b_m:float, c:float, c_m:float, d:float, d_m:float):
    '''a < 0 < b < c < d'''

    assert(a<0<b<=c<=d)

    sol = []

    if abs(a)<b:
        a_even, b_even, c_even, d_even = canonical_form(abs(a),b,c,d)
        a_m_even, b_m_even, c_m_even, d_m_even = canonical_form(abs(a_m),b_m,c_m,d_m)

        lower_even, upper_even = case_i_set_choice(a_even,b_even,c_even,d_even)
        sol += DS(a_even,a_m_even,b_even,b_m_even,c_even,c_m_even,d_even,d_m_even,'E',lower_even,upper_even)
    
    if abs(a)<d and mean(a,a_m,d,d_m,1)<= mean(b,b_m,c,c_m,1):
        lower_odd, upper_odd = case_ii_c_set_choice(a,b,c,d)
        sol += DS(a,a_m,b,b_m,c,c_m,d,d_m,'PO',lower_odd,upper_odd)
    
    return sol


def case_ii(a:float, a_m:float, b:float, b_m:float, c:float, c_m:float, d:float, d_m:float):
    '''a < 0 < b, c, d'''

    assert(a<0<b<=c and d>0)
    
    if d < b:
        return [-p for p in case_ii_c(1/a_m, 1/a, 1/c_m, 1/c, 1/b_m, 1/b, 1/d_m, 1/d)]
            
    elif b<=d<=c:
        return case_ii_b(a, a_m, b, b_m, c, c_m, d, d_m)
        
    else:
        return case_ii_c(a, a_m, b, b_m, c, c_m, d, d_m)
    

def case_iv_set_choice_odd(a:float, b:float, c:float, d:float):
    '''Gives numbers l and u such that m_l(a,d)<m_l(b,c) and m_u(a,d)>m_u(b,c)'''

    lower = floor(log(2) / log(abs(a)/abs(b)))
    if lower % 2 != 1:
        lower -= 1

    upper = ceil(log(2) / log(d/c))
    if upper % 2 != 1:
        upper += 1

    return (lower, upper)

def case_iv(a:float, a_m:float, b:float, b_m:float, c:float, c_m:float, d:float, d_m:float):
    '''a < b < 0 < c, d'''

    assert(a<=b<0 and c>0 and d>0)

    sol = []

    a_odd, b_odd, c_odd, d_odd = canonical_form(abs(a),abs(b),d,c)
    a_m_odd, b_m_odd, c_m_odd, d_m_odd = canonical_form(abs(a_m),abs(b_m),d_m,c_m)

    a_even, b_even, c_even, d_even = canonical_form(abs(a),abs(b),c,d)
    a_m_even, b_m_even, c_m_even, d_m_even = canonical_form(abs(a_m),abs(b_m),c_m,d_m)
    
    if a_even<b_even<=c_even<d_even:
        lower_even, upper_even = case_i_set_choice(a_even,b_even,c_even,d_even)

        sol += DS(a_even,a_m_even,b_even,b_m_even,c_even,c_m_even,d_even,d_m_even,'E',lower_even,upper_even)
    
    if c_odd < d_odd:
        lower_odd, upper_odd = case_iv_set_choice_odd(a_odd, b_odd, c_odd, d_odd)

        sol += DS(a_odd,a_m_odd,b_odd,b_m_odd,c_odd,c_m_odd,d_odd,d_m_odd,'O',lower_odd,upper_odd)
    
    return sol


def case_x(a:float, a_m:float, b:float, b_m:float, c:float, c_m:float, d:float, d_m:float):
    '''a < d < 0 b < c'''

    assert(a<=d<0<b<=c)

    sol = []

    if b<abs(d)<=abs(a)<c or abs(d)<b<=c<abs(a):
        a, b, c, d = canonical_form(abs(a),b,c,abs(d))
        a_m, b_m, c_m, d_m = canonical_form(abs(a_m),b_m,c_m,abs(d_m))

        lower_even, upper_even = case_i_set_choice(a,b,c,d)

        sol += DS(a,a_m,b,b_m,c,c_m,d,d_m,'E',lower_even,upper_even)
    
    return sol


def case_1_set_choice(a:float, b:float, c:float, d:float):

    lower = 0

    upper = ceil(log(2) / log(d/c))
    if upper % 2 != 0:
        upper += 1

    return (lower, upper)

def case_1(a:float, b:float, c:float, d:float):

    sol = []

    if c<d:
        lower, upper = case_1_set_choice(a, b, c, d)
        sol += DS(a,a,b,b,c,c,d,d,'R',lower,upper)

    return sol


def case_2_set_choice(a:float, b:float, c:float, d:float):
    '''Gives number u such that m_u(a,d)>m_u(b,c)'''
    success_flag = True

    lower = 1

    upper = ceil(log(2) / log(d/c))
    if upper % 2 != 1:
        upper += 1

    return (lower, upper, success_flag)
    
    
def case_2(a:float, b:float, c:float, d:float):
    sol = []

    if d<c:
        a_even, b_even, c_even, d_even = canonical_form(abs(a),b,c,d)
        lower_even, upper_even, success_even = case_1_set_choice(a_even,b_even,c_even,d_even)

        if success_even:
            sol += DS(a_even,a_even,b_even,b_even,c_even,c_even,d_even,d_even,'E',lower_even,upper_even)

    elif abs(a)<d and c<d and mean(0,d,1) <= mean(a,c,1):
        lower_odd, upper_odd, success_odd = case_2_set_choice(b,abs(a),c,d)
        if success_odd: 
            sol += DS(b,b,abs(a),abs(a),c,c,d,d,'PO',lower_odd,upper_odd)

    return sol


def case_3(a:float, b:float, c:float, d:float):

    sol = []

    if c<abs(a):
        a_even, b_even, c_even, d_even = canonical_form(abs(a),b,c,d)
        lower_even, upper_even, success_even = case_1_set_choice(a_even,b_even,c_even,d_even)

        if success_even:
            sol += DS(a_even,a_even,b_even,b_even,c_even,c_even,d_even,d_even,'E',lower_even,upper_even)

    return sol


def alg(a:float, b:float, c:float, d:float) -> list:

    a, b, c, d = canonical_form(a,b,c,d)
    a_m, b_m, c_m, d_m = a, b, c, d
    
    if a != 0 or b != 0 or c != 0 or d != 0:
        m = min([abs(x) for x in [a,b,c,d] if x != 0])
        M = max([abs(x) for x in [a,b,c,d] if x != 0])

        a_temp, b_temp, c_temp, d_temp = a, b, c, d
        if M != 0:
            a, b, c, d = a_temp/M, b_temp/M, c_temp/M, d_temp/M
        if m != 0:
            a_m, b_m, c_m, d_m = a_temp/m, b_temp/m, c_temp/m, d_temp/m

    aux = []
    for p in [-float('inf'), 0, float('inf')]:
        if mean(a,a_m,d,d_m,p) == mean(b,b_m,c,c_m,p):
            aux += [p]

    if a>0 and b>0 and c>0 and d>0:
        if a==b and c==d:
            return aux + ['IR']
        
        return aux + case_i(a, a_m, b, b_m, c, c_m, d, d_m)
    
    elif a<0 and b>0 and c>0 and d>0:
        if min(abs(a),d)==b and max(abs(a),d)==c:
            return aux + ['2Z^*']
        
        return aux + case_ii(a, a_m, b, b_m, c, c_m, d, d_m)
    
    elif a<0 and b<0 and c>0 and d>0:
        if abs(a)==abs(b)==c==d:
            return aux + ['IR \ (Z^*_- \ 2Z)']
        elif abs(a)==abs(b) and c==d:
            return aux + ['IR']                
        elif abs(a)==c and abs(b)==d:
            return aux + ['2Z^*']
        elif abs(a)==d and abs(b)==c:
            return aux + ['Z^*_+ \ 2Z']
        
        return aux + case_iv(a, a_m, b, b_m, c, c_m, d, d_m)
    
    elif a<0 and b>0 and c>0 and d<0:
        if abs(a)==c and b==abs(d):
            return aux + ['2Z^*']
        
        return aux + case_x(a, a_m, b, b_m, c, c_m, d, d_m)


    elif a==0 and b>0 and c>0 and d>0:
        return aux + case_1(a,b,c,d)

    elif a<0 and b==0 and c>0 and d>0:
        return aux + case_2(a,b,c,d)

    elif a<0 and b>0 and c>0 and d==0:
        return aux + case_3(a,b,c,d)

    elif a==b==0 and c>0 and d>0:
        if c==d:
            return aux + ['R_+']
        else:
            return aux
        
    elif a<0 and b==d==0 and c>0:
        if abs(a)==c:
            return aux + ['2Z_+']
        else:
            return aux

    elif a==d==0 and b>0 and c>0:
        return aux

    elif a<0 and b==c==0 and d>0:
        if abs(a)==d:
            return aux + ['Z_+ \ 2Z']

    elif a==b==c==0!=d:
        return aux

    elif a==b==c==d==0:
        return aux + ['R_+']
    
    else:
        return
    

if __name__ == "__main__":
    a = 1
    b = 2
    c = 3
    d = 4
    result = alg(a, b, c, d)
    print(f"{a}:{b}::^p{c}:{d} for p in {set(result)} ")