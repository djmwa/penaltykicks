---
title: Penalty Kicks in Professional Soccer
description: Daniel Moser<br>May 11, 2025
---

**Document Type:** Discussion  
**Purpose:** To expand on the origins of this project, introduce myself, and explain the rationale behind the selection of leagues and datasets.

***

## Project Background

### Expanding on the Project's Origins
This project began with a passing comment during a soccer game I watched with my dad. A second penalty kick had just been awarded—there were no other goals yet in the match—when he casually said, “Maybe a penalty kick should only count for half a goal.” We didn’t explore the thought much at the time, but it stuck with me.

In fact, he and I have often discussed how penalty kicks affect scoring races, particularly the Golden Boot awards. Since most teams assign one designated penalty taker, that player’s goal tally can be significantly inflated compared to others who score only from open play. This project is my attempt to analyze that idea more thoroughly—both for the Golden Boot and broader match outcomes—while also sharpening my data analysis skills through a topic I genuinely care about.

### A Bit About Me
I come to this project with an unconventional background. I trained and worked as a pharmacist, but over time, due to both personal and professional reasons, it became clear that pharmacy was no longer a sustainable long-term path for me.

My interest in data analysis goes back to high school, though I’ve pursued it informally for many years—mostly through personal projects. I recently started formally reskilling, taking online courses in SQL, R, Python, and general data analytics. While I don’t have a traditional tech or statistics background, I bring analytical rigor from my pharmacy and organic chemistry training, and a lot of curiosity and persistence. This project is one of my first major data analysis endeavors using R, and it will serve as both a learning process and a portfolio piece.

### Project Timeframe
Since this is a personal project, I’m working on it during my free time. My goal is to produce at least one meaningful update or deliverable each week to maintain momentum and track progress.

***

## On Choosing the Data
### Why Not Use World Cup Data?
At first glance, the FIFA World Cup might seem like a perfect dataset: it’s widely followed, globally relevant, and full of high-stakes moments. However, for this kind of analysis, it has several limitations:

1. **Sample Size:** The World Cup includes only 64 matches every four years. In contrast, the English Premier League plays 380 matches each season. The limited number of World Cup games significantly constrains statistical power.
1. **Mixed Contexts:** World Cup matches are split between group stages and knockout rounds, each with different incentives and match dynamics, making apples-to-apples comparisons difficult.
1. **National vs. Club Teams:** The World Cup features national teams, which are assembled infrequently and have far less continuity than club teams in professional leagues.

In short, while the World Cup is iconic, it lacks the volume and consistency needed for a robust analysis of penalty kicks over time.

### Why These Leagues?
I selected 12 professional leagues across Europe and North America:

- **Top-tier European leagues ("Big Five"):**  
Premier League (England), Ligue 1 (France), Bundesliga (Germany), Serie A (Italy), La Liga (Spain)
- **Their corresponding second divisions:**  
EFL Championship, Ligue 2, 2. Bundesliga, Serie B, Segunda División
- **North American leagues:**  
Major League Soccer (USA), Liga MX (Mexico)

The European “Big Five” leagues are considered the most competitive and visible club competitions globally, making them ideal for cross-country comparison. Including each country's second division allows me to explore how penalty impacts might differ across levels of play, especially since teams often move between divisions due to promotion and relegation.

As for the North American leagues, MLS is the one I follow most closely, and Liga MX provides a useful regional contrast. Neither league uses promotion/relegation currently, and the second-division structures in both countries are either unstable (U.S.) or suspended (Mexico), which makes consistent second-tier data difficult to obtain.

***

## What's Missing—and Why
### Women's Leagues:
I chose not to include women’s leagues in this initial analysis simply due to scope. Expanding the project to include women’s soccer is absolutely worth pursuing—but to keep this project focused and manageable, I’ve limited the current analysis to men’s professional leagues. A follow-up project dedicated to women’s leagues could provide fascinating comparisons.

### Club Tournaments and Playoffs:
I’ve intentionally excluded knockout tournaments like the UEFA Champions League and postseason playoffs (such as those in MLS or Liga MX). These competitions introduce different pressures, formats, and incentives. By sticking to regular-season league play, I can ensure a more consistent context for comparing the influence of penalty kicks across teams, seasons, and leagues.

[Home](/penaltykicks)  
[Previous: Introduction](introduction)  
[Next: Data Collection](data_collection.md)
