import pandas as pd
import os
from typing import List, Tuple

def get_column_name(df: pd.DataFrame, possible_names: List[str]) -> str:
    '''
    Find the actual column name from a list of possible names.
    
    Args:
        df: DataFrame to search in
        possible_names: List of possible column names
    
    Returns:
        The actual column name found in the DataFrame
    
    Raises:
        ValueError: If none of the possible names are found
    '''
    for name in possible_names:
        if name in df.columns:
            return name
    raise ValueError(f'None of the column names {possible_names} found in DataFrame')

def process_match_column(match_str: str) -> Tuple[str, str]:
    '''
    Split the match column into home and away teams.
    
    Args:
        match_str: String containing team names separated by 'vs ' or ' vs'
    
    Returns:
        Tuple of (home_team, away_team)
    '''
    # Handle missing values (NaN, None, etc.)
    if pd.isna(match_str) or match_str is None:
        return ('', '')
    
    # Convert to string in case it's not already
    match_str = str(match_str)
    
    if 'vs ' in match_str:
        parts = match_str.split('vs ')
        home_team = parts[0].strip()
        away_team = parts[1].strip()
    elif ' vs' in match_str:
        parts = match_str.split(' vs')
        home_team = parts[0].strip()
        away_team = parts[1].strip()
    else:
        raise ValueError(f'Cannot parse match string: {match_str}')
    
    return home_team, away_team

def load_and_process_football_data(file_path: str) -> pd.DataFrame:
    '''
    Load and process football data CSV file.
    
    Args:
        file_path: Path to the CSV file
    
    Returns:
        Processed DataFrame with standardized column names
    '''
    df = pd.read_csv(file_path)
    
    # Get the actual column names for the flexible columns
    home_goals_col = get_column_name(df, ['FTHG', 'HG'])
    away_goals_col = get_column_name(df, ['FTAG', 'AG'])
    result_col = get_column_name(df, ['FTR', 'Res'])
    
    # Select and rename columns
    selected_df = df[['HomeTeam', 'AwayTeam', home_goals_col, away_goals_col, result_col]].copy()
    
    # Standardize column names
    selected_df.columns = ['HomeTeam', 'AwayTeam', 'HomeGoals', 'AwayGoals', 'Result']
    
    return selected_df

def load_and_process_penalty_data(file_path: str) -> pd.DataFrame:
    '''
    Load and process penalty data CSV file.
    
    Args:
        file_path: Path to the CSV file
    
    Returns:
        Processed DataFrame with split match column
    '''
    # Load CSV without header, with Latin-1 encoding to handle special characters
    try:
        df = pd.read_csv(file_path, header=None, encoding='latin-1')
    except UnicodeDecodeError:
        # Fallback to Windows-1252 if Latin-1 fails
        df = pd.read_csv(file_path, header=None, encoding='windows-1252')
    
    # Check if we have enough columns
    if len(df.columns) <= 7:
        print(f"Warning: CSV only has {len(df.columns)} columns, need at least 8")
        return pd.DataFrame()
    
    # Select relevant columns (4, 5, and 7) and give them names
    penalty_df = df.iloc[:, [4, 5, 7]].copy()
    penalty_df.columns = ['PK_Team', 'Match', 'Outcome']
    
    # Filter out rows with missing data
    penalty_df = penalty_df.dropna(subset=['Match', 'PK_Team', 'Outcome'])
    
    if penalty_df.empty:
        return pd.DataFrame()
    
    # Split the Match column into HomeTeam and AwayTeam
    penalty_df[['HomeTeam', 'AwayTeam']] = penalty_df['Match'].apply(
        lambda x: pd.Series(process_match_column(x))
    )
    
    # Drop the original Match column
    penalty_df = penalty_df.drop('Match', axis=1)
    
    # Create home/away indicator
    penalty_df['is_home'] = penalty_df['PK_Team'] == penalty_df['HomeTeam']
    penalty_df['is_away'] = penalty_df['PK_Team'] == penalty_df['AwayTeam']

    # Create penalty outcome indicators
    penalty_df['pk_scored'] = (penalty_df['Outcome'] == 'Scored').astype(int)
    penalty_df['pk_awarded'] = 1  # Every row represents an awarded penalty

    # Aggregate by game (HomeTeam, AwayTeam)
    agg_data = []
    
    for (home_team, away_team), game_group in penalty_df.groupby(['HomeTeam', 'AwayTeam']):
        # Initialize counters
        home_pk_scored = 0
        home_pk_awarded = 0
        away_pk_scored = 0
        away_pk_awarded = 0
        
        # Count penalties for each team
        for _, row in game_group.iterrows():
            if row['is_home']:
                home_pk_scored += row['pk_scored']
                home_pk_awarded += row['pk_awarded']
            elif row['is_away']:
                away_pk_scored += row['pk_scored']
                away_pk_awarded += row['pk_awarded']
        
        # Add to aggregated data
        agg_data.append({
            'HomeTeam': home_team,
            'AwayTeam': away_team,
            'home_pk_scored': home_pk_scored,
            'home_pk_awarded': home_pk_awarded,
            'away_pk_scored': away_pk_scored,
            'away_pk_awarded': away_pk_awarded
        })
    
    # Convert to DataFrame
    penalty_result_df = pd.DataFrame(agg_data)
    
    return penalty_result_df

