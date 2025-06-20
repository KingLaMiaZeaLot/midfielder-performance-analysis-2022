import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
sns.set_style("whitegrid", {'grid.linestyle': '--', 'axes.edgecolor': '#333333'})

# Load the dataset
data = """
Player,Squad,Min,Cmp%,DribSucc%,SoT%,TklW,Int
Sergio Oliveira,Galatasaray,2310,84.3,61.7,22.5,32,27
Lucas Torreira,Galatasaray,2670,86.7,68.4,18.3,41,35
Kerem Aktürkoğlu,Galatasaray,3010,76.9,58.4,44.3,15,11
Berkan Kutlu,Galatasaray,1780,82.1,63.2,15.8,28,19
Dries Mertens,Galatasaray,1890,79.8,57.3,38.7,7,9
Yunus Akgün,Galatasaray,1640,75.4,59.6,36.2,11,14
Fredrik Midtsjø,Galatasaray,2050,83.5,64.1,19.5,26,22
Etebo,Galatasaray,920,83.8,66.2,15.3,18,14
Dusan Tadić,Fenerbahçe,3120,82.4,63.1,45.3,22,14
Miguel Crespo,Fenerbahçe,2210,87.2,68.9,19.1,38,29
İrfan Can Kahveci,Fenerbahçe,2450,83.7,61.8,39.6,26,18
Sebastian Szymański,Fenerbahçe,2840,81.6,58.7,42.1,19,23
Willian Arao,Fenerbahçe,1980,88.9,65.3,12.4,31,25
Miha Zajc,Fenerbahçe,1420,80.2,60.7,37.8,13,16
Ferdi Kadıoğlu,Fenerbahçe,2980,79.3,62.4,33.6,29,21
Lincoln,Fenerbahçe,1250,76.8,59.2,40.1,8,11
Gedson Fernandes,Beşiktaş,2750,83.5,67.8,31.7,35,28
Salih Uçan,Beşiktaş,1870,85.7,62.4,18.9,27,21
Alexandru Maxim,Beşiktaş,1560,79.8,59.3,38.2,14,17
Rachid Ghezzal,Beşiktaş,2580,76.5,62.4,43.7,9,13
Berkay Vardar,Beşiktaş,680,77.3,56.1,29.4,5,8
Tayfur Bingöl,Beşiktaş,1320,81.9,64.7,21.8,19,15
Umut Meraş,Beşiktaş,1580,78.4,58.9,17.5,23,18
Nathan Redmond,Beşiktaş,1720,75.6,61.3,41.2,7,10
Anastasios Bakasetas,Trabzonspor,2920,81.9,57.8,41.5,24,19
Manolis Siopis,Trabzonspor,2740,86.3,64.7,14.6,42,37
Uğurcan Yazğılı,Trabzonspor,2150,78.5,59.2,25.3,19,22
Marek Hamšík,Trabzonspor,1890,84.7,60.8,19.8,21,17
Abdülkadir Ömür,Trabzonspor,1420,79.2,61.4,33.7,11,15
Yusuf Yazıcı,Trabzonspor,1350,78.9,59.7,38.4,8,11
Jean Evrard Kouassi,Trabzonspor,1210,76.3,58.6,28.9,16,13
Andreas Cornelius,Trabzonspor,1280,75.4,52.8,46.1,3,4
Dorukhan Toköz,Beşiktaş,1540,82.6,65.1,17.2,23,16
Emre Kılınç,Galatasaray,1430,80.7,63.5,26.8,15,12
Arda Güler,Fenerbahçe,980,81.4,64.8,40.3,6,9
Bartuğ Elmaz,Galatasaray,720,77.9,60.2,31.5,9,7
Efe Can Kaya,Trabzonspor,650,79.6,58.3,35.2,5,8
Batuhan Kör,Beşiktaş,580,76.2,55.7,28.7,7,9
"""

df = pd.read_csv(StringIO(data))

# Team colors
TEAM_COLORS = {
    'Galatasaray': '#E30A17',
    'Fenerbahçe': '#0A7EC1',
    'Beşiktaş': '#000000',
    'Trabzonspor': '#B30019'
}

# Create defensive contribution metric
df['Defensive Actions'] = df['TklW'] + df['Int']

# Filter players with sufficient minutes (at least 900)
analysis_df = df[df['Min'] >= 900].copy()

