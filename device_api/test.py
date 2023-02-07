import random
import string

def generate_rand(length,choices):
    if len(choices)>length:
        print("Impossible to generate password with the given length")
        exit
    ans=[]
    for ch in choices:
        if ch=='1':
            ans.append(random.choice(string.ascii_uppercase))           
        elif ch=='2':
            ans.append(random.choice(string.ascii_lowercase))
        elif ch=='3':
            ans.append(random.choice(string.digits))
        elif ch=='4':
            ans.append(random.choice('@#$-'))
        else:
            print("Invalid Choice")
            exit
        length-=1
    for i in range(length):
        ans.append(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits+'@#$-'))
    print(ans)
    random.shuffle(ans)
    return ans

choices_str = input("Enter 1 for uppercase character, 2 for lowercase character, 3 for number and 4 for special character (only @,#,-,$). Leave blank for all cases : ")
choices=[]
if not choices_str:
    choices = ['1','2','3','4']
else:
    choices = choices_str.split(' ')
length=int(input("Enter Length of random password : "))
ans=generate_rand(length,choices)
ans=''.join(ans)
print(ans)