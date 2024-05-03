# Pitch Tonic
Real-time pitch helper for difficult investor calls.

## Overview
Pitch Tonic is an innovative tool designed to assist individuals in refining and testing their pitch skills in real-time. Developed for challenging investor calls, Pitch Tonic facilitates users to improve the way they handle potential investors effectively. Whether you’re practicing or in an actual investor call, Pitch Tonic provides you with the critical feedback you need to succeed.

This tool is proudly developed by the open-source community at Tonic-AI. It leverages audio input via microphone, allowing users to either use live investor input or prerecorded audio for training purposes.

## Features
- **Real-Time Feedback:** Get immediate insights on your pitching skills.
- **Dual Audio Input:** Use investor’s input or your own recordings to train and enhance your capabilities.
- **Community Driven:** A product built with the contributions from the open-source community.

## Getting Started

### Prerequisites
To use Pitch Tonic, make sure you have Python installed on your system. You can download Python [here](https://www.python.org/downloads/).

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://git.tonic-ai.com/contribute/Pitch-Tonic/Pitch_Tonic
   cd Pitch_Tonic
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Launch Pitch Tonic**
   ```bash
   python main.py

## Configure Pitch Tonic

To configure Pitch Tonic, follow the detailed setup instructions for the Azure OpenAI service and VoyageAI, and then set up MongoDB credentials. These services are essential for running Pitch Tonic effectively.

### Azure OpenAI Configuration

1. **Go to Azure OpenAI Studio**
   - Access the [Azure OpenAI Studio](https://studio.openai.azure.com).
  
2. **Access the Playground**
   - Depending on which Large Language Model (LLM) you intend to use, go to either the 'Chat' or 'Completions' playground.
  
3. **View API Details**
   - Click on "view code" to reveal the API setup information. Here's what you need to look for:
     ![click view code in the Open AI Studio Dashboard](your-image-url-here)

4. **Record API Details**
   - Note down the following details which are crucial for integrating with Azure:
     - `api_type`
     - `api_base`
     - `api_version`
     - `engine` (should match the "deployment name" previously noted)
     - `key`

### VoyageAI API Key

1. **Sign-In to VoyageAI**
   - Visit [VoyageAI Dashboard](https://dash.voyageai.com/) and sign in.

2. **Access API Keys**
   - Locate the 'API Keys' option in the top left-hand corner of the dashboard.
     ![API Keys Snapshot](https://path-to-image/imagesnapshot.jpg)

3. **Save the API Key**
   - Note down the API key as it will be required for setting up VoyageAI integrations in your application.

### MongoDB Configuration

1. **Environment File Setup**
   - Navigate to the `.env.example` file in your repository.
   
2. **Add MongoDB Credentials**
   - Replace the placeholder values with your actual MongoDB credentials:
     - `MONGO_USERNAME`: Your MongoDB username.
     - `MONGO_PASSWORD`: Your MongoDB password.
     - `MONGO_URI`: Your MongoDB connection URI.
   
3. **Rename `.env.example` to `.env`**
   - Once you fill in your details, rename the file to `.env` to activate the environment variables.

By following these steps, you will have successfully configured all necessary services for running Pitch Tonic. This includes setting up Azure OpenAI, obtaining a VoyageAPI key, and configuring MongoDB. These configurations are crucial for the optimal operation of the app.

### Join the Community

Connect with us and other community members on [Discord](#). Engage, get help and contribute!

### Contribute

Pitch Tonic is an open-source project hosted on GitLab. To contribute, follow these steps:

1. **Sign Up & Join the Repository**
   - Visit [Pitch Tonic Repository](https://git.tonic-ai.com/contribute/Pitch-Tonic/Pitch_Tonic) to sign up and join.
2. **Open an Issue**
   - Found a bug or have a feature suggestion? Open an issue to get started.
3. **Branching**
   - Create a named branch to work on your issue or feature.
4. **Add Testing & Documentation**
   - Help us make Pitch Tonic more robust by adding tests and enriching documentation.
5. **Example Usage Applications**
   - Enhance understanding by providing examples of how Pitch Tonic can be used effectively.

### Join Team Tonic

Tonic-AI is always building and growing. Join us to make a difference in the open-source community!

## Support

For support, you can reach out through our Discord channel or open an issue in the GitLab repository. We are here to help!

## License

Pitch Tonic is MIT licensed.
