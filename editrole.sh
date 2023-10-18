rolename=example
for ns in $(kubectl get namespaces -o custom-columns=NAME:.metadata.name --no-headers); do
  kubectl edit role $rolename -n $ns
done
