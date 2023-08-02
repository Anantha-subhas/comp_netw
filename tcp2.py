import socket


def download_web_page(url):
    # Parse the URL to extract the host and path
    host, path = parse_url(url)

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the web server using port 80 (HTTP)
    server_address = (host, 80)
    client_socket.connect(server_address)

    # Form the HTTP request
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"

    # Send the request to the server
    client_socket.sendall(request.encode())

    # Receive and process the response from the server
    response = b''
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        response += data

    # Close the socket connection
    client_socket.close()

    # Process the HTTP response
    headers, content = response.split(b'\r\n\r\n', 1)
    status_line = headers.decode().split('\r\n')[0]
    status_code = int(status_line.split()[1])

    if status_code in (301, 302):
        # Handle redirect
        location_header = headers.decode().split('\r\n')[1]
        new_url = location_header.split(' ')[1]
        print(f"Redirecting to: {new_url}")
        # Recursive call to download the redirected page
        download_web_page(new_url)
    elif status_code == 200:
        # Save the content to a file
        with open('downloaded_page.html', 'wb') as f:
            f.write(content)
        print("Download successful.")
    else:
        print(f"Failed to download web page. Status code: {status_code}")


def parse_url(url):
    # Remove the "http://" or "https://" part from the URL
    url = url.replace("http://", "").replace("https://", "")

    # Split the host and path
    parts = url.split("/", 1)
    host = parts[0]
    path = "/" + parts[1] if len(parts) > 1 else "/"

    return host, path


if __name__ == "__main__":
    # Replace this URL with the web page you want to download
    url_to_download = "http://example.com"
    download_web_page(url_to_download)
