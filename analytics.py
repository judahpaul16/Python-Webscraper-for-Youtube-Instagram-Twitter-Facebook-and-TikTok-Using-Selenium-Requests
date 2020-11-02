#!/usr/bin/env python3

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from tkinter import simpledialog as tk_input
from tkinter import messagebox, Frame, Label, Entry, StringVar
import tkinter as tk

import base64
import time
import sys
import ssl
import os
import csv
import re

class MainDialog(tk_input.Dialog):

    def body(self, master):
        self.winfo_toplevel().title("Social Media Analytics v5.0")

        Label(master, text="Provide the\nOR enter \'0\'", font=('Helvetica', 14, 'bold')).grid(row=0, column=0)
        Label(master, text="respective social media usernames for lookup,\nif the person doesn't have a particular account:", font=('Helvetica', 14, 'bold')).grid(row=0, column=1)
        Label(master, text="").grid(row=1)
        Label(master, text="Instagram:").grid(row=2)
        Label(master, text="YouTube:").grid(row=3)
        Label(master, text="Twitter:").grid(row=4)
        Label(master, text="Facebook:").grid(row=5)
        Label(master, text="TikTok:").grid(row=6)

        self.e1 = Entry(master, textvariable=StringVar())
        self.e2 = Entry(master, textvariable=StringVar())
        self.e3 = Entry(master, textvariable=StringVar())
        self.e4 = Entry(master, textvariable=StringVar())
        self.e5 = Entry(master, textvariable=StringVar())

        self.e1.grid(row=2, column=1, sticky='nswe')
        self.e2.grid(row=3, column=1, sticky='nswe')
        self.e3.grid(row=4, column=1, sticky='nswe')
        self.e4.grid(row=5, column=1, sticky='nswe')
        self.e5.grid(row=6, column=1, sticky='nswe')
        return self.e1 # initial focus

    def validate(self):
        ig_tag = str(self.e1.get())
        yt_tag = str(self.e2.get())
        twitter_tag = str(self.e3.get())
        fb_tag = str(self.e4.get())
        tiktok_tag = str(self.e5.get())
        self.result = ig_tag, yt_tag, twitter_tag, fb_tag, tiktok_tag
        if ig_tag == '' or yt_tag == '' or twitter_tag == '' or fb_tag == '' or tiktok_tag == '':
            return 0
        else:
            return 1

# Remove html tags from a string
def remove_html_tags(text):

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# centers a tkinter window
def center(master):

    master.withdraw()
    master.update_idletasks()
    width = master.winfo_width()
    frm_width = master.winfo_rootx() - master.winfo_x()
    win_width = width + 3 * frm_width
    height = master.winfo_height()
    titlebar_height = master.winfo_rooty() - master.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = master.winfo_screenwidth() // 3 - win_width // 3
    y = master.winfo_screenheight() // 3 - win_height // 3
    master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    master.resizable(False, False)
    master.deiconify()

