import sys
import os
import requests
import csv
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError
import pypyodbc
import re, string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from itertools import zip_longest
from PYjenkins import AddUser

user = os.getenv('user')
password = os.getenv('pass')
serviceuser =  os.getenv('service_user')
servicepasswd = os.getenv('service_passwd')


#Lists for Use
list_members = []
new_list_members = []

list_members_exclude = []
new_list_members_exclude = []


#Jenkins jobs
NewUser = ""
RemoveUser = ""


#Querying Active Directory 
def get_na_group_members (group_sam_account_name, user_name, user_domain_name, user_password):
 server = Server('', port=3269, use_ssl=True, allowed_referral_hosts=[('', True), ('', False)])
 conn = Connection(server, user='{}\\{}'.format(user_domain_name, user_name), password=user_password, authentication=NTLM, auto_bind=True)
 conn.search(
  search_base='DC=,DC=,DC=com',
  search_filter=f'(sAMAccountName={group_sam_account_name})',
  attributes=[
   'distinguishedName'
  ]
 )

 group_dn = conn.entries[0].distinguishedName.value
 conn.search(
  search_base=group_dn,
  search_filter='(objectClass=group)',
  search_scope='SUBTREE',
  attributes = ['member']
 )

 for entry in conn.entries:
  for member in entry.member.values:
   conn.search(
    search_base='DC=,DC=',
    search_filter=f'(distinguishedName={member})',
    attributes=[
     'sAMAccountName',
     'employeeType'
    ]
   )
   if group_sam_account_name == '' or group_sam_account_name == '':
       list_members.append((conn.entries[0].sAMAccountName.value, conn.entries[0].employeeType.value, group_sam_account_name))
   else:
       list_members_exclude.append((conn.entries[0].sAMAccountName.value, conn.entries[0].employeeType.value, group_sam_account_name))


# Main Function
def userAccount(Pool):
    for i in new_list_members:
        User = i[0]
        Employement = i[1]

        #Getting User Count
        SQLQuery(Pool,User)
        UserQuery = SQLQuery(Pool, User)[0]

        #Getting User Count in Order pool
        SQLQuery1(Pool, User)
        UserQuery1 = SQLQuery1(Pool,User)[0]

        #Checking if User already got Email about being on a different pool
        SQLQuery2(User)
        UserQuery2 = SQLQuery2(User)[0]
        
        # Checking if User is Terminated
        if Employement == 'terminated':
            print('User: {} has been Terminated'.format(User))

            if UserQuery == 1:
                print('Terminated User: {} has a vDesk Assigned, Placing vDesk into Maintenance Mode'.format(User))
                jenkinsbuild(User, ' ', Pool, RemoveUser)
        else:
            # Checking if User has a vDesk Assigned in Different Pool
            if UserQuery1 == 1:
                print('User appears to have a vDesk in a Different Pool within this Environment: {}'.format(User))
                #TO DO Add User to Ex List
                listName = " "
                justification = 'User has a vDesk'
                
                justification = 'vDesk Added for User: {}'.format(listMembers)
                resp = requests.post(" ".format(listName,User,justification),auth=(serviceuser, servicepasswd),verify=False)

                if UserQuery2 == 1:
                    print('Email Sent to User Already: {}'.format(User))
                else:
                    print('Senting Email to User: {}'.format(User))
                    Email(User, Pool)

            # Check if User has a vDesk in this pool Already 
            elif UserQuery == 1:
                print('User Already has a vDesk within this Pool: {}'.format(User))

            else:
                #Checking if User is not a Member of the Exclude Lists
                if (any(User in i for i in new_list_members_exclude)):
                    print('User is part of the ExcludedList: {}'.format(User))
                else:
                    print('Building vDesk for User: {}'.format(User,Group))
                    AddUser(User, ' ', Pool, NewUser)
                   
  

def main():
    exclude =[(),()]  # Exclude Group 
    Group = [(), ()] # Main Group

    # Using Iterator.zip function two loop over the two Tutples 
    for f, b in zip(exclude, Group):
        GroupExclude = f[1]
        GroupMain = b[1]
        Pool = f[0]

        get_na_group_members(GroupExclude, user, '', password)
        get_na_group_members(GroupMain, user, '', password)

    # Beacuse of iterator.zip needs Even Tutples, Looping over a.exclude Twice was needed Removing Duplicates
    mylist = list(dict.fromkeys(list_members_exclude))
    for i in mylist:
        new_list_members_exclude.append(i)

    # Remove Any Duplicates from the Employee List
    mylist = list(dict.fromkeys(list_members))
    for i in mylist:
        new_list_members.append(i)

    userAccount(Pool)


    
if __name__ == "__main__":
    main()
