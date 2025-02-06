from openai import OpenAI
import json
import csv
from datetime import datetime
import os
import re

"""
Author: Majeks Software LLC
Developer: Sami Halwani
Project Name: SEO Blogger
Description: The Purpose of this application is to create an automated blogging tool using the OpenAI API. 



"""
class SEOBlogger():
   
   def __init__(self): #initialize openAI API client
      self.apiKey = os.getenv("API_KEY")
      # print(self.apiKey)
      if (self.apiKey == None): 
        self.apiKey = "YOUR_API_KEY"
      self.client = OpenAI(api_key=self.apiKey)    
      self.now = datetime.now().strftime("%m-%d-%Y")

  
   def generateBlogTopics(self, client_data: list): #Generate a List of Blog Topics Based on the tentative_blogging_schedule.csv File. 
      blogTopics = []
      for index,row in enumerate(client_data):
        for num in range(int(row["Number of Blogs"])):
          prompt = (f'You are an SEO Specialist Trying to improve a {row["Business Type"]}\'s website SEO. ' +
            f'The {row["Business Type"]}\'s name is {row["Business Name"]} and they are looking to improve their SEO for {row["Target Location"]}. ' +
            f'Blog Topics should be similar to: {row["Similar Topics"]}; Randomly Select from the Similar Topics. Avoid using previously used topics like: "{row["Previous Topics"]}". ' + 
            f'Provide me a Single Topic Based on this Prompt. Only Provide me the String of the Topic. Nothing More. Do not put it in Quotes')
          
          current_topic = f'blogTopic{num}'
          if self.apiKey != "Your_API_Key":
            response = self.client.chat.completions.create(
              model = "gpt-4o-mini",
              store=True,
              messages=[
                  {"role": "developer",
                  "content": f'{prompt}'
                }
              ],
            )
            current_topic = response.choices[0].message.content

          # print(current_topic)
          if len(client_data[index]['Previous Topics']) == 0:
             client_data[index]['Previous Topics'] = current_topic
          else:
            client_data[index]['Previous Topics'] = f'{client_data[index]['Previous Topics']}|{current_topic}'

          blogTopics.append({'businessName': row["Business Name"], 'businessType': row["Business Type"], 'seoLocation': row["Target Location"], 'blogTopic': re.sub(r"[\\/:*?\"<>|]", "" , current_topic)})
        
      return blogTopics,client_data
   
   def generateBlogJson(self, blogTopic):
      jsonTopic = []
      prompt = (f'You are an SEO Specialist tasked on improving a {blogTopic["businessType"]}\'s Website SEO. '+
                f'The Business Name is {blogTopic["businessName"]}, focusing on improving the website SEO for {blogTopic["seoLocation"]}. '+
                f'Write a prompt that can be used to generate a 800-1000 word, Long-Form, blog to improve {blogTopic["businessName"]}\'s search engine ranking. '+
                f'The topic of this blog will be {blogTopic["blogTopic"]}. Include headers for the sections to be discussed in this blog. '+
                f'The prompt should be formatted as a json. The Layout should be as such: ' + 
                "{'businessName': '<businessName>', " +
                "'seoLocation': '<seoLocation City, State>', " +
                "'blogTopic': '<blogTopic>', " +
                "'meta-title': '<meta-title>', " +
                "'meta-desc': '<meta-description>'," + 
                "'Discussion': [{'header2-item': '<Topic of header 2 Section>', header2-subjects: ['subject1','subject2','Subject3',...]}]} "+
                f'Discussions section should include 6-8 or more headers not including an introduction, conclusion and "Why Choose {blogTopic["businessName"]}" section. '
                )
      
      if self.apiKey != "Your_API_Key":
        response = self.client.chat.completions.create(
          model="gpt-4o-mini",
          store=True,
          messages=[
            {"role": "system",
            "content": "You are an AI assistant that responds in JSON format."
            },
            {"role": "user",
            "content": prompt
            }
          ],
          response_format={"type": "json_object"}
        )
      jsonTopic = response.choices[0].message.content

      return jsonTopic
   

   def generateBlogs(self, blogTopic, json):
      
      folder = f'{str(self.now)}_blogs'
      os.makedirs(folder, exist_ok=True)

      businessFolder = os.path.join(folder, blogTopic["businessName"])
      os.makedirs(businessFolder, exist_ok=True)
      file_path = os.path.join(businessFolder, f'{blogTopic["blogTopic"]}.txt')

      response = self.client.chat.completions.create(
        model = "gpt-4o-mini",
        store=True,
        messages=[
            {"role": "system",
            "content": "You are an AI SEO Specialist that Returns the Response in HTML"
          },
          {"role": "user",
            "content": (f'Write me the full Blog Given the prompt.(Not a Structured Outline) The Blog MUST be 800-1000 Words: {json}' + 
                        f'Do Not include a footer with a "All Rights Reserved". Also do no include the(```html ```) in the content.'+
                        f'Be sure to focus on Best in practice SEO. ')
          }
        ],
      )

      blog = response.choices[0].message.content

      with open(file_path, "w", encoding="utf-8") as file:
        file.write(f'{blog}')
      
      return 



if __name__ == "__main__":

  # client_details = "client_data_defaults.csv"
  client_details = "client_data_test.csv"
  # client_details = "client_data.csv"
  
  client_data = []
  with open(client_details, newline='', encoding='utf-8') as file:
     reader = csv.DictReader(file)
     for row in reader:
        client_data.append(dict(row))


  seoBlogger = SEOBlogger()
  blogTopics,client_data = seoBlogger.generateBlogTopics(client_data)

  # Create Tenative Blogging Schedule for Current Cycle
  with open(f'{seoBlogger.now}_blogTopics.csv', mode="w", newline="") as file:

     fieldnames = ["businessName", "businessType", "seoLocation", "blogTopic" ]
     writer = csv.DictWriter(file, fieldnames=fieldnames)
     writer.writeheader()
     writer.writerows(blogTopics)

  # Store Client Blogging Details Based on Current Cycle
  with open(f'client_data.csv', mode="w", newline="") as file:
     fieldnames = ["Business Name","Business Type","Target Location","Number of Blogs","Previous Topics","Similar Topics"]
     writer = csv.DictWriter(file, fieldnames=fieldnames)
     writer.writeheader()
     writer.writerows(client_data)

  json_list = []
  for blogTopic in blogTopics:
    seoBlogger.generateBlogs(blogTopic, json.loads(seoBlogger.generateBlogJson(blogTopic)))
  
  #seoBlogger.generateBlogs(blogTopics)
  

  