# Create performance score
metrics = ['Cmp%', 'DribSucc%', 'SoT%', 'Defensive Actions']
for metric in metrics:
    analysis_df[f'{metric}_norm'] = (analysis_df[metric] - analysis_df[metric].min()) / (analysis_df[metric].max() - analysis_df[metric].min()) * 100

analysis_df['Performance Score'] = analysis_df[[f'{m}_norm' for m in metrics]].mean(axis=1)

# Create consistency score
z_scores = analysis_df[metrics].apply(lambda x: (x - x.mean()) / x.std())
analysis_df['Consistency Score'] = z_scores.abs().mean(axis=1)
analysis_df['Consistency Index'] = 100 - (analysis_df['Consistency Score'] / analysis_df['Consistency Score'].max() * 100)

# Sort by performance and consistency
analysis_df = analysis_df.sort_values('Performance Score', ascending=False)

# Create visualizations
def create_top_performers_chart():
    plt.figure(figsize=(14, 10))
    top_10 = analysis_df.head(10)
    colors = [TEAM_COLORS[team] for team in top_10['Squad']]
    
    plt.barh(top_10['Player'], top_10['Performance Score'], color=colors, edgecolor='#333', linewidth=0.8)
    
    # Add team labels
    for i, (player, team) in enumerate(zip(top_10['Player'], top_10['Squad'])):
        plt.text(5, i, team, ha='left', va='center', fontsize=12, fontweight='bold', color='white')
    
    # Add performance scores
    for i, score in enumerate(top_10['Performance Score']):
        plt.text(score + 1, i, f'{score:.1f}', ha='left', va='center', fontsize=12)
    
    plt.title('Top 10 Midfielders: Overall Performance', fontsize=20, pad=20)
    plt.xlabel('Performance Score (0-100)', fontsize=14)
    plt.xlim(0, 100)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('top_performers.png', dpi=300)
    plt.show()

def create_consistency_chart():
    plt.figure(figsize=(14, 10))
    top_consistent = analysis_df.sort_values('Consistency Index', ascending=False).head(10)
    colors = [TEAM_COLORS[team] for team in top_consistent['Squad']]
    
    plt.barh(top_consistent['Player'], top_consistent['Consistency Index'], color=colors, edgecolor='#333', linewidth=0.8)
    
    # Add team labels
    for i, (player, team) in enumerate(zip(top_consistent['Player'], top_consistent['Squad'])):
        plt.text(5, i, team, ha='left', va='center', fontsize=12, fontweight='bold', color='white')
    
    # Add consistency scores
    for i, score in enumerate(top_consistent['Consistency Index']):
        plt.text(score + 1, i, f'{score:.1f}', ha='left', va='center', fontsize=12)
    
    plt.title('Top 10 Most Consistent Midfielders', fontsize=20, pad=20)
    plt.xlabel('Consistency Index (0-100)', fontsize=14)
    plt.xlim(0, 100)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('consistency.png', dpi=300)
    plt.show()

def create_performance_comparison():
    plt.figure(figsize=(16, 12))
    
    # Prepare data
    metrics = ['Cmp%', 'DribSucc%', 'SoT%', 'Defensive Actions']
    metric_names = ['Passing %', 'Dribble Success %', 'Shots on Target %', 'Defensive Actions']
    
    # Create subplots
    for i, (metric, name) in enumerate(zip(metrics, metric_names)):
        plt.subplot(2, 2, i+1)
        top_players = analysis_df.sort_values(metric, ascending=False).head(8)
        colors = [TEAM_COLORS[team] for team in top_players['Squad']]
        
        bars = plt.barh(top_players['Player'], top_players[metric], color=colors, edgecolor='#333', linewidth=0.8)
        
        # Add team labels
        for j, (player, team) in enumerate(zip(top_players['Player'], top_players['Squad'])):
            plt.text(top_players[metric].min()/2, j, team, ha='left', va='center', 
                     fontsize=11, fontweight='bold', color='white')
        
        # Add metric values
        for j, value in enumerate(top_players[metric]):
            plt.text(value + (top_players[metric].max()*0.02), j, f'{value:.1f}', 
                     ha='left', va='center', fontsize=11)
        
        plt.title(f'Top Players: {name}', fontsize=16)
        plt.xlabel(name.split(' ')[0], fontsize=12)
        plt.gca().invert_yaxis()
        plt.grid(axis='x', alpha=0.2)
    
    plt.suptitle('Positional Leaders: Key Performance Metrics', fontsize=20, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('position_leaders.png', dpi=300)
    plt.show()

def create_team_comparison():
    plt.figure(figsize=(14, 10))
    
    # Calculate team averages
    team_stats = analysis_df.groupby('Squad').agg({
        'Cmp%': 'mean',
        'DribSucc%': 'mean',
        'SoT%': 'mean',
        'Defensive Actions': 'mean',
        'Consistency Index': 'mean'
    }).reset_index()
    
    # Normalize for radar chart
    categories = ['Passing', 'Dribbling', 'Chance Creation', 'Defense', 'Consistency']
    for col in ['Cmp%', 'DribSucc%', 'SoT%', 'Defensive Actions', 'Consistency Index']:
        team_stats[col] = (team_stats[col] - team_stats[col].min()) / (team_stats[col].max() - team_stats[col].min()) * 100
    
    # Prepare radar chart
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Plot each team
    for i, row in team_stats.iterrows():
        values = row[['Cmp%', 'DribSucc%', 'SoT%', 'Defensive Actions', 'Consistency Index']].values.tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=3, label=row['Squad'], color=TEAM_COLORS[row['Squad']])
        ax.fill(angles, values, alpha=0.1, color=TEAM_COLORS[row['Squad']])
    
    # Configure radar chart
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=14)
    ax.set_rlabel_position(30)
    plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"], color="grey", size=10)
    plt.ylim(0, 100)
    
    plt.title('Team Comparison: Midfielder Performance', fontsize=20, pad=30)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    plt.tight_layout()
    plt.savefig('team_comparison.png', dpi=300)
    plt.show()

