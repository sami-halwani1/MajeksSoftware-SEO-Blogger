from openai import OpenAI
import json
import csv
from datetime import datetime
import os

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
      if (self.apiKey == None): self.apiKey = "YOUR_API_KEY"
      self.client = OpenAI(api_key=self.apiKey)      


  
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

          print(current_topic)
          #current_topic = f'blogTopic{num}'
          if len(client_data[index]['Previous Topics']) == 0:
             client_data[index]['Previous Topics'] = current_topic
          else:
            client_data[index]['Previous Topics'] = f'{client_data[index]['Previous Topics']}|{current_topic}'

          blogTopics.append({'businessName': row["Business Name"], 'businessType': row["Business Type"], 'seoLocation': row["Target Location"], 'blogTopic': f'blogTopic{num}'})
        
      return blogTopics,client_data
   
   def generateBlogs(self, blogTopics):
      now = datetime.now()
      now = now.strftime("%m-%d-%Y")

      folder = f'{str(now)}_blogs'
      os.makedirs(folder, exist_ok=True)

      for i in range(len(blogTopics)):
        businessFolder = os.path.join(folder, blogTopics[i]["businessName"])
        os.makedirs(businessFolder, exist_ok=True)
        file_path = os.path.join(businessFolder, f'{blogTopics[i]["blogTopic"]}.txt')

        # response = self.client.chat.completions.create(
        #   model = "gpt-4o-mini",
        #   store=True,
        #   messages=[
        #       {"role": "developer",
        #       "content": f''
        #     }
        #   ],
        #   response_format={"type": "json_object"}
        # )

        with open(file_path, "w") as file:
          file.write(f'{blogTopics[i]["blogTopic"]}')
          # print(f"File saved at: {file_path}")
      
      return 
# response = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "developer",
#      "content": "You are an SEO Specialist trying to improve a Software companies Website SEO. The company name is \'Majeks Software\'. Please provide me a List of 5 Blog Topics to improve their websites search engine ranking. Blog Topic should be formatted as a json file. Each Topic should include the topic title, topic_metaTitle, and topic_metaDescription."
#     }
#   ],
#   response_format={"type": "json_object"}
# )

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user",
#      "content": "Write me the full Blog Given the prompt.(Not a Structured Outline) The Blog MUST be 400 Words. Return the Blog in <HTML> Format: \"topic_title\": \"The Importance of Cybersecurity in Software Development\", \"topic_metaTitle\": \"Cybersecurity in Software Development | Majeks Software\", \"topic_metaDescription\": \"Understand the critical role cybersecurity plays in software development. Majeks Software discusses best practices and strategies to secure your applications.\""
#     }
#   ]
# )

# json_content = response.choices[0].message.content
# print(json_content)

# if isinstance(json_content, str):
#     json_data = json.loads(json_content)

# json_name = "openai_response.json"

# with open(json_name , 'w') as json_file:
#     json.dump(json_data, json_file, indent=4)



# print(f'JSON response saved as {json_name}')
# json_name = "openai_response.json"
# with open(json_name, 'r') as json_content:
#     json_data = json.load(json_content)
# print(json_data)


# for topic in range(len(json_data['blogTopics'])):
#     print(f'Topic {topic}\n---------')
#     print(f'Title: {json_data['blogTopics'][topic]["topicTitle"]}')
#     print(f'MetaTitle: {json_data['blogTopics'][topic]["topic_metaTitle"]}')
#     print(f'MetaDescription: {json_data['blogTopics'][topic]["topic_metaDescription"]}')
#     print("---------\n")

# print(json_data['blogTopics'][0])

# json_useCase = json_data['blogTopics'][0]

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user",
#      "content": f"Write me the full Blog Given the prompt.(Not a Structured Outline) The Blog MUST be 400 Words. Return the Blog in <HTML> Format: {json_useCase}"
#     }
#   ]
# )

# print(completion.choices[0].message.content)

if __name__ == "__main__":
  # openAI_client = OpenAI( api_key="Your_API_Key")

  client_details = "tentative_blogging_schedule.csv"
  client_data = []
  with open(client_details, newline='', encoding='utf-8') as file:
     reader = csv.DictReader(file)
     for row in reader:
        client_data.append(dict(row))


  # json_file = "client_details.json"
  # # print(client_data)
  # with open(json_file, "w", encoding="utf-8") as jsonf:
  #   json.dump(client_data, jsonf, indent=4)  # Pretty print with indentation

  seoBlogger = SEOBlogger()
  blogTopics,client_data = seoBlogger.generateBlogTopics(client_data)
  print(client_data)
  seoBlogger.generateBlogs(blogTopics)
  # print(blogTopics)

  