#####################################################################################################################################
# This code checks a given list of park run events for the previous week, for a given list of names, e.g. joe blogs
# and or members of specific running clubs e.g. 'speed freaks'.
# it then collates those people's run statistics into a speadsheet. 
# people are also recorded if they volunteer
# this hasn't been tested in an event cancellation situation, code may fall over if attempting to check an event that is cancelled.
# current to 12/4/25
#####################################################################################################################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def get_random_n_char_string(numChars):
    import random
    import string

    # Generate a random 4-character string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=numChars))
    print(random_string)
    return random_string

# Define the target URL and list of runner names to search for
def mainFunction():
    names_to_search = [
    "lowercase parkrun name here",
    "john doe",
    "jane o'doe",

]

# this is thepark run name from the event url  e.g. https://www.parkrun.co.nz/orakeibay/results/latestresults/
    parkruns_to_search = [
                            'northernpathway'
                            ,'sherwoodreserve'
                            ,'southernpath'
                            ]

    # Function to write results to CSV
    def write_to_csv(datestring, data, ):
        filename="parkrun_results_"+datestring+"_"+str(get_random_n_char_string(4))+".csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Park R","Date", "Position", "Name", "Gender", "Age Category", "Time", "Club"])
            for row in data:
                writer.writerow(row)

    # Set up Selenium WebDriver (adjust the path to your WebDriver as needed)
    driver = webdriver.Chrome()
    output_data = []
    for pr in parkruns_to_search:

            #### note that this is a country specific URL, if you are not in NZ, CHANGE THE URL!!!
            url = "https://www.parkrun.co.nz/"+str(pr)+"/results/latestresults/"
            print("Now doing \n"+str(pr))

            # Load the page
            driver.get(url)

            # Wait for the results table to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Results")))

            # Initialize the output data
            dates = driver.find_elements(By.CSS_SELECTOR, ".format-date")
            for date in dates:
                prDate = date

            dates = driver.find_elements(By.CSS_SELECTOR, ".format-date")
            for date in dates:
                event_date = date.text.strip()
                print(f"Event Date: {event_date}")
                prDate = event_date
            # Scrape the results table
            rows = driver.find_elements(By.CSS_SELECTOR, "table.Results-table tr")
             
            for row in rows[1:]:  # Skip the header row
                # print("row \n"+str(row))
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 5:
                    position = cols[0].text.strip()
                    name = cols[1].text.strip()
                    gender = cols[2].text.strip()
                    age_category = cols[3].text.strip()
                    club = cols[4].text.strip()
                    time = cols[5].text.strip()

                    decorator = ""
                    # Check if cols[5] contains specific classes
                    class_attr = cols[5].get_attribute("class")  # Get the class attribute of cols[5]
                    if "Results-table-td--pb" in class_attr:
                        decorator  = decorator +"PB! " 
                    if "Results-table-td--ft" in class_attr:
                        decorator  = decorator +"FT " 
                     
                    if name.lower() in names_to_search or club.lower()=="pr running club name lower case":
                        output_data.append([pr,prDate,position, name, gender, age_category,decorator+ time, club,""])

            # Scrape the volunteers section
            try:
                volunteer_section = driver.find_element(By.CLASS_NAME, "paddedb")
                volunteers = volunteer_section.find_elements(By.TAG_NAME, "a")
                for volunteer in volunteers:
                    volunteer_name = volunteer.text.strip()
                    if volunteer_name.lower() in names_to_search  or club.lower()=="pr running club name lower case":
                        output_data.append([pr,prDate,"Volunteer", volunteer_name])
            except:
                print("Volunteer section not found.")

            # Write the results to a CSV file
     
        # Close the WebDriver
    write_to_csv(prDate.replace("/","_"), output_data)

    print("Scraping completed. Results saved to v:/parkrun_results_"+str(prDate)+".csv")
    driver.quit()


###################################################################   main  ###################################################################    
###################################################################   main  ###################################################################    
###################################################################   main  ###################################################################    

if __name__ == "__main__":

    # stuff only to run when NOT  called via 'import' here
    print("\n======================================  running "+__name__+" from main ======================================  \n")

    result = mainFunction()
else:
     # stuff   to run when   called via 'import' here
    print("\n___       ++++++++++++++++++++++++ imported "+__name__)
    