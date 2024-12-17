# Voting Methods

This voting methods script contains the definitions of 6 different voting methods - *dictatorship*, *scoring_rule*, *plurality*, *veto*, *borda* and *STV* - defined using individual Python functions.

![A person votes anonymously using a ballot box.](https://images.pexels.com/photos/1550337/pexels-photo-1550337.jpeg)

## How it works

This programme takes **voters** (keys in the ```v_dict``` dictionary) and **candidates** (values in the list of each voter in ```v_dict```) and is written to handle any number of voters and any number of candidates. The order of candidates for each voter illustrates their voting preference - first position in the list indicates the most preferred candidate for a given voter.

The script also contains a ```tie_breaker_winner``` function to decide on the winner if multiple voting candidates receive the same score by picking the favourite candidate of a single elected voter.

## Testing

Before the voting functions are defined, the ```Preference``` class and its related ```pref_obj``` are given. These can be edited to change the number of candidates and voters for the test - just make sure to be consistent with numbers of each! 

At the bottom of the script, there is a test to print the output of each voting method. Feel free to download the script and change the number of candidates and voters to prove that it works! :)
