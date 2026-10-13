import http.client
import urllib.parse

def simulate_crawler(url_string, user_agent):
    """Simulates a crawler accessing a URL, respecting robots.txt and checking status codes."""
    parsed_url = urllib.parse.urlparse(url_string)
    host = parsed_url.netloc
    path = parsed_url.path
    if not path:
        path = "/"

    print(f"--- Simulating access for: {url_string} with User-Agent: {user_agent} ---")

    # 1. Check robots.txt
    robots_path = "/robots.txt"
    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", robots_path, headers={'User-Agent': user_agent})
        robots_response = conn.getresponse()
        print(f"robots.txt status: {robots_response.status} {robots_response.reason}")

        if robots_response.status == 200:
            robots_content = robots_response.read().decode('utf-8')
            print("robots.txt content:\n", robots_content)
            # Basic check: is the current path disallowed for this user agent?
            disallowed = False
            for line in robots_content.splitlines():
                if line.lower().startswith('user-agent:'):
                    current_agent = line.split(':', 1)[1].strip()
                    if current_agent == '*' or current_agent == user_agent:
                        # Found a rule for this agent or a general rule
                        pass
                elif line.lower().startswith('disallow:') and current_agent == user_agent:
                    disallowed_path = line.split(':', 1)[1].strip()
                    if path.startswith(disallowed_path):
                        disallowed = True
                        break
            if disallowed:
                print(f"\nALERT: Path '{path}' is DISALLOWED for User-Agent '{user_agent}' in robots.txt.")
                # In a real crawler, we would stop here.

        elif robots_response.status == 404:
            print("robots.txt not found. Assuming all paths are allowed.")
        else:
            print(f"Warning: Could not fetch robots.txt, received status {robots_response.status}.")

    except Exception as e:
        print(f"Error checking robots.txt: {e}")

    finally:
        if 'conn' in locals() and conn:
            conn.close()

    # 2. Access the actual URL
    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", path, headers={'User-Agent': user_agent})
        response = conn.getresponse()
        print(f"\nPage access status: {response.status} {response.reason}")

        # Simulate JavaScript effect: If status is 200, we'd normally parse HTML.
        # For this demo, we'll just note if it's a success.
        if response.status == 200:
            print("Page content successfully fetched. A real crawler would parse HTML and execute JS if capable.")
            # In a real scenario, you'd fetch and parse HTML, then potentially render JS.
            # For simplicity, we're not fetching content here.
        elif response.status == 404:
            print("Page not found.")
        elif response.status == 403:
            print("Access forbidden.")
        elif response.status == 301 or response.status == 302:
            location = response.getheader('Location')
            print(f"Redirected to: {location}")
            # A real crawler would follow redirects (up to a limit).

    except Exception as e:
        print(f"Error accessing page: {e}")

    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    # Example 1: Googlebot accessing a hypothetical allowed page
    simulate_crawler("https://www.example.com/", "Googlebot")

    print("\n" + "="*50 + "\n")

    # Example 2: A disallowed crawler trying to access a specific path
    # Note: This is a simulation. The actual behavior depends on the server's robots.txt.
    # For this demo, we assume example.com has a robots.txt that disallows 'BadBot' from '/private/'
    # To test this, you'd need a server with a specific robots.txt configuration.
    simulate_crawler("https://www.example.com/private/secret.html", "BadBot")

    print("\n" + "="*50 + "\n")

    # Example 3: A crawler getting a 404
    simulate_crawler("https://www.example.com/nonexistent-page-12345.html", "Bingbot")
