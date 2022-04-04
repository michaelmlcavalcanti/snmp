# smnp
Simple management network protocol implementation.

# How to run

Install the folowing packages

```
pip install virtualenv
```


Then create a folder and activate a virtual environment.

```
virtualenv snmp snmp/Scripts/activate
```

Install the dependencies running

``` 
pip -r requirements.txt
```


# What's is SNMP?

Pretty text


# **Open endpoints**

## Get oid info


```POST URL_API/get_oid_info```: Pretty test

### **Request body (example)**
```
{
    "ip_address": "192.168.5.1",
    "oid_list": ["1.3.6.1.4.1.343", "1.3.6.1.4.1.343"]
}
```

### **Response body (example)**

HTTP Status Code: **200 OK**
```
{
    "expiration_time": "Thu, 21 Oct 2021 17:19:57 GMT",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTYzNDg0NzU5Ny43MTc1NDd9.S6PP67fhJfUIoCf1OYj2dDGYZzHYxG-y1sESd-N9UCs"
}
```