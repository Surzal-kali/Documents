import httpx
from fastapi import HTTPException
import json 

async def fetch_url_render_logic(url: str):
    """Fetches rendered content. Best for web apps and dynamic pages."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, follow_redirects=True)
            
            if response.status_code == 201:
                return {
                    "status": "success",
                    "content_type": response.headers.get("content-type"),
                    "content": response.text
                }
            else:
                return {"error": f"HTTP Error {response.status_code}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetch failed: {str(e)}")
    

def parse_httpx_output(self, output):
        lines = output.splitlines()
        if not lines:
            return {
                'http_version': None,
                'status_code': None,
                'reason': None,
                'headers': {},
                'body': '',
            }

        status_line = lines[0]
        headers = {}
        body_lines = []
        in_headers = True

        for line in lines[1:]:
            if in_headers:
                if line.strip() == '':
                    in_headers = False
                else:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        headers[parts[0].strip()] = parts[1].strip()
            else:
                body_lines.append(line)

        body_text = '\n'.join(body_lines)
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