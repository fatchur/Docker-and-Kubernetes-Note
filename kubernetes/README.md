## Kubernetes Note

### Prerequisities
- ubuntu prerequisities     
`sudo apt-get update`   
`sudo apt-get install -y apt-transport-https`

- virtual box   
`sudo apt-get install -y virtualbox virtualbox-ext-pack`    
`sudo apt-get update`

- kubectl   
`curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo touch /etc/apt/sources.list.d/kubernetes.list`     
`echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list`     
`sudo apt-get update`   
`sudo apt-get install -y kubectl`


### Virtual-box Note
#### A. Creating new vm
- Download ubuntu-64 image in `osboxes.org` 
- open virtual-box
- select `new`
- fill `name`, select *linuk* for type and choose your ubuntu version
- select `next`, choose your memory size (2GB)
- selct `next`, choose `use an existing cirtual harddisk file`, then select the *.vdi* ubuntu image
- select `create`

#### B. Setting-up VM internet
- right click on vm
- choose `network`, change from `NAT` to `Bridge-adapter`
- ok    
or 
- choose `NAT` for wifi connection

#### C. Creating steps snapshot
- click snapshot
- if you want to documented the steps, click `take`

#### D. Setting SSH 
- checking ssh status: `service sshd status`, if not found activate it by following commands.
- `sudo apt-get update`, `sudo apt-get install openssh-server`  
to change the sshd configuration, follow this steps,    
- `sudo nano /etc/ssh/sshd_config`
- uncomment these: `PermitRootLogin prohibit-password`, `PasswordAuthentication yes`, `PermitRootLogin yes`.





