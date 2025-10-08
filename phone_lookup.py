#!/usr/bin/env python3
"""
Phone Number Lookup Tool for Kali Linux
Comprehensive phone number analysis and information gathering tool
Author: Security Researcher
License: MIT
"""

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import argparse
import sys
import requests
import re
from bs4 import BeautifulSoup
import json
from urllib.parse import quote

class PhoneLookupTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
        })
    
    def print_banner(self):
        """Display tool banner"""
        banner = """
                                                                                                    
                                                                                                    
                                 ###############                                                    
                             #######################                                                
                          #############################                                             
                        ##################################                                          
                      ######################################                                        
                     #########################################                                      
                    ############################################                                    
                   ##############################################                                   
                  ################################################                                  
                  ##################################################                                
                 ######################################################                             
                 ###########################################################                        
                 ######################################%%%######################%                   
                ###################################%%%#**#%%%%%%%%%######%%%%%%%                    
                ###############################%%%%*-::...:::-+*%%%%%%%%%%%%%%                      
                %##########################%%%%%+:...............                                   
                %######################%%%%%#****-...............:                                  
                 %#################%%%%%#******#*:.................                                 
                 %#############%%%%%#********#*=:..................                                 
                 %%###########%%##**********#+........::.....:......                                
                  %############*************#=........=+=::-++-.......                              
                  %%###########****#**=:-***#+.........:-==-:..........                             
                  %###########***#*-:...:+***#-.........................                            
                  ##########%#**#*-.....:=***#+...........................                          
                 ##########%%***#=:......=**#*-...........................:                         
                #########%%%****#=........:::............................::                         
               #######%%%%#*****#+:....................................::::                         
               ##%%%%%%#**********+::................................:::::                          
              %%%%%%% ***************+=:.............................:::                            
                    ###****************#-............................::                             
                   #########***********#=:...........................::                             
                 ##############********#+:..........................:-+++                           
                ##################*****#+:..........................:-#**++                         
               ######################*##=..........................::: #**++                        
             ###########################=:.......................::::   #***+                       
            #############################*=......................:::    *****  ++++++++++           
          %#%%#############################*-:...................::     *****+ **********+          
           %%%%%%%%%#########################+-::::..............::     ****** ***********          
                @%%%%%%%######################***=-::::::.......:::     ****** ***********          
                     @%%%%%%#####################%%%#*-::::::::::::     ****** ***********          
                         @%%%%%%%#################%%%%##    ::::        ******+***********          
                             @@%%%%%################%%%##              #******************          
                                  %%%%%##############%%%##              #****************#          
                                     %%%%%%###########%%%##             ##**************##          
                                        @%%%%%#########%%%##             #######*****####           
                                            %%%%%######%%%%#                 ##########             
                                              @%%%%#####%%%%#                                       
                                                 @%%%%##%@%%#                                       
                                                    %%%%#@@@%#                                      
                                                      %%%  @@%                                      
                                                        %%   %                                      
                                                                                                    
                                                                                                    
        """
        print(banner)
    
    def validate_phone_number(self, phone_number):
        """Validate phone number format"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            return phonenumbers.is_valid_number(parsed)
        except:
            return False
    
    def basic_lookup(self, phone_number, verbose=False):
        """Perform basic phone number analysis"""
        print("\n" + "="*60)
        print("🔍 BASIC PHONE NUMBER ANALYSIS")
        print("="*60)
        
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            
            if not phonenumbers.is_valid_number(parsed_number):
                print("❌ Invalid phone number")
                return
            
            # Basic information
            info = {
                "number": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                "e164_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
                "valid": phonenumbers.is_valid_number(parsed_number),
                "possible": phonenumbers.is_possible_number(parsed_number),
                "location": geocoder.description_for_number(parsed_number, "en") or "Unknown",
                "carrier": carrier.name_for_number(parsed_number, "en") or "Unknown",
                "timezones": list(timezone.time_zones_for_number(parsed_number)),
                "country_code": parsed_number.country_code,
                "national_number": parsed_number.national_number,
            }
            
            # Number type
            number_type = phonenumbers.number_type(parsed_number)
            type_map = {
                phonenumbers.PhoneNumberType.MOBILE: "📱 Mobile",
                phonenumbers.PhoneNumberType.FIXED_LINE: "🏠 Fixed Line",
                phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "📞 Fixed Line or Mobile",
                phonenumbers.PhoneNumberType.VOIP: "💻 VOIP",
                phonenumbers.PhoneNumberType.TOLL_FREE: "🆓 Toll Free",
                phonenumbers.PhoneNumberType.PREMIUM_RATE: "💰 Premium Rate",
                phonenumbers.PhoneNumberType.SHARED_COST: "👥 Shared Cost",
                phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "👤 Personal Number",
                phonenumbers.PhoneNumberType.PAGER: "📟 Pager",
                phonenumbers.PhoneNumberType.UAN: "🏢 UAN",
                phonenumbers.PhoneNumberType.VOICEMAIL: "📭 Voicemail",
            }
            info["type"] = type_map.get(number_type, "❓ Unknown")
            
            # Print results
            print(f"\n📊 Basic Information:")
            print(f"  International: {info['number']}")
            print(f"  National:      {info['national_format']}")
            print(f"  E164:          {info['e164_format']}")
            print(f"  Valid:         {'✅ Yes' if info['valid'] else '❌ No'}")
            print(f"  Possible:      {'✅ Yes' if info['possible'] else '❌ No'}")
            print(f"  Type:          {info['type']}")
            print(f"  Location:      {info['location']}")
            print(f"  Carrier:       {info['carrier']}")
            print(f"  Country Code:  +{info['country_code']}")
            print(f"  National No:   {info['national_number']}")
            print(f"  Timezones:     {', '.join(info['timezones']) if info['timezones'] else 'Unknown'}")
            
            if verbose:
                print(f"\n🔍 Verbose Information:")
                print(f"  Raw Type:      {number_type}")
                print(f"  Country Source: {geocoder.country_name_for_number(parsed_number, 'en')}")
                
            return info
            
        except Exception as e:
            print(f"❌ Error in basic lookup: {e}")
            return None
    
    def advanced_analysis(self, phone_number):
        """Perform advanced number analysis"""
        print("\n" + "="*60)
        print("🔬 ADVANCED ANALYSIS")
        print("="*60)
        
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            national_number = str(parsed_number.national_number)
            
            print(f"\n📈 Number Pattern Analysis:")
            print(f"  Total digits: {len(national_number)}")
            
            # Pattern detection
            patterns = self.detect_patterns(national_number)
            if patterns:
                print("  🎭 Detected Patterns:")
                for pattern in patterns:
                    print(f"    • {pattern}")
            
            # Risk assessment
            risk = self.assess_risk(national_number)
            print(f"  🎯 Risk Level: {risk['level']} - {risk['reason']}")
            
            # Number characteristics
            print(f"\n🔢 Number Characteristics:")
            print(f"  Even digits: {sum(1 for d in national_number if int(d) % 2 == 0)}")
            print(f"  Odd digits: {sum(1 for d in national_number if int(d) % 2 == 1)}")
            print(f"  Unique digits: {len(set(national_number))}")
            
            # Country-specific info
            country = geocoder.country_name_for_number(parsed_number, "en")
            if country:
                print(f"\n🌍 Country Information:")
                print(f"  Country: {country}")
                
                # Typical number length by country
                typical_lengths = {
                    "US": 10, "GB": 10, "CA": 10, "AU": 9, "DE": 10, 
                    "FR": 9, "IT": 10, "ES": 9, "BR": 11, "IN": 10
                }
                
                for code, length in typical_lengths.items():
                    if country.lower().find(code.lower()) != -1:
                        actual_length = len(national_number)
                        status = "✅ Normal" if actual_length == length else "⚠️  Atypical"
                        print(f"  Typical length: {length} digits ({status})")
                        break
            
        except Exception as e:
            print(f"❌ Error in advanced analysis: {e}")
    
    def detect_patterns(self, number_str):
        """Detect interesting number patterns"""
        patterns = []
        
        # All same digits
        if len(set(number_str)) == 1:
            patterns.append("All digits are the same")
        
        # Sequential ascending
        if self.is_sequential(number_str, ascending=True):
            patterns.append("Sequential ascending digits")
        
        # Sequential descending
        if self.is_sequential(number_str, ascending=False):
            patterns.append("Sequential descending digits")
        
        # Palindrome
        if number_str == number_str[::-1]:
            patterns.append("Palindrome number")
        
        # Repeated pattern
        repeated = self.find_repeated_pattern(number_str)
        if repeated:
            patterns.append(f"Repeated pattern: {repeated}")
        
        # Consecutive pairs
        if self.has_consecutive_pairs(number_str):
            patterns.append("Contains consecutive digit pairs")
        
        return patterns
    
    def is_sequential(self, number_str, ascending=True):
        """Check if digits are sequential"""
        for i in range(len(number_str) - 1):
            current = int(number_str[i])
            next_digit = int(number_str[i + 1])
            
            if ascending and next_digit != current + 1:
                return False
            elif not ascending and next_digit != current - 1:
                return False
        
        return len(number_str) > 1
    
    def find_repeated_pattern(self, number_str):
        """Find repeated patterns in number"""
        n = len(number_str)
        for pattern_len in range(1, n // 2 + 1):
            pattern = number_str[:pattern_len]
            if pattern * (n // pattern_len) == number_str[:len(pattern) * (n // pattern_len)]:
                return pattern
        return None
    
    def has_consecutive_pairs(self, number_str):
        """Check for consecutive digit pairs"""
        for i in range(len(number_str) - 1):
            if number_str[i] == number_str[i + 1]:
                return True
        return False
    
    def assess_risk(self, number_str):
        """Assess potential risk level of number"""
        risk_factors = 0
        reasons = []
        
        # All same digits
        if len(set(number_str)) == 1:
            risk_factors += 2
            reasons.append("All digits identical")
        
        # Sequential
        if self.is_sequential(number_str, True) or self.is_sequential(number_str, False):
            risk_factors += 2
            reasons.append("Sequential digits")
        
        # Very short number
        if len(number_str) < 7:
            risk_factors += 1
            reasons.append("Very short number")
        
        # Repeated pattern
        if self.find_repeated_pattern(number_str):
            risk_factors += 1
            reasons.append("Repeated pattern")
        
        if risk_factors >= 3:
            return {"level": "🔴 High", "reason": "; ".join(reasons)}
        elif risk_factors >= 2:
            return {"level": "🟡 Medium", "reason": "; ".join(reasons)}
        else:
            return {"level": "🟢 Low", "reason": "Normal number pattern"}
    
    def web_search(self, phone_number):
        """Search for phone number information online"""
        print("\n" + "="*60)
        print("🌐 WEB SEARCH")
        print("="*60)
        
        print("\n⚠️  Web search features should be used responsibly")
        print("   Respect robots.txt and terms of service")
        
        search_queries = [
            f'"{phone_number}"',
            f"phone number {phone_number}",
            f"telephone {phone_number}",
            f"contact {phone_number}"
        ]
        
        print(f"\n🔍 Suggested search queries:")
        for query in search_queries:
            encoded_query = quote(query)
            print(f"  • {query}")
            print(f"    https://www.google.com/search?q={encoded_query}")
        
        # Try some free APIs (educational purposes)
        try:
            print(f"\n📡 Checking free APIs...")
            self.check_free_apis(phone_number)
        except Exception as e:
            print(f"    API check failed: {e}")
    
    def check_free_apis(self, phone_number):
        """Check free phone number APIs"""
        apis = [
            {
                "name": "NumVerify",
                "url": f"http://apilayer.net/api/validate?access_key=YOUR_KEY&number={phone_number}",
                "note": "Requires free API key"
            },
            {
                "name": "AbstractAPI",
                "url": f"https://phonevalidation.abstractapi.com/v1/?api_key=YOUR_KEY&phone={phone_number}",
                "note": "Requires free API key"
            }
        ]
        
        for api in apis:
            print(f"  • {api['name']}: {api['note']}")
    
    def format_output(self, phone_number, info, advanced_data=None):
        """Format final output"""
        print("\n" + "="*60)
        print("📋 SUMMARY REPORT")
        print("="*60)
        
        print(f"\n📱 Target: {phone_number}")
        print(f"📅 Generated: {self.get_timestamp()}")
        
        if info:
            print(f"\n✅ Valid: Yes")
            print(f"🌍 Location: {info.get('location', 'Unknown')}")
            print(f"📞 Carrier: {info.get('carrier', 'Unknown')}")
            print(f"🎯 Type: {info.get('type', 'Unknown')}")
        else:
            print(f"\n❌ Valid: No")
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def run_comprehensive_analysis(self, phone_number, verbose=False, web_search_flag=False):
        """Run complete analysis"""
        self.print_banner()
        
        # Validate input
        if not self.validate_phone_number(phone_number):
            print("❌ Invalid phone number format. Use international format: +1234567890")
            print("   Example: +14155552671 (US) or +442079460000 (UK)")
            return
        
        print(f"🎯 Analyzing: {phone_number}")
        
        try:
            # Basic lookup
            info = self.basic_lookup(phone_number, verbose)
            
            # Advanced analysis
            self.advanced_analysis(phone_number)
            
            # Web search (if requested)
            if web_search_flag:
                self.web_search(phone_number)
            
            # Final summary
            self.format_output(phone_number, info)
            
            print(f"\n{'='*60}")
            print("✅ Analysis complete!")
            print("⚠️  Remember: Use this tool responsibly and legally")
            print(f"{'='*60}")
            
        except KeyboardInterrupt:
            print(f"\n\n⚠️  Operation cancelled by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

def main():
    """Main command line interface"""
    parser = argparse.ArgumentParser(
        description='Phone Number Lookup Tool - Comprehensive phone number analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 phone_lookup.py +14155552671
  python3 phone_lookup.py +442079460000 --verbose
  python3 phone_lookup.py +33145006000 --web
  python3 phone_lookup.py +1234567890 --all

Legal Notice:
  This tool is for educational and authorized testing purposes only.
  Users are responsible for complying with all applicable laws.
        """
    )
    
    parser.add_argument('phone_number', help='Phone number in international format (e.g., +1234567890)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-w', '--web', action='store_true', help='Enable web search suggestions')
    parser.add_argument('-a', '--all', action='store_true', help='Run all analysis types')
    
    args = parser.parse_args()
    
    tool = PhoneLookupTool()
    
    # Determine which analyses to run
    web_search = args.web or args.all
    verbose = args.verbose or args.all
    
    tool.run_comprehensive_analysis(args.phone_number, verbose, web_search)

if __name__ == "__main__":
    # Check dependencies
    try:
        import phonenumbers
        import requests
        import bs4
    except ImportError as e:
        print("❌ Missing dependencies. Please install required packages:")
        print("   pip install phonenumbers requests beautifulsoup4")
        sys.exit(1)
    
    main()
