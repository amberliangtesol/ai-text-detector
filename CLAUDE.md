# AI Text Detector - Project Documentation for Claude

## 📋 專案概述
這是一個使用 ModernBERT 模型的 AI 文本檢測應用程式，可以識別文本是否由 AI 生成。

## 🌐 部署資訊
- **線上網址**: https://ai-text-detect.streamlit.app/
- **本地運行**: `streamlit run app.py`
- **GitHub**: https://github.com/amberliangtesol/ai-text-detector

## 🤖 使用模型
- **模型名稱**: AICodexLab/answerdotai-ModernBERT-base-ai-detector
- **Hugging Face 連結**: https://huggingface.co/AICodexLab/answerdotai-ModernBERT-base-ai-detector
- **特點**: 
  - 基於 ModernBERT-base 輕量版模型
  - 二元分類任務：Label 1 = AI 生成文本，Label 0 = 人類撰寫文本

## ✨ 主要功能

### 1. AI 文本檢測
- 整體文本分析，計算 AI 生成的可能性百分比
- 分段分析，將文本分成多個段落獨立評分
- 信心分數顯示，提供檢測結果的可信度

### 2. 視覺化報告
- **圓環圖 (Donut Chart)**: 顯示整體 AI 百分比
- **分段分析圖表**: 顯示前 10 個段落的 AI 可能性
- **內容分類圓餅圖**: 顯示不同類型內容的比例

### 3. 內容分類系統
- **Identical**: 完全相同的 AI 生成內容 (>80% AI 分數)
- **Minor Changes**: 稍作修改的 AI 內容 (60-80% AI 分數)
- **Paraphrased**: 改寫過的 AI 內容 (40-60% AI 分數)
- **Unique**: 獨特的人類撰寫內容 (<40% AI 分數)

### 4. 使用者介面特色
- 自動滾動功能：點擊檢測後自動滾動到結果區域
- 美化的載入動畫：紅色主題的旋轉圓環
- 響應式設計：適應不同螢幕尺寸
- Sample Text 功能：提供範例文本快速測試

## 🎨 設計規格

### 顏色主題
- **主色調**: #fd373b (紅色)
- **背景色**: #ffffff (白色)
- **次要背景**: #f5f5f5 (淺灰)
- **文字色**: #1a1a1a (深灰)

### UI 元件
- Logo 尺寸: 250px
- 內容 padding: 2rem 6rem
- 圓角: 15-20px
- 陰影: 輕微的 box-shadow 效果

## 📁 專案結構
```
ai-text-detector/
├── app.py              # 主要應用程式
├── requirements.txt    # Python 依賴
├── assets/            
│   ├── logo.png       # Logo 圖片
│   └── bg.png         # 背景圖片
├── styles/
│   └── custom.css     # 自定義 CSS 樣式
├── .streamlit/
│   └── config.toml    # Streamlit 設定
├── README.md          # 專案文檔
└── CLAUDE.md          # Claude AI 專用文檔
```

## 🛠️ 技術棧
- **前端框架**: Streamlit
- **AI 模型**: Hugging Face Transformers
- **視覺化**: Plotly
- **樣式**: Custom CSS
- **部署**: Streamlit Cloud

## 📝 開發注意事項

### 常見問題修復
1. **縮排錯誤**: 確保所有 `with` 區塊內的程式碼正確縮排
2. **變數作用域**: 確保變數在 try-except 區塊的正確位置定義
3. **Streamlit 參數**: 注意 `use_container_width` 即將被棄用，未來需改用 `width='stretch'`

### CSS 客製化重點
- `.st-emotion-cache-zy6yx3`: 主容器 padding 設定
- `.st-key-sample_btn`: Sample Text 按鈕連結樣式
- `.st-key-detect_btn`: Detect AI 按鈕漸層樣式
- `.logo-section img`: Logo 尺寸控制

### 性能優化
- 使用 `@st.cache_resource` 快取模型載入
- 文本分段分析限制在前 10 個段落
- 載入動畫延遲 0.5 秒提升使用體驗

## 🚀 部署指令

### 本地運行
```bash
# 安裝依賴
pip install -r requirements.txt

# 運行應用
streamlit run app.py
```

### 推送更新
```bash
git add .
git commit -m "更新說明"
git push
```

### Streamlit Cloud 部署
1. 登入 https://share.streamlit.io/
2. 選擇 GitHub repository
3. 設定 branch: main
4. 設定 main file: app.py
5. 點擊 Deploy

## 📊 分析邏輯

### 文本分段分析
- 將文本每 50 個詞分為一段
- 使用 25 個詞的重疊（50% overlap）
- 少於 10 個詞的段落跳過分析

### AI 判定標準
- AI Generated: AI 分數 > 50%
- Human Written: AI 分數 ≤ 50%

### 建議系統
- 高 AI 內容 (>70%): 警告訊息，建議重寫
- 中等 AI 內容 (40-70%): 提示訊息，部分段落需要修改
- 低 AI 內容 (<40%): 成功訊息，主要為人類撰寫

## 🔄 最近更新
- 增加 logo 尺寸至 250px
- Sample Text 改為連結樣式
- 修復縮排錯誤問題
- 添加自動滾動功能
- 實現自定義載入動畫
- 優化 CSS 樣式

## 📧 聯絡資訊
- GitHub: @amberliangtesol
- 專案連結: https://github.com/amberliangtesol/ai-text-detector