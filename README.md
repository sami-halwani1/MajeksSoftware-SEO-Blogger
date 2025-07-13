# SEO Blogger
**Automated Blog Generation for SEO Optimization Using OpenAI**

## Overview
**SEO Blogger** is a Python-based automation tool built to generate long-form SEO-optimized blog content for businesses. It leverages the OpenAI API to:
- Suggest blog topics tailored to a client's niche and location
- Generate JSON-formatted blog outlines
- Produce full-length (800–1000 word) HTML blogs with headers and SEO best practices

---

## Features

- **Smart Topic Generation**  
  Avoids duplicate topics and intelligently pulls ideas from a list of similar topics.

- **Prompt Engineering**  
  Uses custom-crafted prompts to get structured outlines or full blog content from OpenAI.

- **Organized Output**  
  Blogs are saved in date-stamped folders, organized by business name.

- **CSV Integration**  
  Reads and updates client data from a structured `.csv` file.

- **Dynamic JSON Prompting**  
  Requests OpenAI to respond in clean JSON format for structured blog outlines.

---

## File Structure
<pre>```
.
├── client_data.csv # Input CSV containing business info
├── <MM-DD-YYYY>_blogTopics.csv # Output CSV of generated topics
├── <MM-DD-YYYY>_blogs/ # Output folder with subfolders per business
│ └── <BusinessName>/
│ └── <Topic>.txt # HTML blog content
├── seo_blogger.py # Main script

```</pre>

---

## CSV Input Format (`client_data.csv`)

| Business Name | Business Type | Target Location | Number of Blogs | Previous Topics | Similar Topics |
|---------------|----------------|------------------|------------------|------------------|------------------|
| MajeksSoftwareLLC | Cloud R&D | Santa Ana, CA | 1 | "Why AWS Is the Best Tool for your Cloud Infrastructure" | AWS Cloudformation: Why Use Infrastructure as Code \| EC2 vs Lambda: What Should You Use for Your Application |

- **Previous Topics**: Pipe-separated string of old topics (e.g., `BlogA | BlogB`)
- **Similar Topics**: Ideas to pull inspiration from when prompting

---

## Usage

1. **Set up OpenAI API Key**  
   Add your API key to your environment:
   ```bash
   export API_KEY='your_openai_key_here'
   ```

## Edit Client Data
Modify or create client_data.csv with your target clients and blog info.

## Check Output
 - Generated blog topics → MM-DD-YYYY_blogTopics.csv
 - Full HTML blog content → MM-DD-YYYY_blogs/<BusinessName>/<BlogTopic>.txt

## Dependencies
 - openai
 - json
 - csv
 - datetime
 - os
 - re

## Notes & Warnings
 - The script uses OpenAI's GPT-4o Mini model. This may incur usage costs depending on your OpenAI plan.
 - Ensure topics are sanitized and not reused for clients with overlapping scopes.
 - Output assumes blog content will be posted directly as HTML.

## Roadmap
 - Add Support for Fully Serverless Application
   - Use AWS Lambda Fronted by API Gateway To Trigger Blog Generated
   - Use DynamoDB To Store User Information, Blogs Topics, and Blog Details 
 - Integrate directly with WordPress REST API