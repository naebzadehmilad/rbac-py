import subprocess
import base64
import json
from kubernetes import config, client
from kubernetes.client.rest import ApiException
from kubernetes.client import CoreV1Api





import subprocess
import base64
import json
from kubernetes import config, client
from kubernetes.client.rest import ApiException


def generate_service_account_token(api_instance, namespace, service_account_name, token=None):
    v1 = client.CoreV1Api(api_instance.api_client)

    try:
        secrets = v1.list_namespaced_secret(namespace)
        service_account_secrets = [secret for secret in secrets.items if secret.metadata.annotations and secret.metadata.name.startswith(f"{service_account_name}-token-")]

        if service_account_secrets:
            token_base64 = service_account_secrets[0].data['token']
            token = base64.b64decode(token_base64).decode('utf-8')
            print(f"Token: {token}")
        else:
            print(f"No service account token secrets found in namespace '{namespace}' for service account '{service_account_name}'.")
            token = None  # Set token to None when not found

    except ApiException as e:
        print(f"Error listing secrets: {e}")

    return token  # Return the token value (which could be None)




def create_service_account(api_instance, namespace, service_account_name):
    v1 = client.CoreV1Api(api_instance.api_client)  # Use CoreV1Api

    body = client.V1ServiceAccount(metadata=client.V1ObjectMeta(name=service_account_name))

    try:
        v1.create_namespaced_service_account(namespace, body)
        print(f"Service Account '{service_account_name}' created in namespace '{namespace}'.")
    except ApiException as e:
        if e.status == 409:
            print(f"Service Account '{service_account_name}' already exists in namespace '{namespace}'. Skipping creation.")
        else:
            print(f"Error creating Service Account: {e}")
            return

def create_namespace(api_instance, namespace):
    v1 = CoreV1Api(api_instance.api_client)  # Use CoreV1Api to create the namespace

    body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))

    try:
        v1.create_namespace(body=body)
        print(f"Namespace '{namespace}' created.")
    except ApiException as e:
        if e.status == 409:
            print(f"Namespace '{namespace}' already exists. Skipping creation.")
        else:
            raise


def create_role(api_instance, namespace, role_name, resources, verbs):
    rule = client.V1PolicyRule(
        api_groups=[""],
        resources=resources,
        verbs=verbs  # Pass the 'verbs' argument here
    )

    role = client.V1Role(
        metadata=client.V1ObjectMeta(name=role_name),
        rules=[rule]
    )

    try:
        api_instance.create_namespaced_role(namespace, role)
        print(f"Role '{role_name}' created in namespace '{namespace}'.")
    except ApiException as e:
        if e.status == 409:
            print(f"Role '{role_name}' already exists in namespace '{namespace}'. Skipping creation.")
        else:
            print(f"Error creating role: {e}")


def create_role_binding(api_instance, namespace, role_binding_name, role_name, service_account_name):
    role_ref = client.V1RoleRef(
        kind="Role",
        name=role_name,
        api_group="rbac.authorization.k8s.io"
    )

    subject = client.V1Subject(
        kind="ServiceAccount",
        name=service_account_name,
        namespace=namespace
    )

    role_binding = client.V1RoleBinding(
        metadata=client.V1ObjectMeta(name=role_binding_name),
        subjects=[subject],
        role_ref=role_ref
    )

    try:
        api_instance.create_namespaced_role_binding(namespace, role_binding)
        print(f"RoleBinding '{role_binding_name}' created in namespace '{namespace}'.")
    except ApiException as e:
        if e.status == 409:
            print(f"RoleBinding '{role_binding_name}' already exists in namespace '{namespace}'. Skipping creation.")
        else:
            print(f"Error creating role binding: {e}")
            return

def extract_ca_data(kubeconfig_path):
    try:
        cmd = f'kubectl config view --minify --raw --output=json --kubeconfig={kubeconfig_path}'
        result = subprocess.check_output(cmd, shell=True)
        kubeconfig_data = json.loads(result)
        ca_data = kubeconfig_data['clusters'][0]['cluster']['certificate-authority-data']
        ca_crt = base64.b64decode(ca_data).decode('utf-8')
        return ca_crt
    except subprocess.CalledProcessError as e:
        print(f"Error extracting certificate-authority-data: {e}")
        return None
