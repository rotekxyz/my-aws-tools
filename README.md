# my-aws-tools
aws cli scripts by python.  
userful tools to myself.

## get_userlist.py
`$ ./get_userlist.py [credential profile name]`

result sample
```
### Userlists
hogehoge,Admin,MFA_True,Login_Yes
fugafuga,,MFA_False,Login_Yes
piyopiyo,DevOps,MFA_True,Login_No

### GroupLists
Admin,AdministratorAccess
DevOps,IAMPassRoleAccess:PowerUserAccess
```

Formats (delimiter is : )
```
### Userlists
[User Name],[Attach Group],[MFA Status],[Web Console Login Status]

### GroupLists
[Group Name],[Attach Policy Name]
```


#### Requirements
- boto3

#### Usage
- ./get_hogehoge.py default


