This project contains a python implementation of Ranked Choice vVoting algorithm.

Input file: In this code, we are using the file "votes_data.txt" to read our reqiured inputs. The format is:
_ Line 1: Number of candidates
_ Line 2 to EOF: Comma seperated user's vote per line


### How to run?
Requirement: Python3

```sh
$ python3 rapid_voting.py
```

### Methodology
Every voter's card is sorted in buckets of each candidate's key in dictionary
Candidate Wise Ballot = { candidateVoteList: [list of all votes where candidate is ranked 1] }.

    FOR n ITERATIONS:
        FOR all candidates in Candidate Wise Ballot,
		check if any candidate has a clear majority at rank 1
		(check if any candidate's vote list has count > (totalVoters/2)+1 , clear majority?)
		if yes:
		    CLEAR WINNER
		if no:
		    check if we can eliminate a lowest ranking candidate. 
		    (checking if the lowest ranking candidate's rank 1 votes are equal to the highest ranking candidate's rank 1 votes.)
		    if yes:
			tie
			resolve_tie()
		    if no:
			DISCARDED_CANDIDATES = append list of eliminated candidates in this round.
					Call Eliminate Lowest Ranking Candidate 

        NEXT ITERATION


Eliminating the candidate requires us to go through the voters in this candidate's bucket and look at the SECOND ranking choices of each voter card, and adding them to the SECOND candidate's bucket if it is valid(has not been eliminated previously).

    FOR all DISCARDED_CANDIDATES:
    	FOR all votercards in discarded_cand:
    		SECOND_ranking_candidate = voter card's  SECOND ranking candidate
    		if the second_ranking_candidate is eliminated (in DISCARDED_CANDIDATES):
    			leave the card.
    		else:
    			remove card from this bucket and add to bucket of Candidate Wise Ballot["second_ranking_candidate"]

Note: Everytime the eliminateLowestRankingCandidate() function is called with the next ITERATION, the rank in question will increase. SECOND/THIRD/FOURTH/Nth

##### Breaking Tie:
If there is no clear majority, and lowest ranking candidates are eliminated, then all candidates that are not eliminated will have equal 1st ranking votes. 
At this point, we need to count the second ranking votes, and check for clear majority. 
Initialize a dictionary of tied candidates vote count as the 1st ranking vote

    FINAL BALLOTS ={candidate: count, ... }
    FOR RANK second to last:
	    Go to each candidate's bucket, and count the RANKing vote for this candidate and increase the count everytime.
	    check if clear majority reached.
	    if yes:
		    WINNER
    if no one has one, then all votes are equally ranked among ties candidates.
    therefore:
    	NO WINNER.


### Best Case Scenario
Majority is established in first iteration itself. A single candidate has the >50% of the number of votes.
However, we are first creating a candidate_wise_ballot by iterating on all votes of dimension (m x n)
Therefore, Best Case Time Complexity will be *O(m.n)*

### Worst case
No clear majority.

    Recursively 
    	checks for clear winner, 
    		eliminate candidate
    			calculate tied ranking votes
    				check for clear winner

When resolving tie in the case when no candidate is left for elimination, the algorithm iterates over the total number of candidates(n), filtered candidates(in worst case, n) and all  user's vote(m)
Therefore, Worst Case Time Complexity will be *O(n^2.m)*


### Improvements
1. Modify the looping algorithm, to use recursion.
2. Instead of a two step calculation, we could use a multidimensional array that only keeps counts instead of complete ballots.
3. Optimize the logic for resolving a tie when no candidate is left for elimination
