#Mybe add gui (make it look batter ??? )


import requests
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from serpapi import GoogleSearch

# Replace these with your API keys
NUMVERIFY_API_KEY = "5a5fd1c0b652cc08ac08f1ee91b2d6e9"
NUMVERIFY_BASE_URL = "http://apilayer.net/api/validate"
SERPAPI_KEY = "f17fef540a0df69104546a4184eb4bdae0ead66639fe9cdce0f423ad1b27972f"


class SearchSnapchatMentions:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.results = {"phone_number": phone_number, "snapchat_mentions": [], "additional_info": []}

    def search_snap_mentions(self):
        """Search for Snapchat mentions of the provided phone number."""
        try:
            print("[*] Searching for Snapchat mentions on Google...")

            # Enhanced search with variations of the query
            queries = [
                f"Snapchat {self.phone_number}",
                f"{self.phone_number} site:snapchat.com",
                f"{self.phone_number} Snapchat user",
            ]

            for query in queries:
                print(f"[*] Querying: {query}")
                search = GoogleSearch({"q": query, "api_key": SERPAPI_KEY})
                results = search.get_dict()

                # Extracting detailed results
                for result in results.get("organic_results", []):
                    mention = {
                        "title": result.get("title", "No Title"),
                        "link": result.get("link", "No Link"),
                        "snippet": result.get("snippet", "No Snippet"),
                        "source": result.get("displayed_link", "Unknown Source"),
                    }
                    self.results["snapchat_mentions"].append(mention)

            print(f"[+] Found {len(self.results['snapchat_mentions'])} total Snapchat mentions.")
        except Exception as e:
            print(f"[!] Error during Snapchat mentions search: {e}")



    def generate_report(self):
        """Generate a detailed PDF report of the findings with Unicode support."""
        print("[*] Generating detailed Snapchat mentions report...")

        pdf = FPDF()
        pdf.add_page()

        # Add a Unicode-compatible font (remove uni=True as it is deprecated)
        try:
            # Register DejaVuSans Regular and Bold versions explicitly
            pdf.add_font('DejaVu', '', '/home/doc123/Downloads/dejavu-sans/DejaVuSans.ttf')  # Regular
            pdf.add_font('DejaVu', 'B', '/home/doc123/Downloads/dejavu-sans/DejaVuSans-Bold.ttf')  # Bold
            pdf.set_font("DejaVu", size=12)
        except Exception as e:
            print(f"[!] Error setting font: {e}")

        # Report Header
        pdf.set_font("DejaVu", style="B", size=16)
        pdf.cell(200, 10, text="Snapchat Mentions Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(10)  # To add some space after the header

        # Phone Number Section
        pdf.set_font("DejaVu", style="B", size=14)
        pdf.cell(200, 10, text="Phone Number:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, text=self.phone_number, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(10)

        # Snapchat Mentions Section
        pdf.set_font("DejaVu", style="B", size=14)
        pdf.cell(200, 10, text="Snapchat Mentions:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("DejaVu", size=12)
        if self.results["snapchat_mentions"]:
            for mention in self.results["snapchat_mentions"]:
                pdf.cell(200, 10, text=f"Title: {mention['title']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(200, 10, text=f"Link: {mention['link']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(200, 10, text=f"Snippet: {mention['snippet']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(5)
        else:
            pdf.cell(200, 10, text="No mentions found.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(10)

        # Save Report
        pdf.output("enhanced_snapchat_mentions_report.pdf")
        print("[+] Report saved as enhanced_snapchat_mentions_report.pdf.")

    def run(self):
        """Run the enhanced Snapchat mentions OSINT process."""
        self.search_snap_mentions()
        self.generate_report()



class PhoneNumberOSINT:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.results = {"phone_number": phone_number}

    def fetch_numverify_data(self):
        """Fetch basic info about the phone number from Numverify API."""
        try:
            print("[*] Fetching Numverify data...")
            url = f"{NUMVERIFY_BASE_URL}?access_key={NUMVERIFY_API_KEY}&number={self.phone_number}"
            response = requests.get(url)
            data = response.json()

            if data.get("valid"):
                self.results.update({
                    "country": data.get("country_name", "N/A"),
                    "location": data.get("location", "N/A"),
                    "carrier": data.get("carrier", "N/A"),
                    "line_type": data.get("line_type", "N/A"),
                })

                print("\n[+] Numverify Data:")
                print(f"  Country: {data.get('country_name', 'Unknown')}")
                print(f"  Location: {data.get('location', 'Unknown')}")
                print(f"  Carrier: {data.get('carrier', 'Unknown')}")
                print(f"  Line Type: {data.get('line_type', 'Unknown')}")
            else:
                print("[-] Invalid phone number.")
        except Exception as e:
            print(f"[!] Error fetching Numverify data: {e}")

    def search_google_mentions(self):
        """Search Google for mentions of the phone number on social media platforms."""
        try:
            print("[*] Searching Google for mentions on social media...")

            # Define search queries for social media platforms
            search_queries = {
                "Twitter": f"{self.phone_number} site:twitter.com",
                "Facebook": f"{self.phone_number} site:facebook.com",
                "Instagram": f"{self.phone_number} site:instagram.com",
                "Snapchat": f"{self.phone_number} site:snapchat.com",
            }

            # Perform searches for each platform
            for platform, query in search_queries.items():
                print(f"[*] Searching {platform}...")
                search = GoogleSearch({"q": query, "api_key": SERPAPI_KEY})
                results = search.get_dict()

                # Debug: print the structure of the search results to check what's inside
                print(f"Results for {platform}: {results}")

                mentions = []
                organic_results = results.get("organic_results", [])

                for result in organic_results:
                    if isinstance(result, dict):
                        mentions.append({
                            "title": result.get("title"),
                            "link": result.get("link"),
                            "snippet": result.get("snippet"),
                        })
                    else:
                        print (f"[!] Unexpected result format: {type(result)} - {result}")

                self.results[f"{platform.lower()}_mentions"] = mentions
                print(f"[+] Found {len(mentions)} mentions on {platform}.")

        except Exception as e:
            print(f"[!] Error searching Google: {e}")

    def display_results(self):
        """Display the search results."""
        print("\n[+] Final Results:")
        for platform, mentions in self.results.items():
            print(f"\n{platform.upper()} Mentions:")

            # Ensure mentions is a list of dictionaries
            if isinstance(mentions, list):
                for mention in mentions:
                    # Check if mention is a dictionary
                    if isinstance(mention, dict):
                        title = mention.get('title', 'No Title')
                        link = mention.get('link', 'No Link')
                        snippet = mention.get('snippet', 'No Snippet')

                        print(f"  Title: {title}")
                        print(f"  Link: {link}")
                        print(f"  Snippet: {snippet}")
                    else:
                        print(f"[!] Unexpected mention format: {mention}")
            else:
                print(f"[!] Unexpected format for mentions in {platform}. Expected a list of dictionaries.")

            print("\n" + "-" * 30)

    def run(self):
        """Run the OSINT process."""
        self.fetch_numverify_data()
        self.search_google_mentions()
        self.display_results()


# Main Execution
if __name__ == "__main__":
    user_choice = input("Insert 1 for Snapchat or 2 for Phone OSINT: ")

    if user_choice == '2':
        phone_number = input("Enter desired phone number (e.g +14155552671): ")
        osint_phone = PhoneNumberOSINT(phone_number)
        osint_phone.run()
    elif user_choice == '1':
        phone_number = input("Enter desired phone number (e.g +14155552671): ")
        osint_snap = SearchSnapchatMentions(phone_number)
        osint_snap.run()
    else:
        print("[!] Invalid choice. Please enter 1 or 2.")
