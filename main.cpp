#include <unistd.h>
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include "utils.hpp"
using namespace std;

int cnt_data=0;

//vector<string> data;
char data_buffer[20002];

void getQuotesFromPage()
{
  // Get all the quotes in a page
	// Parse html that just crawled
	parseHtml(buffer);
  // Find appropriate css selector for single quote
  char art_selector_template[] = "#block-system-main > div > div > div > div.moscone-flipped-container.moscone-flipped-column-content.clearfix > div.moscone-flipped-column-content-region.moscone-flipped-content.panel-panel > div > div > div > div > div > div.view-content";
  char selector[MAX_URL_LEN];

  // generate selector for quote and strip quote
  sprintf(selector, art_selector_template);
  stripContent(selector);

  //cout << stripped << '\n';

  memset(data_buffer, 0, sizeof(data_buffer));
  char *head = stripped;
  char *key = "發布日期：";
  char *key2 = "錯誤】";
  char *p_key, *p_key2;
  
  ofstream file;
  while(head!=nullptr)
  {
    p_key = strstr(head, key);
    if(p_key==nullptr) break;
    p_key2 = strstr(head, key2);
    if(p_key2==nullptr) break;

    strncpy(data_buffer, p_key2+strlen(key2), p_key-p_key2-strlen(key2));
    data_buffer[p_key-p_key2-strlen(key2)]='\0';
    cout << ">> " << data_buffer << '\n';

    char data_name[25];
    sprintf(data_name, "data_%04d.txt", cnt_data);
    //data.push_back(data_buffer);
    file.open(data_name);
    file << data_buffer;
    file.close();
    head = p_key+strlen(key)+16;
    cnt_data++;
  }
}

int main()
{
  init();
  // Find appropriate url template for page enumeration
  int status, page = 1;
  char url_template[] = "https://tfc-taiwan.org.tw/articles/category/26/27";
  char url_template2[] = "https://tfc-taiwan.org.tw/articles/category/26/27?page=%d";
  char url[MAX_URL_LEN];
  bool end;

  // Enumerate Page until End Condition
  do
  {
    // Using sprintf() and url_template to generate url
    if (page==1)
      sprintf(url, url_template);
    else
      sprintf(url, url_template2, page);
    status = requestPage(url);

    if (status == 200)
      getQuotesFromPage();
    sleep(2);
    // Find end condition
    end = (page >= 168);
  } while (!end && page++);

  return 0;
}