def create_allrounders_chart():
    plt.figure(figsize=(14, 8))
    
    # Create all-rounder score
    analysis_df['All-Round Score'] = analysis_df[metrics].apply(lambda x: x.mean(), axis=1)
    top_allround = analysis_df.sort_values('All-Round Score', ascending=False).head(5)
    
    # Prepare data for visualization
    player_data = []
    for i, player in top_allround.iterrows():
        player_metrics = player[metrics].values
        player_data.append({
            'Player': player['Player'],
            'Squad': player['Squad'],
            'Passing': player_metrics[0],
            'Dribbling': player_metrics[1],
            'Chance Creation': player_metrics[2],
            'Defense': player_metrics[3]
        })
    
    # Create grouped bar chart
    bar_width = 0.15
    index = np.arange(len(metrics))
    
    for i, player in enumerate(player_data):
        plt.bar(index + i*bar_width, 
                [player['Passing'], player['Dribbling'], player['Chance Creation'], player['Defense']],
                width=bar_width, 
                label=f"{player['Player']} ({player['Squad']})",
                color=TEAM_COLORS[player['Squad']])
    
    # Configure chart
    plt.xlabel('Performance Metrics', fontsize=14)
    plt.ylabel('Performance Value', fontsize=14)
    plt.title('Top 5 All-Round Midfielders', fontsize=20, pad=20)
    plt.xticks(index + bar_width*2, ['Passing %', 'Dribbling %', 'Shots on Target %', 'Defensive Actions'])
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('allrounders.png', dpi=300)
    plt.show()

# Generate all visualizations
create_top_performers_chart()
create_consistency_chart()
create_performance_comparison()
create_team_comparison()
create_allrounders_chart()

# Print top performers
print("\n" + "="*80)
print("2022-2023 SÜPER LIG MIDFIELDER ANALYSIS".center(80))
print("="*80)

print("\nTOP 5 OVERALL PERFORMERS:")
print(analysis_df[['Player', 'Squad', 'Performance Score']].head(5).to_string(index=False))

print("\nTOP 5 MOST CONSISTENT PLAYERS:")
consistent = analysis_df.sort_values('Consistency Index', ascending=False).head(5)
print(consistent[['Player', 'Squad', 'Consistency Index']].to_string(index=False))

print("\nTOP DEFENSIVE MIDFIELDERS:")
defensive = analysis_df.sort_values('Defensive Actions', ascending=False).head(5)
print(defensive[['Player', 'Squad', 'Defensive Actions']].to_string(index=False))

print("\nTOP CREATIVE MIDFIELDERS:")
creative = analysis_df.sort_values('SoT%', ascending=False).head(5)
print(creative[['Player', 'Squad', 'SoT%']].to_string(index=False))

print("\nBEST PASSERS:")
passers = analysis_df.sort_values('Cmp%', ascending=False).head(5)
print(passers[['Player', 'Squad', 'Cmp%']].to_string(index=False))