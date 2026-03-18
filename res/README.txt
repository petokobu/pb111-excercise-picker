Program pb111 chooses a random excercise.
The score and finished excercises are saved.

### Use ###

pb111 XX pick - picks a random pending excercise from week XX
pb111 XX YY pick - picks a random pending excercise from week XX to week YY
pb111 all pick - picks a random pending excercise

pb111 XX reset - resets data about pending excercises from week XX
pb111 XX YY reset - resets data about pending excercises from week XX to week YY
pb111 all reset - resets data about pending excercises

pb111 XX score - prints score from week XX
pb111 XX YY score - prints score from week XX to week YY
pb111 all score - prints score

pb111 XX T N passed - forces to register excercise
                      from week XX of type T numbered N as passed
pb111 XX T N failed - forces to register excercise
                      from week XX of type T numbered N as failed

- XX and YY are from interval <1, 12>
- T are one of the following: p, r, v
- N is usually from the interval <1, 6>, but depends on the week and type

Best of luck!