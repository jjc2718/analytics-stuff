#!/usr/bin/env python
# coding: utf-8

# ## 2023 Women's World Cup group stages: squad rotation analysis
# 
# At the end of the group stage of the 2023 Women's World Cup, I wanted to see if the perception of the US as rotating less than other teams was supported by the data. I picked 3 metrics to look at in an attempt to quantify “squad rotation”:
# 
# - Mean number of subs used per game (fewer = less rotation, more = more rotation)
# - Median sub time (earlier = more rotation, later = less rotation; I used median instead of mean to de-emphasize early injury subs and similar outliers)
# - Median number of minutes played per player (lower = more rotation since minutes are more “spread” amongst players, higher = less rotation; same rationale for median as sub time)
# 
# Below, I visualized the distributions of each metric over all 32 teams, with the US and Sweden marked on each plot.
# 
# All data is from FBRef (I collected the substitution counts/times from the match reports by hand, and the player data came from https://fbref.com/en/comps/106/playingtime/Womens-World-Cup-Stats)

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ### Mean number of substitutions across games

# In[2]:


n_subs_df = pd.read_csv(
    './data/wc_2023_num_subs.csv',
    names=['team', 'game_1', 'game_2', 'game_3']
).set_index('team')

print(n_subs_df.shape)
n_subs_df.head()


# In[3]:


mean_subs_df = (n_subs_df
  .mean(axis='columns')
  .to_frame(name='mean_subs')
  .reset_index()
  .sort_values(by='mean_subs', ascending=True)
)

mean_subs_df.head()


# In[4]:


mean_subs_df


# In[5]:


sns.set({'figure.figsize': (8, 4)})

ax = sns.histplot(
    data=mean_subs_df, x='mean_subs', binwidth=0.5, binrange=(2, 5.5)
)

us_mean_subs = mean_subs_df[mean_subs_df.team == 'USA'].mean_subs.values[0]
ax.axvline(
    x=us_mean_subs, linestyle='--', color='black'
)
ax.text(
    us_mean_subs+0.05, 8, f'USA ({us_mean_subs:.2f})',
    size=10, bbox={'facecolor': 'white', 'edgecolor': 'black'}
)

sweden_mean_subs = mean_subs_df[mean_subs_df.team == 'Sweden'].mean_subs.values[0]
ax.axvline(
    x=sweden_mean_subs, linestyle='--', color='black'
)
ax.text(
    sweden_mean_subs+0.05, 8, f'Sweden ({sweden_mean_subs:.2f})',
    size=10, bbox={'facecolor': 'white', 'edgecolor': 'black'}
)

plt.title('Mean subs used per game, group stage')
plt.xlabel('Mean subs used')

plt.savefig('./mean_subs_used.png', bbox_inches='tight', dpi=200)


# ### Median substitution time, across games

# In[6]:


sub_times_df = pd.read_csv(
    './data/wc_2023_sub_times.csv', index_col=0, header=None, names=list(range(17))
)
sub_times_df.index.name = 'team'

print(sub_times_df.shape)
sub_times_df.head()


# In[7]:


median_sub_times_df = (sub_times_df
  .median(axis='columns') # excludes NA by default
  .to_frame(name='median_sub_time')
  .reset_index()
  .sort_values(by='median_sub_time', ascending=True)
)

median_sub_times_df.head(10)


# In[8]:


median_sub_times_df


# In[9]:


sns.set({'figure.figsize': (8, 4)})

ax = sns.histplot(
    data=median_sub_times_df, x='median_sub_time', binwidth=5, binrange=(50, 90)
)

us_median_time = median_sub_times_df[median_sub_times_df.team == 'USA'].median_sub_time.values[0]
ax.axvline(
    x=us_median_time, linestyle='--', color='black'
)
ax.text(
    us_median_time+0.5, 8, f'USA ({us_median_time:.0f})',
    size=10, bbox={'facecolor': 'white', 'edgecolor': 'black'}
)

sweden_median_time = median_sub_times_df[median_sub_times_df.team == 'Sweden'].median_sub_time.values[0]
ax.axvline(
    x=sweden_median_time, linestyle='--', color='black'
)
ax.text(
    sweden_median_time+0.5, 8, f'Sweden ({sweden_median_time:.0f})',
    size=10, bbox={'facecolor': 'white', 'edgecolor': 'black'}
)

plt.title('Median substitution time, group stage')
plt.xlabel('Median sub time')

plt.savefig('./median_sub_time.png', bbox_inches='tight', dpi=200)


# ### Median number of minutes played, across players on each team

# In[15]:


players_df = pd.read_csv(
    './data/wc_2023_playing_time.csv', sep='\t', index_col=0, header=None
)

