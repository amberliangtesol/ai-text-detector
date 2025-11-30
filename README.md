# AI Text Detector 🤖

使用 Hugging Face 預訓練模型偵測文字是由人類撰寫還是 AI 生成。

## 專案結構

```
ai-text-detector/
├── app.py              # 主程式
├── requirements.txt    # 套件依賴
├── assets/            # 資源資料夾
│   └── logo.png       # (請放置你的 logo 圖片)
├── styles/            # 樣式資料夾
│   └── custom.css     # 自訂 CSS 樣式
└── README.md          # 專案說明
```

## 安裝

```bash
cd ai-text-detector
pip install -r requirements.txt
```

## 執行

```bash
streamlit run app.py
```

## 新增 Logo

將你的 logo 圖片放在 `assets/logo.png`，應用程式會自動載入。

## 自訂樣式

編輯 `styles/custom.css` 來自訂應用程式的外觀。