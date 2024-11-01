# daily-ai-podcast
generate a daily podcast of the top AI papers using NotebookLM

# Implementation Plan

**Updated Product Specification for Daily AI Papers Podcast Automation**

---

### **1. Introduction**

The goal is to automate the creation of a daily podcast summarizing top AI papers, focusing on simplicity and efficiency. The system will:

- Use Zapier to monitor your Gmail for the arrival of the AInews email and trigger a webhook.
- Use Google's NotebookLM to generate audio summaries (mp3 files) of the papers.
- Stitch the audio summaries together, creating smooth transitions and accurate timestamps.
- Publish the final podcast to Spotify, using an RSS feed if necessary, in the simplest way possible.
- Deploy the entire system on an easy-to-use platform like Replit or Railway.

---

### **2. High-Level Architecture**

1. **Email Monitoring Module**: Uses Zapier to detect the arrival of the AInews email in Gmail and sends a webhook to trigger the pipeline.
2. **Content Generation Module**: Generates audio summaries using NotebookLM.
3. **Audio Processing Module**: Combines audio files and adds transitions.
4. **Publishing Module**: Publishes the podcast to Spotify via an RSS feed using a simple podcast hosting service.
5. **Deployment**: The entire system runs on Replit or Railway for simplicity.

---

### **3. Functional Requirements**

#### **3.1 Email Monitoring Module**

- **Functionality**:
  - Use Zapier to monitor your Gmail inbox for the AInews email.
  - When the email arrives, Zapier sends a webhook to your application to trigger the pipeline.
  - The application accesses the email content via Gmail API to parse and extract paper titles and URLs.

- **Files**:
  - `email_monitor.py`: Handles the webhook received from Zapier and retrieves the email content.

- **Design Decisions**:
  - Using Zapier simplifies email monitoring without writing complex polling code.
  - Zapier's Gmail integration can detect new emails based on specific criteria (e.g., sender, subject).
  - Webhooks provide a quick and efficient way to trigger your application as soon as the email arrives.

#### **3.2 Content Generation Module**

- **Functionality**:
  - Automate interactions with NotebookLM to generate audio summaries (mp3 files) for each paper.
  - Download the generated mp3 files.

- **Files**:
  - `content_generator.py`: Orchestrates the content generation process, including automating NotebookLM interactions.

- **Design Decisions**:
  - Use Playwright or Selenium for browser automation.
  - Ensure the automation script can log in, process paper URLs, and download mp3 files efficiently.

#### **3.3 Audio Processing Module**

- **Functionality**:
  - Combine the mp3 files into a single audio file.
  - Add simple transitions between summaries.
  - Generate timestamps for each segment.

- **Files**:
  - `audio_processor.py`: Handles merging audio files and adding transitions.

- **Design Decisions**:
  - Use a simple audio processing library like Pydub.
  - Keep transitions minimal—use brief silence or a simple sound effect.

#### **3.4 Publishing Module**

- **Functionality**:
  - Publish the final podcast to Spotify.
  - Use a podcast hosting service that automatically generates an RSS feed compatible with Spotify.
  - Manage episode details like title, description, and timestamps.

- **Files**:
  - `publisher.py`: Handles uploading the podcast to the hosting service.

- **Design Decisions**:
  - Use a simple podcast hosting platform like Anchor.fm (now Spotify for Podcasters) or Buzzsprout.
  - These platforms simplify the publishing process and handle RSS feed generation automatically.
  - They also integrate directly with Spotify, making publishing straightforward.

---

### **4. Simplified Workflow**

1. **Email Monitoring and Triggering**:
   - **Zapier Setup**:
     - Create a Zap that connects Gmail to a webhook.
     - Trigger: New email in Gmail matching specific criteria.
     - Action: Send a POST request to your application's webhook URL.

2. **Email Retrieval and Parsing**:
   - `email_monitor.py` receives the webhook and extracts necessary data.
   - Access the email content via Gmail API using the message ID provided by Zapier.
   - Parse the email to extract paper titles and URLs.

3. **Content Generation**:
   - `content_generator.py` uses automation to interact with NotebookLM.
   - Generates and downloads mp3 summaries for each paper.

