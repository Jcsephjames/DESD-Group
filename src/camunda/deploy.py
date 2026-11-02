"""Deploy selected BPMN files and all exported forms in a single request."""
import json
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import uuid


def deploy():
    root = Path('/resources')
    paths = [root / line.strip() for line in (root / 'deployments.txt').read_text().splitlines()
             if line.strip() and not line.lstrip().startswith('#')]
    paths.extend(sorted((root / 'form_files').rglob('*.form')))
    paths.extend(sorted((root / 'bpmn_files').rglob('*.form')))
    if not paths:
        raise ValueError('No resources selected in deployments.txt.')
    forms = {json.loads(p.read_text())['id'] for p in paths if p.suffix == '.form'}
    import xml.etree.ElementTree as ET
    for path in paths:
        if path.suffix == '.bpmn':
            tree = ET.parse(path)
            for form in tree.findall('.//{http://camunda.org/schema/zeebe/1.0}formDefinition'):
                form_id = form.get('formId')
                if form_id and not form_id.startswith('=') and form_id not in forms:
                    raise ValueError(f'{path.name} requires form {form_id!r}. Export its .form file into form_files first.')
    boundary = uuid.uuid4().hex
    body = bytearray()
    for path in paths:
        print(f'Deploying: {path.name}', flush=True)
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="resources"; filename="{path.name}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode())
        body.extend(path.read_bytes())
        body.extend(b'\r\n')
    body.extend(f'--{boundary}--\r\n'.encode())
    request = Request('http://camunda:8080/v2/deployments', data=bytes(body),
                      headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
    with urlopen(request, timeout=90) as response:
        print(response.read().decode(), flush=True)


if __name__ == '__main__':
    try:
        deploy()
    except HTTPError as error:
        print(f'Camunda rejected deployment ({error.code}): {error.read().decode()}', file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        print(f'Deployment failed: {error}', file=sys.stderr)
        sys.exit(1)