def process_season_data(season_suffix: str, season_label: str) -> pd.DataFrame:
    '''
    Process data for a single season.
    
    Args:
        season_suffix: Suffix for the football data file (e.g., '1213')
        season_label: Label for the season (e.g., '2012-13')
    
    Returns:
        Combined DataFrame for the season
    '''
    # File paths
    football_file = f'football-data_game_data/E0_{season_suffix}.csv'
    penalty_file = f'epl_penalties_by_game/epl_penalty_stats_{season_label}.csv'
    
    print(f'Processing {season_label} season...')
    
    # Load and process football data
    if not os.path.exists(football_file):
        print(f'Warning: {football_file} not found. Skipping season {season_label}')
        return pd.DataFrame()

    football_df = load_and_process_football_data(football_file)
        
    # Load and process penalty data
    if not os.path.exists(penalty_file):
        print(f'Warning: {penalty_file} not found. Skipping penalty data for season {season_label}')
        penalty_df = pd.DataFrame()
    else:
        penalty_df = load_and_process_penalty_data(penalty_file)
    
    # Add season column to football data
    football_df['Season'] = season_label
    
    # Merge the dataframes if penalty data exists
    if not penalty_df.empty:
        # Merge on HomeTeam and AwayTeam
        combined_df = pd.merge(
            football_df, 
            penalty_df, 
            on = ['HomeTeam', 'AwayTeam'], 
            how = 'left'
        )
    else:
        # If no penalty data, just use football data with empty penalty columns
        combined_df = football_df.copy()
        combined_df['home_pk_scored'] = 0
        combined_df['home_pk_awarded'] = 0
        combined_df['away_pk_scored'] = 0
        combined_df['away_pk_awarded'] = 0
    
    # Fill NaN values with 0 for games that had no penalties
    penalty_columns = ['home_pk_scored', 'home_pk_awarded', 'away_pk_scored', 'away_pk_awarded']
    for col in penalty_columns:
        if col in combined_df.columns:
            combined_df[col] = combined_df[col].fillna(0).astype(int)
    
    print(f'Season {season_label}: {len(football_df)} games, {len(penalty_df) if not penalty_df.empty else 0} penalty records')
    
    return combined_df

def main():
    '''Main function to process all seasons and save each to separate CSV files.'''
    
    # Define the season mappings
    seasons = [
        (f'{year:02d}{year+1:02d}', f'20{year:02d}-{year+1:02d}')
        for year in range(12, 20)
    ]
    
    # Process each season and save individually
    processed_seasons = []
    
    for season_suffix, season_label in seasons:
        season_data = process_season_data(season_suffix, season_label)
        if not season_data.empty:
            # Reorder columns for better readability
            column_order = [
                'Season', 'HomeTeam', 'AwayTeam', 'HomeGoals', 'AwayGoals', 'Result', 
                'home_pk_scored', 'home_pk_awarded', 'away_pk_scored', 'away_pk_awarded'
                ]
            season_data = season_data[column_order]
            
            # Save individual season to CSV
            output_file = f'organized_pk_data/football_penalty_data_{season_label}.csv'
            season_data.to_csv(output_file, index=False)
            
            print(f'Season {season_label}: {len(season_data)} records saved to {output_file}')
            processed_seasons.append(season_label)
    
    # Display summary
    if processed_seasons:
        print(f'\nData processing complete!')
        print(f'Processed seasons: {", ".join(processed_seasons)}')
        print(f'Individual CSV files saved for each season.')
    else:
        print('No data was processed successfully.')

if __name__ == '__main__':
    main()
