import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import re
import sys
import os
import pyfiglet
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

# --- Configuration ---
# REPLACE WITH YOUR VALID VERIPHONE API KEY
# If you don't have an API Key, the Veriphone feature will not work.
# You can get a free API Key with certain limitations at veriphone.io
VERIPHONE_API_KEY = "3A99D5B325584F9F8D0624742239434B"

# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints the ASCII art banner and tool information."""
    clear_screen() # Clear screen before printing banner
    banner = pyfiglet.figlet_format("SIMDetect", font="slant")
    print(Fore.RED + Style.BRIGHT + banner)

    print(Fore.CYAN + Style.BRIGHT + "   SIMDetect Ver.1.0 (Python Edition)")
    print(Fore.CYAN + "   Coded by YatAja" + Style.RESET_ALL)
    print(Fore.GREEN + "-" * 60 + Style.RESET_ALL)
    print(Fore.YELLOW + "   Focus: Accurate Phone Number & SIM Information." + Style.RESET_ALL)
    print(Fore.GREEN + "-" * 60 + Style.RESET_ALL)
    print("")

# --- Main Tool Function ---
def get_accurate_phone_info(phone_number_input):
    print(f"\n{Fore.GREEN}{'='*40}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Analyzing Number: {Fore.YELLOW}{phone_number_input}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*40}{Style.RESET_ALL}")

    # 1. Validate and Clean Phone Number using phonenumbers
    parsed_number = None
    try:
        # Initial regex validation for +XX... format
        if not re.match(r'^\+\d{1,3}\d{6,14}$', phone_number_input):
            print(f"{Fore.RED}[X] ERROR: Invalid phone number format. Please use international format (+CountryCodeNumber), e.g., +6281234567890.{Style.RESET_ALL}")
            return

        parsed_number = phonenumbers.parse(phone_number_input)

        if not phonenumbers.is_valid_number(parsed_number):
            print(f"{Fore.RED}[X] ERROR: The entered phone number is structurally invalid.{Style.RESET_ALL}")
            print(f"{Fore.RED}    Please ensure the country code and number length are correct.{Style.RESET_ALL}")
            return

        # Format number for API
        formatted_e164 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        print(f"{Fore.LIGHTBLACK_EX}Formatted Number (E.164): {formatted_e164}{Style.RESET_ALL}")

    except phonenumbers.NumberParseException as e:
        print(f"{Fore.RED}[X] ERROR parsing number: {e}. Please check the number format.{Style.RESET_ALL}")
        return
    except Exception as e:
        print(f"{Fore.RED}[X] Unexpected error during initial validation: {e}{Style.RESET_ALL}")
        return

    # 2. Accurate Information from Veriphone API
    print(f"\n{Fore.CYAN}--- Accurate Information (Source: Veriphone & phonenumbers) ---{Style.RESET_ALL}")

    # Information from phonenumbers (always available if number is valid)
    ph_location = geocoder.description_for_number(parsed_number, "en")
    ph_operator = carrier.name_for_number(parsed_number, "en")
    ph_time_zones = timezone.time_zones_for_number(parsed_number)

    # Initialize variables for Veriphone data
    veriphone_status = "N/A"
    veriphone_phone_valid = "N/A"
    veriphone_phone_type = "N/A"
    veriphone_carrier = "N/A"
    veriphone_country = "N/A"
    veriphone_country_code = "N/A"
    veriphone_timezones = []
    veriphone_location_detail = ""
    veriphone_carrier_validity = "N/A"

    if not VERIPHONE_API_KEY or VERIPHONE_API_KEY == "YOUR_VERIPHONE_API_KEY":
        print(f"{Fore.YELLOW}[!] Veriphone API Key not set or invalid. Relying on basic data.{Style.RESET_ALL}")
    else:
        veriphone_url = f"https://api.veriphone.io/v2/verify?key={VERIPHONE_API_KEY}&phone={formatted_e164}"
        try:
            response = requests.get(veriphone_url, timeout=15)
            response.raise_for_status()
            veriphone_data = response.json()

            if veriphone_data.get('status') == 'success':
                veriphone_status = "SUCCESS"
                veriphone_phone_valid = str(veriphone_data.get('phone_valid', 'N/A'))
                veriphone_phone_type = str(veriphone_data.get('phone_type', 'N/A'))
                veriphone_carrier = str(veriphone_data.get('carrier', 'N/A'))
                veriphone_country = str(veriphone_data.get('country', 'N/A'))
                veriphone_country_code = str(veriphone_data.get('country_code', 'N/A'))
                veriphone_timezones = veriphone_data.get('timezones', [])
                veriphone_location_detail = str(veriphone_data.get('location', ''))
                veriphone_carrier_validity = str(veriphone_data.get('carrier_validity', 'N/A'))

            else:
                print(f"{Fore.RED}[!] Veriphone API ERROR: {veriphone_data.get('message', 'Unknown error message.')}{Style.RESET_ALL}")
                if "Daily API lookup limit reached" in veriphone_data.get('message', ''):
                    print(f"{Fore.RED}    Daily API limit reached for Veriphone.{Style.RESET_ALL}")
                elif "Invalid API key" in veriphone_data.get('message', ''):
                    print(f"{Fore.RED}    Your Veriphone API Key is invalid.{Style.RESET_ALL}")
                veriphone_status = "FAILED_API_ERROR"

        except requests.exceptions.Timeout:
            print(f"{Fore.RED}[X] ERROR: Veriphone API request timed out. Check your internet connection.{Style.RESET_ALL}")
            veriphone_status = "FAILED_TIMEOUT"
        except requests.exceptions.HTTPError as e:
            print(f"{Fore.RED}[X] HTTP ERROR from Veriphone API: {e.response.status_code} - {e.response.text}{Style.RESET_ALL}")
            veriphone_status = "FAILED_HTTP_ERROR"
        except requests.exceptions.ConnectionError as e:
            print(f"{Fore.RED}[X] Connection ERROR to Veriphone API: {e}. Ensure stable internet connection.{Style.RESET_ALL}")
            veriphone_status = "FAILED_CONNECTION"
        except ValueError as e:
            print(f"{Fore.RED}[X] ERROR parsing Veriphone API response: {e}. Not valid JSON.{Style.RESET_ALL}")
            veriphone_status = "FAILED_JSON_PARSE"
        except Exception as e:
            print(f"{Fore.RED}[X] Unexpected error contacting Veriphone API: {e}{Style.RESET_ALL}")
            veriphone_status = "FAILED_UNKNOWN"

    # Consolidate and Display Output
    print(f"  {Fore.CYAN}Verification Status (Veriphone): {Fore.YELLOW}{veriphone_status}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Number Valid: {Fore.YELLOW}{veriphone_phone_valid.capitalize()}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Number Type: {Fore.YELLOW}{veriphone_phone_type.capitalize()}{Style.RESET_ALL}")

    operator_display = veriphone_carrier if veriphone_carrier and veriphone_carrier != 'N/A' else ph_operator
    print(f"  {Fore.CYAN}Operator: {Fore.YELLOW}{operator_display.capitalize() if operator_display else 'Unknown'}{Style.RESET_ALL}")

    country_display = veriphone_country if veriphone_country and veriphone_country != 'N/A' else ph_location
    country_code_display = veriphone_country_code if veriphone_country_code and veriphone_country_code != 'N/A' else (str(parsed_number.country_code) if parsed_number else 'N/A')
    print(f"  {Fore.CYAN}Country: {Fore.YELLOW}{country_display.capitalize() if country_display else 'Unknown'}{Style.RESET_ALL} ({country_code_display})")

    # Output Timezone - Prioritize from Veriphone, then from phonenumbers
    final_timezones = veriphone_timezones if veriphone_timezones else ph_time_zones
    print(f"  {Fore.CYAN}Timezone: {Fore.YELLOW}{', '.join(final_timezones) if final_timezones else 'Unknown'}{Style.RESET_ALL}")

    # Output City/Area - Explain limitations for mobile numbers
    display_city_area = ""
    if veriphone_location_detail and veriphone_location_detail != 'N/A':
        display_city_area = veriphone_location_detail
    elif ph_location and ph_location != country_display:
        display_city_area = ph_location

    if display_city_area:
        print(f"  {Fore.CYAN}City/Area (Estimated): {Fore.YELLOW}{display_city_area.capitalize()}{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}(Based on initial/regional number allocation, not current user location){Style.RESET_ALL}")
    else:
        print(f"  {Fore.CYAN}City/Area (Estimated): {Fore.YELLOW}Unknown{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}(Specific city/area info is often unavailable for public mobile numbers due to privacy and portability){Style.RESET_ALL}")

    carrier_validity_display = veriphone_carrier_validity if veriphone_carrier_validity and veriphone_carrier_validity != 'N/A' else 'N/A'
    print(f"  {Fore.CYAN}Carrier Validity (Veriphone): {Fore.YELLOW}{carrier_validity_display.capitalize()}{Style.RESET_ALL}")

    int_num_display = veriphone_data.get('international_number', 'N/A') if veriphone_status == 'SUCCESS' else phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    local_num_display = veriphone_data.get('local_number', 'N/A') if veriphone_status == 'SUCCESS' else parsed_number.national_number

    print(f"  {Fore.CYAN}International Number: {Fore.YELLOW}{str(int_num_display)}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Local Number: {Fore.YELLOW}{str(local_num_display)}{Style.RESET_ALL}")

    print(f"{Fore.GREEN}{'='*40}{Style.RESET_ALL}")


# --- Main Interactive Section ---
if __name__ == "__main__":
    try:
        print_banner()

        print(f"{Fore.WHITE}Enter phone number in international format (e.g., +6281234567890).{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Type '{Fore.RED}exit{Fore.WHITE}' to quit.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'-'*60}{Style.RESET_ALL}")

        while True:
            user_input = input(f"{Fore.GREEN}[SIMDetect]{Fore.WHITE} Enter Phone Number: {Style.RESET_ALL}").strip()

            if user_input.lower() == 'exit':
                print(f"\n{Fore.GREEN}Thank you for using this tool. Goodbye!{Style.RESET_ALL}")
                sys.exit(0)
            elif not user_input:
                print(f"{Fore.YELLOW}[!] Input cannot be empty. Please enter a phone number.{Style.RESET_ALL}")
                continue

            get_accurate_phone_info(user_input)
            print("\n")

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program interrupted by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}A fatal error occurred: {e}{Style.RESET_ALL}")
        sys.exit(1)