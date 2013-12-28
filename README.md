caltrainfails
=============

reads information about caltrain delays from a twitter feed, and tees up some analytics



details:

My new job makes Caltrain an attractive commuting option, but based on the last time I tried public transit to the South Bay I'm rather skeptical that it will work out. But was it my bad luck or is Caltrain routinely horrible?

I couldn't find a well structured dataset that would provide me with delay information, but there is this cool Twitter feed @caltrain. there is a style-guide (http://cow.org/c/updating-guide) so there's some structure but it still is messy enough to make a nice insomnia problem :P

From a CSV file of caltrain fails, we output number of minutes of delays, time (from the timestamp), and direction of train by processing the tweets with REs. See the Excel sheet to understand how I worked some of the data up.

known areas for improvement:

- set up a cronjob to update the tweets regularly (and get around the Twitter API imposed limit for retriveing them)
- better way of figuring out where we need to update from than writing an ID and then tossing it out later
- generally get more data to improve the analysis
- improve the tests, which really are just function calls at this point :P
- remove the double hits for NB vs SB, and better handle absence of train direction
- general improved extraction of data from the tweets (thoughts?)
- use the timestamp in the tweet text rather than from the tweet object
- the timestamps look like they are occasionally coming out AM when they should be PM
- for an actual commuter, what matters is how a NB morning leg and SB evening leg does (vs. NB in general). I need to think of a clean way of structuring this vs. just looking at graphs to make inferences