def main():

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
    headers = {'User-Agent': user_agent}
    context = ssl.SSLContext()

    ig_tag = ''
    yt_tag = ''
    twitter_tag = ''
    fb_tag = ''
    tiktok_tag = ''

    # get user input
    ROOT = tk.Tk()
    center(ROOT)
    ROOT.update()
    ROOT.withdraw()
    d = MainDialog(ROOT)

    ig_tag = d.result[0].replace(' ', '')
    yt_tag = d.result[1].replace(' ', '%20')
    twitter_tag = d.result[2].replace(' ', '')
    fb_tag = d.result[3].replace(' ', '')
    tiktok_tag = d.result[4].replace(' ', '')

    if ig_tag == '' or yt_tag == '' or twitter_tag == '' or fb_tag == '' or tiktok_tag == '':
        ROOT.destroy()
        raise SystemExit

    no_ig = False
    if ig_tag == "0":
        no_ig = True
        ig_followers = "0"
        ig_engage = "0"
        ig_percentage = "0%"

    no_yt = False
    if yt_tag == "0":
        no_yt = True
        yt_subscribers = "0"
        yt_views = "0"
        yt_percentage = "0%"

    no_twitter = False
    if twitter_tag == "0":
        no_twitter = True
        twitter_followers = "0"
        twitter_likes = "0"
        twitter_percentage = "0%"

    no_fb = False
    if fb_tag == "0":
        no_fb = True
        fb_followers = "0"
        fb_likes = "0"
        fb_percentage = "0%"

    no_tiktok = False
    if tiktok_tag == "0":
        no_tiktok = True
        tiktok_followers = "0"
        tiktok_likes = "0"
        tiktok_percentage = "0%"

    # find youtube channel id for provided youtube channel name
    if no_yt == False:    
        yt_search_html = urlopen(f"https://www.youtube.com/results?search_query={yt_tag}&sp=EgIQAg%253D%253D", context=context)

        try:
            yt_channel_id = re.findall(r"/(channel|user)/([a-zA-Z0-9\-_]+)", yt_search_html.read().decode())[0][1]
            
        except IndexError:
            yt_tag = tk_input.askstring(title="WARNING! YouTube Lookup Failed!",
                parent=ROOT, prompt=f"Please Verify the YouTube Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a YouTube Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            while yt_tag == '':
                yt_tag = tk_input.askstring(title="WARNING! YouTube Lookup Failed!",
                    parent=ROOT, prompt=f"Please Verify the YouTube Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a YouTube Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            if yt_tag == "0":
                no_yt = True
                yt_subscribers = "0"
                yt_views = "0"
                yt_percentage = "0%"
            else:
                yt_search_html = urlopen(f"https://www.youtube.com/results?search_query={yt_tag}&sp=EgIQAg%253D%253D")
                try:
                    yt_channel_id = re.findall(r"/(channel|user)/([a-zA-Z0-9\-_]+)", yt_search_html.read().decode())[0][1]
                except IndexError:
                    pass
    
    # getting the data
    if no_ig == False:   
        ig_url = f"https://socialblade.com/instagram/user/{ig_tag}/"
        ig_url2 = f"https://instagram.com/{ig_tag}/"
        ig_login_url = "https://www.instagram.com/accounts/login/"
    if no_yt == False:
        yt_url = f"https://socialblade.com/youtube/channel/{yt_channel_id}/"
    if no_twitter == False:   
        twitter_url = f"https://socialblade.com/twitter/user/{twitter_tag}/"
    if no_fb == False:   
        fb_url = f"https://socialblade.com/facebook/page/{fb_tag}/"
        fb_url2 = f"https://facebook.com/{fb_tag}/"
    if no_tiktok == False:   
        tiktok_url = f"https://socialblade.com/tiktok/user/{tiktok_tag}/"

    if no_ig == False:
        request_ig = Request(ig_url, headers=headers)
    if no_yt == False:
        request_yt = Request(yt_url, headers=headers)
    if no_twitter == False:    
        request_twitter = Request(twitter_url, headers=headers)
    if no_fb == False:
        request_fb = Request(fb_url, headers=headers)
        request_fb2 = Request(fb_url2, headers=headers)
    if no_tiktok == False:
        request_tiktok = Request(tiktok_url, headers=headers)

    if no_ig == False:
        try:
            ig_page = urlopen(request_ig, context=context).read()
            ig_soup = BeautifulSoup(ig_page, 'html.parser')
            ig_info_block = ig_soup.find('div', attrs={'id': 'YouTubeUserTopInfoBlock'}).find_all('div', recursive=False)
            ig_followers = ig_info_block[2].find('span', attrs={'style': 'font-weight: bold;'})
            ig_likes = int(remove_html_tags(str(ig_info_block[5].find('span', attrs={'style': 'font-weight: bold;'}))).split(".")[0].replace(',',''))
            ig_comments = int(remove_html_tags(str(ig_info_block[6].find('span', attrs={'style': 'font-weight: bold;'}))).split(".")[0].replace(',',''))
            ig_engage = ig_likes + ig_comments

            options = Options()
            options.headless = True
            drv = webdriver.Chrome(executable_path='./chromedriver', options=options)

            drv.get(ig_login_url)
            time.sleep(3)
            try:
                username = "Enter Your IG Username Here"
                password = "Enter Your IG Password Here or Implement a Password Handler."
                drv.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[1]/div/label/input").send_keys(username)
                drv.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[2]/div/label/input").send_keys(password) 
                drv.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[3]/button").click()
                time.sleep(3)
            except:
                pass

            drv.get(ig_url2)
            time.sleep(3)

            try:
                ig_influence = str(drv.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/a/span").get_attribute('innerHTML')).split('+')[-1].replace(' more','')
                drv.quit()

            except:
                messagebox.askretrycancel("Error", "Instagram lookup failed!\nCheck the name and try again.")
                drv.quit()
                main()

        except AttributeError:
            messagebox.askretrycancel("Error", "Instagram lookup failed!\nCheck the name and try again.")
            main()
            
        except (URLError, HTTPError) as e:
            messagebox.askretrycancel("Error", f"Instagram lookup failed!\n{e.reason}")
            main()
    
    if no_yt == False:    
        try:
            request_yt = Request(yt_url, headers=headers)
            yt_page = urlopen(request_yt, context=context).read()
            yt_soup = BeautifulSoup(yt_page, 'html.parser')
            yt_info_block = yt_soup.find('div', attrs={'id': 'YouTubeUserTopInfoBlock'}).find_all('div', recursive=False)
            yt_views = yt_info_block[3].find('span', attrs={'style': 'font-weight: bold;'})
            yt_subscribers = remove_html_tags(str((yt_info_block[2].find('span', attrs={'style': 'font-weight: bold;'}))))
            units = {"K": 1000,"M": 1000000,"B": 1000000000}
            unit = yt_subscribers[-1]

            try:
                yt_subscribers = float(yt_subscribers)
            except ValueError:
                yt_subscribers = '{:,}'.format(float( yt_subscribers[:-1] ) * units[unit]).replace(',','').replace('.0', '')

            yt_percentage = '{:,.2%}'.format((float(remove_html_tags(str(yt_views)).replace(',','')) / float(yt_subscribers)))

        except AttributeError:
            yt_tag = tk_input.askstring(title="WARNING! YouTube Lookup Failed!",
                parent=ROOT, prompt=f"Please Verify the YouTube Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a YouTube Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            while yt_tag == '':
                yt_tag = tk_input.askstring(title="WARNING! YouTube Lookup Failed!",
                    parent=ROOT, prompt=f"Please Verify the YouTube Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a YouTube Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            if yt_tag == "0":
                yt_subscribers = "0"
                yt_views = "0"
                yt_percentage = "0%"
            else:    
                try:
                    request_yt = Request(yt_url, headers=headers)
                    yt_page = urlopen(request_yt, context=context).read()
                    yt_soup = BeautifulSoup(yt_page, 'html.parser')
                    yt_info_block = yt_soup.find('div', attrs={'id': 'YouTubeUserTopInfoBlock'}).find_all('div', recursive=False)
                    yt_views = yt_info_block[3].find('span', attrs={'style': 'font-weight: bold;'})
                    yt_subscribers = remove_html_tags(str((yt_info_block[2].find('span', attrs={'style': 'font-weight: bold;'}))))
                    units = {"K": 1000,"M": 1000000,"B": 1000000000}
                    unit = yt_subscribers[-1]

                    try:
                        yt_subscribers = float(yt_subscribers)
                    except ValueError:
                        yt_subscribers = '{:,}'.format(float( yt_subscribers[:-1] ) * units[unit]).replace('.0', '')
                
                    yt_percentage = '{:,.2%}'.format((float(remove_html_tags(str(yt_views)).replace(',','')) / float(yt_subscribers)))

                except AttributeError:
                    messagebox.askretrycancel("ERROR! YouTube Lookup Failed!", "Check the name and try again.")
                    main()

        except (URLError, HTTPError) as e:
            messagebox.askretrycancel("Error", f"YouTube lookup failed!\n{e.reason}")
            main()

    if no_twitter == False:
        try:
            twitter_page = urlopen(request_twitter, context=context).read()
            twitter_soup = BeautifulSoup(twitter_page, 'html.parser')
            twitter_info_block = twitter_soup.find('div', attrs={'id': 'YouTubeUserTopInfoBlock'}).find_all('div', recursive=False)
            twitter_followers = twitter_info_block[1].find('span', attrs={'style': 'font-weight: bold;'})
            twitter_likes = twitter_info_block[3].find('span', attrs={'style': 'font-weight: bold;'})
            twitter_percentage = '{:,.2%}'.format((float(remove_html_tags(str(twitter_likes)).replace(',','')) / float(remove_html_tags(str(twitter_followers)).replace(',',''))))
        
        except AttributeError:
            twitter_tag = tk_input.askstring(title="WARNING! Twitter Lookup Failed!",
                parent=ROOT, prompt=f"Please Verify the Twitter Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a Twitter Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            while twitter_tag == '':
                twitter_tag = tk_input.askstring(title="WARNING! Twitter Lookup Failed!",
                    parent=ROOT, prompt=f"Please Verify the Twitter Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a Twitter Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            if twitter_tag == "0":
                twitter_followers = "0"
                twitter_likes = "0"
                twitter_percentage = "0%"
            else:    
                try:
                    twitter_url = f"https://socialblade.com/twitter/user/{twitter_tag}"
                    request_twitter = Request(twitter_url, headers=headers)
                    twitter_page = urlopen(request_twitter, context=context).read()
                    twitter_soup = BeautifulSoup(twitter_page, 'html.parser')
                    twitter_info_block = twitter_soup.find('div', attrs={'id': 'YouTubeUserTopInfoBlock'}).find_all('div', recursive=False)
                    twitter_followers = twitter_info_block[1].find('span', attrs={'style': 'font-weight: bold;'})
                    twitter_likes = twitter_info_block[3].find('span', attrs={'style': 'font-weight: bold;'})
                    twitter_percentage = '{:,.2%}'.format((float(remove_html_tags(str(twitter_likes)).replace(',','')) / float(remove_html_tags(str(twitter_followers)).replace(',',''))))
                
                except AttributeError:
                    messagebox.askretrycancel("ERROR! Twitter Lookup Failed!", "Check the name and try again.")
                    main()

        except (URLError, HTTPError) as e:
            messagebox.askretrycancel("Error", f"Twitter lookup failed!\n{e.reason}")
            main()
    
    if no_fb == False:    
        try:
            fb_page = urlopen(request_fb, context=context).read()
            fb_soup = BeautifulSoup(fb_page, 'html.parser')
            fb_page2 = urlopen(request_fb2, context=context).read()
            fb_soup2 = BeautifulSoup(fb_page2, 'html.parser')
            fb_likes = fb_soup.find('div', attrs={'style': 'padding: 0px 50px 30px 50px; text-align: center;'}).find_all('p', attrs={'style': 'color:#aaa; font-size: 10pt;'})[0]
            fb_followers = fb_soup2.find('div', attrs={'id': 'PagesProfileHomeSecondaryColumnPagelet'}).find('div', {'class':'_4-u2 _6590 _3xaf _4-u8'}).find_all('div', {'class':'_2pi9 _2pi2'}, recursive=False)[1].find('div', {'class':'_4bl9'}).find('div')
            fb_percentage = '{:,.2%}'.format((float(remove_html_tags(str(fb_likes)).split()[0].replace(',','').lstrip()) / float(remove_html_tags(str(fb_followers)).split()[0].replace(',','').lstrip())))
        
        except AttributeError:
            fb_tag = tk_input.askstring(title="WARNING! Facebook Lookup Failed!",
                parent=ROOT, prompt=f"Please Verify the Facebook Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a Facebook Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            while fb_tag == '':
                fb_tag = tk_input.askstring(title="WARNING! Facebook Lookup Failed!",
                    parent=ROOT, prompt=f"Please Verify the Facebook Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a Facebook Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')

            if fb_tag == "0":
                fb_followers = "0"
                fb_likes = "0"
                fb_percentage = "0%"
            else:    
                try:
                    fb_url = f"https://socialblade.com/facebook/page/{fb_tag}"
                    fb_url2 = f"https://facebook.com/{fb_tag}"
                    request_fb = Request(fb_url, headers=headers)
                    request_fb2 = Request(fb_url2, headers=headers)
                    fb_page = urlopen(request_fb, context=context).read()
                    fb_page2 = urlopen(request_fb2, context=context).read()
                    fb_soup = BeautifulSoup(fb_page, 'html.parser')
                    fb_soup2 = BeautifulSoup(fb_page2, 'html.parser')
                    fb_likes = fb_soup.find('div', attrs={'style': 'padding: 0px 50px 30px 50px; text-align: center;'}).find_all('p', attrs={'style': 'color:#aaa; font-size: 10pt;'})[0]
                    fb_followers = fb_soup2.find('div', attrs={'id': 'PagesProfileHomeSecondaryColumnPagelet'}).find('div', {'class':'_4-u2 _6590 _3xaf _4-u8'}).find_all('div', {'class':'_2pi9 _2pi2'}, recursive=False)[1].find('div', {'class':'_4bl9'}).find('div')
                    fb_percentage = '{:,.2%}'.format((float(remove_html_tags(str(fb_likes)).split()[0].replace(',','').lstrip()) / float(remove_html_tags(str(fb_followers)).split()[0].replace(',','').lstrip())))

                except AttributeError:
                    messagebox.askretrycancel("Error", "Facebook lookup failed!\nCheck the name and try again.")
                    main()
        
                except (URLError, HTTPError):
                    fb_tag = tk_input.askstring(title="WARNING! Facebook Lookup Failed!",
                        parent=ROOT, prompt=f"Please Verify the Facebook Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a Facebook Account:\n" +
                            "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
                    while fb_tag == '':
                        fb_tag = tk_input.askstring(title="WARNING! Facebook Lookup Failed!",
                            parent=ROOT, prompt=f"Please Verify the Facebook Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a Facebook Account:\n" +
                            "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')

                    if fb_tag == "0":
                        fb_followers = "0"
                        fb_likes = "0" 
                        fb_percentage = "0%"
                    else:
                        try:
                            fb_url = f"https://socialblade.com/facebook/page/{fb_tag}"
                            fb_url2 = f"https://facebook.com/{fb_tag}"
                            request_fb = Request(fb_url, headers=headers)
                            request_fb2 = Request(fb_url2, headers=headers)
                            fb_page = urlopen(request_fb, context=context).read()
                            fb_page2 = urlopen(request_fb2, context=context).read()
                            fb_soup = BeautifulSoup(fb_page, 'html.parser')
                            fb_soup2 = BeautifulSoup(fb_page2, 'html.parser')
                            fb_likes = fb_soup.find('div', attrs={'style': 'padding: 0px 50px 30px 50px; text-align: center;'}).find_all('p', attrs={'style': 'color:#aaa; font-size: 10pt;'})[0]
                            fb_followers = fb_soup2.find('div', attrs={'id': 'PagesProfileHomeSecondaryColumnPagelet'}).find('div', {'class':'_4-u2 _6590 _3xaf _4-u8'}).find_all('div', {'class':'_2pi9 _2pi2'}, recursive=False)[1].find('div', {'class':'_4bl9'}).find('div')
                            fb_percentage = '{:,.2%}'.format((float(remove_html_tags(str(fb_likes)).split()[0].replace(',','').lstrip()) / float(remove_html_tags(str(fb_followers)).split()[0].replace(',','').lstrip())))

                        except (URLError, HTTPError) as e:
                            messagebox.askretrycancel("Error", f"Facebook lookup failed!\n{e.reason}")
                            main()

        except (URLError, HTTPError):
            fb_tag = tk_input.askstring(title="WARNING! Facebook Lookup Failed!",
                parent=ROOT, prompt=f"Please Verify the Facebook Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a Facebook Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            while fb_tag == '':
                fb_tag = tk_input.askstring(title="WARNING! Facebook Lookup Failed!",
                    parent=ROOT, prompt=f"Please Verify the Facebook Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a Facebook Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')

            if fb_tag == "0":
                fb_followers = "0"
                fb_likes = "0" 
                fb_percentage = "0%"
            else:
                try:
                    fb_url = f"https://socialblade.com/facebook/page/{fb_tag}"
                    fb_url2 = f"https://facebook.com/{fb_tag}"
                    request_fb = Request(fb_url, headers=headers)
                    request_fb2 = Request(fb_url2, headers=headers)
                    fb_page = urlopen(request_fb, context=context).read()
                    fb_page2 = urlopen(request_fb2, context=context).read()
                    fb_soup = BeautifulSoup(fb_page, 'html.parser')
                    fb_soup2 = BeautifulSoup(fb_page2, 'html.parser')
                    fb_likes = fb_soup.find('div', attrs={'style': 'padding: 0px 50px 30px 50px; text-align: center;'}).find_all('p', attrs={'style': 'color:#aaa; font-size: 10pt;'})[0]
                    fb_followers = fb_soup2.find('div', attrs={'id': 'PagesProfileHomeSecondaryColumnPagelet'}).find('div', {'class':'_4-u2 _6590 _3xaf _4-u8'}).find_all('div', {'class':'_2pi9 _2pi2'}, recursive=False)[1].find('div', {'class':'_4bl9'}).find('div')
                    fb_percentage = '{:,.2%}'.format((float(remove_html_tags(str(fb_likes)).replace(' page likes','').replace(',','').lstrip()) / float(remove_html_tags(str(fb_followers)).replace(' people follow this','').replace(',','').lstrip())))

                except (URLError, HTTPError) as e:
                    messagebox.askretrycancel("Error", f"Facebook lookup failed!\n{e.reason}")
                    main()

    if no_tiktok == False:
        try:
            tiktok_page = urlopen(request_tiktok, context=context).read()
            tiktok_soup = BeautifulSoup(tiktok_page, 'html.parser')
            tiktok_info_block = tiktok_soup.find('div', attrs={'id': 'YouTubeUserTopInfoBlock'}).find_all('div', recursive=False)
            tiktok_followers = tiktok_info_block[2].find('span', attrs={'style': 'font-weight: bold;'})
            tiktok_likes = tiktok_info_block[4].find('span', attrs={'style': 'font-weight: bold;'})
            tiktok_percentage = '{:,.2%}'.format((float(remove_html_tags(str(tiktok_likes)).replace(',','')) / float(remove_html_tags(str(tiktok_followers)).replace(',',''))))
        
        except AttributeError:
            tiktok_tag = tk_input.askstring(title="WARNING! TikTok Lookup Failed!",
                parent=ROOT, prompt=f"Please Verify the TikTok Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a TikTok Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            while tiktok_tag == '':
                tiktok_tag = tk_input.askstring(title="WARNING! TikTok Lookup Failed!",
                    parent=ROOT, prompt=f"Please Verify the TikTok Name Separately For \'{ig_tag}\' OR Type \'0\' If The Person Doesn't Have a TikTok Account:\n" +
                    "\n    /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ /!\ Warning Message /!\ \n").replace(' ', '')
            if tiktok_tag == "0":
                tiktok_followers = "0"
                tiktok_likes = "0"
                tiktok_percentage = "0%"
            else:    
                try:
                    tiktok_url = f"https://socialblade.com/tiktok/user/{tiktok_tag}"
                    request_tiktok = Request(tiktok_url, headers=headers)
                    tiktok_page = urlopen(request_tiktok, context=context).read()
                    tiktok_soup = BeautifulSoup(tiktok_page, 'html.parser')
                    tiktok_info_block = tiktok_soup.find('div', attrs={'id': 'YouTubeUserTopInfoBlock'}).find_all('div', recursive=False)
                    tiktok_followers = tiktok_info_block[2].find('span', attrs={'style': 'font-weight: bold;'})
                    tiktok_likes = tiktok_info_block[4].find('span', attrs={'style': 'font-weight: bold;'})
                    tiktok_percentage = '{:,.2%}'.format((float(remove_html_tags(str(tiktok_likes)).replace(',','')) / float(remove_html_tags(str(tiktok_followers)).replace(',',''))))
                
                except AttributeError:
                    messagebox.askretrycancel("ERROR! TikTok Lookup Failed!", "Check the name and try again.")
                    main()

        except (URLError, HTTPError) as e:
            messagebox.askretrycancel("Error", f"{e.reason}")
            main()

    # check for duplicate entries
    lines = list()
    tag = ig_tag.replace('%20', ' ').title()
    with open('social_media_stats.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == tag:
                    lines.remove(row)
    with open('social_media_stats.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

    # write the data to file
    file = open(
            'social_media_stats.csv',
            'a',
            newline='',
            encoding='utf-8'
        )
    writer = csv.writer(file)

    writer.writerow(
        [
            tag,
            ig_influence,
            remove_html_tags(str(ig_followers)),
            str("{:,}".format(ig_engage)),
            '{:,.2%}'.format((ig_engage / float(remove_html_tags(str(ig_followers)).replace(',','')))),
            str("{:,}".format(int(yt_subscribers))),
            remove_html_tags(str(yt_views)),
            yt_percentage,
            remove_html_tags(str(twitter_followers)),
            remove_html_tags(str(twitter_likes)),
            twitter_percentage,
            remove_html_tags(str(fb_followers)).split()[0].lstrip(),
            remove_html_tags(str(fb_likes)).split()[0].lstrip(),
            fb_percentage,
            remove_html_tags(str(tiktok_followers)),
            remove_html_tags(str(tiktok_likes)),
            tiktok_percentage,
        ]
    )

    main()
    
if __name__ == "__main__":

    file = open(
        'social_media_stats.csv',
        'a',
        newline='',
        encoding='utf-8'
    )
    writer = csv.writer(file)

    # creates the csv file if it doesn't exist
    if os.path.getsize('social_media_stats.csv')==0:    
        writer.writerow(
            [
                'DJ / Personality',
                'IG Influence',
                'IG Followers',
                'IG Engagement',
                'IG E/F Percentage',
                'YouTube Subscribers',
                'YouTube Views',
                'YouTube V/S Percentage',
                'Twitter Followers',
                'Twitter Likes',
                'Twitter L/F Percentage',
                'FB Followers',
                'FB Likes',
                'FB L/F Percentage',
                'TikTok Followers',
                'TikTok Likes',
                'TikTok L/F Percentage',
            ]
        )
    file.close()
    main()