4. **Audio Processing**:
   - `audio_processor.py` combines the mp3 files.
   - Adds simple transitions (e.g., brief silence).
   - Generates timestamps.

5. **Publishing**:
   - `publisher.py` uploads the final audio file to the podcast hosting platform.
   - The hosting platform generates an RSS feed and distributes the podcast to Spotify.

---

### **5. Steps to Set Up Zapier Hook**

- **Create a Zapier Account**: Sign up for a free Zapier account if you don't have one.

- **Create a New Zap**:
  1. **Trigger**:
     - App: Gmail
     - Event: New Email Matching Search
     - Connect your Gmail account.
     - Set up search criteria (e.g., from: "ainews@example.com", subject contains: "AI News").
  2. **Action**:
     - App: Webhooks by Zapier
     - Event: POST
     - Set up the webhook:
       - URL: The endpoint of your application (e.g., `https://yourapp.repl.co/webhook`)
       - Payload Type: JSON
       - Include data from the email (e.g., message ID, subject, sender).
  3. **Test the Zap**: Ensure it triggers correctly and sends the webhook.

- **Configure Your Application to Receive the Webhook**:
  - In `email_monitor.py`, set up a simple web server using Flask or FastAPI to receive the POST request.
  - Extract the message ID from the webhook payload.

- **Access the Email Content**:
  - Use Gmail API to retrieve the email content using the message ID.
  - Parse the email to extract paper titles and URLs.

---

### **6. Publishing to Spotify via RSS Feed**

#### **Simplest Way to Publish**

