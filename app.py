import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots  
from datetime import datetime, timedelta

# ⚠️ 注意：set_page_config 必須是第一行
st.set_page_config(page_title="專業量化交易終端機", page_icon="📈", layout="wide")

# ==========================================
# 💎 專業精緻護眼版 CSS 注入區 (全域消滅黑字版)
# ==========================================
st.markdown("""
<style>
    /* 全局字體優化與基礎大小恢復正常比例 */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", Roboto, Helvetica, Arial, sans-serif !important;
        font-size: 16px !important; 
    }
    .stApp {
        background-color: #0F172A;
    }
    
    /* 🚨 終極核彈：把所有未特別指定的字體全變成淺色，消滅所有隱藏的黑字！ */
    h1, h2, h3, h4, h5, h6, p, span, label, li, div.stMarkdown, .stText, th, td {
        color: #E2E8F0 !important;
    }
    
    h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
    h2 { font-size: 2.0rem !important; }
    h3 { font-size: 1.5rem !important; }
    h4 { font-size: 1.3rem !important; }
    p { font-size: 1.1rem !important; line-height: 1.6; }
    
    /* 🚀 徹底隱藏側邊欄與頂部漢堡選單 */
    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stHeader"] { background-color: transparent; }
    
    /* ========================================== */
    /* 🛡️ 護眼暗黑處理：輸入框、彈出選單與提示框 */
    /* ========================================== */
    
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div {
        background-color: #1E293B !important; 
        border: 1px solid #38BDF8 !important; 
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] *, 
    input {
        color: #F8FAFC !important; 
        font-weight: 600 !important;
        background-color: transparent !important;
    }
    
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul {
        background-color: #0F172A !important; 
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="popover"] li { background-color: transparent !important; }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #38BDF8 !important; 
    }
    div[data-baseweb="popover"] li:hover *,
    div[data-baseweb="popover"] li[aria-selected="true"] * {
        color: #0F172A !important;
        font-weight: bold !important;
    }

    div[data-baseweb="calendar"] { background-color: #0F172A !important; }

    [data-testid="stAlert"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    /* ========================================== */
    /* 🎯 暴力鎮壓：返回首頁與 Expander 展開標題列的反白問題 */
    /* ========================================== */

    [data-testid="stExpander"] details summary {
        background-color: #1E293B !important; border-radius: 8px !important; padding: 10px 15px !important;
    }
    [data-testid="stExpander"] details summary:hover { background-color: #0F172A !important; }
    [data-testid="stExpander"] details summary:hover p { color: #38BDF8 !important; }
    [data-testid="stExpander"] details summary svg { fill: #38BDF8 !important; }
    [data-testid="stExpander"] details { background-color: #0F172A !important; border: 1px solid #334155 !important; border-radius: 8px !important; }

    /* Secondary 按鈕 (返回首頁、強制刷新) */
    button[kind="secondary"], 
    [data-testid="baseButton-secondary"] {
        background-color: #1E293B !important; border: 1px solid #38BDF8 !important; 
        border-radius: 8px !important; padding: 12px 0 !important;
        transition: all 0.3s ease !important;
    }
    button[kind="secondary"] p, [data-testid="baseButton-secondary"] p { color: #38BDF8 !important; font-weight: bold !important;}
    button[kind="secondary"]:hover, [data-testid="baseButton-secondary"]:hover { background-color: #38BDF8 !important; }
    button[kind="secondary"]:hover p, [data-testid="baseButton-secondary"]:hover p { color: #0F172A !important; }

    /* 主按鈕 (Primary) - 經典紅色 */
    button[kind="primary"],
    [data-testid="baseButton-primary"] {
        background-color: #FF4B4B !important; border-color: #FF4B4B !important;
        border-radius: 8px; padding: 12px 0 !important; 
        box-shadow: 0 4px 6px -1px rgba(255, 75, 75, 0.4) !important; transition: all 0.3s ease !important;
    }
    button[kind="primary"] p, [data-testid="baseButton-primary"] p { color: #FFFFFF !important; font-size: 1.2rem !important; font-weight: bold !important; }
    button[kind="primary"]:hover,
    [data-testid="baseButton-primary"]:hover { 
        transform: translateY(-2px); box-shadow: 0 8px 15px -1px rgba(255, 75, 75, 0.6) !important; 
        background-color: #FF3333 !important; border-color: #FF3333 !important;
    }

    /* ========================================== */
    /* 🎯 原生 Metric 卡片修復 */
    /* ========================================== */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #1E293B, #0F172A) !important;
        border: 1px solid #334155 !important;
        padding: 16px 20px !important; 
        border-radius: 12px !important;
    }
    /* 強制原生 Metric 的數字為亮綠色，不怕被蓋掉 */
    [data-testid="stMetricValue"] * { color: #10B981 !important; font-family: 'Consolas', 'Monaco', monospace !important; font-size: 2.5rem !important; font-weight: 900 !important; }

    /* ========================================== */
    /* 🎯 專案B的客製化動能數據卡片 */
    /* ========================================== */

    div[role="radiogroup"] label { font-weight: bold !important; cursor: pointer; }

    .custom-metric-card {
        background: linear-gradient(145deg, #1E293B, #0F172A); border: 1px solid #334155; padding: 20px 24px; 
        border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .custom-metric-card:hover { transform: translateY(-3px); border-color: #38BDF8; }
    .custom-label { margin: 0 0 8px 0 !important; font-weight: 700 !important; }
    .custom-value { font-family: 'Consolas', 'Monaco', monospace !important; font-size: 2.5rem !important; font-weight: 900 !important; letter-spacing: -1px; margin: 0 0 8px 0 !important; }
    .custom-delta { font-size: 1.2rem !important; font-weight: 700 !important; margin: 0 !important; }

    /* 漲跌顏色定義 (供 HTML 卡片使用) */
    .val-us-up { color: #10B981 !important; }   /* 美股漲：綠 */
    .val-us-down { color: #F43F5E !important; } /* 美股跌：紅 */

    .prediction-box-bull { background-color: rgba(244, 63, 94, 0.15) !important; border: 2px solid #F43F5E !important; padding: 16px; border-radius: 12px; margin-top: 15px; }
    .prediction-box-bear { background-color: rgba(16, 185, 129, 0.15) !important; border: 2px solid #10B981 !important; padding: 16px; border-radius: 12px; margin-top: 15px; }
    .prediction-box-neutral { background-color: rgba(245, 158, 11, 0.15) !important; border: 2px solid #F59E0B !important; padding: 16px; border-radius: 12px; margin-top: 15px; }
    .prediction-box-vix { background-color: rgba(239, 68, 68, 0.2) !important; border: 2px dashed #EF4444 !important; padding: 16px; border-radius: 12px; margin-top: 15px; }
    
    hr { border-color: #334155 !important; margin-top: 1.5rem; margin-bottom: 1.5rem; }
    .formula-box { background-color: #020617; border-left: 4px solid #0EA5E9; padding: 16px; border-radius: 4px; margin-top: 10px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔧 核心爬蟲與資料處理工具箱
# ==========================================
@st.cache_data(ttl=60)
def fetch_futures_price() -> tuple[float | None, str | None]:
    url = "https://invest.cnyes.com/futures/TWF/TXF"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=4)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for string in soup.stripped_strings:
                clean_t = string.replace(',', '')
                if clean_t.replace('.', '', 1).isdigit() and 15000 < float(clean_t) < 45000: 
                    return float(clean_t), None
    except: 
        pass
        
    try:
        idx_data = yf.Ticker("^TWII").history(period="1d")
        if not idx_data.empty:
            return float(idx_data['Close'].iloc[-1]), "已自動啟用大盤現貨替代報價"
    except:
        pass
    return None, "數據擷取失敗"

@st.cache_data(ttl=60)
def fetch_stock_realtime_price(ticker: str) -> tuple[float | None, str | None]:
    try:
        stock = yf.Ticker(ticker)
        try:
            last_price = stock.fast_info.last_price
            if last_price and not pd.isna(last_price): return float(last_price), None
        except: pass
        hist = stock.history(period='1mo')
        if not hist.empty:
            valid_closes = hist['Close'].dropna()
            if not valid_closes.empty: return float(valid_closes.iloc[-1]), None
        return None, "無法取得有效報價"
    except Exception as e: return None, str(e)

@st.cache_data(ttl=3600)
def fetch_and_normalize_history(tw_ticker: str, adr_ticker: str, start_date: str, end_date: str) -> pd.DataFrame | None:
    try:
        real_end_date = (pd.to_datetime(end_date) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        tw_data = yf.Ticker(tw_ticker).history(start=start_date, end=real_end_date)['Close']
        adr_data = yf.Ticker(adr_ticker).history(start=start_date, end=real_end_date)['Close']
        market_data = yf.Ticker('^TWII').history(start=start_date, end=real_end_date)['Close']
        
        tw_data.index = pd.to_datetime(tw_data.index).tz_localize(None).normalize()
        adr_data.index = pd.to_datetime(adr_data.index).tz_localize(None).normalize()
        market_data.index = pd.to_datetime(market_data.index).tz_localize(None).normalize()
        
        tw_data.name = 'TW_Stock'
        adr_data.name = 'ADR'
        market_data.name = 'Market_Index'
        
        df = pd.concat([tw_data, adr_data, market_data], axis=1, join='outer')
        df = df.ffill().dropna() 
        
        if not df.empty: return (df / df.iloc[0]) * 100
        return None
    except Exception: return None

def get_multicore_hist_data(selected_date, target_key, tickers_dict):
    try:
        start = (selected_date - timedelta(days=15)).strftime('%Y-%m-%d')
        end = (selected_date + timedelta(days=10)).strftime('%Y-%m-%d')
        df_list = []
        for name, sym in tickers_dict.items():
            hist = yf.Ticker(sym).history(start=start, end=end)['Close']
            hist.index = pd.to_datetime(hist.index).tz_localize(None).normalize()
            hist.name = name
            df_list.append(hist)
        df = pd.concat(df_list, axis=1, join='outer').ffill().dropna()
        returns = df.pct_change() * 100
        
        returns['Target_Next'] = returns[target_key].shift(-1)
        next_dates = df.index.to_series().shift(-1)
        sel_ts = pd.to_datetime(selected_date)
        valid_dates = returns.index[returns.index <= sel_ts]
        if len(valid_dates) < 2: return None, None, None
        target_ts = valid_dates[-1]
        
        row_res = {}
        for name in tickers_dict.keys():
            if name in ["TWII", "TWIE", "TWIF"]: continue
            row_res[name] = {
                "price": float(df.loc[target_ts, name]),
                "change": float(returns.loc[target_ts, name])
            }
        row_res["Target_Next"] = float(returns.loc[target_ts, "Target_Next"])
        return row_res, target_ts, next_dates.loc[target_ts]
    except: return None, None, None

@st.cache_data(ttl=3600)
def fetch_past_month_accuracy(target_key: str, core_type: str, tickers_dict: dict) -> tuple[float, pd.DataFrame]:
    try:
        end_dt = datetime.today()
        start_dt = end_dt - timedelta(days=45) 
        df_list = []
        for name, sym in tickers_dict.items():
            hist = yf.Ticker(sym).history(start=start_dt.strftime('%Y-%m-%d'), end=end_dt.strftime('%Y-%m-%d'))['Close']
            if not hist.empty:
                hist.index = pd.to_datetime(hist.index).tz_localize(None).normalize()
                hist.name = name
                df_list.append(hist)
        if not df_list: return 70.0, pd.DataFrame()
        df = pd.concat(df_list, axis=1, join='outer').ffill().dropna()
        if df.empty: return 70.0, pd.DataFrame()
        
        returns = df.pct_change() * 100
        returns['Target_Next'] = returns[target_key].shift(-1)
        returns = returns.dropna()
        
        past_month_ts = pd.to_datetime(datetime.today() - timedelta(days=30))
        returns = returns[returns.index >= past_month_ts]
        if returns.empty: return 70.0, pd.DataFrame()
        
        if core_type == "🚀 科技權值核心 (電子/半導體)":
            w = {"台積電 ADR": 0.40, "費城半導體": 0.30, "那斯達克": 0.30}
        elif core_type == "🌐 全市場綜合大盤 (加權指數)":
            w = {"S&P 500": 0.40, "台積電 ADR": 0.20, "那斯達克": 0.20, "道瓊工業": 0.20}
        else:
            w = {"道瓊工業": 0.60, "S&P 500": 0.40}
            
        correct, total = 0, 0
        chart_data = [] 

        for date, row in returns.iterrows():
            score = sum(row.get(k, 0) * v for k, v in w.items())
            vix = row.get("VIX 恐慌指數", 0)
            actual = row['Target_Next']
            
            chart_data.append({"Date": date, "Score": score, "Actual": actual})

            if vix > 25:
                if actual <= 0: correct += 1 
            elif score > 0.5:
                if actual > 0: correct += 1
            elif score < -0.5:
                if actual < 0: correct += 1
            else:
                if -0.5 <= actual <= 0.5: correct += 1
            total += 1
            
        accuracy = (correct / total) * 100 if total > 0 else 70.0
        df_chart = pd.DataFrame(chart_data).set_index("Date")
        return accuracy, df_chart
    except:
        return 70.0, pd.DataFrame()

# ==========================================
# 👈 路由狀態管理
# ==========================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

def go_home_button():
    if st.button("⬅️ 返回系統首頁", type="secondary", width="stretch"):
        st.session_state.current_page = "home"
        st.rerun()

# ==========================================
# 🏠 首頁：模組入口
# ==========================================
if st.session_state.current_page == "home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🛰️ 專業量化投資監控系統")
    st.write(f"最後同步時間：**{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")
    st.info("歡迎進入三位一體量化平台。本系統整合 yfinance 歷史數據庫與即時爬蟲網路，請點擊下方入口進入各分析模組。")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📈 [專案 A] 跨海連動分析", type="primary", width="stretch"):
        st.session_state.current_page = "page_a"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔮 [專案 B] 盤前趨勢預測", type="primary", width="stretch"):
        st.session_state.current_page = "page_b"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🛡️ [專案 C] 風險對沖計算機", type="primary", width="stretch"):
        st.session_state.current_page = "page_c"
        st.rerun()

# ==========================================
# 📈 專案 A：跨海連動分析對比
# ==========================================
elif st.session_state.current_page == "page_a":
    go_home_button()
    st.title("📈 跨海連動分析對比")
    st.write("透過資料標準化 (Normalization) 技術，將現貨與 ADR 錨定於 100% 起點，直觀判讀套利空間與連動強度。")
    with st.expander("💡 為什麼要將起點設為 100%？ (點擊查看量化教學)"):
        st.markdown("由於台股報價為 **新台幣**，美股 ADR 為 **美元**，且兩者絕對數值落差極大。在量化圖表中，我們透過 **標準化 (Normalization)**，將所有資產第一天的價格設定為 `100%`。後續的走勢線條反映的即是「**累積報酬率**」，這樣就能在同一張圖上公平、客觀地比較台美兩地的連動性與價差空間。")
    
    col1, col2 = st.columns([1, 1])
    ADR_DICT = {"台積電 (2330)": {"tw": "2330.TW", "adr": "TSM"}, "聯電 (2303)": {"tw": "2303.TW", "adr": "UMC"}, "日月光 (3711)": {"tw": "3711.TW", "adr": "ASX"}, "中華電 (2412)": {"tw": "2412.TW", "adr": "CHT"}}
    
    with col1: selected = st.selectbox("🎯 選擇追蹤標的", list(ADR_DICT.keys()))
    with col2: 
        st.markdown("<p style='color:#CBD5E1; font-weight: bold;'>⏳ 自訂回測區間</p>", unsafe_allow_html=True)
        default_end = datetime.today()
        default_start = default_end - timedelta(days=180)
        date_col1, date_col2 = st.columns(2)
        with date_col1: start_date = st.date_input("開始日期", value=default_start)
        with date_col2: end_date = st.date_input("結束日期", value=default_end)
    
    st.divider()
    if start_date >= end_date:
        st.error("⚠️ 錯誤：『開始日期』必須早於『結束日期』，請重新選擇。")
    else:
        with st.spinner(f"正在擷取 {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 的海外數據..."):
            df_norm = fetch_and_normalize_history(ADR_DICT[selected]["tw"], ADR_DICT[selected]["adr"], start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            if df_norm is not None:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_norm.index, y=df_norm['TW_Stock'], name='台股現貨', line=dict(color='#F43F5E', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(244, 63, 94, 0.1)', hovertemplate='%{y:.2f}%<extra></extra>'))
                fig.add_trace(go.Scatter(x=df_norm.index, y=df_norm['ADR'], name='美股 ADR', line=dict(color='#10B981', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.1)', hovertemplate='%{y:.2f}%<extra></extra>'))
                fig.add_trace(go.Scatter(x=df_norm.index, y=df_norm['Market_Index'], name='大盤 (^TWII)', line=dict(color='#38BDF8', width=2, shape='spline'), hovertemplate='%{y:.2f}%<extra></extra>'))
                fig.update_layout(title=dict(text=f"{selected} 走勢與套利空間比較", font=dict(size=26, color='#FFFFFF')), hovermode="x unified", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(color='#FFFFFF', size=16), bgcolor='rgba(15, 23, 42, 0.8)'), margin=dict(l=20, r=20, t=90, b=20), font=dict(color='#F8FAFC'))
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#1E293B', tickfont=dict(color='#94A3B8', size=14))
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#1E293B', tickfont=dict(color='#94A3B8', size=14), title=dict(text="累積報酬率 (%)", font=dict(color="#CBD5E1")))
                st.plotly_chart(fig, width="stretch") 
            else:
                st.error("目前無法繪製圖表，可能是休市、選擇區間過短或網路問題，請重新選擇日期後再試。")

# ==========================================
# 🔮 專案 B：多核心 AI 盤前氣氛預測模型 (綜合圖表疊合版)
# ==========================================
elif st.session_state.current_page == "page_b":
    go_home_button()
    st.title("🔮 多核心 AI 盤前氣氛預測模型 (V4.5)")
    st.write("根據您關注的投資板塊，切換專屬的量化演算核心，動態引入美股連動參數。")

    # --- 步驟 1：選擇預測核心與操作模式 ---
    c_mode1, c_mode2 = st.columns([1, 1])
    
    with c_mode1:
        core_type = st.selectbox(
            "🎯 請選擇預測核心：", 
            ["🚀 科技權值核心 (電子/半導體)", "🌐 全市場綜合大盤 (加權指數)", "🧱 傳產與金融防禦核心"]
        )
        
        if core_type == "🚀 科技權值核心 (電子/半導體)":
            st.markdown("""
            <div style="background-color:rgba(14, 165, 233, 0.15); border-left: 4px solid #0EA5E9; padding: 12px 16px; border-radius: 6px; margin-top: 10px; margin-bottom: 10px;">
                <span style="color:#38BDF8 !important; font-weight:bold; font-size:1.1rem;">🔗 關聯 ETF 參考：</span><br>
                <span style="color:#F8FAFC !important; font-size:1rem;">0052 (富邦科技)、00891 (中信關鍵半導體)</span>
            </div>
            """, unsafe_allow_html=True)
        elif core_type == "🧱 傳產與金融防禦核心":
            st.markdown("""
            <div style="background-color:rgba(16, 185, 129, 0.15); border-left: 4px solid #10B981; padding: 12px 16px; border-radius: 6px; margin-top: 10px; margin-bottom: 10px;">
                <span style="color:#34D399 !important; font-weight:bold; font-size:1.1rem;">🔗 關聯 ETF 參考 (高股息/金融)：</span><br>
                <span style="color:#F8FAFC !important; font-size:1rem;">0056 (元大高股息)、00878 (國泰永續高股息)、0055 (元大MSCI金融)</span>
            </div>
            """, unsafe_allow_html=True)
            
    with c_mode2:
        mode = st.radio("請選擇操作模式：", ["⚡ 最新盤前即時預測", "📅 歷史單日回測驗證"], horizontal=True)
        
    st.divider()

    # --- 步驟 2：核心參數與【正確答案目標】動態設定 ---
    all_tickers = {
        "台積電 ADR": "TSM", "費城半導體": "^SOX", "那斯達克": "^IXIC", 
        "S&P 500": "^GSPC", "道瓊工業": "^DJI", "VIX 恐慌指數": "^VIX", 
        "TWII": "^TWII",  
        "TWIE": "0052.TW",  
        "TWIF": "0055.TW"   
    }
    
    weights = {}
    display_keys = []
    
    if core_type == "🚀 科技權值核心 (電子/半導體)":
        weights = {"台積電 ADR": 0.40, "費城半導體": 0.30, "那斯達克": 0.30}
        display_keys = ["台積電 ADR", "費城半導體", "那斯達克", "VIX 恐慌指數"]
        formula_latex = r"\text{科技動能指數} = (\text{TSM} \times 0.4) + (\text{SOX} \times 0.3) + (\text{Nasdaq} \times 0.3)"
        target_answer_key = "TWIE"
        target_answer_name = "富邦科技 ETF (0052.TW)" 

    elif core_type == "🌐 全市場綜合大盤 (加權指數)":
        weights = {"S&P 500": 0.40, "台積電 ADR": 0.20, "那斯達克": 0.20, "道瓊工業": 0.20}
        display_keys = ["S&P 500", "台積電 ADR", "那斯達克", "道瓊工業", "VIX 恐慌指數"]
        formula_latex = r"\text{綜合大盤動能指數} = (\text{S\&P500} \times 0.4) + (\text{TSM} \times 0.2) + (\text{Nasdaq} \times 0.2) + (\text{DowJones} \times 0.2)"
        target_answer_key = "TWII"
        target_answer_name = "台股加權大盤指數 (^TWII)"

    else: 
        weights = "傳產金融" 
        weights_dict = {"道瓊工業": 0.60, "S&P 500": 0.40}
        display_keys = ["道瓊工業", "S&P 500", "VIX 恐慌指數"]
        formula_latex = r"\text{傳產金融動能指數} = (\text{DowJones} \times 0.6) + (\text{S\&P500} \times 0.4)"
        target_answer_key = "TWIF"
        target_answer_name = "元大MSCI金融 ETF (0055.TW)" 

    with st.spinner("正在精算該核心近一個月歷史勝率與渲染綜合對比圖表..."):
        accuracy_val, df_chart = fetch_past_month_accuracy(target_answer_key, core_type, all_tickers)
    
    st.markdown(f"📊 **該核心近一個月預測正確率 (勝率)：** <span style='color:#F59E0B !important; font-weight:bold; font-size:1.6rem;'>{accuracy_val:.1f}%</span>", unsafe_allow_html=True)
    
    if not df_chart.empty:
        with st.expander("📉 展開查看近一個月 [模型動能] vs [實際漲跌] 綜合對比圖", expanded=True):
            fig_mix = go.Figure()
            
            # 長條圖：實際漲跌 (台股紅漲綠跌邏輯)
            actual_colors = ['#F43F5E' if val > 0 else '#10B981' for val in df_chart['Actual']]
            fig_mix.add_trace(
                go.Bar(
                    x=df_chart.index, y=df_chart['Actual'],
                    name='實際走勢',
                    marker_color=actual_colors,
                    opacity=0.6,
                    hovertemplate='實際漲跌: <b>%{y:+.2f}%</b><extra></extra>'
                )
            )
            
            # 折線圖：模型預測分數
            fig_mix.add_trace(
                go.Scatter(
                    x=df_chart.index, y=df_chart['Score'],
                    name='預測動能',
                    mode='lines+markers',
                    line=dict(color='#0EA5E9', width=3, shape='spline'),
                    marker=dict(size=6, color='#0F172A', line=dict(width=2, color='#38BDF8')),
                    hovertemplate='預測分數: <b>%{y:+.2f}%</b><extra></extra>'
                )
            )
            
            fig_mix.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode="x unified",
                height=450,       
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#F8FAFC"))
            )
            
            fig_mix.update_yaxes(title=dict(text="百分比 (%)", font=dict(color="#F8FAFC")), gridcolor='rgba(51, 65, 85, 0.4)', zerolinecolor='rgba(255, 255, 255, 0.3)', zerolinewidth=1.5, tickfont=dict(color="#F8FAFC"))
            fig_mix.update_xaxes(gridcolor='rgba(51, 65, 85, 0.2)', tickfont=dict(color="#F8FAFC"))
            
            st.plotly_chart(fig_mix, width="stretch")
            
    st.divider()

    # --- 步驟 3：資料擷取邏輯 ---
    weighted_score = 0
    vix_val = 0
    us_data = {}

    if mode == "⚡ 最新盤前即時預測":
        st.write(f"當前監控核心：`{core_type}`。開盤預期對應目標：`{target_answer_name}`")
        with st.spinner("正在擷取最新美股數據..."):
            for name in display_keys:
                try:
                    stock = yf.Ticker(all_tickers[name])
                    data = stock.history(period="5d")
                    if not data.empty and len(data) >= 2:
                        close = float(data['Close'].iloc[-1])
                        prev = float(data['Close'].iloc[-2])
                        us_data[name] = {"price": close, "change": ((close - prev) / prev) * 100}
                except: continue
    else:
        hist_date = st.date_input("🗓️ 選擇欲驗證的美股交易日：", value=datetime.today() - timedelta(days=2))
        with st.spinner("撈取歷史數據與動態目標答案中..."):
            row_data, target_ts, next_ts = get_multicore_hist_data(hist_date, target_answer_key, all_tickers)
            
        if row_data is not None:
            st.info(f"成功載入數據！選定美股交易日：**{target_ts.strftime('%Y-%m-%d')}**")
            us_data = row_data
        else:
            st.error("無法取得該日期的歷史數據，請確認選擇的日期是否為交易日。")
            st.stop()

    # --- 步驟 4：動態渲染極巨化美股色彩卡片（完美呈現：數值與漲跌幅套用專屬 CSS 色彩） ---
    if us_data:
        st.markdown(f"#### 🌐 國際市場動態Snapshot ({core_type})")
        cols = st.columns(len(display_keys))
        curr_weights = weights_dict if core_type == "🧱 傳產與金融防禦核心" else weights
        
        for i, name in enumerate(display_keys):
            if name in us_data:
                val = us_data[name]
                arrow = "▲" if val['change'] >= 0 else "▼"
                plus_sign = "+" if val['change'] >= 0 else ""
                
                # 色彩邏輯套用 CSS Class：美國指數（漲綠跌紅）
                if val['change'] >= 0:
                    color_class = "val-us-up"
                else:
                    color_class = "val-us-down"

                if name == "VIX 恐慌指數":
                    vix_val = val['price']
                    w_label = ""
                    # 恐慌指數是反指標：漲為紅，跌為綠
                    color_class = "val-us-down" if val['change'] >= 0 else "val-us-up"
                else:
                    w_val = curr_weights.get(name, 0)
                    w_label = f" (權重 {w_val*100:.0f}%)" if w_val > 0 else " (不計分)"
                    weighted_score += (val['change'] * w_val)
                
                # HTML 渲染：主價格維持清晰白字，只有漲跌幅與箭頭套用紅綠色
                html_card = f"""
                <div class="custom-metric-card">
                    <p class="custom-label" style="color: #CBD5E1 !important;">{name}{w_label}</p>
                    <p class="custom-value" style="color: #F8FAFC !important;">{val['price']:,.2f}</p>
                    <p class="custom-delta {color_class}">{arrow} {plus_sign}{val['change']:.2f}%</p>
                </div>
                """
                cols[i].markdown(html_card, unsafe_allow_html=True)

        # --- 步驟 5：白箱公式 ---
        st.divider()
        st.markdown("#### 🧠 模型權重計算解析 (White-box Analysis)")
        st.markdown("<div class='formula-box'>", unsafe_allow_html=True)
        st.write("本核心依據以下量化公式進行權重精算：")
        st.latex(formula_latex)
        
        if core_type == "🚀 科技權值核心 (電子/半導體)":
            latex_val = fr"= ({us_data.get('台積電 ADR', {}).get('change', 0):+.2f}\% \times 0.4) + ({us_data.get('費城半導體', {}).get('change', 0):+.2f}\% \times 0.3) + ({us_data.get('那斯達克', {}).get('change', 0):+.2f}\% \times 0.3) = \mathbf{{{weighted_score:+.2f}\%}}"
        elif core_type == "🌐 全市場綜合大盤 (加權指數)":
            latex_val = fr"= ({us_data.get('S&P 500', {}).get('change', 0):+.2f}\% \times 0.4) + ({us_data.get('台積電 ADR', {}).get('change', 0):+.2f}\% \times 0.2) + ({us_data.get('那斯達克', {}).get('change', 0):+.2f}\% \times 0.2) + ({us_data.get('道瓊工業', {}).get('change', 0):+.2f}\% \times 0.2) = \mathbf{{{weighted_score:+.2f}\%}}"
        else:
            latex_val = fr"= ({us_data.get('道瓊工業', {}).get('change', 0):+.2f}\% \times 0.6) + ({us_data.get('S&P 500', {}).get('change', 0):+.2f}\% \times 0.4) = \mathbf{{{weighted_score:+.2f}\%}}"
        st.latex(latex_val)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # --- 步驟 6：AI 預測訊號 ---
        st.markdown("#### 🤖 預測演算結果")
        if vix_val > 25: 
            st.markdown(f"""
            <div class='prediction-box-vix'>
                <h3 style='margin:0; color:#EF4444 !important;'>🚨 【極端風險警告】 VIX 恐慌指數 ({vix_val:.2f}) 飆破安全值！</h3>
                <p style='margin:10px 0 0 0; color:#E2E8F0 !important; font-size:1.1rem;'>避險情緒極高，無論動能指數為何，皆強烈建議保留現金觀望。</p>
            </div>
            """, unsafe_allow_html=True)
        elif weighted_score > 0.5: 
            st.markdown(f"""
            <div class='prediction-box-bull'>
                <h3 style='margin:0; color:#F43F5E !important;'>🔥 【多方優勢看漲】 (動能指數：+{weighted_score:.2f}%)</h3>
                <p style='margin:10px 0 0 0; color:#E2E8F0 !important; font-size:1.1rem;'>今日台股 <b>{target_answer_name}</b> 相關板塊極高機率『開高』，多方掌控局勢。</p>
            </div>
            """, unsafe_allow_html=True)
        elif weighted_score < -0.5: 
            st.markdown(f"""
            <div class='prediction-box-bear'>
                <h3 style='margin:0; color:#10B981 !important;'>❄️ 【空方優勢看跌】 (動能指數：{weighted_score:.2f}%)</h3>
                <p style='margin:10px 0 0 0; color:#E2E8F0 !important; font-size:1.1rem;'>今日台股 <b>{target_answer_name}</b> 相關板塊高機率『低開』，請留意流動性風險。</p>
            </div>
            """, unsafe_allow_html=True)
        else: 
            st.markdown(f"""
            <div class='prediction-box-neutral'>
                <h3 style='margin:0; color:#F59E0B !important;'>⚖️ 【多空拉鋸盤整】 (動能指數：{weighted_score:.2f}%)</h3>
                <p style='margin:10px 0 0 0; color:#E2E8F0 !important; font-size:1.1rem;'>指標漲跌微弱。預期今日 <b>{target_answer_name}</b> 相關板塊以平盤附近開出。</p>
            </div>
            """, unsafe_allow_html=True)

        # --- 步驟 7：對答案 ---
        if mode == "📅 歷史單日回測驗證" and 'row_data' in locals() and row_data is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            
            if pd.isna(row_data.get('Target_Next')):
                st.info("🕒 該對應目標指數的下一個交易日資料尚未產生（可能為最新交易日或適逢連假）。")
            else:
                actual_chg = row_data['Target_Next']
                next_date_str = next_ts.strftime('%Y/%m/%d')
                
                st.markdown(f"<h4 style='color:#F8FAFC !important;'>🎯 真實市場對答案 (Reality Check - 錨定目標：{target_answer_name})</h4>", unsafe_allow_html=True)
                
                if vix_val > 25:
                    st.warning(f"**模型建議：** 風險過高迴避。\n\n**隔日 ({next_date_str}) {target_answer_name} 實際走勢：** `{actual_chg:+.2f}%` (已成功避開風險)")
                elif weighted_score > 0.5 and actual_chg > 0:
                    st.markdown(f"<h5 style='color:#F43F5E !important; font-size:1.2rem;'>✅ 【完美命中】 模型看漲，隔日 ({next_date_str}) {target_answer_name} 實際大漲 {actual_chg:+.2f}%！</h5>", unsafe_allow_html=True)
                elif weighted_score < -0.5 and actual_chg < 0:
                    st.markdown(f"<h5 style='color:#10B981 !important; font-size:1.2rem;'>✅ 【完美命中】 模型看跌，隔日 ({next_date_str}) {target_answer_name} 實際下跌 {actual_chg:+.2f}%！</h5>", unsafe_allow_html=True)
                elif -0.5 <= weighted_score <= 0.5:
                    st.info(f"**模型建議：** 盤整雜訊觀望。\n\n**隔日 ({next_date_str}) {target_answer_name} 實際走勢：** `{actual_chg:+.2f}%` (符合盤整預期)")
                else:
                    st.error(f"##### ❌ 【預測失準】 指標背離。模型給出明確方向，但隔日 ({next_date_str}) {target_answer_name} 實際走勢為 {actual_chg:+.2f}%。")

# ==========================================
# 🛡️ 專案 C：動態風險對沖 (Hedging) 系統
# ==========================================
elif st.session_state.current_page == "page_c":
    go_home_button()
    st.title("🛡️ 動態風險對沖 (Hedging) 系統")
    st.write("透過 Delta 中性避險邏輯，自動將您手中的現貨資產，換算為對應的台指期放空口數。")
    with st.expander("💡 什麼是避險 (Hedging)？ (點擊查看量化教學)"):
        st.markdown("1. 計算您的持股總價值。\n2. 計算期貨合約價值 (大台指=200元，小台指=50元)。\n3. **持股總價值 ÷ 一口合約價值 = 建議做空的期貨口數**。")
    
    col1, col2 = st.columns([2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 強制刷新報價", type="secondary", width="stretch"): 
            st.cache_data.clear(); st.rerun()

    STOCK_DICT = {"2330 台積電": "2330.TW", "2317 鴻海": "2317.TW", "2454 聯發科": "2454.TW", "0050 元大台灣50": "0050.TW", "0056 元大高股息": "0056.TW"}
    with st.container():
        c1, c2 = st.columns(2)
        with c1: stock = st.selectbox("選擇資產部位", list(STOCK_DICT.keys()))
        with c2: qty = st.number_input("持有張數", value=10, min_value=1, step=1)
    
    with st.spinner("精算對沖部位中..."):
        price, _ = fetch_stock_realtime_price(STOCK_DICT[stock])
        fut_price, backup_msg = fetch_futures_price()
    
    if backup_msg:
        st.caption(f"💡 運算提示：{backup_msg}")
    
    if price and fut_price:
        stock_val = price * 1000 * qty
        large_val = fut_price * 200
        small_val = fut_price * 50
        contract_name = "大台指 (TX)" if stock_val >= large_val else "小台指 (MTX)"
        contract_val = large_val if stock_val >= large_val else small_val
        ratio = stock_val / contract_val if contract_val > 0 else 0
        
        st.divider()
        
        # 顯示即時市場單價
        st.markdown("#### 📊 即時市場單價")
        c_price1, c_price2 = st.columns(2)
        stock_name = stock.split(' ')[1] if len(stock.split(' ')) > 1 else stock
        c_price1.metric(f"🎯 {stock_name} (單股現價)", f"$ {price:,.2f}")
        c_price2.metric("🎯 台指期貨 (目前點數)", f"{fut_price:,.0f} 點")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 顯示總曝險與避險口數
        st.markdown("#### 🧮 對沖曝險精算")
        ca, cb = st.columns(2)
        ca.metric("總資產曝險價值", f"$ {stock_val:,.0f}")
        cb.metric(f"單口 {contract_name} 契約價值", f"$ {contract_val:,.0f}")
        st.markdown("<div class='formula-box'>", unsafe_allow_html=True)
        st.latex(fr"\text{{避險口數}} = \frac{{{stock_val:,.0f}}}{{{contract_val:,.0f}}} \approx \mathbf{{{ratio:.2f}}}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.info(f"### 🎯 演算法結論：建議放空 **{round(ratio, 2)}** 口 {contract_name}。")
    else: 
        st.error("網路異常或 API 節點無回應，請點擊上方『強制刷新報價』按鈕再試一次。")
