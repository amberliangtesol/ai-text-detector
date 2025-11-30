# AI Text Detector 🔍

A modern web application that detects AI-generated content using the ModernBERT model from Hugging Face.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-text-detector.streamlit.app)

## 🌟 Features

- **AI Detection**: Uses state-of-the-art ModernBERT model to identify AI-generated text
- **Visual Analytics**: Interactive donut charts and segment analysis
- **Content Classification**: Categorizes text into 4 levels (Identical, Minor Changes, Paraphrased, Unique)
- **Real-time Analysis**: Instant feedback with confidence scores
- **Modern UI**: Clean, responsive design with animated elements
- **Sample Text**: Built-in example for quick testing

## 🚀 Live Demo

Visit the live app: [AI Text Detector](https://ai-text-detector.streamlit.app)

## 💻 Local Installation

```bash
# Clone the repository
git clone https://github.com/amberliangtesol/ai-text-detector.git
cd ai-text-detector

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📦 Requirements

- Python 3.8+
- streamlit==1.29.0
- transformers==4.36.0
- torch==2.1.0
- plotly==5.18.0
- numpy==1.24.3
- Pillow==10.1.0

## 📁 Project Structure

```
ai-text-detector/
├── app.py              # Main application
├── requirements.txt    # Package dependencies
├── assets/            # Resource folder
│   ├── logo.png       # Logo image
│   └── bg.png        # Background image
├── styles/            # Style folder
│   └── custom.css     # Custom CSS styles
├── .streamlit/        # Streamlit configuration
│   └── config.toml    # Theme and server settings
└── README.md          # Project documentation
```

## 🎯 How It Works

1. **Input Text**: Paste or type the text you want to analyze
2. **Click Detect**: The AI model analyzes your text
3. **View Results**: 
   - Overall AI percentage in a donut chart
   - Segment-by-segment analysis
   - Content classification breakdown
   - Detection verdict (AI Generated or Human Written)

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: AICodexLab/answerdotai-ModernBERT-base-ai-detector
- **Visualization**: Plotly
- **Styling**: Custom CSS with modern design

## 👤 Author

**amberliangtesol**

- GitHub: [@amberliangtesol](https://github.com/amberliangtesol)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!