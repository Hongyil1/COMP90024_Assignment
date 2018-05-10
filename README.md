## Team 56

 * Xiaolu Zhang 886161
 * Jianbo Ma 807590
 * Hongyi Lin 838776
 * Xiaoyu Wang 799778
 * Shalitha Weerakoon Karunatilleke 822379
 
# COMP90024 Cluster and Cloud Computing
## Social Media Analytics on Melbourne & Sydney


### Prerequisites

* Python3 & Pip3 
[Insatllation Guide](https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3) - Python 3 and Pip3

If you have your own project
* Create SSH keys and update the key pairs in NeCTAR portal with the key name 'team56'
* Create a security group 'team56_security' with rules

### Installation

Install the requrements.txt in your enviroment or create a python virtual machine in your local

```
pip3 install -r requirements.txt --no-index --find-links file:///tmp/packages
```

### NeCTAR Credentials 
Change the credential information in this script
```
vi deployment.py
```

### Run the Script for a Dynamic Deployment 
```
python3 deployment.py
```
