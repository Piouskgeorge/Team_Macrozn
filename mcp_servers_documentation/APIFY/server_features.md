# Apify Conversational Interface

A conversational interface that connects Azure OpenAI with your Apify MCP server, allowing the AI model to access Apify tools based on user queries.

## Features

- 🤖 Conversational AI powered by Azure OpenAI GPT-4
- 🔧 Access to all Apify MCP tools
- 💬 Interactive chat interface
- 🛠️ Automatic tool calling based on user queries
- 📝 Conversation history management
- 📸 Enhanced Instagram scraping support with error handling

## Available Tools

The interface can access all the tools from your Apify MCP server:

### 🧠 Actors
- `run_actor` - Run an Apify actor asynchronously
- `run_actor_sync` - Run an Apify actor synchronously and return output
- `get_actor_run` - Get details of a specific actor run
- `get_last_actor_run` - Get the last run of a specific actor
- `abort_actor_run` - Abort a running actor

### 🎯 Tasks
- `run_task` - Run an Apify task asynchronously
- `run_task_sync` - Run an Apify task synchronously and return output
- `get_task` - Get details of a specific task
- `get_last_task_run` - Get the last run of a specific task

### 🗃️ Datasets
- `get_datasets` - Get list of datasets
- `get_dataset` - Get details of a specific dataset
- `get_dataset_items` - Get items from a dataset
- `get_dataset_stats` - Get statistics of a dataset

### 🔑 Key-Value Stores
- `get_key_value_stores` - Get list of key-value stores
- `get_key_value_store` - Get details of a specific store
- `get_key_value_record` - Get a record from a store
- `store_key_value_record` - Store a record in a store

### 📋 Utilities
- `list_available_actors` - List available actors
- `get_account_info` - Get Apify account information
- `get_run_log` - Get log of a specific run

## Instagram Scraping

The interface includes enhanced support for Instagram scraping with two main actors:

### 📸 Instagram Profile Scraper (`dSCLg0C3YEZ83HzYX`)
- Scrapes profile information from Instagram accounts
- Input: `{"usernames": ["username1", "username2"], "resultsLimit": 10}`
- Returns profile details, follower counts, bio, etc.

### 📱 Instagram Scraper (`shu8hvrXbJbY3Eb9W`)
- General Instagram scraping for posts, hashtags, and URLs
- Input: `{"hashtags": ["travel"], "resultsLimit": 5}` or `{"directUrls": ["https://instagram.com/username"]}`
- Returns posts, images, captions, engagement data

### 🛠️ Enhanced Error Handling
- Automatic detection of private profiles
- Rate limiting warnings
- Anti-bot measure alerts
- Helpful troubleshooting suggestions
- Alternative approach recommendations

### 📋 Recommended Public Profiles for Testing
- `instagram` (Official Instagram account)
- `natgeo` (National Geographic)
- `nike`, `adidas` (Brand accounts)
- `starbucks`, `apple`, `microsoft` (Corporate accounts)

## Web Scraping

The interface includes enhanced support for web scraping with two main actors:

### 🌐 Cheerio Scraper (`YrQuEkowkNCLdk4j2`)
- Fast scraping of static HTML websites
- Best for simple content extraction
- Lightweight and fast
- **Limitations:** No JavaScript execution, may fail with modern web apps

### 🌐 Web Scraper (`apify/web-scraper`)
- Full browser rendering with JavaScript execution
- Best for modern web applications and documentation sites
- Handles dynamic content and complex rendering
- **Advantages:** More reliable for complex sites, handles JavaScript-heavy pages

### 🛠️ Enhanced Error Handling
- Automatic detection of jQuery errors (`$ is not a function`)
- Recommendations for appropriate scraper selection
- Troubleshooting for modern web applications
- Alternative approaches when scraping fails

### 📋 Recommended Use Cases
- **Cheerio Scraper:** Static websites, simple content extraction
- **Web Scraper:** Documentation sites, modern web apps, JavaScript-heavy pages

