#include "curl/curl.h"
#include "gq/Document.h"
#include "gq/Node.h"
#include <cstring>
using namespace std;

const int MAX_DOC_LEN = 1048576;
const int MAX_URL_LEN = 1024;
char buffer[MAX_DOC_LEN];
char stripped[MAX_DOC_LEN];
CDocument doc;

void init();
int requestPage(const char url[]);

void init(){
  curl_global_init(CURL_GLOBAL_DEFAULT);
}

size_t writeFunction(char *ptr, size_t size, size_t nmemb,
                  std::string *data){
  if(data == NULL)
    return 0;
 
  data->append(ptr, size*nmemb);
 
  return size * nmemb;
}

int requestPage(const char url[]){
  std::string response_string;
  std::string header_string;

  auto curl = curl_easy_init();
  long status_code;

  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "curl/7.42.0");
    curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 50L);
    curl_easy_setopt(curl, CURLOPT_TCP_KEEPALIVE, 1L);

    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeFunction);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string);

    curl_easy_perform(curl);
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);

    strcpy(buffer, response_string.c_str());

    curl_easy_cleanup(curl);
    curl = NULL;

    return status_code;
  }

  return -1;
}

void parseHtml(const char html[]){
	doc.parse(html);
}

int stripContent(const char selector[]){
  CSelection c = doc.find(selector);

  if(c.nodeAt(0).valid()){
    strcpy(stripped, c.nodeAt(0).text().c_str());
    return 0;
  }

  return 1;
}