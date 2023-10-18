import configparser
def generate_default_config():
    config_parser = configparser.ConfigParser()
    config_parser['RBAC'] = {
        'namespaces': 'default',
        'service_account_name': 'example-sa',
        'role_name': 'example-role',
        'role_binding_name': 'example-role-binding',
        'verbs': 'create, delete ,deletecollection ,get, list, patch, update,watch',
        'resources': 'extensions,pods,apps,replicasets,pods/exec'
    }
    config_parser['KubeConfig'] = {
        'kube_config_path': '/path/to/your/kubeconfig.yaml',
        'output_kubeconfig_file': 'kubeconfig.yaml',
        'server_url': '127.0.0.1:6443'
    }



    config_parser['Header'] = {
        'header_comment': '# Resources:\n'
                         '# pods: Pod resources\n'
                         '# services: Service resources\n'
                         '# configmaps: ConfigMap resources\n'
                         '# secrets: Secret resources\n'
                         '# deployments: Deployment resources\n'
                         '# ingresses: Ingress resources\n'
                         '# persistentvolumes: PersistentVolume resources\n'
                         '# persistentvolumeclaims: PersistentVolumeClaim resources\n'
                         '# namespaces: Namespace resources\n'
                         '# roles: Role resources\n'
                         '# rolebindings: RoleBinding resources\n'
                         '# replicasets: ReplicaSet resources\n'
                         '# events: Event resources\n'
                         '# tokenreviews: TokenReview resources\n'
                         '# selfsubjectaccessreviews: SelfSubjectAccessReview resources\n'
                         '# selfsubjectrulesreviews: SelfSubjectRulesReview resources\n'
                         '# subjectaccessreviews: SubjectAccessReview resources\n'
                         '# localsubjectaccessreviews: LocalSubjectAccessReview resources\n'
                         '# certificatesigningrequests: CertificateSigningRequest resources\n'
                         '# leases: Lease resources\n'
                         '# certificates: Certificate resources\n'
                         '# endpointslices: Endpointslice resources\n'
                         '# pods/log: Pod log resources\n'
                         '# serviceaccounts: ServiceAccount resources\n'
                         '\n'
                         '# Verbs:\n'
                         '# get: Allows getting resources\n'
                         '# list: Allows listing resources\n'
                         '# watch: Allows watching changes to resources\n'
                         '# create: Allows creating new resources\n'
                         '# update: Allows updating resources\n'
                         '# patch: Allows patching resources\n'
                         '# delete: Allows deleting resources\n'
                         '# deletecollection: Allows deleting collections of resources\n'
                         '# exec: Allows executing commands in a container\n'
                         '# attach: Allows attaching to a running container\n'
                         '# portforward: Allows port forwarding\n'
                         '# proxy: Allows proxying requests\n'
                         '# connect: Allows establishing a connection to a container'
    }

    with open("config.ini", 'w') as config_file:
        config_parser.write(config_file)
    print("Default config.ini file created. Complete the file and run the script")
    exit(1)
