import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from PIL import Image
import os
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import re
import time

# 頁面配置
st.set_page_config(
    page_title="AI Text Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 載入自訂 CSS
def load_css():
    # Add background image using base64 encoding
    bg_path = "assets/bg.png"
    if os.path.exists(bg_path):
        import base64
        with open(bg_path, "rb") as img_file:
            bg_base64 = base64.b64encode(img_file.read()).decode()
            bg_css = f'''
            <style>
            .stApp {{
                background-image: url('data:image/png;base64,{bg_base64}') !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            }}
            
            /* Also apply to main container */
            .main, [data-testid="stAppViewContainer"] {{
                background: transparent !important;
            }}
            
            /* Apply to sidebar if exists */
            section[data-testid="stSidebar"] {{
                background: transparent !important;
            }}
            </style>
            '''
            st.markdown(bg_css, unsafe_allow_html=True)
    
    # Load custom CSS
    css_file = "styles/custom.css"
    if os.path.exists(css_file):
        with open(css_file) as f:
            css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

load_css()

# 載入模型
@st.cache_resource
def load_model():
    MODEL_NAME = "AICodexLab/answerdotai-ModernBERT-base-ai-detector"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    clf = pipeline("text-classification", model=model, tokenizer=tokenizer)
    return clf, tokenizer

clf, tokenizer = load_model()

# 分析文字片段
def analyze_text_segments(text, clf, tokenizer, segment_size=50):
    """將文字分段並分析每段的 AI 機率"""
    words = text.split()
    segments = []
    scores = []
    
    for i in range(0, len(words), segment_size//2):  # 重疊分段
        segment = ' '.join(words[i:i+segment_size])
        if len(segment.split()) < 10:  # 太短的片段跳過
            continue
        
        result = clf(segment, truncation=True)[0]
        is_ai = result["label"].endswith("1")
        score = result["score"] if is_ai else 1 - result["score"]
        
        segments.append(segment)
        scores.append(score)
    
    return segments, scores

# 創建圓環圖
def create_donut_chart(ai_percentage):
    """創建類似參考圖的圓環圖"""
    # 只顯示 AI 部分為紅色漸層，其餘為淺灰
    labels = ['AI Generated', 'Human Written']
    values = [ai_percentage, 100 - ai_percentage]
    
    # 使用漸層紅色和淺灰色
    if ai_percentage > 0:
        colors = ['#fd373b', '#f0f0f0']
    else:
        colors = ['#f0f0f0', '#4ade80']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.75,
        marker=dict(
            colors=colors,
            line=dict(color='#ffffff', width=3)
        ),
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'
    )])
    
    fig.update_layout(
        annotations=[dict(
            text=f'{ai_percentage:.0f}%',
            x=0.5, y=0.5,
            font_size=36,
            font=dict(color='#fd373b', family="Arial", weight=700),
            showarrow=False
        ), dict(
            text='AI Content',
            x=0.5, y=0.42,
            font_size=14,
            font=dict(color='#999'),
            showarrow=False
        )],
        showlegend=False,
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',
        margin=dict(t=10, b=10, l=10, r=10),
        height=200
    )
    
    return fig

