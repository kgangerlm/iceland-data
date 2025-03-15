Now your task is to generate a beautiful and compelling guidebook style itinerary

First review the following 

Overview images 

<images>
Day,Image
1,https://raw.githubusercontent.com/kgangerlm/iceland-data/refs/heads/main/images/day1.jpg
2,https://github.com/kgangerlm/iceland-data/blob/main/images/day2.jpg?raw=true
3,https://github.com/kgangerlm/iceland-data/blob/main/images/day3.png?raw=true
4,https://raw.githubusercontent.com/kgangerlm/iceland-data/refs/heads/main/images/day4.webp
5,https://github.com/kgangerlm/iceland-data/blob/main/images/day5.jpg?raw=true
6,https://github.com/kgangerlm/iceland-data/blob/main/images/day6.jpg?raw=true
7,https://github.com/kgangerlm/iceland-data/blob/main/images/day7.jpg?raw=true
8,https://github.com/kgangerlm/iceland-data/blob/main/images/day8.jpg?raw=true
9,https://raw.githubusercontent.com/kgangerlm/iceland-data/refs/heads/main/images/day9.avif
10,https://github.com/kgangerlm/iceland-data/blob/main/images/day10.jpg?raw=true
11,https://raw.githubusercontent.com/kgangerlm/iceland-data/refs/heads/main/images/day11.avif
<images>

Now use the plan above to create a beautiful, inspirational, and factually accurate itinerary in html format

Remember these important guidelines. 
 - Anything that is a hidden gem should be highlighted and marked with a gem emoji. 
 - Anything I told you to highlight as an activity should be marked with a sparkle emoji and have more details than other items
 - always include lodging information from the tripit data 
 - always include an emoji and overview image for each day 
 - always include a summary and inspirational quote for the day
 - carefully consider what I should be thinking about and add that in the notes section for each day 
 - Add links for more information wherever possible. Look for links I provided you then use your best judgment to find others. 
 - include a page break before each day based on the example i provide you
 - find a picture from the information I gave you and insert the correct one into the "[day image]" area in the <imag> tag.  

 Now Generate a compelling, accurate itinerary in the following format

 # 11-Day Iceland Adventure
## July 14-24, 2025

![overview image](https://res.cloudinary.com/enchanting/q_80,f_auto,c_lfill,w_1920,h_400,g_auto/exodus-web/2021/12/kirkjufellsfoss_iceland.jpg)

## Trip Overview

- **Day [day number]: [short date]** [starting location] -> ending location [very brief description of the day] [enclose bullet point with a link to the details for the day]

[repeat the following for each day]

----
<div style="page-break-after: always; visibility: hidden"> 
\pagebreak 
</div>

## [emoji for the day] Day [day number]: [date]- [very brief summary of the day]]

<div align="center">
  <img src="[day image]" width="100%" style="max-width: 800px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"/>
</div>

*[overview of the day]*

<div style="padding: 20px; background-color: #f5f7f9; border-left: 4px solid #3498db; margin: 20px 0; border-radius: 5px;">
  <em>[inspirational quote that is relevant to the day and location]</em>
</div>
### Overview
- **Driving**: ([total miles] , [total time])  
- **Location**: [starting city] -> [ending city]

### Morning

- [list morning itinerary pay attention to highlighted activities and hidden gems]

### Afternoon 

- [list Afternoon itinerary pay attention to highlighted activities and hidden gems]

### Evening 

- [list Afternoon itinerary pay attention to highlighted activities and hidden gems]

### Accommodations

[Give a nice overview of the lodeging for the night from the tripit data.]

#### Notes
[Do your best to combine my notes and your notes for each day.  Include practical considerations, and omit if there is nothing important]


