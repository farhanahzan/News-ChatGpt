from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def run_scraper():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        
        # Create a context with specific viewport dimensions
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        # Navigate to the Daily Mirror website
        page.goto("https://www.dailymirror.lk/")
        page.wait_for_load_state('networkidle')
        
        # Handle notification popup
        try:
            page.wait_for_selector('button#onesignal-slidedown-cancel-button', timeout=5000)
            page.click('button#onesignal-slidedown-cancel-button')
        except:
            print("Notification popup not found")

        # Wait for and handle the second popup
        try:
            page.wait_for_selector('a#close0', state='visible', timeout=5000)
            page.click('a#close0')
        except:
            print("Second popup not found")

        # Wait for and click on the menu bar with "Sections" text
        page.wait_for_selector('a.bar:has-text("Sections")', state='visible') 
        page.click('a.bar:has-text("Sections")')

        # Click on the "Today's Paper" menu item
        page.click('a[href="https://www.dailymirror.lk/print"]')

        # Wait for navigation to the print page
        page.wait_for_load_state('networkidle')
        
        page.wait_for_selector('h3.section_title:has-text("Today\'s Paper")', state='visible')

        article_data = []
        # Initialize a variable to keep track of the number of buttons clicked
        total_buttons = 0

        while True:
            # Wait for buttons to be visible after page load
            try:
                page.wait_for_selector('a.btn.btn-dark.more-btn:text-is("More")', state='visible', timeout=5000)
            except:
                print("No More buttons found, exiting loop.")
                break  # Exit the loop if no buttons are found

            # Find all "More" buttons with exact text match
            more_buttons = page.query_selector_all('a.btn.btn-dark.more-btn:text-is("More")')
            if not more_buttons:
                print("No More buttons found, exiting loop.")
                break  # Exit if no buttons are found

            print(f"Found {len(more_buttons)} More button(s)")

            # Check if we have already clicked all buttons
            if total_buttons >= len(more_buttons):
                print("All More buttons have been clicked, exiting loop.")
                break

            for index in range(total_buttons, len(more_buttons)):
                # Select the button at the current index
                button = more_buttons[index]
                
                # Wait for navigation and page load
                button.scroll_into_view_if_needed()
                page.wait_for_timeout(1000)  # Wait for scroll to complete

                # Click the button
                button.click()

                # Wait for navigation and page load
                page.wait_for_load_state('networkidle')

                # Check if the breadcrumb is visible to confirm navigation
                if not page.is_visible('a.breadcrumb-item:has-text("Home")'):
                    print("Navigation failed, going back.")
                    page.go_back()
                    page.wait_for_load_state('networkidle')
                    continue  # Skip to the next button if navigation fails

                # Get the category from breadcrumb
                category_element = page.query_selector('nav.breadcrumb.bmod a.breadcrumb-item:nth-child(2)')
                category = category_element.inner_text() if category_element else "No category found"

                # Find all article rows
                article_rows = page.query_selector_all('div.top-header-sub div.row:has(div.col-md-4)')
                
                for row in article_rows:
                    # Extract article details
                    link = row.query_selector('a[href^="https://www.dailymirror.lk/print"]')
                    if link:
                        article_url = link.get_attribute('href')
                        title_element = row.query_selector('h3')
                        title = title_element.inner_text() if title_element else "No title found"
                        
                        date_element = row.query_selector('span.gtime')
                        raw_date = date_element.inner_text().strip() if date_element else "No date found"
                        
                        # Convert date to standard format
                        try:
                            date_obj = datetime.strptime(raw_date, "%d %b %Y")
                            formatted_date = date_obj.strftime("%Y-%m-%d")
                        except:
                            formatted_date = raw_date
                        
                        desc_element = row.query_selector('p')
                        desc = desc_element.inner_text().strip() if desc_element else "No description found"
                        
                        article_data.append({
                            'url': article_url,
                            'title': title,
                            'date': formatted_date,
                            'description': desc,
                            'category': category
                        })

                # Increment the total buttons clicked
                total_buttons += 1

                # Go back to the previous page
                page.go_back()
                page.wait_for_load_state('networkidle')

                # Re-fetch the "More" buttons to ensure we have the latest references
                more_buttons = page.query_selector_all('a.btn.btn-dark.more-btn:text-is("More")')        
        print(f"Total articles collected: {len(article_data)}")
        # Save article data to JSON file
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(article_data, f, indent=4, ensure_ascii=False)
            
        # Print confirmation
        print(f"Saved {len(article_data)} articles to news.json")

        # Close the browser
        browser.close()

# Run the scraper
run_scraper()