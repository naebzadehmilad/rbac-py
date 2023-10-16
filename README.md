# rbac-py
rbac-shared-sa-py


Run the main.py with Python and then edit the config.ini file


<pre>


namespaces = hd-wallet,backend,backend1
service_account_name = miladnaebzadeh-test
role_name = get-test
role_binding_name = miladnaebzadeh-test
verbs = get, list , exec
resources = pods, deployments, services

kube_config_path = /opt/rbac-py/kubeconfig.yaml
output_kubeconfig_file = kubeconfig-user.yaml
server_url = https://192.168.168.28:6449



For example, we want our token to work for 3 of the half spaces


#kubectl edit rolebinding (rolename) -n (target-access-namesapce) 

1.
   # kubectl edit rolebinding get-test -n  hd-wallet


   #We see a text similar to the one below

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: "2023-10-16T16:30:19Z"
  name: get-test
  namespace: hd-wallet
  resourceVersion: "15464458"
  uid: 97c44cb7-d4b8-48f1-9fd1-f4f50835fdd0
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: get-test
subjects:
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: hd-wallet

2.  We add  to the namespaces we want to access and save

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: "2023-10-16T16:30:19Z"
  name: get-test
  namespace: hd-wallet
  resourceVersion: "15464458"
  uid: 97c44cb7-d4b8-48f1-9fd1-f4f50835fdd0
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: get-test
subjects:
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: hd-wallet
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: backend
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: backend1

3. We repeat the steps for the namespaces

 # kubectl edit rolebinding get-test -n  backend1


apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: "2023-10-16T16:30:19Z"
  name: get-test
  namespace: backend1
  resourceVersion: "15464463"
  uid: 74072339-8069-4120-a6a5-47e174826d15
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: get-test
subjects:
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: backend1
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: hd-wallet
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: backend


4.
# kubectl edit rolebinding get-test -n  backend
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: "2023-10-16T16:30:19Z"
  name: get-test
  namespace: backend
  resourceVersion: "15466623"
  uid: 97c44cb7-d4b8-48f1-9fd1-f4f50835fdd0
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: get-test
subjects:
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: backend
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: backend1
- kind: ServiceAccount
  name: miladnaebzadeh-test
  namespace: hd-wallet


 5.  kubectl   --kubeconfig=kubeconfig-user.yaml  get po -n hd-wallet
     kubectl   --kubeconfig=kubeconfig-user.yaml  get po -n backend
     kubectl   --kubeconfig=kubeconfig-user.yaml  get po -n backend1


</pre>

