import entergy_scrapper
#import mp_scrapper
#import riviera_scrapper
#import al_scrapper
#import cleco_scrapper
from time import sleep


def main():
    print("start main")
    entergy_scrapper.current_entergy("Louisiana","zip")
    sleep(1)
    entergy_scrapper.current_entergy("Louisiana","county")
    sleep(1)
    entergy_scrapper.current_entergy("Mississippi","county")
    sleep(1)
    entergy_scrapper.current_entergy("Mississippi","zip")
    #riviera_scrapper.current_riviera()
    #al_scrapper.get_al_outages("zip")
    #al_scrapper.get_al_outages("county")
    #sleep(5)
    #cleco_scrapper.get_cleco_outages("county")
    #sleep(3)
    #cleco_scrapper.get_cleco_outages("zip")
    #mp_scrapper.csv_step("county")
    #sleep(6)
    #mp_scrapper.csv_step("town")
    print("end main")

if __name__ == "__main__":
    main()