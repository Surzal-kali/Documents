import json
import subprocess

class HttpMe:
    def __init__(self):
        pass

    @staticmethod
    def parse_httpx_output(self, output):
        if not output:
            return {
                'http_version': None,
                'status_code': None,
                'reason': None,
                'headers': {},
                'body': None,
            }

        lines = output.splitlines()
        status_line = lines[0]
        header_lines = []
        body_start = len(lines)

        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == '':
                body_start = index + 1
                break
            header_lines.append(line)

        headers = {}
        for line in header_lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key] = value

        body_text = '\n'.join(lines[body_start:]).strip() or None
        body = body_text
        if body_text:
            try:
                body = json.loads(body_text)
            except json.JSONDecodeError:
                body = body_text

        if status_line.startswith('HTTP/'):
            parts = status_line.split(' ', 2)
            http_version = parts[0]
            status_code = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
            reason = parts[2] if len(parts) > 2 else None
        else:
            http_version = None
            status_code = None
            reason = None

        return {
            'http_version': http_version,
            'status_code': status_code,
            'reason': reason,
            'headers': headers,
            'body': body,
        }


    def http_request(self, method, url, headers=None, data=None, timeout=5.0):
        command = ['httpx', url, '--method', method.upper(), '--timeout', str(timeout)]

        if headers:
            for key, value in headers.items():
                command.extend(['--headers', key, str(value)])

        if data is not None:
            if isinstance(data, (dict, list)):
                command.extend(['--json', json.dumps(data)])
            else:
                command.extend(['--content', str(data)])

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            return {
                'ok': False,
                'error': 'httpx command was not found in PATH.',
                'command': command,
            }

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        parsed_output = self.parse_httpx_output(self, output=stdout)

        return {
            'ok': result.returncode == 0,
            'return_code': result.returncode,
            'command': command,
            'http_version': parsed_output['http_version'],
            'status_code': parsed_output['status_code'],
            'reason': parsed_output['reason'],
            'headers': parsed_output['headers'],
            'body': parsed_output['body'],
            'stderr': stderr or None,
        }