# 創建分析細節圖表
def create_analysis_chart(segments, scores):
    """創建文字片段分析圖表"""
    fig = go.Figure()
    
    # 加入柱狀圖
    colors = ['#fd373b' if s > 0.5 else '#4ade80' for s in scores]
    fig.add_trace(go.Bar(
        y=[f"Segment {i+1}" for i in range(len(scores))],
        x=[s * 100 for s in scores],
        orientation='h',
        marker=dict(color=colors),
        text=[f'{s*100:.1f}%' for s in scores],
        textposition='outside',
        hovertemplate='<b>Segment %{y}</b><br>AI Score: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title="AI Probability (%)",
        yaxis_title="Text Segments",
        paper_bgcolor='#ffffff',
        plot_bgcolor='#f8f8f8',
        font=dict(color='#333'),
        xaxis=dict(gridcolor='#e0e0e0', range=[0, 105]),
        yaxis=dict(gridcolor='#e0e0e0'),
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    
    return fig

# 標註文字
def highlight_text(text, segments, scores):
    """根據分析結果標註文字"""
    if not segments or not scores:
        return text
    
    # 簡單的標註邏輯：將高 AI 分數的片段標紅
    highlighted = text
    for segment, score in zip(segments, scores):
        if score > 0.7 and len(segment) > 20:
            # 使用 HTML 標籤標註
            highlighted = highlighted.replace(
                segment,
                f'<span class="ai-highlight">{segment}</span>'
            )
    
    return highlighted

# 主介面
def main():
    # Add animated tech circles background
    st.markdown('''
    <div class="tech-circles">
        <div class="tech-circle"></div>
        <div class="tech-circle"></div>
        <div class="tech-circle"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Logo Section - larger size
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        col1, col2, col3 = st.columns([2, 3, 2])
        with col2:
            logo = Image.open(logo_path)
            st.image(logo, width='stretch')
    
    # Subtitle only
    st.markdown('<p class="subtitle">Maintain the authenticity of your writing by identifying AI-generated content</p>', unsafe_allow_html=True)
    
    # 輸入區域標題與範例按鈕並排
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h3 style="color: #fd373b;">📝 Enter Text to Analyze</h3>', unsafe_allow_html=True)
    with col2:
        # 範例文章
        sample_text = """Global Warming: A Warning Signal for Our Future

In recent years, "global warming" has become more than a term in textbooks—it is something we experience every day. From record-breaking heatwaves and frequent heavy rainfall to longer summers, the impact of climate change is now visible across the world. The World Meteorological Organization (WMO) has warned that within the next five years, the world is highly likely to cross the 1.5°C warming threshold, meaning extreme weather events will become even more intense and unpredictable.

The main cause of global warming is the large amount of greenhouse gases—such as carbon dioxide and methane—released from burning fossil fuels. These gases act like a "heat-trapping blanket" around the Earth, preventing heat from escaping into space and causing temperatures to rise year after year. Although global warming may seem like "just hotter weather," the consequences are far more complex.

For Taiwan, the effects are especially evident. Longer summers bring more days of extreme heat, which is dangerous for vulnerable groups such as the elderly and children. Warmer ocean temperatures strengthen typhoons, making them more destructive. Heavy rain and sudden downpours occur more frequently, increasing flooding risks in coastal and low-lying areas. Even agriculture and fisheries face challenges as crop seasons shift and marine environments change.

However, global warming is not an irreversible path. We still have the opportunity to slow down its progression and buy more time for the planet. Some key actions include:

Reducing reliance on fossil fuels by promoting renewable energy and improving energy efficiency.

Green transportation such as public transit, electric vehicles, walking, and cycling.

Changing electricity-use habits, like turning off unused devices and choosing energy-saving appliances.

Government and corporate action, including carbon pricing, climate policies, and building climate-resilient cities.

Most importantly, raising climate awareness among the public is crucial. Global warming is not one person's responsibility, but every individual's choices can drive meaningful change.

Earth is our only home. Faced with an accelerating warming trend, now is the best time to act. Even small changes in daily life can help cool our planet and secure a more hopeful future for the next generation."""
        
        # 載入範例文字連結樣式
        st.markdown('''
        <style>
        .sample-text-link {
            color: #fd373b;
            text-decoration: none;
            font-size: 0.95rem;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.5rem;
            transition: opacity 0.2s;
        }
        .sample-text-link:hover {
            opacity: 0.8;
            text-decoration: underline;
        }
        </style>
        ''', unsafe_allow_html=True)
        
        if st.button("⬇ Load Sample Text", key="sample_btn", help="Click to load a sample text for testing", type="tertiary"):
            st.session_state.text_area_input = sample_text
            st.rerun()
    
    # 文字輸入區
    text = st.text_area(
        "Text Input",
        height=300,
        placeholder="Paste your text here or upload a file to check for AI content...",
        label_visibility="collapsed",
        key="text_area_input"
    )
    
    # Red gradient decoration below input
    st.markdown('<div class="input-decoration"></div>', unsafe_allow_html=True)
    
    # 分析按鈕 with animated sparkle
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        analyze_button = st.button(
            "✦ DETECT AI",
            type="primary",
            use_container_width=True,
            key="detect_btn"
        )
    
    if analyze_button and text:
        loading_placeholder = st.empty()
        try:
            # 立即添加自動滾動錨點和JavaScript
            st.markdown('<div id="loading-section"></div>', unsafe_allow_html=True)
            st.markdown('''
            <script>
                // 立即滾動到加載區域
                setTimeout(function() {
                    var element = document.getElementById("loading-section");
                    if (element) {
                        element.scrollIntoView({ behavior: "smooth", block: "start" });
                    }
                }, 100);
            </script>
            ''', unsafe_allow_html=True)
            
            # 顯示自定義加載動畫
            with loading_placeholder.container():
                st.markdown('''
                <div class="loading-container">
                    <div class="loading-wheel"></div>
                    <div class="loading-text">
                        🤖 Analyzing your text<span class="loading-dots"></span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # 加入短暫延遲讓動畫效果更明顯
            time.sleep(0.5)
            
            # 執行分析
            # 整體分析
            result = clf(text, truncation=True, max_length=512)[0]
            is_ai = result["label"].endswith("1")
            overall_score = result["score"] if is_ai else 1 - result["score"]
            ai_percentage = overall_score * 100
            
            # 分段分析
            segments, segment_scores = analyze_text_segments(text, clf, tokenizer)
            
            # 清除加載動畫
            loading_placeholder.empty()
            
            # 結果展示 - 添加報告標題 (與 Enter Text to Analyze 相同樣式)
            st.markdown('<div id="results"></div>', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center;">📋 AI Detector Report</h3>', unsafe_allow_html=True)
            
            # 自動滾動到結果區域
            st.markdown('''
        <script>
            // 滾動到結果區域
            setTimeout(function() {
                var element = document.getElementById("results");
                if (element) {
                    element.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }, 200);
        </script>
            ''', unsafe_allow_html=True)
            
            # 使用container來包含所有內容
            with st.container():
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                
                # 簡化布局 - 只顯示圓環圖和信心分數
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.markdown(f'''
                    <div class="metric-container">
                        <div class="metric-label">Confidence Score</div>
                        <div class="metric-value">{overall_score:.2%}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    # 圓環圖
                    fig = create_donut_chart(ai_percentage)
                    st.plotly_chart(fig, use_container_width=True, key="donut_chart")
                
                with col3:
                    # 空白或其他內容
                    st.markdown('<div style="height: 100%;"></div>', unsafe_allow_html=True)
            
            # 詳細分析區
            st.markdown("---")
            
            # 注入CSS來樣式化columns
            st.markdown('''
            <style>
            /* Target the columns that contain analysis sections */
            .row-widget.stHorizontalBlock > [data-testid="column"]:nth-child(1) > div:first-child {
                background: #f5f5f5 !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 20px !important;
                padding: 1.8rem !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
            }
            
            .row-widget.stHorizontalBlock > [data-testid="column"]:nth-child(2) > div:first-child {
                background: #f5f5f5 !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 20px !important;
                padding: 1.8rem !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
            }
            
            /* Style section headers */
            .analysis-header, .section-header {
                color: #1a1a1a;
                padding-bottom: 1rem;
                border-bottom: 2px solid rgba(253, 55, 59, 0.1);
                margin-bottom: 1.5rem;
                font-size: 1.5rem;
                font-weight: bold;
            }
            
            .section-header {
                margin-top: 2rem;
            }
            </style>
            ''', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1], gap="large")
            
            with col1:
                st.markdown('<div class="analysis-header">📊 Text Analysis Breakdown</div>', unsafe_allow_html=True)
                
                if segments and segment_scores:
                    # 統計資料
                    stats = {
                        "Total Words": len(text.split()),
                        "AI Segments": sum(1 for s in segment_scores if s > 0.5),
                        "Human Segments": sum(1 for s in segment_scores if s <= 0.5),
                        "Avg AI Score": f"{np.mean(segment_scores)*100:.1f}%"
                    }
                    
                    cols = st.columns(4)
                    for i, (label, value) in enumerate(stats.items()):
                        with cols[i]:
                            st.metric(label, value)
                    
                    # 分段分析圖表
                    fig_segments = create_analysis_chart(segments[:10], segment_scores[:10])
                    st.plotly_chart(fig_segments, use_container_width=True)
            
            with col2:
                st.markdown('<div class="analysis-header">🎯 Content Classification</div>', unsafe_allow_html=True)
                
                # Calculate real percentages based on segment analysis
                if segments and segment_scores:
                    # Count segments in each category based on their scores
                    identical_segments = sum(1 for s in segment_scores if s > 0.8)
                    minor_segments = sum(1 for s in segment_scores if 0.6 < s <= 0.8)
                    paraphrased_segments = sum(1 for s in segment_scores if 0.4 < s <= 0.6)
                    unique_segments = sum(1 for s in segment_scores if s <= 0.4)
                    
                    total_segments = len(segment_scores)
                    if total_segments > 0:
                        identical_pct = round((identical_segments / total_segments) * 100)
                        minor_pct = round((minor_segments / total_segments) * 100)
                        paraphrased_pct = round((paraphrased_segments / total_segments) * 100)
                        unique_pct = round((unique_segments / total_segments) * 100)
                        
                        # Ensure percentages add up to 100%
                        total = identical_pct + minor_pct + paraphrased_pct + unique_pct
                        if total != 100:
                            diff = 100 - total
                            unique_pct += diff
                    else:
                        # Fallback if no segments
                        identical_pct = 0
                        minor_pct = 0
                        paraphrased_pct = 0
                        unique_pct = 100
                else:
                    # If no segment analysis, estimate based on overall score
                    if ai_percentage > 80:
                        identical_pct = int(ai_percentage - 20)
                        minor_pct = 20
                        paraphrased_pct = 10
                        unique_pct = 100 - identical_pct - minor_pct - paraphrased_pct
                    elif ai_percentage > 60:
                        identical_pct = 10
                        minor_pct = int(ai_percentage - 30)
                        paraphrased_pct = 20
                        unique_pct = 100 - identical_pct - minor_pct - paraphrased_pct
                    elif ai_percentage > 40:
                        identical_pct = 5
                        minor_pct = 15
                        paraphrased_pct = int(ai_percentage - 10)
                        unique_pct = 100 - identical_pct - minor_pct - paraphrased_pct
                    else:
                        identical_pct = 0
                        minor_pct = 5
                        paraphrased_pct = int(ai_percentage)
                        unique_pct = 100 - identical_pct - minor_pct - paraphrased_pct
                
                # Create donut chart for classification with controlled container
                labels = ['Identical', 'Minor changes', 'Paraphrased', 'Unique text']
                values = [identical_pct, minor_pct, paraphrased_pct, unique_pct]
                colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
                
                fig_class = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=.65,
                    marker=dict(
                        colors=colors,
                        line=dict(color='#ffffff', width=2)
                    ),
                    textinfo='none',
                    hovertemplate='<b>%{label}</b><br>%{value}%<extra></extra>'
                )])
                
                fig_class.update_layout(
                    showlegend=False,
                    paper_bgcolor='rgba(245,245,245,0)',
                    plot_bgcolor='rgba(245,245,245,0)',
                    margin=dict(t=0, b=0, l=0, r=0),
                    height=200,
                    annotations=[dict(
                        text=f'{ai_percentage:.0f}%',
                        x=0.5, y=0.55,
                        font_size=32,
                        font=dict(color='#1a1a1a', weight=700),
                        showarrow=False
                    ), dict(
                        text='AI Generated Text',
                        x=0.5, y=0.42,
                        font_size=12,
                        font=dict(color='#666'),
                        showarrow=False
                    )]
                )
                
                # Use empty container to control plotly chart styling
                with st.empty():
                    st.plotly_chart(fig_class, use_container_width=True, key="class_donut")
                
                # Legend with colored dots
                st.markdown(f'''
                <div class="classification-legend">
                    <div class="legend-item">
                        <span class="legend-dot" style="background: #e74c3c;"></span>
                        <span class="legend-text"><strong>{identical_pct}%</strong> Identical</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-dot" style="background: #f39c12;"></span>
                        <span class="legend-text"><strong>{minor_pct}%</strong> Minor changes</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-dot" style="background: #3498db;"></span>
                        <span class="legend-text"><strong>{paraphrased_pct}%</strong> Paraphrased</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-dot" style="background: #2ecc71;"></span>
                        <span class="legend-text"><strong>{unique_pct}%</strong> Unique text</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Detection Result moved here (below legend)
                st.markdown(f'''
                <div style="text-align: center; margin-top: 1.5rem; padding: 1rem; background: #f8f8f8; border-radius: 10px;">
                    <div class="metric-label">Detection Result</div>
                    <div class="metric-value {'ai-detected' if ai_percentage > 50 else 'human-detected'}" style="font-size: 1.8rem;">
                        {'🤖 AI Generated' if ai_percentage > 50 else '✍️ Human Written'}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # 關閉 result-container
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 標註文字展示（預設展開）
            st.markdown('<div class="section-header">📝 View Highlighted Text</div>', unsafe_allow_html=True)
            if segments and segment_scores:
                highlighted = highlight_text(text, segments, segment_scores)
                st.markdown(f'<div class="highlighted-text">{highlighted}</div>', unsafe_allow_html=True)
            else:
                st.text(text)
            
            # 建議 - 移到最下面
            st.markdown('<div class="section-header">💡 Recommendations</div>', unsafe_allow_html=True)
            if ai_percentage > 70:
                st.warning("⚠️ High AI content detected. Consider rewriting for authenticity.")
            elif ai_percentage > 40:
                st.info("ℹ️ Moderate AI content. Some sections may need revision.")
            else:
                st.success("✅ Content appears to be primarily human-written.")
        
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Error during analysis: {str(e)}")
            st.stop()
    
    elif analyze_button and not text:
        st.warning("⚠️ Please enter text to analyze!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '''
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: #888; font-size: 0.9rem; margin-bottom: 0.5rem;">
                Powered by amberliangtesol
            </p>
            <a href="https://github.com/amberliangtesol/ai-text-detector" target="_blank" style="text-decoration: none;">
                <svg height="24" width="24" viewBox="0 0 16 16" version="1.1" style="vertical-align: middle; fill: #888;">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
                <span style="color: #888; margin-left: 0.5rem; font-size: 0.9rem;">GitHub</span>
            </a>
        </div>
        ''',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()