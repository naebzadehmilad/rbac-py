import argparse
import os
import configparser
import yaml
import subprocess
import base64
from kubernetes import config, client
from kubernetes.client.rest import ApiException
from config_generator import generate_default_config
from kubernetes.client import CoreV1Api

from service_account_creator import (
    generate_service_account_token,
    create_service_account,
    create_role,
    create_role_binding,
    extract_ca_data,
    create_namespace
)

def namespace_exists(api_instance, namespace):
    v1 = client.CoreV1Api(api_instance.api_client)  # Use CoreV1Api

    try:
        v1.read_namespace(namespace)
        return True
    except ApiException as e:
        if e.status == 404:
            return False
        else:
            raise

def main():
    parser = argparse.ArgumentParser(description="Kubernetes RBAC Token and Kubeconfig Generator")
    parser.add_argument("--config", default="config.ini", help="Path to the configuration file (default: config.ini)")

    args = parser.parse_args()

    if not os.path.exists(args.config):
        generate_default_config()

    config_parser = configparser.ConfigParser()
    config_parser.read(args.config)

    namespaces = config_parser['RBAC']['namespaces'].split(',')
    service_account_name = config_parser['RBAC']['service_account_name']
    role_name = config_parser['RBAC']['role_name']
    resources = [resource.strip() for resource in config_parser['RBAC']['resources'].split(',')]
    verbs = [verb.strip() for verb in config_parser['RBAC']['verbs'].split(',')]

    kubeconfig_section = config_parser['KubeConfig']
    kube_config_path = kubeconfig_section['kube_config_path']
    server_url = kubeconfig_section['server_url']
    output_kubeconfig_file = kubeconfig_section['output_kubeconfig_file']

    ca_crt = extract_ca_data(kube_config_path)

    try:
        config.load_kube_config(config_file=kube_config_path)

        api_instance = client.RbacAuthorizationV1Api()

        for namespace in namespaces:
            if not namespace_exists(api_instance, namespace):
                create_namespace(api_instance, namespace)

            # Create Service Account in each namespace
            create_service_account(api_instance, namespace, service_account_name)

            # Create Role in each namespace with the specified resources and verbs
            create_role(api_instance, namespace, role_name, resources, verbs)

            # Create Role Binding in each namespace to bind Service Account with Role
            create_role_binding(api_instance, namespace, f"{role_name}", role_name, service_account_name)

        # Check for the service account token secret in each namespace
        token = generate_service_account_token(api_instance, namespace, service_account_name)


        kubeconfig = {
                'apiVersion': 'v1',
                'kind': 'Config',
                'clusters': [
                    {
                        'name': 'cluster',
                        'cluster': {
                            'server': server_url,
                            'certificate-authority-data': base64.b64encode(ca_crt.encode()).decode('utf-8')
                        },
                    },
                ],
                'contexts': [
                    {
                        'name': 'context',
                        'context': {
                            'cluster': 'cluster',
                            'namespace': namespaces[0],
                            'user': service_account_name,
                        },
                    },
                ],
                'current-context': 'context',
                'users': [
                    {
                        'name': service_account_name,
                        'user': {
                            'token': token,
                        },
                    },
                ],
            }

        with open(output_kubeconfig_file, 'w') as kubeconfig_file:
                kubeconfig_file.write(yaml.dump(kubeconfig))

        print(f"Service Account: {service_account_name}")
        print(f"Role Name: {role_name}")
        print(f"Kubeconfig saved to {output_kubeconfig_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
