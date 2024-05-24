from bs4 import BeautifulSoup
import requests
import logging
import dotenv
import pprint
import os


dotenv.load_dotenv()
logger = logging.getLogger()


N_RESULTS = 3


def ask_brave(query:str, n_results:int):
    print("\n\n########### AI ASKED FOLLOWING QUERY ###########\n\n")
    print(query)
    
    url = f"https://api.search.brave.com/res/v1/web/search"
    
    params = {
        "q": query,
        "count": str(n_results),
    }
    
    headers = {
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.getenv("BRAVE_KEY"),
    }
    
    resp = requests.get(url, headers=headers, params=params)
    
    if str(resp.status_code)[0] in ["4", "5"]:
        print("error occured")
        return "no information found"
        
        
    data = resp.json()
    #pprint.pprint(data)
    
    web_results:str = ""
    for i, result in enumerate(data["web"]["results"]):
        result_url: str = result["url"]
        
        try:
            resp = requests.get(result_url)
            text:str = BeautifulSoup(resp.text, "html.parser").get_text()
            
            web_results += f"RESULT {str(i)}: \n\n"
            web_results += text.replace("\n", " ").replace("  ", "")
            
                
        except Exception as e:
            logger.error(str(e))
            print(f"Could not parse {result_url}")
            
    
    print("\n\n########### AI GOT FOLLOWING DATA ###########\n\n")
    print(web_results)
    return web_results


class AskBrave:
    name = "AskQuestion"
    input_variable = "query"
    desc = "searches the internet for the query and returns information"

    def __init__(self, k=3):
        pass
    
    def __call__(self, query:str) -> str:
        text:str = ask_brave(query, n_results=N_RESULTS)
        return text