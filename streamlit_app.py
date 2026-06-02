import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib # 한글 폰트 깨짐 방지
from collections import Counter

# 페이지 설정
st.set_page_config(page_title="실시간 대푯값 탐구", page_icon="📈", layout="centered")

st.title("📈 실시간 대푯값 탐구 계산기")
st.markdown("""
슬라이더를 움직여 **극단적인 값(Outlier)**이 평균과 중앙값에 어떤 영향을 미치는지 눈으로 직접 확인해 보세요!
""")

# 1. 기본 데이터 설정
st.subheader("1. 기본 데이터 설정")
st.info("이 데이터는 고정되어 있습니다. 학생들의 평범한 시험 점수나 용돈이라고 생각해 보세요.")
base_data_input = st.text_input("기본 데이터를 입력하세요 (쉼표 구분):", "10, 20, 30, 40, 50")

try:
    # 텍스트 입력을 숫자 리스트로 변환
    base_data = [float(x.strip()) for x in base_data_input.split(',')]
    
    # 2. 극단값 조작 슬라이더
    st.subheader("2. 전학생의 점수 (극단값 조작하기)")
    st.markdown("새로 온 전학생 한 명의 점수를 마우스로 드래그해서 아주 낮게, 또는 아주 높게 바꿔보세요.")
    
    # 슬라이더로 실시간 조작할 값 (최소, 최대 범위를 넉넉하게 줌)
    outlier = st.slider("👇 마우스로 드래그하여 점수를 움직여보세요!", min_value=-50, max_value=250, value=60, step=1)
    
    # 전체 데이터 합치기
    data = base_data + [outlier]
    
    # 대푯값 계산
    mean_val = np.mean(data)
    median_val = np.median(data)
    
    # 최빈값 계산
    counts = Counter(data)
    max_count = max(counts.values())
    modes = [k for k, v in counts.items() if v == max_count]
    mode_str = "없음" if max_count == 1 else ", ".join([f"{m:g}" for m in modes])

    # 3. 결과 표시
    st.subheader("3. 대푯값 실시간 변화")
    col1, col2, col3 = st.columns(3)
    
    # 메트릭 UI로 강조해서 보여주기
    col1.metric(label="평균 (Mean) 🔴", value=f"{mean_val:.2f}")
    col2.metric(label="중앙값 (Median) 🟢", value=f"{median_val:g}")
    col3.metric(label="최빈값 (Mode)", value=mode_str)

    # 4. 시각화 그래프
    st.subheader("4. 수직선에서 움직임 관찰하기")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    
    # 기본 데이터 점 찍기 (파란색)
    y_base = np.zeros_like(base_data)
    ax.scatter(base_data, y_base, s=150, alpha=0.6, color="royalblue", label="기본 데이터")
    
    # 조작 중인 극단값 점 찍기 (크고 눈에 띄는 노란색)
    ax.scatter([outlier], [0], s=300, alpha=0.9, edgecolors="black", color="gold", label="조작 중인 데이터 (전학생)", zorder=5)
    
    # 평균과 중앙값 수직선 긋기
    ax.axvline(mean_val, color='tomato', linestyle='dashed', linewidth=3, label=f'평균 ({mean_val:.2f})')
    ax.axvline(median_val, color='forestgreen', linestyle='solid', linewidth=3, label=f'중앙값 ({median_val:g})')
    
    # x축을 고정하여 점이 이동하는 것을 명확히 보여줌
    min_x = min(min(base_data) - 10, -50)
    max_x = max(max(base_data) + 10, 250)
    ax.set_xlim(min_x, max_x)
    
    # 불필요한 축 숨기기
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # 범례 위치 조정
    ax.legend(loc='upper right', bbox_to_anchor=(1, 1.25), ncol=2, fontsize=9)
    
    st.pyplot(fig)
    
    # 5. 수업용 해설 정리
    with st.expander("💡 수업 핵심 정리: 평균 vs 중앙값"):
        st.success("""
        **관찰 포인트:** 노란색 점(전학생)을 오른쪽 끝(250)으로 쭈욱 당겨보세요!
        
        * 🔴 **평균의 한계:** 빨간 점선(평균)은 노란색 점을 따라 크게 오른쪽으로 끌려갑니다. 극단적으로 크거나 작은 값이 있을 때, 평균은 전체 집단을 제대로 대표하지 못할 수 있습니다.
        * 🟢 **중앙값의 장점:** 초록 실선(중앙값)은 노란색 점이 아무리 멀리 가도 크게 변하지 않습니다! 중앙값은 가운데 순서에 있는 값이므로, 극단적인 값(이상치)의 영향을 거의 받지 않습니다.
        """)
        
except ValueError:
    st.error("🚨 기본 데이터를 올바른 숫자 형식으로 입력해주세요. (예: 10, 20, 30)")
