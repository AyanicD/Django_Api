from django.db.models import Q

def filter_dname(device_list, names):
    print(names)
    if names:
        return device_list.filter(name__icontains=names[0]) 

    return device_list

def filter_type(device_list, types):
    if types:
        return device_list.filter(type__in=types) 
    return device_list

def filter_ename(emp_list, names):
    if names:
        return emp_list.filter(name__icontains=names[0]) 

    return emp_list

def filter_email(emp_list, emails):
    if emails:
        return emp_list.filter(email__icontains=emails[0]) 

    return emp_list