players_df = (players_df
    .loc[:, [1, 3, 6, 7, 11, 12, 14, 15]]
    .rename(columns={
        1: 'player_name',
        3: 'team',
        6: 'matches_played',
        7: 'minutes_played',
        11: 'starts',
        12: 'min_per_start',
        14: 'subs',
        15: 'min_per_sub'
    })
    .fillna(0)
)

# remove flag letters
players_df['team'] = players_df.team.str[3:]

# remove players who haven't played
players_df = players_df[players_df.matches_played > 0].copy()

print(players_df.shape)
players_df.head()


# In[11]:


print(players_df.team.unique())


# In[17]:


minutes_df = (players_df
    .loc[:, ['team', 'minutes_played']]
    .groupby('team')
    .agg('median')
    .sort_values(by='minutes_played', ascending=False)
    .reset_index()
)

minutes_df.head()


# In[18]:


minutes_df


# In[19]:


sns.set({'figure.figsize': (8, 4)})

ax = sns.histplot(
    data=minutes_df, x='minutes_played', binwidth=20, binrange=(100, 280)
)

us_median_minutes = minutes_df[minutes_df.team == 'USA'].minutes_played.values[0]
ax.axvline(
    x=us_median_minutes, linestyle='--', color='black'
)
ax.text(
    us_median_minutes+2.5, 9, f'USA ({us_median_minutes:.2f})',
    size=10, bbox={'facecolor': 'white', 'edgecolor': 'black'}
)

sweden_median_minutes = minutes_df[minutes_df.team == 'Sweden'].minutes_played.values[0]
ax.axvline(
    x=sweden_median_minutes, linestyle='--', color='black'
)
ax.text(
    sweden_median_minutes+2.5, 9, f'Sweden ({sweden_median_minutes:.2f})',
    size=10, bbox={'facecolor': 'white', 'edgecolor': 'black'}
)

plt.title('Median minutes played per player, group stage')
plt.xlabel('Median minutes played')

plt.savefig('./median_mins_per_player.png', bbox_inches='tight', dpi=200)


# In[25]:


players_df['start_mins'] = players_df.starts * players_df.min_per_start
players_df['sub_mins'] = players_df.subs * players_df.min_per_sub

# sometimes these are off by one from minutes_played, that's fine
players_df.head(15)


# In[31]:


sub_minutes_df = (players_df
    .loc[:, ['team', 'start_mins', 'sub_mins']]
    .groupby('team')
    .agg('sum')
    .reset_index()
)
sub_minutes_df['start_proportion'] = sub_minutes_df.start_mins / (sub_minutes_df.start_mins + sub_minutes_df.sub_mins)
sub_minutes_df['sub_proportion'] = 1 - sub_minutes_df.start_proportion

sorted_df = sub_minutes_df.sort_values(by='start_proportion', ascending=True)
sorted_df.head()


# In[61]:


ro16_teams = ['Switzerland', 'Spain', 'Japan', 'Norway', 'Netherlands', 'South Africa',
              'USA', 'Sweden', 'Australia', 'Denmark', 'England', 'Nigeria', 'Colombia',
              'Jamaica', 'France', 'Morocco']

plot_df = sub_minutes_df[sub_minutes_df.team.isin(ro16_teams)]
sorted_df = plot_df.sort_values(by='start_proportion')
sorted_df.head()


# In[68]:


sns.set({'figure.figsize': (8, 6)})

ax = sns.barplot(
    data=plot_df,
    x='start_proportion', y='team', 
    order=sorted_df.team,
    orient='h', color='#1f77b4', alpha=0.8
)
ax.bar_label(ax.containers[0], fmt='%.2f')

plt.title('Proportion of minutes played by starters, World Cup group stage', x=0.4, y=1.025)
plt.xlabel('Proportion of minutes', labelpad=12)
plt.ylabel('Team', labelpad=12)
plt.xticks(rotation=90)
plt.xlim(0.0, 1.02)

plt.savefig('./proportion_starters.png', bbox_inches='tight', dpi=200)


# So for the US/Sweden matchup in the round of 16, it seems fairly clear that for each of these metrics, the US has rotated “less” than Sweden, and we should probably expect Sweden’s players to be a bit fresher going into the knockout game. Whether it will matter or not, we will see.
# 
# Looking forward to the other teams on the US’s side of the bracket: I didn't mark them on the plots, but generally Japan, Spain, Norway are all toward the “more rotation” side of these measurements; Switzerland, Netherlands and South Africa are more comparable to the US on the “less rotation” side of things. This is obviously only one factor of many, but it’ll be interesting to see how it all plays out!
