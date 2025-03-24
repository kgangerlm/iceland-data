You are an expert travel itinerary creator specializing in Iceland. Your task is to generate a detailed, personalized HTML itinerary for an 11-day Iceland Ring Road adventure based on the provided information and your extensive knowledge of Iceland. The trip will take place from July 14-24, 2025.

First, carefully review the following trip plan you created earlier, and the example html I provided you for formatting.  The trip plan should guide the content for this. 

Now review this additional information. To help you build the maps and overview images for each day. 
Use the images information to add an overview image for each day. 

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

Use this information to insert the correct map for each day
<maps>
Day,Map
Day 1,"<iframe src=""https://www.google.com/maps/d/embed?mid=14SQO22uQjMOhV9Q8E7FtIW0fXMesXQw&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 2,"<iframe src=""https://www.google.com/maps/d/embed?mid=14SQO22uQjMOhV9Q8E7FtIW0fXMesXQw&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 3,"<iframe src=""https://www.google.com/maps/d/embed?mid=16not-P5qZezdTRAHL-W0BhUIyZNpXEw&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 4,"<iframe src=""https://www.google.com/maps/d/embed?mid=1g9ZYp95N7OgXC8GwSDtvVXbikv742fo&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 5,"<iframe src=""https://www.google.com/maps/d/embed?mid=1eRRn2Q6RY1QEGECxiQC3F3eXJZ4QbFs&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 6,"<iframe src=""https://www.google.com/maps/d/embed?mid=1f84QU5RhBBXX-YLQmfDVseVNaWkShsQ&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 7 ,"<iframe src=""https://www.google.com/maps/d/embed?mid=1yLxSSLW5Rj9_ULPOxlD1ptzMxLuSyjc&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 8,"<iframe src=""https://www.google.com/maps/d/embed?mid=1Vl6k8M4-dpx0eJ8ClUu7O3XwsNTDn60&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 9,"<iframe src=""https://www.google.com/maps/d/embed?mid=1rEEyKRYtWJ2wE3hfstl7ShVbcP9n3uw&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
Day 10,"<iframe src=""https://www.google.com/maps/d/embed?mid=1p5j0Ep3wf98qhPSuZYWVhZ3qrQnPHuI&ehbc=2E312F&noprof=1"" width=""100%"" height=""480""></iframe>"
</maps>

Your goal is to create a beautiful, inspirational, and factually accurate itinerary in HTML format. Before generating the final output, please work inside <itinerary_planning> tags in your thinking block. This planning should include:

1. A day-by-day breakdown of the itinerary, following these steps:
   a) List key locations and activities for each day
   b) Research and note accurate driving times and distances between locations
   c) Estimate realistic durations for each activity, considering factors like hiking time, tour length, etc.
   d) Compile a list of associated costs for activities, entrance fees, etc.
   e) Verify accommodation details for each night
   f) Identify potential hidden gems or unique experiences to highlight
   g) Collect a list of links to be included in the itinerary, prioritizing:
      - Links provided in the trip plan
      - Up-to-date links found through web search for additional information

After completing your planning, generate the HTML itinerary using the following guidelines:

1. Structure and Formatting:
   - Use the HTML and CSS structure provided in the example
   - Include a page break before each day (use the provided CSS class)
   - Use emojis to represent the theme of each day
   - Mark hidden gems with a gem emoji (💎)
   - Highlight featured activities with a sparkle emoji (✨)

2. Content for Each Day:
   - Include an overview image (use placeholder URLs from the example)
   - Add an inspirational quote relevant to the day's activities
   - Provide a detailed schedule (morning, afternoon, evening). Use GMT times and make sure the schedule you create is accurate and makes sense. 
   - Include driving information (distance, time)
   - List accommodation details - Use the tripit data
   - Suggest 5-8 alternative activities
   - Add a bad weather activities section. Think about what we should do if their is rain that ruins the primary plan. Style this beautifully.  
   - Add a tip box for important information
   - Include a notes section for practical considerations

3. Additional Elements:
   - Create an overall trip summary at the beginning
   - Include the embedded map provided for each day
   - Add a resources section at the end with useful links and apps

4. Accuracy and Detail:
   - Ensure all timing is accurate, accounting for driving time, hike duration, tour length, etc.
   - Include costs for activities where applicable
   - Use only verified, up-to-date links
   - do not include any confirmation codes or other personal information other than first names

Remember to make the itinerary compelling, accurate, and visually appealing. Do not include any confirmation codes or personal information other than first names.

Your final output should consist only of the HTML itinerary and should not duplicate or rehash any of the work you did in the itinerary planning section.