import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data(path='projects/bollywood-dashboard/BollywoodActorRanking.csv'):
    df = pd.read_csv(path)
    # Basic cleaning used by dashboard: ensure numeric columns and normalize where needed
    for col in ['fameScore','talentScore','balanceScore']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def compute_kpis(df):
    return {
        'Avg Fame': df['fameScore'].mean(),
        'Avg Talent': df['talentScore'].mean(),
        'Avg Balance': df['balanceScore'].mean()
    }

def plot_fame_vs_talent(df, selected=None):
    fig = px.scatter(df, x='fameScore', y='talentScore', hover_data=['actor','movie_count','rating'],
                     color='balanceScore', color_continuous_scale='Turbo',
                     labels={'fameScore':'Fame','talentScore':'Talent'})
    if selected is not None and selected in df['actor'].values:
        r = df[df['actor']==selected]
        fig.add_scatter(x=r['fameScore'], y=r['talentScore'], mode='markers+text',
                        text=r['actor'], textposition='top center', marker=dict(size=14, color='black'))
    fig.update_layout(height=520, margin=dict(t=40,b=10))
    return fig

def story_mode_ui(df):
    st.sidebar.markdown('### Story Mode')
    if 'story_step' not in st.session_state:
        st.session_state.story_step = 1

    def prev_step():
        st.session_state.story_step = max(1, st.session_state.story_step-1)
    def next_step():
        st.session_state.story_step = min(5, st.session_state.story_step+1)

    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        st.button('◀ Prev', on_click=prev_step)
    with col2:
        st.button('Next ▶', on_click=next_step)

    step = st.session_state.story_step
    if step == 1:
        st.sidebar.info('Step 1 — Overview: See KPIs and global distribution of Fame/Talent')
    elif step == 2:
        st.sidebar.info('Step 2 — Stars: Identify top fame actors and inspect talent distribution')
    elif step == 3:
        st.sidebar.info('Step 3 — Hidden gems: Find high-talent low-fame actors')
    elif step == 4:
        st.sidebar.info('Step 4 — Compare: Choose two actors to compare profiles')
    else:
        st.sidebar.info('Step 5 — Export: Download filtered data and next steps')

    return step

def main():
    st.set_page_config(page_title='Bollywood — Fame vs Talent (Improved)', layout='wide')
    st.title('🎥 Bollywood — Fame vs Talent (Improved)')

    df = load_data()
    if df is None or df.shape[0] == 0:
        st.error('Dataset not found. Place `BollywoodActorRanking.csv` in `projects/bollywood-dashboard/`')
        return

    # Sidebar filters
    st.sidebar.header('Filters')
    min_movies = st.sidebar.slider('Min movie count', int(df['movie_count'].min()), int(df['movie_count'].max()), 5)
    rating_min, rating_max = st.sidebar.slider('Rating range', 0.0, 10.0, (df['rating'].min(), df['rating'].max()))
    selected_actor = st.sidebar.selectbox('Select actor (optional)', options=[''] + sorted(df['actor'].unique().tolist()))
    use_story = st.sidebar.checkbox('Enable Story Mode', value=False)

    # Apply filters
    df_filtered = df[(df['movie_count'] >= min_movies) & (df['rating'] >= rating_min) & (df['rating'] <= rating_max)].copy()

    # Top KPI row
    kpis = compute_kpis(df_filtered)
    k1, k2, k3 = st.columns(3)
    k1.metric('Avg Fame', f"{kpis['Avg Fame']:.2f}")
    k2.metric('Avg Talent', f"{kpis['Avg Talent']:.2f}")
    k3.metric('Avg Balance', f"{kpis['Avg Balance']:.2f}")

    if use_story:
        step = story_mode_ui(df_filtered)
    else:
        step = None

    # Main visualization area — step-aware
    if step in (None, 1):
        st.subheader('Fame vs Talent — Scatter')
        st.markdown('Explore the relationship between public attention (Fame) and measured performance (Talent).')
        fig = plot_fame_vs_talent(df_filtered, selected=selected_actor if selected_actor else None)
        st.plotly_chart(fig, use_container_width=True)

    if step == 2:
        st.subheader('Top Fame Actors')
        top_fame = df_filtered.sort_values('fameScore', ascending=False).head(10)
        st.dataframe(top_fame[['actor','movie_count','rating','fameScore','talentScore']].reset_index(drop=True))

    if step == 3:
        st.subheader('High Talent, Low Fame — Hidden Gems')
        candidates = df_filtered[(df_filtered['talentScore'] > df_filtered['talentScore'].quantile(0.75)) &
                                 (df_filtered['fameScore'] < df_filtered['fameScore'].quantile(0.5))]
        st.dataframe(candidates[['actor','movie_count','rating','fameScore','talentScore','balanceScore']])

    if step == 4:
        st.subheader('Compare Actors')
        compare = st.multiselect('Pick up to 2 actors to compare', options=list(df_filtered['actor'].unique()), max_selections=2)
        if compare:
            st.write(df_filtered[df_filtered['actor'].isin(compare)][['actor','movie_count','rating','fameScore','talentScore','balanceScore']])

    if step == 5:
        st.subheader('Export Filtered Data')
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button('Download CSV', csv, 'bollywood_filtered.csv')

    # Non-story extras
    if not use_story:
        st.subheader('Top 10 by Balance Score')
        top_balance = df_filtered.sort_values('balanceScore', ascending=False).head(10)
        st.table(top_balance[['actor','movie_count','rating','fameScore','talentScore','balanceScore']].reset_index(drop=True))

if __name__ == '__main__':
    main()