- **Use Spotify for Podcasters (formerly Anchor.fm)**:
  - **Benefits**:
    - Free and user-friendly.
    - Direct integration with Spotify.
    - Automatically generates an RSS feed for your podcast.
  - **Steps**:
    1. **Create an Account**: Sign up at [Spotify for Podcasters](https://podcasters.spotify.com/).
    2. **Create a Podcast**: Follow the prompts to set up your podcast.
    3. **Upload Episodes**:
       - In `publisher.py`, automate the upload using Spotify for Podcasters API (if available) or manually upload the episode.
       - Alternatively, use email-based publishing if supported.
    4. **Manage Podcast Details**: Set the title, description, and episode notes.

- **Alternative: Use a Simple Podcast Hosting Service**

  - **Buzzsprout**:
    - Offers a free plan with limited storage.
    - Simple interface and automatic RSS feed generation.
    - Distributes your podcast to Spotify and other platforms.
    - API access may be limited; manual upload might be necessary.

- **Automating the Publishing Process**

  - **Option 1: Use APIs**:
    - Some podcast hosting services offer APIs to automate episode uploads.
    - Check if the chosen platform provides an API or supports FTP uploads.

  - **Option 2: Use Email-based Publishing**:
    - Some platforms allow you to publish episodes via email.
    - Send an email with the audio file attached to a specific address.

  - **Option 3: Manual Upload**:
    - If automation is not possible, consider manually uploading the episodes initially.
    - Simplifies the development process, focusing on automation later.

---

### **7. Simplified File Structure**

Consolidate files to minimize complexity:

- `main.py`: Orchestrates the entire process, including receiving the webhook.
- `email_monitor.py`: Handles the webhook received from Zapier and retrieves the email content via Gmail API.
- `content_generator.py`: Automates NotebookLM interactions.
- `audio_processor.py`: Merges audio files and adds transitions.
- `publisher.py`: Publishes the podcast to Spotify via the chosen hosting service.
- `requirements.txt`: Lists all dependencies.

---

### **8. Deployment on Replit or Railway**

- **Replit**:
  - **Setup**:
    - Create a new Replit project.
    - Install dependencies listed in `requirements.txt`.
    - Expose your application via a web server to receive webhooks.
    - Use the always-on feature to keep your application running.
  - **Considerations**:
    - Replit projects may sleep after periods of inactivity unless you have a paid plan.
    - For webhooks, ensure your Replit URL is accessible (e.g., `https://yourapp.repl.co`).

- **Railway**:
  - **Setup**:
    - Create a new Railway project.
    - Deploy your code from a GitHub repository.
    - Configure environment variables for secrets.
    - Use Railway's web service to expose your application for webhooks.
  - **Considerations**:
    - Railway offers free tiers with certain limitations.
    - Suitable for small applications and easy to set up.

---

### **9. Updated Workflow Diagram**

1. **Start**

2. **Email Monitoring and Triggering**:
   - Zapier monitors Gmail and sends a webhook when the AInews email arrives.
   - `main.py` receives the webhook and starts the pipeline.

3. **Email Retrieval and Parsing**:
   - `email_monitor.py` retrieves the email content using Gmail API.
   - Parses the email to extract paper titles and URLs.

4. **Content Generation**:
   - `content_generator.py` automates NotebookLM to generate and download mp3 summaries.

5. **Audio Processing**:
   - `audio_processor.py` merges the mp3 files.
   - Adds simple transitions.
   - Generates timestamps.

6. **Publishing**:
   - `publisher.py` uploads the final podcast episode to the hosting platform.
   - The platform generates an RSS feed and distributes the podcast to Spotify.

7. **End**

---

### **10. Conclusion**

By integrating Zapier for email monitoring and selecting a podcast hosting service that simplifies RSS feed generation and Spotify distribution, the system becomes more straightforward and efficient. Deploying on platforms like Replit or Railway minimizes setup complexity and allows for quick iteration.

---

### **11. Next Steps**

- **Set Up Zapier Integration**:
  - Configure Zapier to monitor your Gmail and send webhooks to your application.

- **Develop and Test Modules**:
  - Code and test each module individually.
  - Ensure that automation scripts for NotebookLM work reliably.

- **Set Up Podcast Hosting**:
  - Create an account with Spotify for Podcasters or another simple hosting service.
  - Familiarize yourself with their upload process and API capabilities.

- **Deploy the Application**:
  - Upload your code to Replit or Railway.
  - Configure environment variables and secrets securely.
  - Test the entire pipeline end-to-end with sample data.

---

### **12. Additional Considerations**

- **Gmail API Access**:
  - Ensure you have the necessary permissions to access email content via the Gmail API.
  - May require OAuth 2.0 authentication.

- **NotebookLM Automation Compliance**:
  - Verify that automating interactions with NotebookLM complies with their terms of service.
  - Consider reaching out to their support team if necessary.

- **Error Handling**:
  - Implement basic error handling to manage failures gracefully.
  - Log errors and consider setting up notifications for critical issues.

---

### **13. Simplified Code Snippet for Receiving Webhooks**

```python
# main.py

from flask import Flask, request
from email_monitor import process_email
from content_generator import generate_audio_summaries
from audio_processor import merge_audio_files
from publisher import publish_podcast

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Process the webhook data and extract the email message ID
    message_id = data.get('message_id')
    if not message_id:
        return 'No message ID found', 400

    # Step 1: Retrieve and parse email
    paper_links = process_email(message_id)

    if not paper_links:
        print("No papers found. Exiting.")
        return 'No papers found', 200

    # Step 2: Generate audio summaries
    audio_files = generate_audio_summaries(paper_links)

    if not audio_files:
        print("No audio files generated. Exiting.")
        return 'No audio files generated', 200

    # Step 3: Merge audio files
    final_podcast = merge_audio_files(audio_files)

    # Step 4: Publish the podcast
    publish_podcast(final_podcast)

    return 'Success', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
```

---

### **14. Resources**

- **Zapier Gmail Integration**: [Zapier Gmail Integration Guide](https://zapier.com/apps/gmail/integrations)
- **Spotify for Podcasters**: [Getting Started Guide](https://podcasters.spotify.com/)
- **Gmail API Documentation**: [Gmail API Overview](https://developers.google.com/gmail/api)
- **Replit Deployment**: [Replit Flask Tutorial](https://docs.replit.com/tutorials/python/flask)
- **Railway Deployment**: [Deploying a Python App on Railway](https://docs.railway.app/deploy/quickstart)

---

### **15. Final Thoughts**

By leveraging Zapier for quick email detection and using a user-friendly podcast hosting service that handles RSS feeds and Spotify distribution, you can significantly simplify your workflow. This approach allows you to focus on the core functionality of generating and processing content without getting bogged down in the complexities of email polling or RSS feed management.

Remember to test each component thoroughly and ensure that all services used comply with their respective terms of service.

---

Feel free to reach out if you have any questions or need further assistance with any part of this setup!