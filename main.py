import time
from playwright.sync_api import sync_playwright

def bypass_cloudflare():
    # 1. Initialization
    with sync_playwright() as p:
        # Launch Chromium
        browser = p.chromium.launch(headless=True)
        
        # 2. Setup Context & Stealth
        # We set a realistic User-Agent and viewport
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US"
        )
        
        # 3. Inject Stealth Scripts
        # These commands run immediately upon page load to hide Playwright signatures
        context.add_init_script("""
            () => {
                // Remove 'navigator.webdriver' flag
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                
                // Mock 'window.chrome' runtime
                window.chrome = { runtime: {} };
                
                // Mock permission queries
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ? Promise.resolve({ state: Notification.permission }) : originalQuery(parameters)
                );
            }
        """)
        
        page = context.new_page()
        
        try:
            # 4. Navigation
            target_url = "https://www.namecheap.com"
            print(f"[*] Navigating to {target_url}...")
            page.goto(target_url, wait_until="commit", timeout=30000)
            
            # Wait for rendering and potential challenge resolution
            time.sleep(3)
            
            title = page.title()
            print(f"[+] Loaded Title: {title}")
            
            # 5. Verify Bypass
            if "Just a moment" in title:
                print("[-] Still on challenge page. (Try adding X-Forwarded-For or waiting longer)")
                page.screenshot(path="bypass_failed.png")
            else:
                print("[+] SUCCESS: Real site content loaded.")
                # Save Proof
                page.screenshot(path="bypass_success.png", full_page=True)
                print("[*] Screenshot saved to bypass_success.png")
                
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    bypass_cloudflare()