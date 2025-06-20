
# Süper Lig 2022-2023 Midfielder Performance Analysis

This project analyzes midfield players from the 2022-2023 Süper Lig season using key performance metrics. It evaluates overall contribution, consistency, and positional strength using normalized scoring, z-score based consistency, and clear visualizations.

## 🧠 Objectives

- Identify top-performing midfielders based on data-driven metrics
- Quantify consistency across key areas of play
- Provide visual comparisons between teams and individual players
- Highlight all-round performers and positional specialists

## 📊 Metrics Used

- **Cmp%** – Pass completion percentage  
- **DribSucc%** – Dribble success rate  
- **SoT%** – Shots on target percentage  
- **TklW + Int** – Defensive contribution (tackles won + interceptions)

## 🔧 Engineered Metrics

- **Performance Score**: Normalized average of four key metrics  
- **Consistency Index**: Based on average absolute z-score across all metrics (higher = more consistent)  
- **All-Round Score**: Simple average of all raw metric values

## 📂 Dataset

- Manually compiled from Süper Lig midfield players across Galatasaray, Fenerbahçe, Beşiktaş, and Trabzonspor  
- Can be extended with scraped data from sources like [fbref](https://fbref.com) or [understat](https://understat.com)

## 📈 Visualizations

| Graphic | Description |
|--------|-------------|
| `top_performers.png` | Top 10 players with highest overall performance |
| `consistency.png` | Top 10 most consistent midfielders |
| `position_leaders.png` | Positional leaders in each core metric |
| `team_comparison.png` | Radar chart comparing team averages |
| `allrounders.png` | Best all-round midfielders across all metrics |

## 🧬 Top Results

```text
Top 5 Overall Performers:
1. Lucas Torreira (Galatasaray)
2. Miguel Crespo (Fenerbahçe)
3. Manolis Siopis (Trabzonspor)
4. Willian Arao (Fenerbahçe)
5. Salih Uçan (Beşiktaş)

Top 5 Most Consistent:
1. Manolis Siopis (Trabzonspor)
2. Lucas Torreira (Galatasaray)
3. Miguel Crespo (Fenerbahçe)
4. Willian Arao (Fenerbahçe)
5. Marek Hamšík (Trabzonspor)
⚽ Created By
Ata Sakik
Software Engineering Student | Football & Data Science Enthusiast