### 🔧 Troubleshooting Web Scraping
- **jQuery errors:** Use Web Scraper instead of Cheerio Scraper
- **No content returned:** Site may require JavaScript rendering
- **Timeout errors:** Increase timeout or use simpler page functions
- **Modern web apps:** Always prefer Web Scraper for documentation sites

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   # Set your Apify API key
   export APIFY_API_KEY="your_apify_api_key_here"
   ```

3. **Run the conversational interface:**
   ```bash
   python start_conversation.py
   ```

## Usage

Once started, you can interact with the AI using natural language. The AI will automatically call the appropriate tools based on your queries.

### Example Conversations

**User:** "Show me my available actors"
- AI will call `list_available_actors`

**User:** "Run actor abc123 with input {'url': 'https://example.com'}"
- AI will call `run_actor` with the specified parameters

**User:** "Get my account information"
- AI will call `get_account_info`

**User:** "Show me my datasets"
- AI will call `get_datasets`

**User:** "Run task xyz789 synchronously"
- AI will call `run_task_sync`

### Instagram Scraping Examples

**User:** "Scrape the Instagram profile of 'nike'"
- AI will use Instagram Profile Scraper with appropriate input

**User:** "Get posts with hashtag 'travel', limit to 5"
- AI will use Instagram Scraper with hashtag input

**User:** "Scrape Instagram posts from 'natgeo' profile"
- AI will use Instagram Scraper with direct URL input

**User:** "Try scraping 'instagram' profile with the profile scraper"
- AI will use Instagram Profile Scraper for the official account

### Web Scraping Examples

**User:** "Scrape the first paragraph from https://example.com"
- AI will use Cheerio Scraper for static content

**User:** "Extract content from this documentation site with browser rendering"
- AI will use Web Scraper for JavaScript-heavy sites

**User:** "Get the title and first paragraph from this LangGraph page"
- AI will use Web Scraper with appropriate page function

**User:** "Summarize the content from this modern web application"
- AI will use Web Scraper with browser rendering

## Testing Instagram Scraping

Use the provided test scripts to verify Instagram scraping functionality:

```bash
# Run comprehensive Instagram scraping tests
python test_instagram_scraping.py

# Run the Instagram scraping guide
python instagram_scraping_guide.py

# Run the simple conversation interface
python simple_conversation.py
```

## Testing Web Scraping

Use the provided test scripts to verify web scraping functionality:

```bash
# Run comprehensive web scraping tests
python web_scraping_helper.py

# Test specific LangGraph documentation scraping
python test_langgraph_scraping.py

# Run the simple conversation interface
python simple_conversation.py
```

## Configuration

The Azure OpenAI configuration is set in the code:
- **Endpoint:** `https://opeanai-eastus.openai.azure.com/`
- **API Key:** `a00d081fe4b849beb5b5c0c4ed8d837f`
- **Model:** `gpt-4o` (Latest GPT-4 model)
- **API Version:** `2024-07-01-preview` (Latest API version)

To change these settings, modify the constants in `conversational_interface.py` or `simple_conversation.py`.

## Architecture

```
User Input → Azure OpenAI → Tool Selection → Apify MCP Server → Tool Execution → Response
```

1. User sends a message
2. Azure OpenAI analyzes the message and determines if tools are needed
3. If tools are needed, the AI calls the appropriate Apify MCP tools
4. MCP server executes the tools and returns results
5. AI processes the results and provides a conversational response

## Troubleshooting

- **Import errors:** Make sure all dependencies are installed with `pip install -r requirements.txt`
- **MCP server errors:** Check that `apify_mcp_server.py` is in the same directory
- **API errors:** Verify your Azure OpenAI credentials and Apify API key
- **Tool calling issues:** Ensure the MCP server is running and accessible

### Instagram Scraping Issues

- **No data returned:** Profile might be private, try public profiles like 'instagram', 'nike', 'natgeo'
- **Rate limiting:** Wait a few minutes between requests
- **Blocked requests:** Instagram actively blocks automated scraping, try different approaches
- **Invalid usernames:** Check spelling and ensure the profile exists

### Web Scraping Issues

- **jQuery errors (`$ is not a function`):** Use Web Scraper instead of Cheerio Scraper
- **No content returned:** Site may require JavaScript rendering, use Web Scraper
- **Timeout errors:** Increase timeout settings or use simpler page functions
- **Modern web apps:** Always prefer Web Scraper for documentation sites
- **Documentation sites:** Use Web Scraper with browser rendering for best results

## Files

- `conversational_interface.py` - Full conversational interface with subprocess
- `simple_conversation.py` - Simple interface that directly imports the MCP server
- `start_conversation.py` - Startup script with environment setup
- `apify_mcp_server.py` - Your Apify MCP server (existing)
- `test_instagram_scraping.py` - Instagram scraping test script
- `instagram_scraping_guide.py` - Instagram scraping guide and helper functions
- `web_scraping_helper.py` - Web scraping guide and helper functions
- `test_langgraph_scraping.py` - LangGraph documentation scraping test script
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Example Use Cases

1. **Web Scraping:** "Run a web scraper actor on this website"
2. **Documentation Analysis:** "Extract and summarize content from this documentation site"
3. **Instagram Analysis:** "Scrape Instagram posts with hashtag 'travel'"
4. **Profile Research:** "Get information about the 'nike' Instagram profile"
5. **Data Processing:** "Process this dataset with a specific actor"
6. **Automation:** "Create a task to run this actor daily"
7. **Monitoring:** "Check the status of my recent runs"
8. **Data Export:** "Export data from this dataset to CSV"
