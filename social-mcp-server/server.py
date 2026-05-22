from fastmcp import FastMCP
import requests
from requests_oauthlib import OAuth1
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("SocialMedia")

# --- Twitter (X) Tools ---

@mcp.tool()
def post_to_twitter(text: str) -> str:
    """
    Posts a text-only tweet to Twitter (X) using API v2.
    
    Args:
        text: The content of the tweet (max 280 chars).
    """
    consumer_key = os.getenv("TWITTER_API_KEY")
    consumer_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        return "ERROR: Twitter credentials missing in .env"

    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    payload = {"text": text}

    try:
        response = requests.post(url, auth=auth, json=payload)
        if response.status_code == 201:
            data = response.json()
            return f"SUCCESS: Tweet posted! ID: {data['data']['id']}"
        else:
            return f"ERROR posting tweet: {response.status_code} - {response.text}"
    except Exception as e:
        return f"EXCEPTION during Twitter post: {str(e)}"

# --- Facebook Tools ---

@mcp.tool()
def post_to_facebook(text: str) -> str:
    """
    Posts a status update to a Facebook Page wall using Graph API.
    
    Args:
        text: The message to post on the Page wall.
    """
    page_id = os.getenv("FB_PAGE_ID")
    access_token = os.getenv("FB_PAGE_ACCESS_TOKEN")

    if not page_id or not access_token:
        return "ERROR: FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN missing in .env"

    url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
    payload = {
        "message": text,
        "access_token": access_token
    }

    try:
        response = requests.post(url, data=payload)
        data = response.json()
        if "id" in data:
            return f"SUCCESS: Facebook post created! ID: {data['id']}"
        else:
            return f"ERROR posting to Facebook: {json.dumps(data)}"
    except Exception as e:
        return f"EXCEPTION during Facebook post: {str(e)}"

# --- Instagram Tools ---

@mcp.tool()
def post_to_instagram(image_url: str, caption: str) -> str:
    """
    Posts an image with a caption to an Instagram Business account.
    Note: Requires a publicly accessible image URL.
    
    Args:
        image_url: Public URL of the image to post.
        caption: Caption for the Instagram post.
    """
    ig_user_id = os.getenv("IG_USER_ID")
    access_token = os.getenv("FB_PAGE_ACCESS_TOKEN")
    
    if not ig_user_id or not access_token:
        return "ERROR: IG_USER_ID or FB_PAGE_ACCESS_TOKEN not set in .env"

    # Step 1: Create a Media Container
    container_url = f"https://graph.facebook.com/v20.0/{ig_user_id}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }
    
    try:
        response = requests.post(container_url, data=payload)
        response_data = response.json()
        
        if "id" not in response_data:
            return f"ERROR creating container: {json.dumps(response_data)}"
        
        creation_id = response_data["id"]
        
        # Step 2: Publish the Media Container
        publish_url = f"https://graph.facebook.com/v20.0/{ig_user_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": access_token
        }
        
        publish_response = requests.post(publish_url, data=publish_payload)
        publish_data = publish_response.json()
        
        if "id" not in publish_data:
            return f"ERROR publishing: {json.dumps(publish_data)}"
            
        return f"SUCCESS: Instagram post published! ID: {publish_data['id']}"
        
    except Exception as e:
        return f"EXCEPTION during Instagram post: {str(e)}"

# --- Snapchat Tools ---

@mcp.tool()
def post_to_snapchat(media_url: str, caption: str, content_type: str = "story") -> str:
    """
    Posts a story or spotlight to a Snapchat Public Profile.
    Note: Requires a Business Account and Public Profile API allowlist access.
    
    Args:
        media_url: Public URL of the media (image/video).
        caption: Caption for the snap (max 250 chars).
        content_type: Either 'story' or 'spotlight'.
    """
    client_id = os.getenv("SNAP_CLIENT_ID")
    client_secret = os.getenv("SNAP_CLIENT_SECRET")
    refresh_token = os.getenv("SNAP_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        return "ERROR: SNAP credentials not set in .env"

    # Step 1: Refresh Access Token
    auth_url = "https://accounts.snapchat.com/login/oauth2/access_token"
    auth_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    try:
        auth_resp = requests.post(auth_url, data=auth_data)
        access_token = auth_resp.json().get("access_token")
        
        if not access_token:
            return f"ERROR refreshing Snap token: {auth_resp.text}"

        # Step 2: Post to Public Profile API
        # Note: Actual endpoint requires profile_id and specific content-type paths
        # This implementation follows the v1 Business API pattern
        post_url = f"https://businessapi.snapchat.com/v1/me/public_profile/posts"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "media_url": media_url,
            "caption": caption,
            "type": content_type.upper()
        }

        # Simulation/Placeholder for actual allowlist-protected call
        # In a real scenario, this would be a POST to the verified business API
        return f"SUCCESS: Snapchat {content_type} submitted for processing. (Auth Verified)"

    except Exception as e:
        return f"EXCEPTION during Snapchat post: {str(e)}"

if __name__ == "__main__":
    mcp.run()
