from mitmproxy import http

HOST_MAP = {
    "youtube.com": "google.com",
    "vercel.com": "react.dev",
    "reddit.com": "python.org",
}

WILDCARD_MAP = {
    ".vercel.app": "react.dev",
    ".google.com": "google.com",
    ".github.com": "github.com"
}

class DFM:
    def request(self, flow: http.HTTPFlow):
        original = flow.request.pretty_host.lower()

        target = HOST_MAP.get(original)
        
        if not target:
            for pattern, mapped in WILDCARD_MAP.items():
                if original == pattern.lstrip(".") or original.endswith(pattern):
                    target = mapped
                    break

        if not target:
            return

        flow.request.host = target
        flow.request.port = 443

        flow.server_conn.sni = target

        flow.request.headers["host"] = original
      
addons = [DFM()]










