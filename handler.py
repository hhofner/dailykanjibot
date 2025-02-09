import datetime
import logging
import random
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from cairosvg import svg2png

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

def run(event, context):
    current_time = datetime.datetime.now().time()
    logger.info("Your cron function ran at " + str(current_time))
    
    path = './kanji'
    files_and_directories = os.listdir(path)
    
    # select random kanji
    random_kanji = None
    while True:
        random_file = random.choice(files_and_directories)
        if (os.path.isfile(os.path.join(path, random_file))):
            random_kanji = random_file
            break
    
    code_point = int(random_kanji.strip(".svg"), 16)
    unicode_char = chr(code_point)
    
    print(f"finalized kanji: {unicode_char}")
    
    # base_url = "https://api.deepseek.com"
    # api_key = os.getenv('DEEPSEEK_API_KEY')
    api_key = os.getenv('OPENAI_API_KEY')
    
    # client = OpenAI(api_key=api_key, base_url=base_url)
    client = OpenAI(api_key=api_key)
    
    role_msg = """
    You are a master assistant of Japanese Kanji characters.
    You talk and respond with concise and simple, yet engaging
    answers about Japanese characters. You only reply with
    normal text and no markdown.
    """
    
    user_msg = f"""
    Please list three words that use the character {unicode_char}, seperated by
    commas, in simplified manner without any other text about
    the words used, like this: Example Words: 新聞、新しい、新札
    Please give me an interesting fact about the kanji character
    {unicode_char}, and don't write "interesting fact", just write the
    fact, and briefly mention modern day usage of the character.
    """
    max_completion_tokens = 500
    response = None
    retry_attempts = 0
    while True:
        print("creating response")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": role_msg},
                {"role": "user", "content": user_msg},
            ],
            stream=False,
            max_completion_tokens=350
        )
        print(response.choices[0].message.content)
        if retry_attempts > 5:
            print("Too many attempts.")
            break
        if len(response.choices[0].message.content) < 500:
            break
        else:
            retry_attempts += 1
            max_completion_tokens -= 50 
    
    print(f"Retry attemps: {retry_attempts}")
    
    content = f"Today's Kanji: {unicode_char}\n\n" + response.choices[0].message.content + f"\n\nhttps://jisho.org/search/{unicode_char}%23kanji"
    print(content)
    
    status_url = os.getenv("MASTODON_URL") + "/api/v1/statuses"
    media_url = os.getenv("MASTODON_URL") + "/api/v2/media"
    access_token = os.getenv("MASTODON_SECRET")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    # create media
    svg2png(url=os.path.join(path, random_kanji), write_to="./output.png", scale=20)
    
    files = {
        'file': open('./output.png', 'rb'),
        'description': f"Image of the Japanese character {unicode_char}, with numbers next to each stroke denoting stroke order." 
    }
    
    # upload media
    media_response = requests.post(media_url, headers=headers, files=files)
    
    media_id = None
    if media_response.status_code == 200:
        res = media_response.json()
        media_id = res["id"]
        print(f"Media uploaded successfully with ID: {media_id}")
    else:
        print(f"Failed to upload media: {media_response.status_code} - {media_response.text}")
    
    print(f"test media id: {media_id}")
    data = {
        'status': content,
        'media_ids': [media_id]
    }
    response = requests.post(status_url, headers=headers, json=data)
    
    # Check the response
    if response.status_code == 200:
        print("Status posted successfully!")
    else:
        print(f"Failed to post status: {response.status_code} - {response.text}")
    
    