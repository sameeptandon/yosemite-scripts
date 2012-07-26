PICLOUD_API_KEY_NUMBER = 0
PICLOUD_API_KEY_PASSWORD = ''
PHONE_NUMBER_TO_TEXT = ''

from urllib2 import * 
import BeautifulSoup
from googlevoice import * 
import cloud

def main():
  # TODO: move (name, url) pairs out of the function as a list of tuples 
  canonical_names = ['half_dome']
  reqs = [ ]
  reqs.append('https://gc.synxis.com/rez.aspx?Chain=398&start=availresults&wsi=&arrive=7/28/2012&depart=7/29/2012&adult=4&child=0&rcp=&DEST=YOSEMITE&=&__utma=101196937.1097410882.1342213067.1342213427.1342218310.3&__utmb=101196937.3.10.1342218310&__utmc=101196937&__utmx=-&__utmz=101196937.1342213427.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)&__utmv=-&__utmk=78880404')

  for i in range(len(reqs)):
  
    #Access the site, get the raw html
    req = urlopen(reqs[i])
    data = req.read()

    #Parse html, the only thing we care about is the HotelListContainer
    soup = BeautifulSoup.BeautifulSoup(data)
    subset_data = soup.find("div", {'class': 'HotelListContainer'})

    #Now tell me if Curry Village is in the Search Results
    is_curry_village_available = unicode(subset_data).find('Curry Village')
    if is_curry_village_available >= 0: 
      voice = Voice()
      voice.login()
      voice.send_sms(PHONE_NUMBER_TO_TEXT, canonical_names[i] + ': Curry Village is Available')

    #And do the same for Housekeeping Camp
    is_housekeeping_camp_available = unicode(subset_data).find('Housekeeping Camp')
    if is_housekeeping_camp_available >= 0: 
      voice = Voice()
      voice.login()
      voice.send_sms(PHONE_NUMBER_TO_TEXT, canonical_names[i] + ': Housekeeping Camp is Available')

#For testing purposes, run main locally to see if the script works 
#main()

#Setup the job on PiCloud as a reoccuring cron job
cloud.setkey(PICLOUD_API_KEY_NUMBER, PICLOUD_API_KEY_PASSWORD)
cloud.cron.register(main, 'yosemite_job', '*/10 17-23 * * *', _env='sameep')
cloud.cron.register(main, 'yosemite_job2', '*/10 0-4 * * *', _env='sameep')
